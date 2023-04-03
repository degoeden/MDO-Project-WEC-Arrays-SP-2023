import modules.model_2WECs as model

# WEC design
r = 2
L = 20
d1 = 100
d2 = 100
x = [r,L,d1,d2]

# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,2]

# Run Model and Print Results
Power_out,efficiency,LCOE,stif = model.run(x,p)
print("Power out: ", Power_out)
print("Efficiency: ", efficiency)
print("LCOE: ", LCOE)
