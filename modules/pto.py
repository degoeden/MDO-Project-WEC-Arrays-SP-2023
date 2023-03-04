# PTO module: Handles power take-off and controller
# Inputs: damping [Ns/m], stiffness [N/m], complex_body_motion [m]
# Outputs: pto_force [N]

from scipy import signal

def pto(d,k,XI):
    s = signal.TransferFunction('s')
    pto_force = (s*d + k)*XI
    return pto_force

# help!!!