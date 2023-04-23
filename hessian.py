# 
import numpy as np
import matplotlib.pyplot as plt
import modules.model_nWECs as model
import modules.minimum_distance as minimum_distance
import modules.maximum_distance as J2

# Parameters
nwec = 4
omega = 1.047
A = 1.5
rho_wec = 850
p = [omega,A,rho_wec,nwec]

# x = [r d1 x2 y2 d2 x3 y3 d3 x4 y4 d4]

x = np.array([5,6,100,-100,6,50,-50,6,150,-150,6])

# Second order central finite difference
# f''~ [f(x+h)-2f(x)+f(x-h)]/h^2

f0 = model.run(x,p)
n=4
f=np.zeros([4,14])

for i in range(n):
    dx=np.zeros(len(x))
    dy=np.zeros(len(x))
    dz=np.zeros(len(x))
    da=np.zeros(len(x))
    dx[i]=h
    dy[(i+1)%n]=h
    dz[(i+2)%n]=h
    da[(i+3)%n]=h
    f[i,0]=model.run(x+dx,p)
    f[i,1]=model.run(x-dx,p)
    if i<1:
        f[i,10]=model.run(x-dz+da,p)
        f[i,11]=model.run(x-dz-da,p)
        f[i,12]=model.run(x+dz+da,p)
        f[i,13]=model.run(x+dz-da,p)

    if i<2:
        f[i,6]=model.run(x-dy+dz,p)
        f[i,7]=model.run(x-dy-dz,p)
        f[i,8]=model.run(x+dy+dz,p)
        f[i,9]=model.run(x+dy-dz,p)
    
    if i<3:
        f[i,2]=model.run(x-dx+dy,p)
        f[i,3]=model.run(x-dx-dy,p)
        f[i,4]=model.run(x+dx+dy,p)
        f[i,5]=model.run(x+dx-dy,p)
    
    


hrr=(f[0,0]-(2*f0)+f[0,1])/h**2
hrd=(f[0,4]-f[0,5]-f[0,2]+f[0,3])/(4*h**2)
hrx=(f[0,6]-f[0,7]-f[0,9]+f[0,8])/(4*h**2)
hry=(f[0,10]-f[0,11]-f[0,13]+f[0,12])/(4*h**2)

hdd=(f[1,0]-(2*f0)+f[1,1])/h**2
hdx=(f[1,4]-f[1,5]-f[1,2]+f[1,3])/(4*h**2)
hdy=(f[1,6]-f[1,7]-f[1,9]+f[1,8])/(4*h**2)

hxx=(f[2,0]-(2*f0)+f[2,1])/h**2
hxy=(f[2,4]-f[2,5]-f[2,2]+f[2,3])/(4*h**2)

hyy=(f[3,0]-(2*f0)+f[3,1])/h**2

hessian = np.array([[hrr,hrd,hrx,hry],
                   [hrd,hdd,hdx,hdy],
                   [hrx,hdx,hxx,hxy],
                   [hry,hdy,hxy,hyy]])

print('\n',hessian,'\n')

u,s,vh=np.linalg.svd(hessian)

print('\n',u,s,vh,'\n')

cn=np.max(s)/np.min(s)

print('\n condition number is: ',cn)
