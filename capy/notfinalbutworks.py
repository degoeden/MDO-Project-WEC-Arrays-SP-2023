#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:33:04 2023

@author: oliviavitale
"""


import capytaine as cpt
import numpy as np
import matplotlib.pyplot as plt
import meshmagick
import meshmagick.mesh as mm
from packaging import version
if version.parse(meshmagick.__version__) < version.parse('3.0'):
    import meshmagick.hydrostatics as hs
else:
    import meshmagick.hydrostatics_old as hs
from scipy.linalg import block_diag
from capytaine.bem.airy_waves import airy_waves_potential, airy_waves_velocity, froude_krylov_force


def run(radius_in,L_in):
    # define bodies
    body1 = cpt.Sphere(radius=radius_in,center=(0,0,0))
    body1.keep_immersed_part()
    body1.center_of_mass = (0, 0, -radius_in)
    body1.add_all_rigid_body_dofs()
    body1.inertia_matrix = body1.compute_rigid_body_inertia()
    body1.hydrostatic_stiffness = body1.compute_hydrostatic_stiffness()
    body2 = cpt.Sphere(radius=radius_in,center=(0,L_in,0))
    body2.keep_immersed_part()
    body2.center_of_mass = (0, 0, -radius_in)
    body2.add_all_rigid_body_dofs()
    body2.inertia_matrix = body2.compute_rigid_body_inertia()
    body2.hydrostatic_stiffness = body2.compute_hydrostatic_stiffness()
    # hydrostatics
    hsd1 = hs.Hydrostatics(mm.Mesh(body1.mesh.vertices, body1.mesh.faces)).hs_data
    m1 = hsd1['disp_mass']
    I1 = body1.inertia_matrix
    M1 = block_diag(m1,m1,m1,I1)
    body1.mass = body1.add_dofs_labels_to_matrix(I1)
    KHS1 = block_diag(0,0,hsd1['stiffness_matrix'],0)
    body1.hydrostatic_stiffness = body1.add_dofs_labels_to_matrix(KHS1)
    c1 = KHS1[2,2]
    hsd2 = hs.Hydrostatics(mm.Mesh(body2.mesh.vertices, body2.mesh.faces)).hs_data
    m2 = hsd2['disp_mass']
    I2 = body2.inertia_matrix
    M2 = block_diag(m2,m2,m2,I2)
    body2.mass = body2.add_dofs_labels_to_matrix(I2)
    KHS2 = block_diag(0,0,hsd2['stiffness_matrix'],0)
    body2.hydrostatic_stiffness = body2.add_dofs_labels_to_matrix(KHS2)
    c2 = KHS2[2,2]
    # hydrodynamics
    solver = cpt.BEMSolver()
    problems1 = [
        cpt.DiffractionProblem(body=body1, omega=1)
        for dof in body1.dofs]
    problems1 += [
        cpt.RadiationProblem(body=body1, radiating_dof=dof)
        for dof in body1.dofs]
    results1 = [solver.solve(pb,keep_details=(True)) for pb in sorted(problems1)]
    dataset1 = cpt.assemble_dataset(results1)
    rao1 = cpt.post_pro.rao(dataset1)
    print(rao1)
    problems2 = [
        cpt.DiffractionProblem(body=body2, omega=1)
        for dof in body2.dofs]
    problems2 += [
        cpt.RadiationProblem(body=body2, radiating_dof=dof)
        for dof in body2.dofs]
    results2 = [solver.solve(pb,keep_details=(True)) for pb in sorted(problems2)]
    dataset2 = cpt.assemble_dataset(results2)
    rao2 = cpt.post_pro.rao(dataset2)
    # added mass and damping
    b1 = dataset1['radiation_damping'].sel(radiating_dof='Heave',
                                     influenced_dof='Heave')
    a1 = dataset1['added_mass'].sel(radiating_dof='Heave',
                                     influenced_dof='Heave')

    b2 = dataset2['radiation_damping'].sel(radiating_dof='Heave',
                                     influenced_dof='Heave')
    a2 = dataset2['added_mass'].sel(radiating_dof='Heave',
                                     influenced_dof='Heave')
    # heave exciting force
    test1 = cpt.DiffractionProblem(body=body1, omega=1, wave_direction=0.)
    res1 = solver.solve(test1)
    FK1 = froude_krylov_force(test1)['Heave']
    dif1 = res1.forces['Heave']
    ex_force1 = FK1 + dif1
    print('body 1 heave exciting force',ex_force1)

    test2 = cpt.DiffractionProblem(body=body2, omega=1, wave_direction=0.)
    res2 = solver.solve(test2)
    FK2 = froude_krylov_force(test2)['Heave']
    dif2 = res2.forces['Heave']
    ex_force2 = FK2 + dif2
    print('body 2 heave exciting force',ex_force2)
    return [(ex_force1.to_numpy(),a1.to_numpy(),b1.to_numpy(),c1.to_numpy()),(ex_force2.to_numpy(),a2.to_numpy(),b2.to_numpy(),c2.to_numpy())]
