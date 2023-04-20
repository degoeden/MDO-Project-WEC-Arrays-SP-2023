'''Plane wave approximation stuff slay!'''
import capytaine as cpt
import numpy as np
from capytaine.bem.airy_waves import airy_waves_potential, airy_waves_velocity, froude_krylov_force
import scipy.integrate as scipy_int
import shutup
def run(bodies,xyzees,rho,omega,beta):
    #print("entering pwa_func")
    
    def get_results(problems):
        results = [solver.solve(pb, keep_details = True) for pb in problems]
        return results


    #calculate angle theta_ij from centre of one body to other
    def theta_ij(X,Y): 
        x1,y1= X[0],X[1]
        x2,y2 = Y[0], Y[1]

        if x1 ==x2 and y1==y2:
            return 0
        if x2==x1:
            theta = np.pi/2
        else:
            theta = np.arctan((y2-y1)/(x2-x1))
        return theta



    def phi_ij(pot,omega,x,y,k,theta):
        amplitude = -1*pot *(1/(-1j * 10*np.exp(k*(z + 1j*(x*np.cos(theta) + y*np.sin(theta))))))
        return amplitude


    #step 2
    def phi_j_star(phi_ij,theta,X,Y,z,k,iterate):

        '''phi_ij is the vector of the effect at that i body from j body'''
        x,y = X[0],X[1]
        xj,yj = Y[0],Y[1]
       # phi_ij = (phi_ij,omega,x,y,k,theta)
        if x==xj and y==yj:
            return 0
        multiplier = np.exp(1j*k*(((x-xj))*np.cos(theta) + (y-yj)*np.sin(theta)))
     #   print(f"th emnultiplier: {multiplier}")
        if iterate==0:
            pot = phi_ij * multiplier #kz = 0 #e^kz = 1 #takes phi_ij =1 
        else:
            pot = phi_ij/multiplier #return amplitude only

        return pot

    #{(10, 10, 0): {(10, 10, 0): 0,
      #(0, 0, 0): (8.415476709952118-2.9519008598532284j),
      #(5, 5, 0): (8.415476709952118-2.9519008598532284j),
      #(15, 15, 0): (8.415476709952118-2.9519008598532284j)

    def get_neighbors(xyzees):
        neighbor = {xyz:[] for xyz in xyzees}
        for xyz in xyzees:
            for zyx in xyzees:
                if not xyz == zyx:
                    neighbor[xyz].append(zyx)
        return neighbor

    def get_phistarj_sum(phi_starj,xyzees):
        xyz_phi = {xyz :[] for xyz in xyzees}
        for k,v in phi_starj.items():
            for s,m in v.items():
                xyz_phi[k].append(m)
        xyz_phi = {k:sum(v) for k,v in xyz_phi.items()}
       
        return xyz_phi





    def solve(diff,diff_res, rad_res,new_potential,keep_details=True):
        """Solve the linear potential flow problem.
        Parameters
        ----------
        problem: LinearPotentialFlowProblem
            the problem to be solved
        keep_details: bool, optional
            if True, store the sources and the potential on the floating body in the output object
            (default: True)
        Returns
        -------
        LinearPotentialFlowResult
            an object storing the problem data and its results
        """
        
        diff_pot = diff_res.potential
       
        rad_pot = rad_res.potential
        potential =   new_potential + diff_pot + rad_pot
        
        rho = 1023
        new_pressure = rho * potential
        # Actually, for diffraction problems: pressure over jω
        #           for radiation problems:   pressure over -ω²
        # The correction is done in `store_force` in the `result` object.

        new_forces = diff.body.integrate_pressure(new_pressure)
        #if np.abs(new_forces['Heave']) > 1e6:
            #gam = 1e6/np.abs(new_forces['Heave'])
            #new_forces['Heave'] = gam*new_forces['Heave'].real + gam*new_forces['Heave'].imag*1j
            #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$@ND")
            #print('we at MAX FORCE!!!!!!!!!!!')
            #print(np.abs(new_forces['Heave']))
            #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$@ND")
        body = diff.body
        #r = float(body.name.split('_')[2])
        #a33 = lambda z: np.pi*rho*(r**2 - z**2)
        #A33 = scipy_int.quad(a33,-r,0)[0]
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$@ND")
        #print(A33)
        #print(new_forces['Heave'].real)
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$@ND")
        
        def inf_hydrodynamics(body,w,B):
            #shutup.please()
            solver = cpt.BEMSolver()
            problems = [
                cpt.DiffractionProblem(body=body, wave_direction=B, omega=w)
                for dof in body.dofs]
            problems += [
                cpt.RadiationProblem(body=body, radiating_dof=dof)
                for dof in body.dofs]
            results = [solver.solve(pb,keep_details=(True)) for pb in sorted(problems)]
            dataset = cpt.assemble_dataset(results)
            a = dataset['added_mass'].sel(radiating_dof='Heave',
                                            influenced_dof='Heave')        # added mass in heave
            b = dataset['radiation_damping'].sel(radiating_dof='Heave',
                                            influenced_dof='Heave')        # damping coeff in heave
            #shutup.jk()
            return a[0],b[0]
        omega_inf = 1e3

        Ainf,Binf = inf_hydrodynamics(body,omega_inf,beta)
        #print(f"\n natural freq stuff {Ainf}           &&&              {Binf}")
        if np.abs(new_forces['Heave'].real) > Ainf*2:
            #print(f"BAD added mass {np.abs(new_forces['Heave'].real)}")
            new_forces['Heave'] = (new_forces['Heave'].real/np.abs(new_forces['Heave'].real))*Ainf*2 + new_forces['Heave'].imag*1j
            #print(f"this is Ainf: {Ainf}")
            #print(f"we should do this...{new_forces['Heave']}")
        if np.abs(new_forces['Heave'].imag) > (Binf/omega)*2:
            #print(f"BAD damping {np.abs(new_forces['Heave'].imag)}")
            new_forces['Heave'] = (new_forces['Heave'].imag/np.abs(new_forces['Heave'].imag))*Binf*2 + new_forces['Heave'].real
            #print(f"This is Binf: {Binf}")
            #print(f"we should do this...{new_forces['Heave']}")
        if not keep_details:
            results = diff.make_results_container(new_forces)
        else:
            results = diff.make_results_container(new_forces, diff_res.sources, potential, new_pressure)

        dataset1 = cpt.assemble_dataset([rad_res])
        added_mass = np.abs(new_forces['Heave'].real)
        #added_mass = dataset1['added_mass'].sel(radiating_dof='Heave',influenced_dof='Heave')

        #print(f"added_mass compare==========================>{added_mass} and {dataset1['added_mass'].sel(radiating_dof='Heave',influenced_dof='Heave')} ")
       
        
        damping = np.abs(new_forces['Heave'].imag) * diff.omega #abs because damping should be positive? does not make sense
        #damping = dataset1['radiation_damping'].sel(radiating_dof='Heave',influenced_dof='Heave')
        return new_forces, {'added_mass':added_mass}, {'damping':damping}

    # ============================================ #
    # Where the actual code happens...             #
    # ============================================ #
    wave_num =  (omega**2)/9.81

    N_bodies = len(bodies)
    max_iteration = N_bodies #(dead or alive lol)

    # body_potential_at_neighbors = {body:(dict(zip(body_neighbors_locs[body], 
    #                                       airy_waves_potential(np.array(body_neighbors_locs[body]),diff_problems[body])))) for body in bodies}
    

