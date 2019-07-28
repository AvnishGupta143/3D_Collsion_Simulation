"""
	1.Trajectory saved in trajectory folder and images saved in Images folder.
	2.Change the values of the program contants from contantss.py file.
	3.Refer to documentation.docx for explanation of concept for 3D collsion.
	4.In case if user has long pressed Ctrl+C than the program terminates there and then just saving till the current
	  progress.
	5.Press Enter to start the program
"""
import constants as const
from ball import Ball
from box import Map
from utils import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

from threading import Thread,Lock

import copy
import time
import sys
import os

def main():
	"""
		Main function which makes the N ball objects inside the Map and then creates a multithreaded call to the update
		functions for every ball to update pos and vel of the balls for the number of time_steps specified in the 
		constants.py file. The function also plots the visual using matplotlib library and saves images of each 
		time step in Images folder and trajectories for all the balls in trajectory folder. After updating for the 
		time steps mentioned the program waits for 2 seconds and then exits.
		In case if user has long pressed Ctrl+C than the program terminates there and then just by saving till the 
		current progress
	"""
	curr_path = os.getcwd()
	num_balls = const.num_balls
	time_steps = const.time_steps
	
	Grid = Map(num_balls = num_balls)
	
	Balls = []
	Ball_Threads = []
	lock = Lock()

	#Matplotlib plot related variables.
	fig = plt.figure()
	ax = Axes3D(fig)
	axes = plt.gca()
	axes.set_xlim([0, int(const.BOX_DIM[0]-1)])
	axes.set_ylim([0, int(const.BOX_DIM[1]-1)])
	axes.set_zlim([0, const.BOX_DIM[2]])
	color_pallete = np.squeeze([np.random.rand(num_balls,),np.random.rand(num_balls,),np.random.rand(num_balls,)]).T

	print("Number of balls:{}\nTime Steps:{}".format(num_balls,time_steps))
	print("Press Enter to Start the Simulation:")
	start = raw_input()
	if start!='':
		sys.exit()

	#Used to make the plt.show() not blocking
	plt.ion()

	#Creating num_balls number of objects of Ball class
	for i in range(num_balls):
		Balls.append(Ball(id = i+1))

	try:
		for step in range(time_steps):
			Ball_Threads = []
			Prev_Grid = copy.deepcopy(Grid)
			Grid.reset()
			start_time = time.time()

			#Starting update thread for every ball
			for i in range(num_balls):
				Ball_Threads.append(Thread(target = Balls[i].update, args = (Prev_Grid, Grid, lock), name = "Ball {}".format(i+1)))
				Ball_Threads[i].setDaemon(True)
				Ball_Threads[i].start()

			#Waiting for all the threads to join
			for t in Ball_Threads:
				t.join()

			stop_time = time.time()

			print("Time Taked in step number {}:.{}".format(step,float(stop_time-start_time)))
			
			#Writing trajectory to the files
			written = False
			write_thread = Thread(target = write_trajectory, args = (num_balls, step, Grid.pos_array, Grid.vel_array), name = "Writer")
			write_thread.start()
			written = True

			#Updating the plot
			x = Grid.pos_array[:,0]
			y = Grid.pos_array[:,1]
			z = Grid.pos_array[:,2]
			plot = ax.scatter(x, y, z, c = color_pallete, s = (const.UNITS_IN_ONE_METER**3)*3.14*1.33*2)
			plt.pause(0.001)
			plt.savefig(curr_path+'/images/{}.png'.format(step))
			if step != time_steps-1:
				plot.remove()
	except KeyboardInterrupt as e:
		print(e)
		plt.savefig(curr_path+'/images/{}.png'.format(step))
		if not written:
			write_thread = Thread(target = write_trajectory, args = (num_balls, step, Grid.pos_array, Grid.vel_array), name = "Writer")
			write_thread.start()
			write_thread.join()
		print("---------------Program Stopped by User by KeyboardInterrupt-----------------")
		for t in Ball_Threads:
			if t.isAlive():
				t.join()
		
		sys.exit()

	plt.show()
	time.sleep(2)
	print("-----------Program Finished-----------")
	plt.close()

if __name__ == '__main__':
	clear_folders()
	main()
