import numpy as np

def grid(nWEC,space):
    xx=[]
    yy=[]
    for i in range(int(nWEC)):
        xx.append(space*(np.floor(i%np.ceil(np.sqrt(nWEC)))))
        yy.append(space*np.floor(i/np.ceil(np.sqrt(nWEC))))
    return xx,yy

def tri(nWEC,space):
    xx=[]
    yy=[]
    # Basis vectors
    e1x=space
    e1y=0
    e2x=space*np.cos(np.pi/3)
    e2y=space*np.sin(np.pi/3)
    e3x=e1x-e2x
    e3y=e1y-e2y
    def span(eig):
        xi=eig[0]*e1x+eig[1]*e2x+eig[2]*e3x
        yi=eig[0]*e1y+eig[1]*e2y+eig[2]*e3y
        return xi,yi
    for i in range(int(nWEC)):
        if i==0:
            xi=0
            yi=0
        elif i<=7:
            vec=[0,0,0]
            vec[(i-1)%3]=(2*np.floor((i-1)/3)-1)
            xi,yi=span(vec)
        xx.append(xi)
        yy.append(yi)
    return xx,yy