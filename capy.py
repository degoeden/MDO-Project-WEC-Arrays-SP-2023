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

# Defining original body
body = cpt.Sphere(radius=2)
body.keep_immersed_part()
body.center_of_mass = (0, 0, -2)
body.add_all_rigid_body_dofs()
body.inertia_matrix = body.compute_rigid_body_inertia()
body.hydrostatic_stiffness = body.compute_hydrostatic_stiffness()

# Duplicate into an array
array_of_bodies = body.assemble_regular_array(20,(2,1))

from scipy.linalg import block_diag
array_of_bodies.inertia_matrix = array_of_bodies.add_dofs_labels_to_matrix(
    block_diag(*[body.inertia_matrix for _ in range(2)])
    )
array_of_bodies.hydrostatic_stiffness = array_of_bodies.add_dofs_labels_to_matrix(
    block_diag(*[body.hydrostatic_stiffness for _ in range(2)])
    )
dofs = array_of_bodies.add_all_rigid_body_dofs()
print(array_of_bodies.inertia_matrix)


# solve diff and rad probs
solver = cpt.BEMSolver()

problems = [
    cpt.DiffractionProblem(body=array_of_bodies, omega=1)
    for dof in array_of_bodies.dofs]

problems += [
    cpt.RadiationProblem(body=array_of_bodies, radiating_dof=dof)
    for dof in array_of_bodies.dofs]

results = [solver.solve(pb,keep_details=(True)) for pb in sorted(problems)]
dataset = cpt.assemble_dataset(results)

# solving for RAOs

hsd = hs.Hydrostatics(mm.Mesh(array_of_bodies.mesh.vertices, array_of_bodies.mesh.faces)).hs_data
m = hsd['disp_mass']
I = array_of_bodies.inertia_matrix

rao = cpt.post_pro.rao(dataset, wave_direction=0.0)
print(rao)


array_of_bodies.show()

# creating mesh of free surface
#free_surface = cpt.FreeSurface(x_range=(-200, 200), y_range=(-200, 200), nx=200, ny=200)
#diffraction_elevation_at_faces = solver.get_free_surface_elevation(diff_result, free_surface)
#radiation_elevation_at_faces = solver.get_free_surface_elevation(rad_result, free_surface)

# add incoming waves
#h_i = free_surface.incoming_waves(diff_result)
#h_t = (diffraction_elevation_at_faces + h_i + radiation_elevation_at_faces)
#kd = h_t/h_i

# plots
#x = np.linspace(-200,200,200)
#y = np.linspace(-200,200,200)
#X, Y = np.meshgrid(x, y)
#Z = kd.reshape(200,200)
#fig, ax = plt.subplots()
#CS = ax.contour(X,Y,Z,200,cmap="viridis")
# plt.plot(-5,0,'ko',markersize=2.5)
# plt.plot(-15,0,'ko',markersize=2.5)
# plt.plot(5,0,'ko',markersize=2.5)
# plt.plot(15,0,'ko',markersize=2.5)
#fig.colorbar(CS)
#ax.set_title('Ratio of Perturbed Free Surface to Incident Wave Elevation')
#ax.set_xlabel('x [m]')
#ax.set_ylabel('y [m]')
