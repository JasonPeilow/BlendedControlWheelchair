#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__________________________________________________________________________________________________
Brief Description
__________________________________________________________________________________________________

The purpose of this script is to set individual goal states that will allow the robot to reach
the other side of the restaurant with little to no incident. This can be achieved by utilizing
the parameters of the navigation stack to detect obstacles within the given environment and plan
a path that can be completed with the minimal navigation cost. This will be in the context of a
specific map drawn from the map_server.

__________________________________________________________________________________________________
1. Imported Clients and Packages
__________________________________________________________________________________________________

rospy is the client library for ros python. The action library provides the ability to broadcast
and listen for goals from the action server/client. These goals are set using the
MoveBaseGoal library and are then communicated to the action server using MoveBaseAciton. This
is passed as an arguement through the SimpleActionClient from the actionlib library.

"""

import rospy
import actionlib
import sys

from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
# (Ferguson, 2019)

"""
__________________________________________________________________________________________________
2. Pose and Orientation
__________________________________________________________________________________________________

In this instance, the robot must follow a series of set goal points to complete a planned path.
An example of designated points are the x and y which are set as (-0.06, 4.70) respectively.
The same applies for the orientation/quaternion coordinates being qz (orientation.z) and qw
(orientation.w), which have been set to 0.70, 1.0. Additionally, is can be noted that z, qx and
qy have been set to zero as default. The reason for this is that the robot only travels along the
x and y plane. Position as a z coordinate refers to elevation/upwards movement. This wheelchair
does not levitate or fly in anyway, z is not required. qx and qy refer to the roll and pitch.
The robot also has no need for these coordinates to access every level of functionality.

"""
GoalPoints = [[(-0.06, 4.70), (0.70, 1.00)],  # 1 start path
              [(0.96, 5.73), (0.70, 1.00)],   # 2 path
              [(6.43, 5.30), (-0.33, 1.00)],  # 3 gate
              [(6.60, -1.75), (-0.33, 1.00)], # 4 crossing
              [(13.74, -2.02), (0.37, 1.00)], # 5 cross road
              [(13.98, 1.66), (0.72, 1.00)],  # 6 pre car
              [(13.93, 6.26), (0.01, 1.00)],  # 7 post car
              [(18.83, 5.92), (0.02, 1.00)],  # 8 cafe
              [(33.94, 5.61), (0.02, 1.00)]]  # 9 goal

def single_goal(pose):
    """
    ______________________________________________________________________________________________
    3. Function: Cycle Through Goal States
    ______________________________________________________________________________________________

    Within this function, the execution of each GoalPoint takes place. As referenced with the
    variable 'move', which has been assigned as setting MoveBaseGoals, the goals are sent to the
    'map' frame. The current planned path can be seen in Rviz, which has a custom configuration
    tailored for robot navigation.

    """
    move = MoveBaseGoal()
    move.target_pose.header.frame_id = 'map'
    move.target_pose.pose.position.x = pose[0][0]       # point x
    move.target_pose.pose.position.y = pose[0][1]       # point y
    move.target_pose.pose.position.z = 0.0              # point z (fixed at 0.0)
    move.target_pose.pose.orientation.x = 0.0           # quaternion x (qx, fixed at 0.0)
    move.target_pose.pose.orientation.y = 0.0           # quaternion y (qx, fixed at 0.0)
    move.target_pose.pose.orientation.z = pose[1][0]    # quaternion z (qz)
    move.target_pose.pose.orientation.w = pose[1][1]    # quaternion w (qw)

    return move # return the current 'move'/ MoveBaseGoal

    rospy.spin() # execute until CTRL + C

    # (packtBhagyashree, 2017)
    # (Fairchild and Harman, 2017, 189-191)


if __name__ == '__main__':
    """
    ______________________________________________________________________________________________
    4. Execution
    ______________________________________________________________________________________________

    The node is initilised below as 'autonomy' and the action library client (SimpleActionClient).
    Arguements to action any MoveBaseGoals are set, to be sent via the move_base topic.
    Below that, a response is waited for by the action server. While the node it initialised,
    the position and orientation in GoalPoints will be accessed and send to the client.
    the result is then anticipated and acknowledged when complete.

    """

    rospy.init_node('go_to_goal') # intialise node: go_to_goal

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction) # broadcast actions
    client.wait_for_server() # listen for actions

    while True:
        for pose in GoalPoints:         # select from the above array
            goal = single_goal(pose)    # call for the pose from the function auto_pure
            client.send_goal(goal)      # send the goal to the action client
            client.wait_for_result()    # await the result from the action server

    # (Quigley et al., 2015, 161-163)

"""
__________________________________________________________________________________________________
References
__________________________________________________________________________________________________

NicolasVaras (2018) move_base. ROS Wiki: Open Robotics. Available from
http://wiki.ros.org/move_base [accessed 15 April 2020].

IsaacSaito (2018) actionlib. ROS Wiki: Open Robotics. Available from
http://wiki.ros.org/actionlib [accessed 15 April 2020].

Ferguson, M. (2019) move_base_msgs. ROS Wiki: Open Robotics. Available from
http://wiki.ros.org/move_base_msgs [accessed 15 April 2020].

packtBhagyashree (2017) Chapter04. Github: PacktPublishing. Available from
https://github.com/PacktPublishing/ROS-Robotics-By-Example-Second-Edition/tree/master/Chapter04
[accessed 15 April 2020].

Fairchild, C. and Harman, T.L. (2017) Ros Robotics By Example, 2nd Edition.
Birmingham, UK: Packt Publishing Ltd.

Quigley, M., Gerkey, B. and Smart, W.D. (2015) Programming Robots with ROS.
Sebastopol, USA: O'Reilly Media, Inc.

"""