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
# x = [r d1 x2 y2 d2 x3 y3 d3 x4 y4 d4]

class MyProblem(ElementwiseProblem):

    def __init__(self,p):
        super().__init__(n_var=11,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=np.array([1,0,-100,-100,0,-100,-100,0,-100,-100,0]),
                         xu=np.array([10,6,100,100,6,100,100,6,100,100,6]))
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        f1 = model.run(x,p)
        g1 = 3*x[0] - minimum_distance.run(x,p)
        out["F"] = [f1]
        out["G"] = [g1]

class MyHardProblem(ElementwiseProblem):
    
    def __init__(self,p):
        super().__init__(n_var=11,
                         n_obj=2,
                         n_ieq_constr=1,
                         xl=np.array([1,0,-100,-100,0,-100,-100,0,-100,-100,0]),
                         xu=np.array([10,6,100,100,6,100,100,6,100,100,6]))
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        f1 = model.run(x,p)
        f2 = J2.run(x,p)
        g1 = 3*x[0] - minimum_distance.run(x,p)
        out["F"] = [f1,f2]
        out["G"] = [g1]

def GA(p):       #   GA method search algorithm
    problem = MyProblem(p)
    algorithm = NSGA2(
        pop_size=10,
        n_offsprings=10,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )
    termination = get_termination("n_gen", 10)
    res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)
    X = res.X
    F = res.F
    return X,F

def MOCHA(p):       #   GA method search algorithm
    problem = MyHardProblem(p)
    algorithm = NSGA2(
        pop_size=10,
        n_offsprings=10,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )
    termination = get_termination("n_gen", 10)
    res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)
    
    #pf = problem.pareto_front(10)
    #print(f"What is this : {pf}")
    #Scatter(title='Pareto curve slayed').add(pf).show()
    
    X = res.X
    F = res.F
    plt.figure(figsize=(7, 5))
    plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
    plt.title("Objective Space")
    plt.show()
    return X,F