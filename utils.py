import numpy as np
import os

def clear_folders():
	"""
		Function to clear all the files in the folder at Initialization of the simulation
	"""
	curr_path = os.getcwd()
	trajectory_path = curr_path + '/trajectory/*.txt'
	image_path = curr_path + '/images/*.png'
	os.system('rm -rf ' + trajectory_path)
	os.system('rm -rf ' + image_path)

def write_trajectory(num_balls, step, pos_array, vel_array):
    '''
        Function to write the trajectory(includes pose and velocity at the current step) to the textfile for the ball object

        Args:
        	num_balls(int) - number of balls
     	    step - Value of the timestep for which we have done the update() call
     	    pos_array(numpy.ndarray) - array of shape [num_ball,3] having position for all balls at a instance
     	    vel_array(numpy.ndarray) - array of shape [num_ball,3] having velocity for all balls at a instance
    '''
    for i in range(num_balls):
    	filename = '{}/trajectory/ball_{}.txt'.format(str(os.getcwd()),str(i))
    	writer  = open(filename,'a+')
    	text ='{0}. Posx:{1} Posy:{2} Posz:{3} Velx:{4} Vely:{5} Velz:{6}\n'.format(str(step),pos_array[i][0],pos_array[i][1],pos_array[i][2],
	    vel_array[i][0],vel_array[i][1],vel_array[i][2])
    	writer.write(text)
    	writer.close()