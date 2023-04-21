# Contains Functions to complets A3b
import scipy.optimize as scipy_opt
import numpy as np
import matplotlib.pyplot as plt
import modules.model_nWECs as model
import modules.model_nWECs_fixr as model_fixr
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.core.problem import ElementwiseProblem
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
import modules.constraint as constraint
import modules.maximum_distance as J2
# x = [d1 x2 y2 d2 x3 y3 d3 x4 y4 d4]

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
        print(f"Our parameters are {p}")
        f1 = model.run(x,p)
        g1 = constraint.run(x,p)
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
        print(f"Our parameters are {p}")
        f1 = model.run(x,p)
        f2 = J2.run(x,p)
        g1 = constraint.run(x,p)
        out["F"] = [f1,f2]
        out["G"] = [g1]

def distance_check(wecx,wecy,r):
    n = len(wecx)
    d = []
    for i in range(n):
        for j in range(i+1,n):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))
    mind = min(d)
    if mind<10*r:
        return 10000*(10*r - mind)**2     
    return 0

def objective1(x,args):         #   Calculates LCOE
    p = args
    if len(p)==4:
        nwec = p[3]
        r = x[0]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec):
            wecx[i] = x[1+i*3]
            wecy[i] = x[2+i*3]

        Power_out,LCOE = model.run(x,p)  #   runs the model
    else:
        nwec = p[3]
        r = p[4]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec-1):
            wecx[i+1] = x[1+i*3]
            wecy[i+1] = x[2+i*3]

        Power_out,LCOE = model_fixr.run(x,p)  #   runs the model
    LCOE = LCOE + distance_check(wecx,wecy,r)
    print(f"This is LCOE {LCOE}")
    return LCOE

def maximumD(wecx,wecy):
    n = len(wecx)
    d = []
    for i in range(n):
        for j in range(i+1,n):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))
    maxd = max(d)    
    return maxd

def objective2(x,args):         #   Calculates LCOE
    p = args
    if len(p)==4:
        nwec = p[3]
        r = x[0]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec):
            wecx[i] = x[1+i*3]
            wecy[i] = x[2+i*3]

        Power_out,LCOE = model.run(x,p)  #   runs the model
    else:
        nwec = p[3]
        r = p[4]
        wecx = np.zeros(nwec)
        wecy = np.zeros(nwec)
        for i in range(nwec-1):
            wecx[i+1] = x[1+i*3]
            wecy[i+1] = x[2+i*3]
    maxd = maximumD(wecx,wecy)
    maxd = maxd + distance_check(wecx,wecy,r)
    return maxd

def gradient_method(x0,p,bnds,opt):     #   Gradient Method Search Algorithm
    history = []
    def callback(x,p):
        fobj = objective1(x,p)
        history.append(fobj)
    res = scipy_opt.minimize(objective1, x0, method='slsqp', args=p, bounds=bnds, options=opt)
    print("The values at each iteration")
    return res.x

def heuristic_method(p):       #   GA method search algorithm
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
    #Scatter(title='Pareto curve slayed').add(pf).show()
    
    X = res.X
    F = res.F
    plt.figure(figsize=(7, 5))
    plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
    plt.title("Objective Space")
    plt.show()
    return X,F