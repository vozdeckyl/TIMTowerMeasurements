#!/usr/bin/env python

import ROOT
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


#fetch the CSV file
imgList = []
with open("A40M-000231_box.csv") as csvfile:
  reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
  for row in reader:
    imgList.append(row)
image = np.array(imgList)

line = np.mean(image, axis=0)[50:-50]

first_derivative = np.gradient(line)
second_derivative = np.gradient(first_derivative)

plt.plot(line, "o")
#plt.plot(first_derivative, "o")
#plt.plot(second_derivative)

bottom_interface = np.argmax(first_derivative[0:int(len(first_derivative)/2)])
top_interface = int(len(first_derivative)/2) + np.argmax(first_derivative[int(len(first_derivative)/2):])

print(bottom_interface)
print(top_interface)

plt.axvline(x=bottom_interface,linewidth=1, color='r')
plt.axvline(x=top_interface,linewidth=1, color='r')

plt.axvline(x=(bottom_interface+5),linewidth=1, color='yellow')
plt.axvline(x=(bottom_interface-5),linewidth=1, color='yellow')

plt.axvline(x=(top_interface+5),linewidth=1, color='yellow')
plt.axvline(x=(top_interface-5),linewidth=1, color='yellow')

plt.show()

h1 = ROOT.TH1Dh1("hgaus", "histo from a gaussian", 150, 0,150)

for n in range(0,len(line)-1):
    h1.SetBinContent(n,line[n])


