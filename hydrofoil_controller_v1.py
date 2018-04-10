########
# Intro.  #
########

# This program is used to control the foils in the hydrofoil system.
# This is done by getting the required values from the Vector Nav 300 registers
# to acquire Velocity (X, Y, Z) , Yaw, Pitch, Roll, Angular Rates (Yaw, Pitch, Roll )
# and from the ToughSonic 14 height in Z.
# Communication is done by USB-to-Serial and using VectorNav Library.
# After reading the values, they are send to a matrix which calculates the angles
# for the foil actuators. 

#############################################
# Installing the library and settings for the VectorNav #
#############################################

# In order to run you must download the library from Vector Nav 
# and follow the instructions to install. First make the C library
# later the python library, in order to avoid problems.
# Configure sensor using the website Sensor Explorer program.
# Set up the sensor and when finish righ-click sensor icon, go to
# Commands> Save Settings to Sensor Memory.
# This will store your settings into a Non-Volatile memory in the sensor that
# will be read upon start.

#########
# To Do: #
#########

# RPM motor, motor current
# Threads
# Calculations
# Send foils degrees


from vnpy import *
import sys
import serial
import io



## Setup ##

VectorNav = VnSensor()

# Connect to Serial Port
# Change according to connected device port
# To see port enter in terminal: dmesg

VectorNav.connect('/dev/ttyUSB0', 921600)  
ToughSonic = serial.Serial('/dev/ttyUSB0', timeout=1)

# Parameters for Blocking or Non-Blocking communication
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), newline = '\r', line_buffering = True)
input_stream = sio.readline() # ingore first read
#s.write_async_data_output_frequency(100) # Set Frequency to 100 Hz


while(1):  
		
		start = timeit.default_timer() # gets start time
		
		ypr = VectorNav.read_yaw_pitch_roll()							 	# Reads the Yaw Pitch Roll register.
		angular = VectorNav.read_angular_rate_measurements()	# Reads the Angular Rate Measurements register.
		gpsecef = VectorNav.read_gps_solution_ecef()					# Reads the GPS Solution - ECEF register.
		
		
		# Yaw,Pitch,Roll
		# Yes, the values don't make sense but the reference frame is all wrong
		psi= ypr.x 	#Yaw
		theta=ypr.y 	# Pitch
		phi=ypr.z 		# Roll
		
		
		# Angular rates in Yaw, Pitch, Roll
		# These values seem to be right
		p = angular.x 	# Velocity in Roll (rad/sec)
		q = angular.y 	# Velocity in Pitch (rad/sec)
		r = angular.z 		# Velocity in Yaw (rad/sec)
		
		# GPS Velocity
		velocity_x = gpsecef.velocity.x 	# ECEF X velocity m/s
		velocity_y = gpsecef.velocity.y 	# ECEF Y velocity m/s
		velocity_z = gpsecef.velocity.z 	# ECEF Z velocity m/s
		
        # Convert data to extract real measurement value.
	        input_stream = sio.readline()
		data = int(input_stream)
		height = data*(0.003384) # multiply by datasheet specified number
		
		### Testing ONLY ###
		
		stop = timeit.default_timer() # gets stop time
		time =  ' ' + str( stop - start ) + ' sec.' # calculates time elapse in seconds
		print (time)
		
		gps_vel = ' Vel X:' + str (velocity_x) +  ' m/s' +' Vel Y:' + str(velocity_y) + ' m/s' + ' Vel Z:' +str(velocity_z) + ' m/s' 
		print(gps_vel)
			
		angular_rates = ' Yaw (rad/sec):' + str(r) + ' Roll (rad/sec):' + str(p) + ' Pitch (rad/sec):' + str(q)
		print(angular_rates)
		
		ypr_data = ' Yaw:' + str(psi) + ' Roll:' + str(phi) + ' Pitch:' + str(theta)
		print(ypr_data)
		
		print()

		
	
