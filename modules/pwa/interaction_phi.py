def interaction_phi(radius):
    '''takes radius = 0.5m for now..look at the default xyz for now.. and create its neighbor and provide it..
    for now lets go with this'''
    def generate_body(xyz):
        mesh1 = cpt.meshes.predefined.mesh_sphere(radius=radius,center=(xyz[0],xyz[1],xyz[2]))
        body = cpt.FloatingBody(mesh1)
        body.add_translation_dof(name='Heave')
        body = body.immersed_part()
        body.name = f'{xyz[0]}_{xyz[1]}_{xyz[2]}'
        return body


    def get_results(problems):
        results = [solver.solve(pb, keep_details = True) for pb in sorted(problems)]
        return results


    #calculate angle theta_ij from centre of one body to other
    def theta_ij(X,Y): 
        x1,y1= X[0],X[1]
        x2,y2 = Y[0], Y[1]
        if x2==x1:
            theta = np.pi/2
        else:
            theta = np.arctan((y2-y1)/(x2-x1))
        return theta


    #step 2
    def phi_j_star(phi_ij,theta,X,Y,z,k):

        '''phi_ij is the vector of all the effect at that body from all other bodies'''
        x,y = X[0],X[1]
        xj,yj = Y[0],Y[1]
        res = phi_ij *np.exp(k*z)*np.exp(1j*k*(x-xj)*np.cos(theta) + (y-yj)*np.sin(theta))
        return res


    def get_phistarj_sum(phi_starj,xyzees):
        xyz_phi = {xyz:[] for xyz in xyzees}
        for k,v in phi_starj.items():
            for s,m in v.items():
                xyz_phi[k].append(m)
        xyz_phi = {k:sum(v) for k,v in xyz_phi.items()}
        return xyz_phi
    
    
    xyzees = {(0,0,0),(10,10,0),(5,5,0),(7,11,0)}
    
    bodies = [generate_body(xyz) for xyz in xyzees ]

    neighbors = {(0,0,0):[(10,10,0),(5,5,0),(7,11,0),(0,0,0)],  #so bad..need to write a funky func for it
                (10,10,0):[(0,0,0),(5,5,0),(7,11,0),(10,10,0)],
                 (5,5,0):[(0,0,0),(10,10,0),(7,11,0),(5,5,0)],
                 (7,11,0):[(0,0,0),(10,10,0),(5,5,0),(7,11,0)]     
                }
    loc_bodies = {body:xyz for xyz,body in zip(xyzees,bodies)}
    loc_to_body = {xyz:body for xyz,body in zip(xyzees,bodies)}
    solver = cpt.BEMSolver()


    diff_problems = {body:cpt.DiffractionProblem(body=body, sea_bottom=-np.infty,
                                          omega=omega, wave_direction=0.) for body in bodies}

    rad_problems = {body: cpt.RadiationProblem(body=body, sea_bottom=-np.infty,
                                          omega=omega) for body in bodies}

    diff_results = {body.name:solver.solve(problem) for body,problem in diff_problems.items()}
    rad_results = {body.name:solver.solve(problem) for body,problem in rad_problems.items()}
    body_neighbors_locs = {body:neighbors.get(loc_bodies.get(body)) for body in bodies}
    body_potential_at_neighbors = {body:(dict(zip(body_neighbors_locs[body], 
                                      airy_waves_potential(np.array(body_neighbors_locs[body]),diff_problems[body])))) for body in bodies}
    
    # def get_all_other_phi(body_potential_at_neighbors):
    all_other_phi_each_loc = {xyz:{loc_bodies.get(d):k.get(xyz,0) for d,k in body_potential_at_neighbors.items()} for xyz in xyzees}
    thetas = {k:{s:theta_ij(k,s) for s,m in v.items()} for k,v in all_other_phi_each_loc.items()}
    z = 0
    phi_starj = {xyz:{nbros:phi_j_star(all_other_phi_each_loc[xyz][nbros],thetas[xyz][nbros],nbros,xyz,z,wave_num) for nbros in neighbors} for xyz in xyzees}
    new_excitation = get_phistarj_sum(phi_starj,xyzees)
    body_potential_at_neighbors = {body:{nbros : phi_j_star(new_excitation[xyz],thetas[loc_bodies[body]][nbros],nbros,xyz,z,wave_num)
                                              for nbros in neighbors} for body in bodies }
    
    
    N_bodies = 4
    max_iteration = 2*N_bodies #(dead or alive lol)

    body_potential_at_neighbors = {body:(dict(zip(body_neighbors_locs[body], 
                                      airy_waves_potential(np.array(body_neighbors_locs[body]),diff_problems[body])))) for body in bodies}
    iterate = 0
    while iterate<max_iteration:
        # def get_all_other_phi(body_potential_at_neighbors):
        all_other_phi_each_loc = {xyz:{loc_bodies.get(d):k.get(xyz,0) for d,k in body_potential_at_neighbors.items()} for xyz in xyzees}
        thetas = {k:{s:theta_ij(k,s) for s,m in v.items()} for k,v in all_other_phi_each_loc.items()}
        phi_starj = {xyz:{nbros:phi_j_star(all_other_phi_each_loc[xyz][nbros],thetas[xyz][nbros],nbros,xyz,z,wave_num) for nbros in neighbors} for xyz in xyzees}

        new_excitation = get_phistarj_sum(phi_starj,xyzees)
        body_potential_at_neighbors = {body:{nbros : phi_j_star(new_excitation[xyz],thetas[loc_bodies[body]][nbros],nbros,xyz,z,wave_num)
                                                  for nbros in neighbors} for body in bodies}

        print(body_potential_at_neighbors)
        print("/n")

        iterate+=1
    return body_potential_at_neighbors


    
    


