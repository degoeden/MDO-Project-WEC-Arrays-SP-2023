import modules.model_2WECs as model

# WEC design
r = 2
L = 20
d1 = 100
d2 = 100
k1 = 300
k2 = 300
x = [r,L,d1,k1,d2,k2]

# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec]

Power_out,efficiency,LCOE = model.run(x,p)
print("--------------------------------------")
print("Power out: ", Power_out)
print("Efficiency: ", efficiency)
print("LCOE: ", LCOE)
