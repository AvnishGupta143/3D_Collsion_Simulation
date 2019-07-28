import numpy as np
import constants as const
import copy
import os

class Ball():
    '''
        Ball class represents the object where const.UNITS_IN_ONE_METER represents 1 meter in the 3D-Space

            Public Methods:  __init__(self, id, UNITS_IN_ONE_METER = const.UNITS_IN_ONE_METERs)
                            __str__(self)
                            move(self)
                            bound_the_ball(self)
                            check_boundary_collision(self)
                            check_body_collsion(self, grid)
                            update(self, Prev_Grid, Grid, lock, step)

    '''

    def __init__(self, id, UNITS_IN_ONE_METER = const.UNITS_IN_ONE_METER):
        '''
            Initialization function for the class Ball object

            Args:
                id(int) - Id of the ball
                UNITS_IN_ONE_METER(int) - Number of units in one meter in the program. By default taken from contants.py

            Attributes:
                id(int) - saves id of the ball object
                UNITS_IN_ONE_METER(int) - saves number of units in one meter
                IsFirst(bool) - Flag which is True when update is called for the first time and then always False
                radius(float) - saves the radius of the ball in units
                boundary_collsion(bool) - Flag indicating occurance of boundary collision at each update. Set to 
                                          False initially and updated by check_boundary_collision() func
                body_collision(bool) - Flag indicating occurance of ball to ball collision at each update. Set to
                                       False initially and updated by check_body_collision() func
                collision_body_ids(numpy.ndarray) - Array haveing ids of the balls in collison with this ball at 
                                                    a instant or time step
                grid(Map) - Variable storing the Map class object written in box.py file. Stores info about current 
                            state. Set to None Initially
                new_pos(numpy.ndarray) - Variable Storing new position of the Ball object in [x,y,z] in the box after 
                                         every update() call.Set initially by generating random numbers between the 
                                         bound of the box
                curr_pos(numpy.ndarray) - Variable storing current position of Ball object
                new_vel(numpy.ndarray) - Variable Storing new velocity of the Ball object in [x,y,z] in the box after 
                                         every update() call. Set initially by generating random numbers between the 
                                         magnitudes for each axis specified in constants.py file.
                curr_vel(numpy.ndarray) - Variable storing current velocity of Ball object

        ''' 
        self.id = id
        self.UNITS_IN_ONE_METER = UNITS_IN_ONE_METER
        self.radius = self.UNITS_IN_ONE_METER/2.0
        
        self.IsFirst = True
        self.boundary_collision = False
        self.body_collision = False
        self.collision_body_ids = None

        self.grid = None
        
        self.new_pos = np.squeeze([np.random.randint(1,const.BOX_DIM[0],size=1),
                                   np.random.randint(1,const.BOX_DIM[1],size=1),
                                   np.random.randint(0,const.BOX_DIM[2],size=1)])
        self.curr_pos = None
        
        self.new_vel = np.squeeze([np.random.randint(-const.VELOCITY_MAG_ALONG_X_AXIS,const.VELOCITY_MAG_ALONG_X_AXIS,size=1),
                                    np.random.randint(-const.VELOCITY_MAG_ALONG_Y_AXIS,const.VELOCITY_MAG_ALONG_Y_AXIS,size=1),
                                    np.random.randint(-const.VELOCITY_MAG_ALONG_Z_AXIS,const.VELOCITY_MAG_ALONG_Z_AXIS,size=1)])
        if const.BOX_DIM[2] < self.UNITS_IN_ONE_METER:
            self.new_vel[2] = 0.0
        if sum(self.new_vel) == 0:
            self.new_vel[0] = 1
        
        self.curr_vel = self.new_vel
        
        self.bound_the_ball()

    def __str__(self):
        '''
            Function to return the current pose and vel of the ball object as a formatted string.
        '''
        return "Position[ x: {} y: {} z: {} ]\nVelocity[ {} ] ".format(self.curr_pos[0], self.curr_pos[1], self.curr_pos[2], self.velocity)

    def move(self):
        '''
            Function to update positon of the ball object after 1 time step. Saves the new position vector of the ball by 
            adding new velocity in each axis to current position in each axis in the box.
        '''
        self.new_pos = self.new_vel + self.curr_pos
        self.bound_the_ball()

    def bound_the_ball(self):
        '''
            Function to bound the position of the ball between the bounds of the box by checking for coordinates near
            the boundary axis.
            Checks if coordinate of the ball along each axis should not exceed box_dimension minus radius in that axis
            and should not be less the radius of the ball. In case if dimension of the box is less than units in one 
            meter (or diameter of the ball) in Z-axis which is the case for 2D collision, the position of ball in Z 
            axis is set to box_dimension_in_that_axis/2 for that axis.

        '''
        #Bounding the ball for axis X
        if self.new_pos[0] < int(self.radius):
            self.new_pos[0] = int(self.radius)
        if self.new_pos[0] >= const.BOX_DIM[0] - int(self.radius):
            self.new_pos[0] = const.BOX_DIM[0] - int(self.radius) - 1

        #Bounding the ball for axis Y
        if self.new_pos[1] < int(self.radius):
            self.new_pos[1] = int(self.radius)
        if self.new_pos[1] >= const.BOX_DIM[1] - int(self.radius):
            self.new_pos[1] = const.BOX_DIM[1] - int(self.radius) - 1

        #Bounding the ball for axis Z
        if const.BOX_DIM[2] > self.UNITS_IN_ONE_METER:
            if self.new_pos[2] < int(self.radius):
                self.new_pos[2] = int(self.radius)
            if self.new_pos[2] >= const.BOX_DIM[2] - int(self.radius):
                self.new_pos[2] = const.BOX_DIM[2] - int(self.radius) - 1
        else:
            self.new_pos[2] = int(const.BOX_DIM[2]/2)

    def check_boundary_collision(self):
        '''
            Function to check collisions on boundary. Updates the new velocity of the ball in all the axis for which ball
            is hitting the boundary. It starts by creating a zeros array collision_axes of size equal to number of axis in
            the box and it represents if particular axis is in collsion with the ball or not in the order X,Y,Z. Element 
            in collsion_axes is set to 1 at that index if collsion occurs in that axis along the boundary by checking 
            current pose for the bounds. Finally velocity of the ball is reversed in magnitude for the index for which 
            the collsion_axes is 1.
        '''
        if const.BOX_DIM[1] < self.UNITS_IN_ONE_METER:
            collision_axes = np.zeros(len(const.BOX_DIM)-1)
        else:
            collision_axes = np.zeros(len(const.BOX_DIM))
        
        self.boundary_collision = False

        #Checking for boundary collsion
        for i in range(len(collision_axes)):
            if (self.curr_pos[i] <= self.radius and self.curr_vel[i] < 0) or (self.curr_pos[i] >= (const.BOX_DIM[i]-self.radius-1) and self.curr_vel[i] > 0):
                collision_axes[i] = 1
                self.boundary_collision = True

        #If boundary_collision = True than update the new velocity due to boundary collsion
        if self.boundary_collision:
            LOI_axis_indexes = np.where(collision_axes == 1)
            for i in LOI_axis_indexes:
                self.new_vel[i] = -self.curr_vel[i]

    def check_body_collsion(self):
        '''
            Function to check ball tp ball collsion. It starts by computing body collision matrix for the ball by
            slicing the part of occupancy Id map in the grid as (current_position - 2*radius, current_position + 
            2*radius) along each axis. If the body collision matrix contains Id's of other balls at this instant, 
            they are saved in collision_body_ids array. If length of collision_body_ids is greater than zeros than
            for each ID in collision_body_ids, new velocity of this ball is updated by adding component of relative 
            velocity of the ball whose ID we are considering wrt to this ball along the common normal directed from 
            center of ID ball to this ball.

            Args:
                grid(Map) - current instance of the box
        '''
        if const.BOX_DIM[2] < self.UNITS_IN_ONE_METER:
            x_min = max(0,int(self.curr_pos[0]-2*self.radius))
            x_max = min(int(self.curr_pos[0]+2*self.radius+1),const.BOX_DIM[0])
            y_min = max(0,int(self.curr_pos[1]-2*self.radius))
            y_max = min(int(self.curr_pos[1]+2*self.radius+1),const.BOX_DIM[1])
            body_col_mat = self.grid.id_map[x_min:x_max,y_min:y_max]

        else:
            x_min = max(0,int(self.curr_pos[0]-2*self.radius))
            x_max = min(int(self.curr_pos[0]+2*self.radius+1),const.BOX_DIM[0])
            y_min = max(0,int(self.curr_pos[1]-2*self.radius))
            y_max = min(int(self.curr_pos[1]+2*self.radius+1),const.BOX_DIM[1])
            z_min = max(0,int(self.curr_pos[2]-2*self.radius))
            z_max = min(int(self.curr_pos[2]+2*self.radius+1),const.BOX_DIM[2])
            body_col_mat = self.grid.id_map[x_min:x_max,y_min:y_max,z_min:z_max]
        
        # find the ids of all the balls that are around the current ball
        self.collision_body_ids = body_col_mat[np.where(body_col_mat!=0)]
        
        # delete the id of the current ball from the list
        self.collision_body_ids = np.delete(self.collision_body_ids, np.where(self.collision_body_ids == self.id))

        if len(self.collision_body_ids > 0):
            self.body_collision = True
        else:
            self.body_collision = False
            
        if self.body_collision:
            for ID in self.collision_body_ids:
                pos_vec1 = self.curr_pos
                pos_vec2 = self.grid.pos_array[int(ID-1)]
                
                # Calculating Line of Impact(LOI) or Line of Collsion between the two balls
                pos_vec12 = pos_vec2 - pos_vec1
                if np.linalg.norm(pos_vec12)!=0:
                    LOI = (pos_vec12)/np.linalg.norm(pos_vec12)
                    
                    vel_vec1 = self.new_vel
                    vel_vec2 = self.grid.vel_array[int(ID-1)]
        
                    # Relative velocity vector of ID ball in collsion with this ball
                    vel_vec12 = vel_vec2 - vel_vec1

                    # Component of the relative velocity along the common normal(LOI)
                    vel_normal = np.dot(vel_vec12, LOI) * LOI
    
                    self.new_vel = self.new_vel + vel_normal
                else:
                    self.new_vel = -self.new_vel

	
                    
        self.new_vel[0] = int(round(self.new_vel[0]))
        self.new_vel[1] = int(round(self.new_vel[1]))
        self.new_vel[2] = int(round(self.new_vel[2]))


    def update(self, Prev_Grid, Grid, lock):   
        '''
            Function which updates thes position and velocity of the ball at each instant. This function is called by a
            multithreaded caller for the simulation so that every ball has its own thread for update function.
            The function checks for boundary and body collision for the ball by calling check_boundary_collision() and 
            check_body_collsion() and then calls move() to update the pose and velocity of the ball. Finally it updates 
            the global Grid, curr_pos, curr_vel.

            Args:
                Prev_Grid(Map) - Map class object storing info about the current instance
                Grid(Map) - Map class object storing info about the next instance
                lock(threading.Lock) - Lock object require to synchronize the update of global Grid variable by all
                                       N number of Ball object threads
        '''   
        self.grid = copy.deepcopy(Prev_Grid)
        if not self.IsFirst:
            self.check_boundary_collision()
            self.check_body_collsion()
            self.move()
        else:
            self.IsFirst = False
        
        #Aquiring lock and updating the global Grid for next instance
        lock.acquire()
        Grid.id_map[int(self.new_pos[0]),int(self.new_pos[1]),int(self.new_pos[2])] = self.id
        Grid.pos_array[self.id-1] = self.new_pos
        Grid.vel_array[self.id-1] = self.new_vel
        lock.release()

        #Updating the current pose and velocity for next update call
        self.curr_pos = self.new_pos
        self.curr_vel = self.new_vel
