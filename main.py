# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:09:02 2018

@author: Alec Mitchell
"""
#Project

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import savgol_filter

my_data = np.loadtxt('WM_1.csv', delimiter=',', skiprows=6)

#Create image of raw data
plt.figure(1)
plt.pcolormesh(my_data,vmin=-5.5, vmax=-5)
plt.grid()

#user inputs y values where a row of indends start and end
#y3 is the location of the center of an indent row
y1=300
y2=440
y3=int(.5*(y1+y2))

xprof = np.linspace(0,16, len(my_data[y3]))
yraw = my_data[y3]

#replace outliers with local average
stdev = np.std(yraw)
mean = np.mean(yraw)
yprof = np.copy(yraw)
for i in range(0,len(yraw)):
    if abs(yraw[i]-mean) >= 3*stdev:
        yprof[i] = .5*(yraw[i+10]+yraw[i-10])

#built in scipy funcion to smooth dat
ysmooth = savgol_filter(yprof, 21, 1)


#use plynomial trendline to correct bow in data
coeff = np.polyfit(xprof, ysmooth, 2)
trendl = coeff[0]*xprof**2 + coeff[1]*xprof + coeff[2]

ycorrected = ysmooth-trendl+trendl[0]


#graph indent profile
plt.figure(2)
plt.ylim(-5.6, -5.25)
plt.grid()
plt.plot(xprof, yprof, xprof, ysmooth, xprof, corrected)


#user defines bounds to focus on one indent 
x_l=3
x_r=9

#graph focusing on one indent
plt.figure(3)
plt.xlim(x_l, x_r)
plt.ylim(-5.6, -5.25)
plt.grid()
plt.plot(xprof, yprof)

#user inputs borders piecewise functions
edge_a=3.82
edge_b=4.07
edge_c=7.6
edge_d=8.14


