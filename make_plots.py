#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)


data_table = {}
labels = []
y_pos = []
x_pos = []
x_err = []
tick_positions = []
with open("out.dat","r") as f:
    for line in f:
        if line[0] == "#":
            continue
        label = line.split("\t")[5]
        value = float(line.split("\t")[1])
        error = float(line.split("\t")[2])
        correction_factor = float(line.split("\t")[3])
        data_table[label] = (value, error, correction_factor)


plt.rcdefaults()
fig, ax = plt.subplots(1,1,figsize=(6,8))

for block in range(6,0,-1):
    for face in range(1,4+1):
        val, err, correction_factor = data_table["Manchester, block {}, face {}".format(block,face)]
        labels.append(str(face))
        y_pos.append(1.5*block + 0.2*face)
        tick_positions.append(1.5*block + 0.2*face)
        x_pos.append(val*correction_factor)
        x_err.append(err*correction_factor)
    ax.errorbar(x_pos, y_pos, xerr=x_err,linewidth=0,elinewidth=1, marker="o", label="Sample {}".format(block))
    x_pos = []
    y_pos = []
    x_err = []

ax.set_yticks(tick_positions)
ax.set_yticklabels(labels)
ax.set_xlim(15,55)
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.legend(loc="lower right")
plt.xlabel("Thermal Conductivity [ $ \\mathrm{W} \cdot \\mathrm{m}^{-1} \\mathrm{K}^{-1}$ ]")
plt.ylabel("Face Number")
plt.grid(axis="x", which="major")
#plt.title("Manchester block - $K_z$ measurements")
plt.tight_layout()
#plt.show()
plt.savefig("/home/lubos/windows_desktop/perpendicularMeasurements.pdf", format="pdf")


#plotting lateral measurements
plt.rcdefaults()
fig, ax = plt.subplots(1,1,figsize=(6,4))
labels = []
y_pos = []
x_pos = []
x_err = []
tick_positions = []
y_position = 1.0

for direction in ["x","y"]:
    for face in [1,3]:
        val, err, correction_factor = data_table["Manchester, block 6, {}-axis, face {}".format(direction,face)]
        labels.append("{}".format(face))
        y_pos.append(y_position)
        tick_positions.append(y_position)
        x_pos.append(val*correction_factor)
        x_err.append(err*correction_factor)
        y_position = y_position + 1
    ax.errorbar(x_pos, y_pos, xerr=x_err,linewidth=0,elinewidth=1, marker="o", label="Sample 6, {}-axis".format(direction))
    x_pos = []
    x_err = []
    y_pos = []
    y_position = y_position + 0.5

ax.set_yticks(tick_positions)
ax.set_yticklabels(labels)
ax.set_xlim(15,55)
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.legend(loc="best")
plt.xlabel("Thermal Conductivity [ $ \\mathrm{W} \cdot \\mathrm{m}^{-1} \\mathrm{K}^{-1}$ ]")
plt.ylabel("Face Number")
plt.grid(axis="x", which="major")
#plt.title("Manchester block - $K_x$ and $K_y$ measurements")
plt.tight_layout()
#plt.show()
plt.savefig("/home/lubos/windows_desktop/longitudonalMeasurements.pdf", format="pdf")


#plottting averages
plt.rcdefaults()
fig, ax = plt.subplots(1,1,figsize=(6,4))

def calculate_average(values):
    
    values_a = np.array(values)
    result_error = 0.5*(np.max(values) - np.min(values))
    result_value = np.mean(values_a)

    return (result_value, result_error)

x_pos = []
y_pos = []
x_err = []
labels = []
y_position = 1.0

for block in range(1,6+1):
    values = []
    for face in range(1,4+1):
        val, err, correction_factor = data_table["Manchester, block {}, face {}".format(block,face)]
        values.append(val)
    average_val, average_err = calculate_average(values)
    labels.append("{}".format(block))
    x_pos.append(average_val)
    x_err.append(average_err)
    y_pos.append(y_position)
    y_position = y_position + 1

ax.errorbar(x_pos, y_pos, xerr=x_err,linewidth=0,elinewidth=1, marker="o")

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlim(15,55)
ax.set_ylim(0,max(y_pos)+1)
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.xaxis.set_minor_locator(MultipleLocator(1))
plt.vlines(17,0,max(y_pos)+1, colors="r", linestyles="dashed")
plt.text(17.2,max(y_pos)-0.8, "Proposed specs", size=7, rotation=-90, color="r")
plt.ylabel("Sample")
plt.xlabel("Thermal Conductivity [ $ \\mathrm{W} \cdot \\mathrm{m}^{-1} \\mathrm{K}^{-1}$ ]")
plt.grid(axis="x", which="major")
#plt.subplots_adjust(left=0.15, right = 0.95, bottom = 0.20, top=0.90)
#plt.title("Manchester block - averaged $K_z$ measurements")
plt.tight_layout()
plt.savefig("/home/lubos/windows_desktop/perpendicularMeasurementsAverage.pdf", format="pdf")
#plt.show()