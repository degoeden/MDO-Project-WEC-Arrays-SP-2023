"""
Created on Tue Mar  7 19:07:50 2023

@author: oliviavitale
"""

# hydrodynamics module - finding RAOs
# Inputs: body, omega (w) [rad/s], wave direction (B) [rad]
# Outputs: RAOs

import capytaine as cpt

def hydrodynamics(body,w,B):
    solver = cpt.BEMSolver()
    problems = [
        cpt.DiffractionProblem(body=body, wave_direction=B, omega=w)
        for dof in body.dofs]
    problems += [
        cpt.RadiationProblem(body=body, radiating_dof=dof)
        for dof in body.dofs]
    results = [solver.solve(pb,keep_details=(True)) for pb in sorted(problems)]
    dataset = cpt.assemble_dataset(results)
    rao = cpt.post_pro.rao(dataset)                                 # response amplitude operator
    a = dataset['added_mass'].sel(radiating_dof='Heave',
                                     influenced_dof='Heave')        # added mass in heave
    b = dataset['radiation_damping'].sel(radiating_dof='Heave',
                                     influenced_dof='Heave')        # damping coeff in heave
    test = cpt.DiffractionProblem(body=body1, omega=1, wave_direction=0.)
    res = solver.solve(test)
    FK = froude_krylov_force(test)['Heave']
    dif = res.forces['Heave']
    ex_force = FK + dif                                             # exciting force in heave
    return rao,a,b,ex_force
