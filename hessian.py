import numpy as np
import modules.model_nWECs as model

def run(x,p):
    # Second order central finite difference
    # f''~ [f(x+h)-2f(x)+f(x-h)]/h^2
    f0 = model.run(x,p)
    n=4
    f=np.zeros([4,14])
    h=0.01
    for i in range(n):
        dx=np.zeros(len(x))
        dy=np.zeros(len(x))
        dz=np.zeros(len(x))
        da=np.zeros(len(x))
        dx[i]=h
        f[i,0]=model.run(x+dx,p)
        f[i,1]=model.run(x-dx,p)
    Lr=((f[0,0]-f0)+(f0-f[0,1]))/h
    Ld=((f[1,0]-f0)+(f0-f[1,1]))/h
    Lx=((f[2,0]-f0)+(f0-f[2,1]))/h
    Ly=((f[3,0]-f0)+(f0-f[3,1]))/h
    hrr=(f[0,0]-(2*f0)+f[0,1])/h**2
    hdd=(f[1,0]-(2*f0)+f[1,1])/h**2
    hxx=(f[2,0]-(2*f0)+f[2,1])/h**2
    hyy=(f[3,0]-(2*f0)+f[3,1])/h**2
    Jacobian = np.array([Lr,Ld,Lx,Ly])
    Hessian = np.array([hrr,hdd,hxx,hyy])
    #print('\n','Jacobian is: ','\n',Jacobian,'\n')
    #print('\n','Hessian is: ','\n',Hessian,'\n')
    cn=np.max(np.abs(Hessian))/np.min(np.abs(Hessian))
    #print('\n condition number is: ',cn)
    return Jacobian, Hessian,cn
