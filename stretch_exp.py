# Write code to fit a stretched exponential 
# (actual like silicon or flipped over like for Germanium) 
# and also the 'Dispersive Recombination' that has also been proposed.

import numpy as np
from pylab import plot,show,draw,figure,loglog,scatter,semilogy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Take as input an irelax file and sort out the times when I checked the voltage in the file (negative spikes).

# Load IRelax file.
filename_freq = input("Enter the Power Spectrum ( .allPS) file you would like to process: ")
print("Your file is ",filename_freq)
f_freq = open(filename_freq,'r')
freq_content = f_freq.readlines()
f_freq.close()

# Turn that power spectrum file into an array for python to understand.
headerlen_freq = 21  # Note: this is less than NOISE files
footerlen_freq = 2 # depends on if the file finished properly or if it ended on computer restart
trim_content_freq = freq_content[headerlen_freq:len(freq_content)-footerlen_freq]


# Delete data points effected by voltage checks:
# Can't use the standard deviation column (some files don't have that info).
# Try looking at the relative change between points to find these spikes.
spike = []
ir_data = []
for row in range(len(trim_content_freq)):

	temp = trim_content_freq[row].split("\t")
	temp[len(temp)-1]=temp[len(temp)-1].rstrip() # remove new line character (\n) from last element
	for item in range(len(temp)):
		temp[item] =float(temp[item])
	ir_data.append(temp[:2])	# I need the first two columns.
	

ir_data = np.transpose(ir_data)
ir_avg = np.mean(ir_data[1])

for row in range(len(ir_data[1])-1):	
	if ir_data[1][row] < ir_avg/2:
		spike.append(row)	
		print(ir_data[1][row])

ir_data = np.transpose(ir_data)
print(spike)
print(len(spike))
print(len(ir_data))
print(ir_data)
#for row in range(len(spike)):
	#print(spike[len(spike)-row-1])
ir_data = np.delete(ir_data,spike,0)  # make sure to delete correct row.

ir_data = np.transpose(ir_data)
print(ir_data)

# plot the current vs time, to start.
plt.figure()
plt.plot(ir_data[0],ir_data[1],label = 'data')
plt.grid()

plt.xlabel('Time (s)')
plt.ylabel('Current (A)')



# Fit the stretched exponential function.
# (This will initially be for germanium or increasing current, but I can later add silicon or decreasing current.)

def str_exp(x, i_o, del_i, tau,beta):
	return i_o + del_i *(1- np.exp(-(x/tau)**beta))


popt,pcov = curve_fit(str_exp, ir_data[0], ir_data[1],p0=[6e-8,2e-7,1.2e5,0.78])
# Initial conditions from playing in microsoft excel.

print(*popt)

plt.plot(ir_data[0],str_exp(ir_data[0],*popt),label = 'fit')
plt.legend()
plt.title('Stretched Exponential fit parameters \n'+r' $ i_o+ \Delta i *(1-\exp(-(t/\tau)^\beta)) -- ( \Delta i = i_{inf} - i_o ) $' +'\n'+ r' $ =  %5.2e + %5.2e *(1-e^{-(t/%5.2e)^{%1.4f}}) $'%(popt[0],popt[1],popt[2],popt[3]), fontsize = 16 )
plt.tight_layout()
plt.show()