#    neighbors = {(0,0,0):[(5,5,0),(10,10,0),(15,15,0)],  #so bad..need to write a funky func for it
#                (10,10,0):[(0,0,0),(5,5,0),(15,15,0)],
#                 (5,5,0):[(0,0,0),(10,10,0),(15,15,0)],
#                 (15,15,0):[(0,0,0),(10,10,0),(5,5,0)]     
#                }
    
    neighbors = get_neighbors(xyzees)

    loc_bodies = {body:xyz for xyz,body in zip(xyzees,bodies)}
    loc_to_body = {xyz:body for xyz,body in zip(xyzees,bodies)}
    solver = cpt.BEMSolver()


    diff_problems = {body:cpt.DiffractionProblem(body=body, sea_bottom=-np.infty,
                                          omega=omega, wave_direction=beta) for body in bodies}
    loc_diff = {loc_bodies.get(body):diff for body,diff in diff_problems.items() }

    rad_problems = {body: cpt.RadiationProblem(body=body, sea_bottom=-np.infty,
                                          omega=omega) for body in bodies}

    diff_results = {body:solver.solve(problem) for body,problem in diff_problems.items()}

    rad_results = {body:solver.solve(problem) for body,problem in rad_problems.items()}



#assembling added mass individually

   # added_mass = {body: cpt.assemble_dataset([res])['added_mass'].sel(radiating_dof='Heave',influenced_dof='Heave') for body,res in rad_results.items()}
   
   


    body_neighbors_locs = {body:neighbors.get(loc_bodies.get(body)) for body in bodies}

    body_potential_at_neighbors = {body:{nbros : airy_waves_potential(np.array(body_neighbors_locs[body]),diff_problems[body])
                                                  for nbros in neighbors} for xyz,body in loc_to_body.items()}


    
    all_other_phi_each_loc = {xyz:{loc_bodies.get(d):k.get(xyz,0) for d,k in body_potential_at_neighbors.items()} for xyz in xyzees}


    thetas = {k:{s:theta_ij(k,s) for s,m in v.items()} for k,v in all_other_phi_each_loc.items()}

    z = 0
    #phi_starj = {xyz:{nbros:phi_j_star(all_other_phi_each_loc[xyz][nbros],thetas[xyz][nbros],nbros,xyz,z,wave_num,omega) for nbros in neighbors} for xyz in xyzees}

    #new_excitation = get_phistarj_sum(phi_starj,xyzees)
    
    body_amplitude_at_neighbors = {body:{nbros : 1.0 for nbros in neighbors} for xyz,body in loc_to_body.items()}
    
    iterate = 0
    while iterate<max_iteration:
        # def get_all_other_phi(body_potential_at_neighbors):
        all_other_phi_each_loc = {xyz:{loc_bodies.get(d):k.get(xyz,0) for d,k in body_amplitude_at_neighbors.items()} for xyz in xyzees}
        #print(all_other_phi_each_loc)
        thetas = {k:{s:theta_ij(k,s) for s,m in v.items()} for k,v in all_other_phi_each_loc.items()}
        phi_starj = {xyz:{nbros:phi_j_star(all_other_phi_each_loc[xyz][nbros],thetas[xyz][nbros],nbros,xyz,z,wave_num,iterate) for nbros in neighbors} for xyz in xyzees}
        #print(phi_starj)

        new_excitation = get_phistarj_sum(phi_starj,xyzees)
       # # look at the new excitation amplitude and reject if the amplitude is bigger than the last two
       #  print("\n")
       #  print(f"excitation for {iterate}")
       #  print(new_excitation)
       #  print("\n")


        body_amplitude_at_neighbors = {body:{nbros : phi_j_star(new_excitation[xyz],thetas[loc_bodies[body]][nbros],nbros,xyz,z,wave_num,iterate) 
                                              for nbros in neighbors} for xyz,body in loc_to_body.items()}
       # print(new_excitation)

        iterate+=1

    new_potential = get_phistarj_sum(phi_starj,xyzees)
  
    new_results = {loc_to_body.get(loc):solve(diff_prob,diff_results[loc_to_body.get(loc)],rad_results[loc_to_body.get(loc)], np.sum(new_potential[loc])) for loc,diff_prob in loc_diff.items()}
    #print("exiting pwa_func")
    return new_results
