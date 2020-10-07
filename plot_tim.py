#!/usr/bin/env python3

import ROOT

# Dimensions of image
nx = 240
ny = 320
temps = []
ixlo = 111
ixhi = 120
iyulo = 190
iyuhi = ny
iydlo = 15
iydhi = 135
isamplo = 140
isamphi = 188
isampedge = 3
dhdx = (140.-10.) / (317.-32.)
ximg = dhdx * nx
yimg = dhdx * ny
xlo = dhdx * (ixlo-1)
xhi = dhdx * ixhi
yulo = dhdx * iyulo
yuhi = dhdx * iyuhi
ydlo = dhdx * iydlo
ydhi = dhdx * iydhi
samplo = dhdx * isamplo
samphi = dhdx * isamphi
sampedge = dhdx * isampedge

# Sample dimensions
Asamp = 20. * 20.
hsamp = 20.

# Thermal conductivity
kPb = 35.3 / 1000.   # Convert to mm

### Read FLIR temperature data file
# Open data file
ifname = 'A40M-000213.csv'
#ifname = 'A40M-000212.csv'
infile = open(ifname)

# Read in header data
ltmp = infile.readline()
ltmp = infile.readline()
ltmp = infile.readline()
ltmp = infile.readline()
ltmp = infile.readline()
ltmp = infile.readline()

# Loop over x data lines
for ix in range(nx):
  ltmp = infile.readline()
  lwords = ltmp.split(',')
  tempys = [ float(lword) for lword in lwords ]
  temps.append(tempys)

# Close data file
infile.close()


### Create temperature histogram
htemp2d = ROOT.TH2D('htemp2d', 'Temperature 2D', nx, 0, ximg, ny, 0, yimg)
htemp2d.SetXTitle('x [mm]')
htemp2d.SetYTitle('y [mm]')
htemp2d.SetZTitle('T [deg C]')

# Fill 2D temperature histogram
for ix,tempys in enumerate(temps,1):
  for iy,tempxy in enumerate(tempys,1):
    htemp2d.SetBinContent(ix,iy,tempxy)

# Project temperature along y-axis
htempy = htemp2d.ProjectionY('_py', ixlo, ixhi)
htempy.Scale(1./float(ixhi-ixlo+1))
htempy.SetTitle('Temperature 1D')
htempy.SetYTitle('T [deg C]')

# Draw 2D temperature histogram
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(1)
c2d = ROOT.TCanvas('c2d', 'Temp 2D', 500, 700)
htemp2d.Draw('colz')
tb = ROOT.TBox()
tb.SetFillStyle(0)
tb.SetLineColor(ROOT.kBlack)
tb.DrawBox(xlo, 0, xhi, yimg)
tl = ROOT.TLine()
tl.DrawLine(0, samplo, ximg, samplo)
tl.DrawLine(0, samphi, ximg, samphi)

# Draw 1D temperature histogram
cy = ROOT.TCanvas('cy', 'Temp y', 700, 500)
cy.SetGridx()
cy.SetGridy()
htempy.Draw('hist')

# Fit upper + lower towers
tfup = ROOT.TF1('tfup', 'pol2', samphi, yuhi)
htempy.Fit(tfup, '', '', yulo, yuhi)
tfup.Draw('same')
tfdn = ROOT.TF1('tfdn', 'pol2', ydlo, samplo)
htempy.Fit(tfdn, '', '', ydlo, ydhi)
tfdn.Draw('same')
tl.DrawLine(samplo, htempy.GetMinimum(), samplo, htempy.GetMaximum())
tl.DrawLine(samphi, htempy.GetMinimum(), samphi, htempy.GetMaximum())

# Fit foam sample
tfsamp = ROOT.TF1('tfsamp', 'pol1', samplo, samphi)
htempy.Fit(tfsamp, '', '', samplo+sampedge, samphi-sampedge)
tfsamp.Draw('same')
#tl.DrawLine(samplo+sampedge, htempy.GetMinimum(), samplo+sampedge, htempy.GetMaximum())
#tl.DrawLine(samphi-sampedge, htempy.GetMinimum(), samphi-sampedge, htempy.GetMaximum())

# Save plots
c2d.Print('timtemp2d.png')
cy.Print('timtemp.png')

# Calculate temperature at sample edges
Tsamplo = tfdn.Eval(samplo)
Tsamphi = tfup.Eval(samphi)
print('temperature at sample edges {} {}'.format(Tsamplo, Tsamphi))
dTdylo = 2. * tfdn.GetParameter(2) * samplo + tfdn.GetParameter(1)
dTdyhi = 2. * tfup.GetParameter(2) * samphi + tfup.GetParameter(1)
print('dT/dx {} {}'.format(dTdylo, dTdyhi))
Tderivlo = tfdn.Derivative(samplo)
Tderivhi = tfup.Derivative(samphi)
print('Tderiv {} {}'.format(Tderivlo, Tderivhi))
dTdyavg = (dTdylo + dTdyhi) / 2.
print('average dT/dx {}'.format(dTdyavg))
qsamp = kPb * Asamp * dTdyavg
print('heat into sample {}'.format(qsamp))
dTsampdylo = tfsamp.Derivative(samplo)
dTsampdyhi = tfsamp.Derivative(samphi)
print('sample dT/dx {} {}'.format(dTsampdylo, dTsampdyhi))
ksamp = qsamp / Asamp / dTsampdylo * 1000.   # Convert back to m
print('sample thermal conductivity {}'.format(ksamp))
print('Archived calculations:')
ksamp = qsamp / Asamp * hsamp/(Tsamphi-Tsamplo) * 1000.   # Convert back to m
print('sample thermal conductivity {}'.format(ksamp))
