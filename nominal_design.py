import main

# Initial WEC design
r = 2
L = 20
d1 = 100
d2 = 100
k1 = 300
k2 = 300

# Parameter
omega = 1.047
A = 1.5
rho = 850


x = [r,L,d1,k1,d2,k2]

Power_out,efficiency,LCOE = main.evaluate(x,0,omega,rho,A)
print("--------------------------------------")
print("Power out: ", Power_out)
print("Efficiency: ", efficiency)
print("LCOE: ", LCOE)