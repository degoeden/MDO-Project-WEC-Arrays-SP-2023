# Calculates the body motion RAO based on the wave exciting force RAO
# Inputs: frequency, wave exciting force RAO, Added Mass, Added Damping, Hydrostatic Restoring, mass, pto damping, pto stiffness
# Outputs: heave motion RAO

def wecdyn(omega,F,A,B,C,m,d,k):
    XI = F/(-(A+m)*omega**2 + (B+d)*omega*1j + C+k)
    return XI
