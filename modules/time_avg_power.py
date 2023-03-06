# Calculates Time Average Power based on RAO of heave motion
# Inputs: heave motion RAO, pto damping, and wave amplitude
# Outputs: Time Average Power

def time_avg_power(XI,d,A):
    power = (1/2)*d*abs(A*XI)**2
    return power