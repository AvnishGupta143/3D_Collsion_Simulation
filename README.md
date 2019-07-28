# 3D_Collsion_Simulation
It has code for simulating 2D and 3D collsion
Running the Code
###Running: 1. Depdendencies can be installed through requirements.txt
	     2. Run this file as $python  run_simulation.py for running the program. Then Press Enter 	         to start.
###Files:
	1. run_simulation.py – Files containing main() function of the pipeline.
	2. ball.py – Class for ball
	3. box.py – Class for box
	4. constants.py – File containing values of program constants. Edit here the change the 	constants value
	5. utils.py – Contains two helper functions to clear the folder and to write trajectory to the 	file 
###Note:
	1. Trajectory for each ball is saved in trajectory folder and images  are saved in Images 	folder.
	2. In case if user has long pressed Ctrl+C than the program terminates there and then just 	saving till the current progress.
	3. Press Enter to start the program.

##Collisions 

In the scenario given in the question the following two types of collision is possible for which we need to update the pose and velocity physically.
  
###1.BOUNDARY COLLSION:

To check for boundary collsion, the concept used is position coordinate of the ball is outside the bounds of the box dimension than ball is said to be in boundary collsion. Diameter of ball is given as 1m which is defined in the program as units in one meter.
Radius of the ball = Diameter/2
                             = Units in one meter/2

Least coordinate possible in any axis = int(radius)
Largest coordinate possible in any axis = Size of box in that axis – int(radius)  - 1

So we say that ball is in boundary collision with the respective box boundary for which:
1.If velocity along that axis is negative and currant coordinate is less than Least coordinate possible in that axis.
						OR
2. If velocity along that axis is positive and currant coordinate is greater than Largest coordinate possible in that axis.

If ball comes in collision with any of the axis, the velocity along that axis is reversed as in case of boundary collision, the collsion axis or boundary becomes the common normal or Line of Impact. And in case if elastic collsion with ver large mass which we have considered for box, velocity is reversed according to conservation of momentum.

###2.BODY TO BODY COLLISON:

A collision in two or three dimensions can be treated like the one-dimensional case by working with quantities "normal" to the collision. Normally change in velocities for Elastic collision is occur only along the Line of Impact or common Normal between the objects. For collisions between balls, that means velocities along the line joining the centers of the two balls will change.
If positions are denoted by vectors x1 and x2, the normal vector between two balls directed from ball 2 to ball 1:
n = (x2 − x1) / |x1 − x2|
With velocities of the two bodies denoted by denoted by vectors v1 and v2, the relative velocity of 2 with respect to ball 1 is:
vrelative  =  v2 − v1
and the relative velocity along the normal direction is
Vnormal  =  (Vrelative⋅n) n
At the time of collision, normal components of momentum are interchanged while tangential components are left alone. Assuming balls of equal mass, momentum and velocity are interchangeable along  LOI for elastic collsion. The collision condition can then be written
v1 = v1  + vnormal
v2  = v2 - vnormal

