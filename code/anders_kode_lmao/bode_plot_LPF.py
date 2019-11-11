from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# variables

C = 97.61e-9
R = 4770
V = 1

# gain as function of frequency

def gain(f):
    X_C = 1/(2*np.pi*f*C)
    Z = np.sqrt(R**2+X_C**2)
    v_out = V*(X_C/Z)
    gain = 20*np.log10(v_out/V)
    return gain

# setting up the data to be plotted

input_freq = np.linspace(0.0000001, 10**6, 10000)
output_gain = gain(input_freq)
freq_cut = 1/(np.pi*2*R*C)

# making the figure pretty

fig = plt.figure()

# for the legend

blue_patch = mpatches.Patch(color = 'blue', label = 'gain')
red_patch = mpatches.Patch(color = 'red', label = 'cutoff frequency')

ax = fig.add_subplot(1, 1, 1)
ax.set_xscale('log')
ax.grid(True)
ax.legend(handles = [blue_patch, red_patch])

# change the axis and add a title

plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f dB'))
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%+.0e Hz'))
plt.xticks(rotation=45)
plt.title('Gain of a signal as a function of frequency')       

#plotting the figure

ax.plot(input_freq, output_gain)
ax.scatter(freq_cut, gain(freq_cut), c = 'red', alpha = 1)
plt.tight_layout()
fig.savefig('/home/anders/Desktop/test.pdf')