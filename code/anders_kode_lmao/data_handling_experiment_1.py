from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches

def data_to_array(data_dir): # konverter forsøgs data til noget vi kan bruge
    data_import = np.loadtxt(data_dir)
    time_arr = np.zeros(len(data_import))
    cap_arr = np.zeros(len(data_import))
    step_arr = np.zeros(len(data_import))

    for i in range(len(data_import)):
        time_arr[i] = data_import[i][0]-data_import[0][0]
        cap_arr[i] = data_import[i][1]
        step_arr[i] = data_import[i][2]
    return time_arr, cap_arr, step_arr

def sqr_wave(V, t, f): # simuler input spænding
    period = f**-1
    if t%period < period/2:
        return V
    else:
        return 0

def cap_charging(t, R, C, V): # opladning af cap
    return V*(1-np.e**(-t/(R*C)))

def cap_discharging(t, R, C, V): # afladning af cap
    return V*(np.e**(-t/(R*C))) 


""" initialize data """
    
data = data_to_array("data_1073hz.dat")
time = data[0]
cap_data = data[1]
step_data = data[2]

cap_sim = np.zeros(len(cap_data))
step_sim = np.zeros(len(step_data))


"""Simuler dataen"""

# input_spændingen
for i in range(len(step_sim)):
    step_sim[i] = sqr_wave(1, time[i], 107.3)

# cap opladning
for i in range(int(len(cap_sim)/2)):
    cap_sim[i] = cap_charging(time[i], 4770, 97.61e-9, step_data[i])

# cap afladning start tid
time_point = int(len(cap_sim)/2)-1

# cap afladning
for i in range(int(len(cap_sim)/2)):
    cap_sim[i+time_point] = cap_discharging(time[i], 4770, 97.61e-9, max(cap_sim))
    

""" Gør plottet pænere """

tau = 97.61e-9 * 4770
plt.grid(True)                     

labels = [str(i) + '\u03C4' for i in range(21)]                     
label_size = [i*tau for i in range(21)]                             
plt.xticks(label_size, labels)                                      

plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f V'))
plt.title('RC-circuit simulation and data')                         


red_patch = mpatches.Patch(color='red', label='Simulated data')     
blue_patch = mpatches.Patch(color='blue', label='Measured data')
black_patch = mpatches.Patch(color='black', label='Input Voltage')

results = stats.linregress(cap_data, cap_sim)    
r_squared = results[2]**2                   
r_val_str = '$R^2$ ={0:.6f} '.format(r_squared)                     

plt.legend(handles=[black_patch, blue_patch, red_patch, mpatches.Patch(fc = 'None', ec = 'None', label = r_val_str)])



""" plot dataen """

plt.plot(time, cap_sim, "red")
plt.plot(time, cap_data, "blue")
plt.plot(time, step_data, "black")


"""eksporter figuren """

fig = plt.gcf()
fig.set_size_inches(10, 6)
fig.savefig('/home/anders/Desktop/test.pdf', dpi=100)
