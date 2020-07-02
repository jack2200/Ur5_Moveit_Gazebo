#!/usr/bin/env python

import argparse
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

def all_close(goal, actual, tolerance):
  """
  Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
  @param: goal       A list of floats, a Pose or a PoseStamped
  @param: actual     A list of floats, a Pose or a PoseStamped
  @param: tolerance  A float
  @returns: bool
  """
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True

class MoveGroupPythonIntefaceTutorial(object):
  def __init__(self):
    super(MoveGroupPythonIntefaceTutorial, self).__init__()

    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial',
                    anonymous=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group = moveit_commander.MoveGroupCommander("manipulator")
    hand_group = moveit_commander.MoveGroupCommander("gripper")
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    planning_frame = group.get_planning_frame()
    #print "============ Reference frame: %s" % planning_frame

    eef_link = group.get_end_effector_link()
    #print "============ End effector: %s" % eef_link

    group_names = robot.get_group_names()
    #print "============ Robot Groups:", robot.get_group_names()

    #print "============ Printing robot state"
    #print robot.get_current_state()
    #print ""

    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.group = group
    self.hand_group = hand_group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names

  def go_to_joint_state(self,goal_list):
    joint_goal = self.group.get_current_joint_values()
    if(goal_list[0] == 0):
      for i in range(len(joint_goal)):
        joint_goal[i] = joint_goal[i] + goal_list[i+1]
    elif(goal_list[0] == pi):
      joint_goal = goal_list[1:]
    else:
      print "Wrong key!!"
      return    
    self.group.go(joint_goal, wait=True)
    self.group.stop()
    current_joints = self.group.get_current_joint_values()
    return all_close(joint_goal, current_joints, 0.01)

  def go_to_pose_goal(self,x,y,z,w):
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = w
    pose_goal.position.x = x
    pose_goal.position.y = y
    pose_goal.position.z = z
    self.group.set_pose_target(pose_goal)
    plan = self.group.go(wait=True)
    self.group.stop()
    self.group.clear_pose_targets()
    current_pose = self.group.get_current_pose().pose
    return all_close(pose_goal, current_pose, 0.01)

  def go_to_shifted_pose(self, axis, value):
    self.group.shift_pose_target(axis, value)
    plan = self.group.go(wait=True)
    self.group.stop()
    self.group.clear_pose_targets()
    return 

  def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=10):
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
      attached_objects = self.scene.get_attached_objects([self.box_name])
      is_attached = len(attached_objects.keys()) > 0
      is_known = self.box_name in self.scene.get_known_object_names()
      if (box_is_attached == is_attached) and (box_is_known == is_known):
        return True
      rospy.sleep(0.1)
      seconds = rospy.get_time()
    return False

  def get_names_of_objects(self):
    names = self.scene.get_known_object_names()
    print names
    return 

  def get_attached_objects(self):
    print "Attached objects: "
    print self.scene.get_attached_objects().keys()
    return

  def attach_box(self, box_name1, timeout=4):
    grasping_group = 'gripper'
    touch_links = self.robot.get_link_names(group=grasping_group)
    self.scene.attach_box(self.eef_link, name=box_name1, touch_links=touch_links)
    return self.wait_for_state_update(box_is_attached=True, box_is_known=False, timeout=timeout)

  def detach_box(self, box_name1, timeout=4):
    self.scene.remove_attached_object(self.eef_link, name=box_name1)
    return self.wait_for_state_update(box_is_known=True, box_is_attached=False, timeout=timeout)

def main():
  try:
    # Get the angle from the command line
    parser = argparse.ArgumentParser(description='UR5_Moveit_Controller')
    parser.add_argument("--change_joint_state", action="store_true")
    parser.add_argument("--change_pose", action="store_true")
    parser.add_argument("--shift_pose", action="store_true")
    parser.add_argument('--joint_values', type=float, nargs='+',
                    help='Give key and states [k, w1, w2, w3, w4, w5, w6] to change joint stage')
    parser.add_argument('--coordinates', type=float, nargs='+',
                    help='Give coordinates [x, y, z, w] to change pose')
    parser.add_argument('--axis_value', type=float, nargs='+',
                    help='axis and value to shift pose')
    parser.add_argument("--attach_box", help="attach box give box name using --box_name",
                    action="store_true")
    parser.add_argument("--detach_box", help="detach box give box name using --box_name",
                    action="store_true")
    parser.add_argument("--objects", help="print objects in gazebo",
                  action="store_true")
    parser.add_argument("--box_name", type=str, help="box name")
    args = parser.parse_args()
    tutorial = MoveGroupPythonIntefaceTutorial()
    if(args.change_pose):
        coords = args.coordinates
        x = float(coords[0])
        y = float(coords[1])
        z = float(coords[2])
        w = float(coords[3])
        tutorial.go_to_pose_goal(x,y,z,w)
        return
    if(args.change_joint_state):
      goal_list = args.joint_values
      goal_list = [float(goal)*pi for goal in goal_list]
      tutorial.go_to_joint_state(goal_list)
      return
    if(args.shift_pose):
      axis, value = args.axis_value[0], args.axis_value[1]
      axis = int(axis)
      value = float(value)
      tutorial.go_to_shifted_pose(axis, value)
      return
    if(args.attach_box):
      print "press Enter and wait for moveit then press 1"
      while(1):
        tutorial.attach_box(box_name1=args.box_name)
        if(raw_input() == "1"):
          return
    if(args.detach_box):
      print "press Enter and wait for moveit then press 1"
      while(1):
        tutorial.detach_box(box_name1=args.box_name)
        if(raw_input() =="1"):
          return
    if(args.objects):
      tutorial.get_names_of_objects()
      return
  except rospy.ROSInterruptException:
    print "Something went wrong!!"
  
if __name__ == '__main__':
  main()