#!/usr/bin/env python3

import csv
import numpy as np
from matplotlib import pyplot as plt
import math
import sys


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
    if pivot=="top":
        fit_up = coefs[2]+3*errors[2] + (coefs[1]-3*errors[1])*x_pixels + (coefs[0]+3*errors[0])*x_pixels*x_pixels
        fit_down = coefs[2]-3*errors[2] + (coefs[1]+3*errors[1])*x_pixels + (coefs[0]-3*errors[0])*x_pixels*x_pixels
    else:
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
    plt.clf()

    gradient = coefs[1]
    gradientError = errors[1]

    return gradient, gradientError

def main(file_path, plot_output_path, print_results=False):
    #fetch the CSV file
    imgList = []
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            imgList.append(row)
    image = np.array(imgList)
    
    line = np.mean(image, axis=0)[:-10]

    first_derivative = np.gradient(line)
    
    
    gap = 5
    bottomInterface = np.argmax(first_derivative[0:int(len(first_derivative)/2)])
    topInterface = int(len(first_derivative)/2) + np.argmax(first_derivative[int(len(first_derivative)/2):])


    sampleLowerBoundary = bottomInterface + gap
    sampleUpperBoundary = topInterface - gap

    topTowerLowerBoundary = topInterface + gap
    topTowerUpperBoundary = len(line) - 50

    bottomTowerLowerBoundary = 50
    bottomTowerUpperBoundary = bottomInterface - gap

    minTemperature = np.min(line) - 2
    maxTemperature = 2 + np.max(line)

    if plot_output_path != "":
        plt.clf()
        plt.plot(line, "o", markersize=1)
        plt.vlines(sampleLowerBoundary,minTemperature,maxTemperature, colors = "r")
        plt.vlines(sampleUpperBoundary,minTemperature,maxTemperature, colors = "r")
        plt.vlines(topTowerLowerBoundary,minTemperature,maxTemperature, colors = "b")
        plt.vlines(topTowerUpperBoundary,minTemperature,maxTemperature, colors = "b")
        plt.vlines(bottomTowerLowerBoundary,minTemperature,maxTemperature, colors = "y")
        plt.vlines(bottomTowerUpperBoundary,minTemperature,maxTemperature, colors = "y")
        plt.xlabel("Pixels")
        plt.ylabel("Temperature [C]")
        plt.title("Temperature profile")
        plt.axis([0,len(line),minTemperature,maxTemperature])
        plt.savefig(plot_output_path.format("wholeTemperatureProfile"), dpi=1000)
        plt.clf()


    gradientSample, gradientErrorSample = fit2polyGradient(line[sampleLowerBoundary:sampleUpperBoundary], "middle", plot_output_path.format("sampleFit"))
    gradientTopTower, gradientErrorTopTower = fit2polyGradient(line[topTowerLowerBoundary:topTowerUpperBoundary], "bottom", plot_output_path.format("topTowerFit"))
    gradientBottomTower, gradientErrorBottomTower = fit2polyGradient(line[bottomTowerLowerBoundary:bottomTowerUpperBoundary], "top",plot_output_path.format("bottomTowerFit"))

    towerGradientDiscrepancy = abs(gradientTopTower - gradientBottomTower)/min(gradientTopTower,gradientBottomTower)

    towerAverageGradient = (gradientTopTower+gradientBottomTower)/2

    towerAverageGradientError = 0.5*math.sqrt(gradientErrorTopTower**2 + gradientErrorBottomTower**2)

    heatConductivityPb = 35.3

    heatConductivity = heatConductivityPb * (towerAverageGradient/gradientSample)

    heatConductivityError = heatConductivity * math.sqrt((towerAverageGradientError/towerAverageGradient)**2 + (gradientErrorTopTower/gradientTopTower)**2)


    if print_results:
        print("Sample")
        print("gradient: \t {} +/- {}".format(gradientSample,gradientErrorSample))
        print("Relative error: \t {}%".format(100*gradientErrorSample/gradientSample))

        print("______________________________________________________________________")

        print("Lower Tower")
        print("gradient: \t {} +/- {}".format(gradientTopTower,gradientErrorTopTower))
        print("Relative error: \t {}%".format(100*gradientErrorTopTower/gradientTopTower))

        print("______________________________________________________________________")

        print("Upper Tower")
        print("gradient: \t {} +/- {}".format(gradientBottomTower,gradientErrorBottomTower))
        print("Relative error: \t {}%".format(100*gradientErrorBottomTower/gradientBottomTower))

        print("______________________________________________________________________")
        print("______________________________________________________________________")

        print("Gradient discrepancy (top vs. bottom tower): \t {}%".format(100*towerGradientDiscrepancy))

        print("______________________________________________________________________")

        print("Heat conductivity: \t {} +/- {}".format(heatConductivity,heatConductivityError))

        print("Relative error: \t {}%".format(100*heatConductivityError/heatConductivity))

        print("______________________________________________________________________")
    
    return (heatConductivity,heatConductivityError)

if __name__ == "__main__":
    main(sys.argv[1],"{}.png",True)
