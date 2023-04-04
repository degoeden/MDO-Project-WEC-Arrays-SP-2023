# Gets the Hydrostatic Coefficients
import capytaine as cpt
import meshmagick
import meshmagick.mesh as mm
if version.parse(meshmagick.__version__) < version.parse('3.0'):
    import meshmagick.hydrostatics as hs
else:
    import meshmagick.hydrostatics_old as hs
from scipy.linalg import block_diag

def run(bodies):
    C = []
    for body in bodies:
        hsd = hs.Hydrostatics(mm.Mesh(body.mesh.vertices, body.mesh.faces)).hs_data
        KHS = block_diag(0,0,hsd['stiffness_matrix'],0)
        C.append(KHS[2,2])
    return C