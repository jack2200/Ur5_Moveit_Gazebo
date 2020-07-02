#!/bin/bash

rosrun gazebo_test_tools cube_spawner cube1 0.35 0.42 0.9 ground_plane
python ur5_control.py --shift_pose --axis_value 2 0.25
python ur5_control.py --shift_pose --axis_value 0 -0.475
python ur5_control.py --shift_pose --axis_value 2 -0.38
python ur5_control.py --shift_pose --axis_value 1 0.06
python send_gripper.py --value 0.45
python send_gripper.py --value 0.46
python ur5_control.py --attach_box --box_name cube1.link
python ur5_control.py --shift_pose --axis_value 2 0.25
python ur5_control.py --shift_pose --axis_value 0 0.25
python ur5_control.py --shift_pose --axis_value 2 -0.2
python ur5_control.py --detach_box --box_name cube1.link
python send_gripper.py --value 0.1
python ur5_control.py --shift_pose --axis_value 2 0.2
python ur5_control.py --shift_pose --axis_value 0 -0.25


#X 0.35 Y 0.42 Z 0.9
#Z 0.25 X -0.475 Z -0.38 Y 0.06


#x 0.36 Y 0.42 z 0.8

#SEND_GRİPPER 0.46
