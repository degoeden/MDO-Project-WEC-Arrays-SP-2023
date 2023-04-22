import capytaine as cpt
import numpy as np
import meshmagick
from packaging import version
if version.parse(meshmagick.__version__) < version.parse('3.0'):
    import meshmagick.hydrostatics as hs
else:
    import meshmagick.hydrostatics_old as hs
from capytaine.bem.airy_waves import froude_krylov_force

def run(r,wave_direction,omega,x,y):
    # sphere 1
    body = cpt.Sphere(radius=r,center=(0,0,0),name='sph')
    body.keep_immersed_part()
    body.center_of_mass = (0, 0, -r/2)
    body.add_all_rigid_body_dofs()
    body.inertia_matrix = body.compute_rigid_body_inertia()
    body.hydrostatic_stiffness = body.compute_hydrostatic_stiffness()

    # create array
    array = body + body.translated((x[1],y[1],0),name='sph2') + body.translated((x[2],y[2],0),name='sph3') + body.translated((x[3],y[3],0),name='sph4')
    array.add_all_rigid_body_dofs()
    array.keep_only_dofs(dofs=['sph__Heave','sph2__Heave','sph3__Heave','sph4__Heave'])

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
    B += [(dataset['radiation_damping'].sel(radiating_dof=['sph2__Heave'],
                                        influenced_dof=['sph2__Heave']))]
    B += [(dataset['radiation_damping'].sel(radiating_dof=['sph3__Heave'],
                                        influenced_dof=['sph3__Heave']))]
    B += [(dataset['radiation_damping'].sel(radiating_dof=['sph4__Heave'],
                                        influenced_dof=['sph4__Heave']))]
    B = np.array(B)

    # added mass
    A1 = np.array(dataset['added_mass'].sel(radiating_dof=['sph__Heave'],
                                        influenced_dof=['sph__Heave']))
    A2 = np.array(dataset['added_mass'].sel(radiating_dof=['sph2__Heave'],
                                        influenced_dof=['sph2__Heave']))
    A3 = np.array(dataset['added_mass'].sel(radiating_dof=['sph3__Heave'],
                                        influenced_dof=['sph3__Heave']))
    A4 = np.array(dataset['added_mass'].sel(radiating_dof=['sph4__Heave'],
                                        influenced_dof=['sph4__Heave']))
    A = np.array([A1, A2, A3, A4])

    # hydrostatic stiffness
    C1 = np.array(dataset['hydrostatic_stiffness'].sel(radiating_dof=['sph__Heave'],
                                        influenced_dof=['sph__Heave']))
    C2 = np.array(dataset['hydrostatic_stiffness'].sel(radiating_dof=['sph2__Heave'],
                                        influenced_dof=['sph2__Heave']))
    C3 = np.array(dataset['hydrostatic_stiffness'].sel(radiating_dof=['sph3__Heave'],
                                        influenced_dof=['sph3__Heave']))
    C4 = np.array(dataset['hydrostatic_stiffness'].sel(radiating_dof=['sph4__Heave'],
                                        influenced_dof=['sph4__Heave']))
    C = np.array([C1, C2, C3, C4])

    # heave exciting forces
    FK = [froude_krylov_force(diff_prob)['sph__Heave']]
    FK += [froude_krylov_force(diff_prob)['sph2__Heave']]
    FK += [froude_krylov_force(diff_prob)['sph3__Heave']]
    FK += [froude_krylov_force(diff_prob)['sph4__Heave']]
    FK = np.array(FK)

    dif = [diff_result.forces['sph__Heave']]
    dif += [diff_result.forces['sph2__Heave']]
    dif += [diff_result.forces['sph3__Heave']]
    dif += [diff_result.forces['sph4__Heave']]
    dif = np.array(dif)

    F = FK + dif
    return A,B,C,F 
