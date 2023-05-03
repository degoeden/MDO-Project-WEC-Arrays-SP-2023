# Handels basic GA and MOCHA stuff
import numpy as np
import matplotlib.pyplot as plt
import modules.model_nWECs as model
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.core.problem import ElementwiseProblem
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
import modules.minimum_distance as minimum_distance
import modules.maximum_distance as J2
# x = [r d1 x2 y2 d2 x3 y3 d3, ... etc]

# ================================================================================= #
#                               Single Objective                                    #
# ================================================================================= #
class MyProblem(ElementwiseProblem):        #   Sinlge Objective Problem

    def __init__(self,p,limits):            #   P is parameters, limits is the bounds on each var type
        nwec = p[3]
        n_var=3*(nwec-1)+2
        xl = np.zeros(n_var)                #   Lower bounds
        xu = np.zeros(n_var)
        xl[0] = limits['r'][0]
        xu[0] = limits['r'][1]
        xl[1] = limits['d'][0]
        xu[1] = limits['d'][1]
        for i in range(nwec-1):
            xl[i*3+2] = limits['x'][0]
            xu[i*3+2] = limits['x'][1]
            xl[i*3+3] = limits['y'][0]
            xu[i*3+3] = limits['y'][1]
            xl[i*3+4] = limits['d'][0]
            xu[i*3+4] = limits['d'][1]
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        f1 = model.run(x,p)                         #   Run the model
        g1 = 3*x[0] - minimum_distance.run(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]

def GA(p,limits):       #   GA method search algorithm
    problem = MyProblem(p,limits)
    algorithm = NSGA2(
        pop_size=100,
        n_offsprings=50,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )
    termination = get_termination("n_gen", 100)
    res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)
    X = res.X
    F = res.F
    H = res.history
    return X,F,H


# ================================================================================= #
#                                     MOCHA                                         #
# ================================================================================= #
class MyHardProblem(ElementwiseProblem):    # same problem as before, except 2 objectives
    
    def __init__(self,p,limits):
        nwec = p[3]
        n_var=3*(nwec-1)+2
        xl = np.zeros(n_var)
        xu = np.zeros(n_var)
        xl[0] = limits['r'][0]
        xu[0] = limits['r'][1]
        xl[1] = limits['d'][0]
        xu[1] = limits['d'][1]
        for i in range(nwec-1):
            xl[i*3+2] = limits['x'][0]
            xu[i*3+2] = limits['x'][1]
            xl[i*3+3] = limits['y'][0]
            xu[i*3+3] = limits['y'][1]
            xl[i*3+4] = limits['d'][0]
            xu[i*3+4] = limits['d'][1]
        super().__init__(n_var=n_var,
                         n_obj=2,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        f1 = model.run(x,p)
        f2 = J2.run(x,p)                #   2nd objective is minimizing the maximum spacing between wecs
        g1 = 3*x[0] - minimum_distance.run(x,p)
        out["F"] = [f1,f2]
        out["G"] = [g1]

def MOCHA(p,limits):       #   Multi Objective Constrained Heuristic Algorithim
    problem = MyHardProblem(p,limits)
    algorithm = NSGA2(
        pop_size=50,
        n_offsprings=30,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )
    termination = get_termination("n_gen", 1000)
    res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)
    
    X = res.X
    F = res.F
    H = res.history
    return X,F,H