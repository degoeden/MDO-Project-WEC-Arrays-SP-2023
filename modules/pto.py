# PTO module: Handles power take-off and controller
# Inputs: damping [Ns/m], stiffness [N/m], complex_body_motion [m]
# Outputs: pto_force [N], power_out [W]

from scipy import signal

def pto(d,k,XI):
    s = signal.TransferFunction('s')
    pto_force = (s*d + k)*XI
    power_out = 0
    return pto_force,power_out

