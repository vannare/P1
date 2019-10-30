#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:28:01 2019

@author: anders
"""

"""importing libraries------------------------------------------------------"""

import math as m #Bruges til konstanter
import matplotlib.pyplot as plt #bruges tl plots
import numpy as np #bruges til plots og arrays
from matplotlib.ticker import FormatStrFormatter #ticks på plottet
from scipy import stats #regression
import matplotlib.patches as mpatches #gør plottet pænere
import matplotlib.pyplot as plt #gør plottet pænere

"""data handling------------------------------------------------------------"""

file = open('new_data.dat')          #open the data file
data = file.readlines()                 #bring in the data

data = [data[i].replace('\t', ' ') for i in range(len(data))] #replace the tabs with commas

for i in range(len(data)):              #split up the data into a nested list
    data[i] = data[i].split()
    
for i in range(len(data)):              #convert the data points into floats
    for j in range(3):
        data[i][j] = float(data[i][j])
        
"""defining the input voltages as functions --------------------------------"""

def sqr_wave(p, u, t):                  #same as tri_wave(), just square isntead
    t = t%p
    
    if t <= p/2:
        return u
    elif p/2 <= t:
        return 0
    else:
        return "something went wrong in the function sqr_wave()"
    
def charge(u, t):                       #returns voltage at time t
    return u*(1-m.e**(-t/(tau)))        

def discharge(u, t):                    #returns voltage at time t
    return u*(m.e**(-t/(tau)))

"""Defining the variables used in the simulation----------------------------"""

u = 1                       #voltage
res = 4770                  #Resistance
cap = 97.61*10**(-9)        #capacitance
tau = res*cap               #time constanc
per =4.66*10**(-3)          #period of the input voltage
n_points = len(data)             #must be even
step_size = per/n_points    #tge size of steps in simulation

voltage = []                #input voltage
charge_arr = []             #charging data points
discharge_arr = []          #discharging data points

"""Simulating the results-"""

for i in range(int(n_points/2)):                    #iterating through the data points
    charge_arr.append(charge(u, i*step_size))
    discharge_arr.append(discharge(u, i*step_size))

for i in range(n_points):                           #set the voltage data 
    voltage.append(sqr_wave(per, u, i*step_size))

"""plotting the results of the simulation-----------------------------------"""

#changing to arrays
charge_full_arr = charge_arr+discharge_arr
charge_full_arr = np.array(charge_full_arr)
voltage = np.array(voltage)
charge_arr = np.array(charge_arr)
discharge_arr = np.array(discharge_arr)

#setting the time where the functions should be plotted
time_voltage = np.linspace(0, per, n_points)
time_charge = np.linspace(0, per/2, int(n_points/2))
time_discharge = np.linspace(per/2, per, int(n_points/2))
time_full = np.linspace(0, per, n_points)

#plotting data
plt.plot(time_voltage, voltage, color = "black")
plt.plot(time_full, charge_full_arr, '-r')

"""plotting the data--------------------------------------------------------"""

time_axis = []                              #axis for the voltage to plotted against
cap_voltage = []                            #list to store voltage data

for i in range(len(data)):                  #append the data
    time_axis.append(data[i][0])
    cap_voltage.append(data[i][1])

time_axis = np.array(time_axis)             #change the lists to arrays
cap_voltage = np.array(cap_voltage)

plt.plot(time_axis, cap_voltage, '-b')            #plot the data

results = stats.linregress(cap_voltage, charge_full_arr)    #getting the r^2
r_squared = results[2]**2                   #isolating the r^2 from the tuple

"""Making the plot prettier and regression----------------------------------"""

labels = [str(i) + '\u03C4' for i in range(11)]                     #labels for x
label_size = [i*tau for i in range(11)]                             #størrelse for x labels
plt.grid(True)                                                      #indsæt grid
plt.xticks(label_size, labels)                                      #ændre x labels
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%1.1f V'))  #ændre y enehder
plt.title('RC-circuit simulation and data')                         #Setting title of the graph

#Writing legends on the plot
red_patch = mpatches.Patch(color='red', label='Simulated data')     #setting the names and colors of legend handles
blue_patch = mpatches.Patch(color='blue', label='Measured data')
black_patch = mpatches.Patch(color='black', label='Input Voltage')
r_val_str = '$R^2$ ={0:.6f} '.format(r_squared)                     #used in next block of code
#the below function adds the legend to the top right
plt.legend(handles=[black_patch, blue_patch, red_patch, mpatches.Patch(fc = 'None', ec = 'None', label = r_val_str)])

"""Printing the results-----------------------------------------------------"""

plt.savefig("/home/anders/Documents/AAU/1_semester/P1/RC_circuit_coding/fig.pdf")
plt.show()