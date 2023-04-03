import capytaine as cpt

def run(r,wecx,wecy):
    def generate_body(xyz,r):
        mesh1 = cpt.meshes.predefined.mesh_sphere(radius=r,center=(xyz[0],xyz[1],xyz[2]))
        body = cpt.FloatingBody(mesh1)
        body.add_translation_dof(name='Heave')
        body = body.immersed_part()
        body.name = f'{xyz[0]}_{xyz[1]}_{xyz[2]}'
    return body
    
    xyzees = []
    for i in range(len(wecx)):
        xyzees.append(wecx[i],wecy[i],0)
    
    bodies = [generate_body(xyz) for xyz in xyzees ]

    return bodies
