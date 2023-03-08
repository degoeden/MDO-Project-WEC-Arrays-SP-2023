#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:33:04 2023

@author: oliviavitale,
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
body1 = cpt.Sphere(radius=2)
body1.keep_immersed_part()
body1.center_of_mass = (0, 0, -2)


# array_of_bodies.keep_immersed_part()
# array_of_bodies.center_of_mass = (0, 0, -2)
#
body2 = body1.translated_y(20)
body2.keep_immersed_part()
body2.center_of_mass = (0, 0, -2)


array_of_bodies = body1 + body2
array_of_bodies.add_all_rigid_body_dofs()
#array_of_bodies.show()



from scipy.linalg import block_diag

# solve diff and rad probs


# solving for RAOs
#array_of_bodies = body.assemble_regular_array(20,(2,1))
print(array_of_bodies)
def bodies_hydrostatics(body):
    hsd = hs.Hydrostatics(mm.Mesh(body.mesh.vertices, body.mesh.faces)).hs_data
    m = hsd['disp_mass']
    I = np.array([[hsd['Ixx'], -1*hsd['Ixy'], -1*hsd['Ixz']],[-1*hsd['Ixy'], hsd['Iyy'], -1*hsd['Iyz']],[-1*hsd['Ixz'], -1*hsd['Iyz'], hsd['Izz']]])
    M = block_diag(m,m,m,I)
    body.mass = body.add_dofs_labels_to_matrix(M)
    stiffness = hsd['stiffness_matrix']

    kHS = block_diag(0,0,stiffness,0)
    print(kHS.shape)
    body.hydrostatic_stiffness = body.add_dofs_labels_to_matrix(kHS)
    return body

body = bodies_hydrostatics(array_of_bodies)

# Duplicate into an array

solver = cpt.BEMSolver()

problems = [
    cpt.DiffractionProblem(body=body, omega=1)
    for dof in body.dofs]

problems += [
    cpt.RadiationProblem(body=body, radiating_dof=dof)
    for dof in body.dofs]

results = [solver.solve(pb,keep_details=(True)) for pb in sorted(problems)]




dataset = cpt.assemble_dataset(results)
rao = cpt.post_pro.rao(dataset, wave_direction=0.0)
print(f"Below are the RAOs \n {rao}" )


#array_of_bodies.show()

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
