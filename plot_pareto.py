import matplotlib.pyplot as plt
import csv

f1,f2 = [],[]
with open('f1and2.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        f1.append(float(row[0]))
        f2.append(float(row[1]))
        print(', '.join(row))
utop1 = min(f1)
utop2 = min(f2)
fig = plt.figure(1)
plt.plot(f1,f2,marker='x')
plt.plot(utop1,utop2,marker='*',color='g')
plt.text(utop1+0.001,utop2+0.1,'Utopia',color='g')
plt.show()
