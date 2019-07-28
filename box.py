import numpy as np
import constants as const

class Map():
	'''
        Map class represents the object which has 3D-Space in which the balls can move.

            Public Methods: __init__(self, num_balls = 5)
                            reset(self)
    '''
	def __init__(self, num_balls = const.num_balls):
		"""
			Initialization function for Map object

			Args: 
				num_balls(int) - Number of balls in the program. Set to default values as const.num_balls written in 
							contants.py

			Attributes:
				num_balls(int) - Number of balls in the program
				id_map(numpy.ndarray) - 3-D array equal to size of box dimensions specified in contants.py. It gets
										updated to ids of the ball at the position where ball is present in the box
										at every instance
				pos_array(numpy.ndarray) - Array of position of all the balls
				vel_array(numpy.ndarray) - Array of	velocity of all the balls

		"""
		self.num_balls = num_balls
		self.id_map = np.zeros([const.BOX_DIM[0],const.BOX_DIM[1],const.BOX_DIM[2]])
		self.pos_array = np.zeros([num_balls,3])
		self.vel_array = np.zeros([num_balls,3])

	def reset(self):
		"""
			Function to reset values of all the object attributes
		"""
		self.__init__(self.num_balls)