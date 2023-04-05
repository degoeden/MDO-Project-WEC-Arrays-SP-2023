import modules.model_2WECs as model

# WEC design
r = 2.5
s = 2
d1 = 7.12974218e+04
d2 = 7.00031493e+03
x = [r,s,d1,d2]

# Parameters
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,2]

# Run Model and Print Results
Power_out,efficiency,LCOE = model.run(x,p)
print("Power out: ", Power_out)
print("Efficiency: ", efficiency)
print("LCOE: ", LCOE)
