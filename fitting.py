#!/usr/bin/env python

#import ROOT
import csv
import numpy as np
from matplotlib import pyplot as plt
import math


def fit2polyGradient(dataArray, pivot, outputPlot=""):

  dataPointsNum = len(dataArray)

  if pivot == "middle":
    x_pixels = range(-math.floor(dataPointsNum/2),math.ceil(dataPointsNum/2))
  elif pivot == "bottom":
    x_pixels = range(0,dataPointsNum)
  elif pivot == "top":
    x_pixels = range(-dataPointsNum,0)
  else:
    print("ERR invalid input")
    return -1, -1

  coefs, cov = np.polyfit(x_pixels, dataArray, 2,cov = True)
  errors = np.sqrt(np.diag(cov))

  fit_nominal = coefs[2] + coefs[1]*x_pixels + coefs[0]*x_pixels*x_pixels
  fit_up = coefs[2]+3*errors[2] + (coefs[1]+3*errors[1])*x_pixels + (coefs[0]+3*errors[0])*x_pixels*x_pixels
  fit_down = coefs[2]-3*errors[2] + (coefs[1]-3*errors[1])*x_pixels + (coefs[0]-3*errors[0])*x_pixels*x_pixels

  plt.clf()
  plt.plot(x_pixels, dataArray, "o", label = "data")
  plt.plot(x_pixels, fit_nominal, label="fit_nominal")
  plt.plot(x_pixels, fit_up, label = "fit_var_up (3 sigma)")
  plt.plot(x_pixels, fit_down, label = "fit_var_down (3 sigma)")

  plt.legend()

  if outputPlot != "":
    plt.savefig(outputPlot)

  gradient = coefs[1]
  gradientError = errors[1]

  return gradient, gradientError


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

#plt.plot(line, "o")
#plt.plot(first_derivative, "o")
#plt.plot(second_derivative)

gap = 5
bottomInterface = np.argmax(first_derivative[0:int(len(first_derivative)/2)])
topInterface = int(len(first_derivative)/2) + np.argmax(first_derivative[int(len(first_derivative)/2):])

print(bottomInterface)
print(topInterface)

sampleLowerBoundary = bottomInterface + gap
sampleUpperBoundary = topInterface - gap

topTowerLowerBoundary = topInterface + gap
topTowerUpperBoundary = len(line) - 50

bottomTowerLowerBoundary = 50
bottomTowerUpperBoundary = bottomInterface - gap


gradientSample, gradientErrorSample = fit2polyGradient(line[sampleLowerBoundary:sampleUpperBoundary], "middle", "sampleFit.png")
gradientTopTower, gradientErrorTopTower = fit2polyGradient(line[topTowerLowerBoundary:topTowerUpperBoundary], "bottom", "topTowerFit.png")
gradientBottomTower, gradientErrorBottomTower = fit2polyGradient(line[bottomTowerLowerBoundary:bottomTowerUpperBoundary], "top","bottomTowerFit.png")

towerGradientDiscrepancy = abs(gradientTopTower - gradientBottomTower)/min(gradientTopTower,gradientBottomTower)

towerAverageGradient = (gradientTopTower+gradientBottomTower)/2

towerAverageGradientError = math.sqrt(gradientErrorTopTower**2 + gradientErrorBottomTower**2)

heatConductivityPb = 35.3

heatConductivity = heatConductivityPb * (towerAverageGradient/gradientSample)

heatConductivityError = heatConductivity * math.sqrt((towerAverageGradientError/towerAverageGradient)**2 + (gradientErrorTopTower/gradientTopTower)**2)


print("Sample")
print("gradient: \t {} +/- {}".format(gradientSample,gradientErrorSample))
print("Rel.eer: \t {}%".format(100*gradientErrorSample/gradientSample))

print("______________________________________________________________________")

print("Lower Tower")
print("gradient: \t {} +/- {}".format(gradientTopTower,gradientErrorTopTower))
print("Rel.eer: \t {}%".format(100*gradientErrorTopTower/gradientTopTower))

print("______________________________________________________________________")

print("Upper Tower")
print("gradient: \t {} +/- {}".format(gradientBottomTower,gradientErrorBottomTower))
print("Rel.eer: \t {}%".format(100*gradientErrorBottomTower/gradientBottomTower))

print("______________________________________________________________________")
print("______________________________________________________________________")

print("Gradient discrepancy (top vs. tower): \t {}%".format(100*towerGradientDiscrepancy))

print("______________________________________________________________________")

print("Heat conductivity: \t {} +/- {}".format(heatConductivity,heatConductivityError))

print("______________________________________________________________________")




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
