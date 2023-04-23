import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv('paretos/domXF@64457bfd.csv')
data=data.sort_values(by=['LCOE'],ascending=True)
print(data)
utop1 = min(data['LCOE'])
utop2 = min(data['Max Spacing'])
nadi1 = max(data['LCOE'])
nadi2 = max(data['Max Spacing'])

index=35

fig,(p1,p2)=plt.subplots(1,2,figsize=(12,5))
p1.plot(data['LCOE'],data['Max Spacing'],marker='o',color='b',fillstyle = 'none',label = 'Pareto Front')
p1.plot(utop1,utop2,marker='*',color='g',label = 'Utopia Point')
p1.text(utop1+0.001,utop2+0.1,'Utopia',color='g')
p1.plot(nadi1,nadi2,marker = 'x',color = 'r',label='Nadir Point')
p1.text(nadi1-0.004,nadi2-0.8,'Nadir',color = 'r')
p1.legend
p1.set_xlabel('LCOE [$/kWh]')
p1.set_ylabel('Maximum Array Dimension [m]')

p2.scatter([0,data['x2'][index],data['x3'][index],data['x4'][index]],[0,data['y2'][index],data['y3'][index],data['y4'][index]])

plt.show()