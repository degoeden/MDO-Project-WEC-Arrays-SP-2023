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
    rao = cpt.post_pro.rao(dataset)
    return rao
