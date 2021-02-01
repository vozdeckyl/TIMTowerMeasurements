#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

data_table = {}
labels = []
y_pos = []
x_pos = []
x_err = []

with open("out.csv","r") as f:
    for line in f:
        if line[0] == "#":
            continue
        label = line.split("\t")[5]
        value = float(line.split("\t")[1])
        error = float(line.split("\t")[2])
        correction_factor = float(line.split("\t")[2])
        data_table[label] = (value, error, correction_factor)


for block in range(1,6+1):
    for face in range(1,4+1):
        val, err, correction_factor = data_table["Manchester, block {}, face {}".format(block,face)]
        labels.append("Block {}, Face {}".format(block, face))
        y_pos.append(block + 0.2*face)
        x_pos.append(val*correction_factor)
        x_err.append(err*correction_factor)

plt.rcdefaults()
fig, ax = plt.subplots()

ax.errorbar(x_pos, y_pos, xerr=x_err,linewidth=0,elinewidth=1, marker="o")
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
plt.show()