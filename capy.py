#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:33:04 2023

@author: oliviavitale
"""


import capy as cpt
import numpy as np
import matplotlib.pyplot as plt

# Defining original body
body = cpt.Sphere(radius=2)
body.keep_immersed_part()
body.center_of_mass = (0, 0, -2)
body.add_all_rigid_body_dofs()
body.inertia_matrix = body.compute_rigid_body_inertia()
body.hydrostatic_stiffness = body.compute_hydrostatic_stiffness()

# Duplicate into an array
array_of_bodies = body.assemble_regular_array(10,(10,1))

from scipy.linalg import block_diag
array_of_bodies.inertia_matrix = array_of_bodies.add_dofs_labels_to_matrix(
    block_diag(*[body.inertia_matrix for _ in range(10)])
    )
array_of_bodies.hydrostatic_stiffness = array_of_bodies.add_dofs_labels_to_matrix(
    block_diag(*[body.hydrostatic_stiffness for _ in range(10)])
    )
dofs = array_of_bodies.add_all_rigid_body_dofs()


# solve diff and rad probs
solver = cpt.BEMSolver()

diff_prob = cpt.DiffractionProblem(body=array_of_bodies, wave_direction=np.pi, omega=1)
diff_result = solver.solve(diff_prob,keep_details=(True))

rad_prob = cpt.RadiationProblem(body=array_of_bodies, radiating_dof=dofs, omega=1)
    #for dof in array_of_bodies.dofs
rad_result = solver.solve(rad_prob,keep_details=(True))

# creating mesh of free surface
free_surface = cpt.FreeSurface(x_range=(-200, 200), y_range=(-200, 200), nx=200, ny=200)
diffraction_elevation_at_faces = solver.get_free_surface_elevation(diff_result, free_surface)
radiation_elevation_at_faces = solver.get_free_surface_elevation(rad_result, free_surface)

# add incoming waves
h_i = free_surface.incoming_waves(diff_result)
h_t = (diffraction_elevation_at_faces + h_i + radiation_elevation_at_faces)
kd = h_t/h_i

# plots
x = np.linspace(-200,200,200)
y = np.linspace(-200,200,200)
X, Y = np.meshgrid(x, y)
Z = kd.reshape(200,200)
fig, ax = plt.subplots()
CS = ax.contour(X,Y,Z,200,cmap="viridis")
# plt.plot(-5,0,'ko',markersize=2.5)
# plt.plot(-15,0,'ko',markersize=2.5)
# plt.plot(5,0,'ko',markersize=2.5)
# plt.plot(15,0,'ko',markersize=2.5)
fig.colorbar(CS)
ax.set_title('Ratio of Perturbed Free Surface to Incident Wave Elevation')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
