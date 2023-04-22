import capytaine as cpt
import numpy as np
import meshmagick
from packaging import version
if version.parse(meshmagick.__version__) < version.parse('3.0'):
    import meshmagick.hydrostatics as hs
else:
    import meshmagick.hydrostatics_old as hs
from capytaine.bem.airy_waves import froude_krylov_force

def run(r,nWEC,wave_direction,omega,x,y):
    # sphere 1
    body = cpt.Sphere(radius=r,center=(0,0,0),name='sph')
    body.keep_immersed_part()
    body.center_of_mass = (0, 0, -r/2)
    body.add_all_rigid_body_dofs()
    body.inertia_matrix = body.compute_rigid_body_inertia()
    body.hydrostatic_stiffness = body.compute_hydrostatic_stiffness()

    # create array
    array = body
    dofnames = ['sph__Heave']
    for i in range(1,nWEC):
        array += body.translated((x[i],y[i],0),name=f'sph{i+1}')
        dofnames.append(f'sph{i+1}__Heave')
    array.add_all_rigid_body_dofs()
    array.keep_only_dofs(dofs=dofnames)
    # solve diff and rad probs
    solver = cpt.BEMSolver()

    diff_prob = cpt.DiffractionProblem(body=array.immersed_part(), wave_direction=wave_direction, omega=omega)
    diff_result = solver.solve(diff_prob,keep_details=(True))

    rad_prob = [
        cpt.RadiationProblem(body=array.immersed_part(), radiating_dof=dof, omega=omega)
        for dof in array.dofs ]
    rad_result = solver.solve_all(rad_prob,keep_details=(True))

    dataset = cpt.assemble_dataset(rad_result + [diff_result])

    # damping
    B = [(dataset['radiation_damping'].sel(radiating_dof=['sph__Heave'],
                                          influenced_dof=['sph__Heave']))]
    for i in range(1,nWEC):
        B += [(dataset['radiation_damping'].sel(radiating_dof=[f'sph{i+1}__Heave'],
                                               influenced_dof=[f'sph{i+1}__Heave']))]
    B = np.array(B)

    # added mass
    A = np.zeros(nWEC)
    A[0] = np.array(dataset['added_mass'].sel(radiating_dof=['sph__Heave'],
                                             influenced_dof=['sph__Heave']))
    for i in range(1,nWEC):
        A[i] = np.array(dataset['added_mass'].sel(radiating_dof=[f'sph{i+1}__Heave'],
                                                 influenced_dof=[f'sph{i+1}__Heave']))
    
    # hydrostatic stiffness
    C = np.zeros(nWEC)
    C[0] = np.array(dataset['hydrostatic_stiffness'].sel(radiating_dof=['sph__Heave'],
                                                        influenced_dof=['sph__Heave']))
    for i in range(1,nWEC):
        C[i] = np.array(dataset['hydrostatic_stiffness'].sel(radiating_dof=[f'sph{i+1}__Heave'],
                                                            influenced_dof=[f'sph{i+1}__Heave']))

    # heave exciting forces
    FK = [froude_krylov_force(diff_prob)['sph__Heave']]
    for i in range(1,nWEC):
        FK += [froude_krylov_force(diff_prob)[f'sph{i+1}__Heave']]
    FK = np.array(FK)

    dif = [diff_result.forces['sph__Heave']]
    for i in range(1,nWEC):
        dif += [diff_result.forces[f'sph{i+1}__Heave']]
    dif = np.array(dif)

    F = FK + dif
    return A,B,C,F 
