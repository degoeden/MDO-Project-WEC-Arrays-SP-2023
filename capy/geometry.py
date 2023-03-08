"""
Created on Tue Mar  7 16:48:46 2023

@author: oliviavitale
"""

# geometry module - defining the body
# Inputs: radius [m], center [x,y,z] (each own input)
# Outputs: body [-]
import capytaine as cpt

def geometry(r,x,y,z):
  body = cpt.Sphere(radius=r,center=(x,y,z))
  body.keep_immersed_part()
  body.center_of_mass(0,0,-r)
  body.add_all_rigid_body_dofs()
  body.inertia_matrix = body.compute_rigid_body_inertia()
  body.hydrostatic_stiffness = body.compute_hydrostatic_stiffness()
  return body
