
def wecdyn(omega,F,A,B,C,m,d,k):
    XI = F/(-(A+m)*omega**2 + (B+d)*omega*1j + C+k)
    return XI
