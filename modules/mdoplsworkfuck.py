"""
Created on Thu Apr 20 15:26:43 2023

@author: oliviavitale
"""


# hydrostatics

import capytaine as cpt
import numpy as np
import meshmagick
import meshmagick.mesh as mm
from packaging import version
if version.parse(meshmagick.__version__) < version.parse('3.0'):
    import meshmagick.hydrostatics as hs
else:
    import meshmagick.hydrostatics_old as hs
from scipy.linalg import block_diag
from capytaine.bem.airy_waves import airy_waves_potential, airy_waves_velocity, froude_krylov_force

# parameters
    # r = 5
    # x2 = 50
    # x3 = 100
    # x4 = 15
    # y2 = 0
    # y3 = 0
    # y4 = 0
    # Defining original body

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

    # hydrostatics
    hsd = hs.Hydrostatics(mm.Mesh(array.mesh.vertices, array.mesh.faces)).hs_data
    m = hsd['disp_mass']
    I = array.inertia_matrix
    M = block_diag(I)

    # solve diff and rad probs
    solver = cpt.BEMSolver()

    diff_prob = cpt.DiffractionProblem(body=array.immersed_part(), wave_direction=wave_direction, omega=omega)
    diff_result = solver.solve(diff_prob,keep_details=(True))

    rad_prob = [
        cpt.RadiationProblem(body=array.immersed_part(), radiating_dof=dof, omega=omega)
        for dof in array.dofs ]
    rad_result = solver.solve_all(rad_prob,keep_details=(True))

    dataset = cpt.assemble_dataset(rad_result + [diff_result])

    # raos
    rao = cpt.post_pro.rao(dataset,wave_direction=wave_direction)
    # print('array RAO',rao)

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
    print('damping',B)

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
    print('added mass',A)

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
    #print('stiffness',K)

    # inertia matrix
    M1 = np.array(dataset['inertia_matrix'].sel(radiating_dof=['sph__Heave'],
                                        influenced_dof=['sph__Heave']))
    M2 = np.array(dataset['inertia_matrix'].sel(radiating_dof=['sph2__Heave'],
                                        influenced_dof=['sph2__Heave']))
    M3 = np.array(dataset['inertia_matrix'].sel(radiating_dof=['sph3__Heave'],
                                        influenced_dof=['sph3__Heave']))
    M4 = np.array(dataset['inertia_matrix'].sel(radiating_dof=['sph4__Heave'],
                                        influenced_dof=['sph4__Heave']))
    m = np.array([M1, M2, M3, M4])
    #print('mass',m)


    # heave exciting forces
    FK = [froude_krylov_force(diff_prob)['sph__Heave']]
    FK += [froude_krylov_force(diff_prob)['sph2__Heave']]
    FK += [froude_krylov_force(diff_prob)['sph3__Heave']]
    FK += [froude_krylov_force(diff_prob)['sph4__Heave']]
    #print('froude_krylov',FK)
    FK = np.array(FK)

    dif = [diff_result.forces['sph__Heave']]
    dif += [diff_result.forces['sph2__Heave']]
    dif += [diff_result.forces['sph3__Heave']]
    dif += [diff_result.forces['sph4__Heave']]
    #print('diffraction force',dif)
    dif = np.array(dif)

    F = FK + dif

    #print('complex exciting force',ex_force)

    mag = np.abs(F)

    #print('array heave exciting force',mag)
    return A,B,C,F 
