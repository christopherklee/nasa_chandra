from pylab import *
import numpy as np
import time

# Update img directory to reflect github
file_name = 'input_small/114_ccd7_small.jpg'
original_image_rgb = imread(file_name)

# Image is black and white so R=B=G
IMG = array( original_image_rgb[:,:,0])

# Get image data
Lx = int32( IMG.shape[0])
Ly = int32( IMG.shape[1])

print "Processing %d x %d image" % (Lx, Ly)

total_start_time = time.time()
setup_start_time = time.time()

# Allocate memory
RAD = np.zeros((Lx, Ly), dtype=np.float64)
TOTAL = np.zeros((Lx, Ly), dtype=np.float64)
NORM = np.zeros((Lx, Ly), dtype=np.float64)
OUT = np.zeros((Lx, Ly), dtype=np.float64)

# Parameters
Threshold = 30.0
MaxRad = 30.0

# Array to hold updated values
# This array can be used to implement the weight sums
# for example gaussian, tophat, cone
# currently set to one for general use.
ww = 1.0#np.ones((Lx, Ly), dtype=np.float64)

setup_stop_time = time.time()
kernel_start_time = time.time()

# Begin smoothing kernel
for xx in range(Lx):
    for yy in range(Ly):
        qq = 0.0        ## size of box
        sum = 0.0       ## value of the sum
        ksum = 0.0      ## value of the kernal sum
        ss = qq         ## size of the box around source pixel
        
        # Continue until parameters
        while (sum < Threshold) and (qq < MaxRad):
            ss = qq
            sum = 0.0
            ksum = 0.0
            
            # Updated for loops for python
            for ii in xrange( int(-ss), int(ss+1) ):
                for jj in xrange( int(-ss), int(ss+1) ):
                    #check for boundary condition
                    #else skip to where qq = boundary
                    if((xx + ss < Lx) and (yy + ss < Ly)):
                        sum += IMG[xx + ii][yy + jj] * 1.0 #ww[ii + ss][jj + ss]
                        ksum += 1.0 #(ww[ii + ss][jj + ss])
                    else:
                        qq = MaxRad
            qq += 1
            
        # 
        RAD[xx][yy] = ss
        TOTAL[xx][yy] = sum
        
        # Determine the normalization for each box
        for ii in xrange( int(-ss), int(ss+1) ):
            for jj in xrange( int(-ss), int(ss+1) ):
                if((xx + ss < Lx) and (yy + ss < Ly)):
                    NORM[xx+ii][yy+jj] += 1.0 / ksum #(ww[ii+ss][jj+ss])/ksum
#---------------------------------------------------------------

# Normalize the image
for xx in range(Lx):
    for yy in range(Ly):
        IMG[xx][yy] /= NORM[xx][yy]

#---------------------------------------------------------------

#
for xx in range(Lx):
    for yy in range(Ly):
        ss = RAD[xx][yy]
        sum = 0.0
        ksum = 0.0

        #
        for ii in xrange( int(-ss), int(ss+1) ):
            for jj in xrange( int(-ss), int(ss+1) ):
                if((xx + ss < Lx) and (yy + ss < Ly)):
                    sum += (IMG[xx+ii][yy+jj] * 1.0) #ww[ii+ss][jj+ss])
                    ksum += 1.0 #ww[ii+ss][jj+ss]
        #check for divide by zero
        if(ksum != 0):
            OUT[xx][yy] = sum / ksum
        else:
            OUT[xx][yy] = 0

kernel_stop_time = time.time()
total_stop_time = time.time()
#---------------------------------------------------------------

# Save the current image. NOT DONE
imsave('input_small/114_ccd7{0}{1}.png'.format('_smooth', '1'), OUT, cmap=cm.gray, vmin=0, vmax=1)

# Print results & save
print "Total Time: %f"      % (total_stop_time - total_start_time)
print "Setup Time: %f"      % (setup_stop_time - setup_start_time)
print "Kernel Time: %f"     % (kernel_stop_time - kernel_start_time)
