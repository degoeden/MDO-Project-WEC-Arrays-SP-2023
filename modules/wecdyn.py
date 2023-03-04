from scipy import signal
def wecdyn(F,A,B,C,m,d,k):
    s = signal.TransferFunction('s')
    XI = F/((A+m)*s^2 + (B+d)*s + C+k)
    return XI
