
# grasp_demo.py
Python code that uses move_it to pick an object

## Some definitions

 1. ***move_group*** = the node that allow us to send tractories and positions  to the joints of the robot by using very simple
   interfaces. (We use *moveit_commander* in python) ![enter image description here](https://raw.githubusercontent.com/JAKD9/Ur5_Moveit_Gazebo/master/Grasp/schema%20for%20move_group.JPG?token=ABLVZNA76Q6PABAKIEP2JNK52CLPK)


 2. After executing the command below:
   
       roslaunch <my_robot_moveit_configfile> <my_robot_exec.launch>
   
     if we get the message:
    > You can start planning_ now! [ INFO]
   
    This means that we can create an instance of the *moveit_commander* 
   inside our python program, and start sending commands to move group
   that is running.
 3. ***moveit_commander*** = a python class that allow us to send python commands to the move_group and move the arm in a very easy way.  
We can send commands to the move_group in **four different ways:** 
    1) Send a **complete pose** you defined during the moveit configuration.
    2) Send a **position for the end effector**. (This case doesn't care how to do kinematics for each one of the joints in order to achieve that position.)
    3) Specify the **goal position** for each joint. (hard way) 
    4) **Specify a trajectory** to follow. (not only the values of the joints but also a specific trajectory of the all the joints in a given amount of time)
    
## Grasping Steps
Whenever we need to do a grasp, we need to implement the following steps
 
 1. Bring the arm to a known position.
 2. Open the gripper.
 3. Bring the arm to the location of the object, minus a certain amount of space.
 4. Move the arm closer to the object until it is between its gripper.
 5. Close the gripper.
 6. Do an additional move to lift the object.

After completing all these steps, robot is considered as it has grasped the object.

In python script `grasp_demo.py` (python2) , steps are implemented assuming the robot should grasp the fixed object.(i.e we are considering we know where the object is)

Note: Variable names for robot and gripper move_groups or other things are indicated in the code.






