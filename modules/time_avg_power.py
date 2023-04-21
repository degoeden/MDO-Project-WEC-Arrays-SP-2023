# Calculates Time Average Power based on RAO of heave motion
# Inputs: heave motion RAO, pto damping, frequency, and wave amplitude
# Outputs: Time Average Power

def time_avg_power(XI,d,omega,A):
    power = (1/2)*d*abs(A*XI*omega*1j)**2
    print(f"damp is {d}")
    #print(f"This is P-signal {power}")
    return power
