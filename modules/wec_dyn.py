# Calculates the body motion RAO based on the wave exciting force RAO
# Inputs: frequency, wave exciting force RAO, Added Mass, Added Damping, Hydrostatic Restoring, mass, pto damping, pto stiffness
# Outputs: heave motion RAO

def wec_dyn(omega,F,A,B,C,m,d):
    k = (omega**2)*(A+m) - C
    if abs(k)>1e7:
        k = k/abs(k)*1e7
    XI = F/(-(A+m)*omega**2 + (B+d)*omega*1j + C+k)
    return XI
