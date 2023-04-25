import matplotlib.pyplot as plt
import csv

f1,f2 = [],[]
with open('paretos/domF@1682225379.1712525.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        f1.append(float(row[0]))
        f2.append(float(row[1]))
        print(', '.join(row))
utop1 = min(f1)
utop2 = min(f2)
nadi1 = max(f1)
nadi2 = max(f2)
fig = plt.figure(1)
plt.plot(f1,f2,marker='o',color='b',fillstyle = 'none',label = 'Pareto Front')
plt.plot(utop1,utop2,marker='*',color='g',label = 'Utopia Point')
plt.text(utop1+0.001,utop2+0.1,'Utopia',color='g')
plt.plot(nadi1,nadi2,marker = 'x',color = 'r',label='Nadir Point')
plt.text(nadi1-0.004,nadi2-0.8,'Nadir',color = 'r')
plt.legend
plt.xlabel('LCOE [$/kWh]')
plt.ylabel('Maximum Array Dimension [m]')
plt.show()
