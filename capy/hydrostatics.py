"""
Created on Tue Mar  7 17:01:16 2023

@author: oliviavitale
"""

# hydrostatics module - defining the body
# Inputs: body
# Outputs: hydrostatic stiffness

import capytaine as cpt
import meshmagick
import meshmagick.mesh as mm
from packaging import version
if version.parse(meshmagick.__version__) < version.parse('3.0'):
    import meshmagick.hydrostatics as hs
else:
    import meshmagick.hydrostatics_old as hs
from scipy.linalg import block_diag

def hydrostatics(body):
    hsd = hs.Hydrostatics(mm.Mesh(body.mesh.vertices, body.mesh.faces)).hs_data
    m = hsd['disp_mass']
    I = body.inertia_matrix
    M = block_diag(m,m,m,I)
    body.mass = body.add_dofs_labels_to_matrix(I)
    KHS = block_diag(0,0,hsd['stiffness_matrix'],0)
    body.hydrostatic_stiffness = body.add_dofs_labels_to_matrix(KHS)
    return I, M, hydrostatics(body)
