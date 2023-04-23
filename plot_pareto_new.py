import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv('paretos/domXF@64456228.csv')
data=data.sort_values(by=['LCOE'],ascending=True)
print(data)
utop1 = min(data['LCOE'])
utop2 = min(data['Max Spacing'])
nadi1 = max(data['LCOE'])
nadi2 = max(data['Max Spacing'])

fig = plt.figure(1)
plt.plot(data['LCOE'],data['Max Spacing'],marker='o',color='b',fillstyle = 'none',label = 'Pareto Front')
plt.plot(utop1,utop2,marker='*',color='g',label = 'Utopia Point')
plt.text(utop1+0.001,utop2+0.1,'Utopia',color='g')
plt.plot(nadi1,nadi2,marker = 'x',color = 'r',label='Nadir Point')
plt.text(nadi1-0.004,nadi2-0.8,'Nadir',color = 'r')
plt.legend
plt.xlabel('LCOE [$/kWh]')
plt.ylabel('Maximum Array Dimension [m]')
plt.show()