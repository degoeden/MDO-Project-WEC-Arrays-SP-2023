import numpy as np
import matplotlib.pyplot as plt
nwec=4
X = np.array([   5.94398401,    4.99397123,  199.62104266,   85.35953212,    4.83145793,
  167.41788152,  106.62794576,    5.28129613,   65.44505861, -114.63865077,
    5.11337849,   87.21817258,   52.37052864,    4.71935522,   62.02985843,
   11.48823208,    4.86327042, -172.08367784, -156.51731971,    4.67782359,
  165.67419155,  187.72903587,    4.91428691, -112.98636852,  -37.52143827,
    5.15739433,  121.04149971,  -52.22653982,    5.15864954])
X = [  6.16508689,   5.19148179, 176.55289471,  51.43802826,   5.25181387,
  33.13876137, -43.56398604,   5.17949576, 178.02307292,  26.23344913,
   5.28842795]
X = [   5.60264556,    5.07073029, -874.03422324,  793.08328416,    4.79457463,
   26.82672909,  388.15469723,    5.11120316,  655.51714507,  425.72612031,
    4.81535879,  117.72976271,  583.96669038,    5.00779822,  -31.25163604,
  448.3718882,     5.02164907,  366.81229526,  806.35951412,    5.20522242,
  650.54858096,  908.82479922,    5.07582385,   60.2600108,   407.11888422,
    5.09969903,  103.34022558,  754.33141126,    5.09007517]
X = [ 3.,  3.,  0., 20.,  3.,  0., 40.,  3.,  0., 60.,  3.]

plt.rcParams.update({'font.size': 12})
damp = np.zeros(nwec)
wecx = np.zeros(nwec)
wecy = np.zeros(nwec)
r = X[0]
damp[0] = 10**X[1]
for i in range(nwec-1):
    wecx[i+1] = X[2+i*3]
    wecy[i+1] = X[3+i*3]
    damp[i+1] = 10**X[4+i*3]
print(damp)
fig, ax = plt.subplots(facecolor='none')
#ax.set_facecolor('none')
#ax.spines['bottom'].set_color('#ffffff')
#ax.spines['top'].set_color('#ffffff') 
#ax.spines['right'].set_color('#ffffff')
#ax.spines['left'].set_color('#ffffff')
#ax.tick_params(axis='x', colors='#ffffff')
#ax.tick_params(axis='y', colors='#ffffff')
for i in range(nwec):
    circles = plt.Circle((wecx[i],wecy[i]),r,color='#dba0db')
    ax.add_patch(circles)
ax.axis('equal')
plt.xlabel('x [m]')
plt.arrow(-40, 0,10,0,width = 1,color = 'k')
plt.ylabel('y [m]')
plt.xlim([-42,42])
plt.text(-40, 2,r'$\beta$',size=16)
plt.show()