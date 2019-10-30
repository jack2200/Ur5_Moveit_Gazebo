# Ur5_Moveit_Gazebo
Python script for simulating UR5 using MoveIt in Gazebo and Rviz

- The code is based on Python script in Moveit Python interface:
https://ros-planning.github.io/moveit_tutorials/doc/move_group_python_interface/move_group_python_interface_tutorial.html 

- Made it work with UR5 (Only change: group name = "manipulator" instead of  group name = "panda")
Deleted some unnecessary comments and variables.

- Made some changes in IO part 
  - Used a while(1) loop to take input until using KeyboardInterrup. This way sequential movement can be simulated.
  - Used a case variable for simulating different movement types. 
  - There are 0 to 7 cases.
  - 0 and 1 cases are usefull for now. Did not make any changes to others.
  - CASE 0: For executing a movement using a joint state goal.
    - The input should be in the form key jgfj1 jgfj2 jgfj3 jgfj4 jgfj5 jgfj6
    - jgfj -> joint goal for joint ...
    - jgfj values are multiplied with pi to compute the values used in the go_to_joint_state function.
    - jgdf values are given as a list to the go_to_joint_state function.
    - key is for using different modes.
      - if key is given as 0, the values in the list is summed with the current joint values of the robot.
      - İf key is given as 1, the current joint values are changed with the values in the list.
  - CASE 1: For execute a movement using a pose goal.
