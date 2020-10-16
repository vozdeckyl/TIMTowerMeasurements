#!/usr/bin/env python

import ROOT
import csv
import numpy as np
from matplotlib import pyplot as plt
import math


#fetch the CSV file
imgList = []
with open("A40M-000231_box.csv") as csvfile:
  reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
  for row in reader:
    imgList.append(row)
image = np.array(imgList)

line = np.mean(image, axis=0)

first_derivative = np.gradient(line)
second_derivative = np.gradient(first_derivative)

plt.figure(figsize=(200,30))
plt.plot(line, "o")
#plt.plot(first_derivative, "o")
#plt.plot(second_derivative)

bottom_interface = np.argmax(first_derivative[0:int(len(first_derivative)/2)])
top_interface = int(len(first_derivative)/2) + np.argmax(first_derivative[int(len(first_derivative)/2):])

print(bottom_interface)
print(top_interface)

plt.axvline(x=bottom_interface,linewidth=1, color='r')
plt.axvline(x=top_interface,linewidth=1, color='r')

plt.axvline(x=(bottom_interface+10),linewidth=1, color='yellow')
plt.axvline(x=(bottom_interface-10),linewidth=1, color='yellow')

plt.axvline(x=(top_interface+10),linewidth=1, color='yellow')
plt.axvline(x=(top_interface-10),linewidth=1, color='yellow')

plt.savefig("plot.png")


coefs_lower, cov_low = np.polyfit(range(0,80), line[40:120], 2,cov = True)
error_lower = np.sqrt(np.diag(cov_low))

coefs_sample, cov_sample = np.polyfit(range(0,40), line[135:175], 2,cov = True)
error_sample = np.sqrt(np.diag(cov_sample))

coefs_upper, cov_upper = np.polyfit(range(0,80), line[180:260], 2,cov = True)
error_upper = np.sqrt(np.diag(cov_upper))

print("lower \t {} +/- {}".format(coefs_lower[1],error_lower[1]))
print("sample \t {} +/- {}".format(coefs_sample[1],error_sample[1]))
print("upper \t {} +/- {}".format(coefs_upper[1],error_upper[1]))

kPb = 35.3

gradient_bottom =  coefs_lower[1]

gradient_sample =  coefs_sample[1]

gradient_top  = coefs_upper[1]

gradient_tower_mean = (gradient_bottom+gradient_top)/2

kSample = kPb * (gradient_tower_mean/gradient_sample)

print("gradient_bottom = {}".format(gradient_bottom))
print("gradient_sample = {}".format(gradient_sample))
print("gradient_top = {}".format(gradient_top))

relative_error = math.sqrt((error_lower[1]/coefs_lower[1])**2 + (error_sample[1]/coefs_sample[1])**2)

print(kSample)

print("error {}%".format(relative_error*100))

print(kSample*relative_error)

"""
c1 = ROOT.TCanvas("c1")
h1 = ROOT.TH1D("hgaus", "histo from a gaussian",300, 0,300)

for n in range(0,len(line)-1):
  h1.SetBinContent(n,line[n])

lowerTowerProfileF = ROOT.TF1('lowerTowerProfileF', 'pol2', 0, (bottom_interface-5))
sampleProfileF = ROOT.TF1('sampleProfileF', 'pol2', (bottom_interface+5), (top_interface-5))
upperTowerProfileF = ROOT.TF1('upperTowerProfileF', 'pol2', (top_interface+5), len(line))

h1.Fit(lowerTowerProfileF, '', '', 0, (bottom_interface-5))
h1.Fit(sampleProfileF, '', '', (bottom_interface+5), (top_interface-5))
h1.Fit(upperTowerProfileF, '', '', (top_interface+5), len(line)-1)

h1.Draw("hist")
lowerTowerProfileF.Draw("same")
sampleProfileF.Draw("same")
upperTowerProfileF.Draw("same")

c1.Print("histo.png")

slopeLower = 2*lowerTowerProfileF.GetParameter(1)*  + lowerTowerProfileF.GetParameter(1)
slopeSample = sampleProfileF.GetParameter(1)
slopeUpper = upperTowerProfileF.GetParameter(1)

slopeTowerMean = (slopeUpper+slopeLower)/2

kPb = 35.3

kSample = kPb * (slopeTowerMean/slopeSample)

print(kSample)
"""
