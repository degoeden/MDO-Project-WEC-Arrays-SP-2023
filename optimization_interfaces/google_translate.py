# Translates from scaled to normal and normal to scaled
import numpy as np

# ================================================================================= #
#                               Normal to Scaled                                    #
# ================================================================================= #
def normal2scaled(x):
    nwec = int((len(x)-2)/3 + 1)
    multiplier = {'r':1, 'x':10, 'y':100, 'd':1}
    x_bar =  np.zeros(len(x))
    x_bar[0] = x[0]*multiplier['r']
    x_bar[1] = x[1]*multiplier['d']
    for i in range(nwec-1):
        x_bar[2+i*3] = x[2+i*3]*multiplier['x']
        x_bar[3+i*3] = x[3+i*3]*multiplier['y']
        x_bar[4+i*3] = x[4+i*3]*multiplier['d']
    return x_bar


# ================================================================================= #
#                               Scaled to Normal                                    #
# ================================================================================= #
def scaled2normal(x_bar):
    nwec = int((len(x_bar)-2)/3 + 1)
    multiplier = {'r':1, 'x':10, 'y':100, 'd':1}
    x =  np.zeros(len(x_bar))
    x[0] = x_bar[0]/multiplier['r']
    x[1] = x_bar[1]/multiplier['d']
    for i in range(nwec-1):
        x[2+i*3] = x_bar[2+i*3]/multiplier['x']
        x[3+i*3] = x_bar[3+i*3]/multiplier['y']
        x[4+i*3] = x_bar[4+i*3]/multiplier['d']
    return x