#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__________________________________________________________________________________________________
Brief Description
__________________________________________________________________________________________________

a

__________________________________________________________________________________________________
1. Imported Clients and Packages
__________________________________________________________________________________________________

a

"""

import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import Joy


class RoomSelect():
    """
    ______________________________________________________________________________________________
    2. The RoomSelect Class
    ______________________________________________________________________________________________

    a

    """
    def __init__(self):

        rospy.init_node('autonomy', anonymous=True)

        self.location = False

        self.living = Pose(Point(-1.736, 2.491, 0.000), Quaternion(0.000, 0.000, 0.223, 7.831))
        self.kitchen = Pose(Point(-4.294, 2.700, 0.000), Quaternion(0.000, 0.000, 0.223, 7.831))
        self.bedroom = Pose(Point(-4.764, 5.975, 0.000), Quaternion(0.000, 0.000, 0.223, 7.831))
        self.bathroom = Pose(Point(-1.965,-1.313, 0.000), Quaternion(0.000, 0.000, 0.223, 7.831))

        self.sub_teleop = rospy.Subscriber("joy", Joy, self.select_room)
        # (GvdHoorn, 2020)
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(60))
        # (IsaacSaito, 2018), (NicolasVaras, 2018)

    def select_room(self, control):
        """
        __________________________________________________________________________________________
        3. Room Selection via Xbox Controller
        __________________________________________________________________________________________

        a

        """
        if control.buttons[3]:
            location = self.living
            print("Living")
        elif control.buttons[2]:
            location = self.kitchen
            print("Kitch")
        elif control.buttons[1]:
            location = self.bedroom
            print("Bed")
        elif control.buttons[0]:
            location = self.bathroom
            print("Bath")
        if control.buttons[4] or control.buttons[5]:
            self.move_base.cancel_goal()
            print("Cancel")

        # Set up the next goal location
        goal = MoveBaseGoal()
        goal.target_pose.pose = location
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()

        # Let the user know where the robot is going next
        rospy.loginfo("Going to: ")

        # Start the robot toward the next location
        move_base.send_goal(goal)

        # Allow 5 minutes to get there
        finished_within_time = move_base.wait_for_result(rospy.Duration(300))

        # Check for success or failure
        if not finished_within_time:
            move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal succeeded!")
            else:
                rospy.loginfo("Goal failed...")

        # (Goebel, 2014)
        # (Goebel, 2012, 89-121)


if __name__ == '__main__':
    """
    ______________________________________________________________________________________________
    4. Execution
    ______________________________________________________________________________________________

    """

    try:
        RoomSelect()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")

#

"""
__________________________________________________________________________________________________
References
__________________________________________________________________________________________________

IsaacSaito (2018) actionlib. ROS Wiki: Open Robotics. Available from
http://wiki.ros.org/actionlib [accessed 15 April 2020].

GvdHoorn (2020) joy. ROS Wiki. Open Robotics. Available from
http://wiki.ros.org/joy [accessed 15 April 2020].

NicolasVaras (2018) move_base. ROS Wiki: Open Robotics. Available from
http://wiki.ros.org/move_base [accessed 15 April 2020].

Ferguson, M. (2019) move_base_msgs. ROS Wiki: Open Robotics. Available from
http://wiki.ros.org/move_base_msgs [accessed 15 April 2020].

Goebel R,P. (2014) rbx1/nav_test.py. Github: pirobot. Available from
https://github.com/pirobot/rbx1/blob/indigo-devel/rbx1_nav/nodes/nav_test.py
[accessed 18 April 2020].

Goebel R,P. (2012) ROS by Example: A Do-It-Yourself Guide To The Robot Operating System, Volume 1.
Stanford, USA: Pi Robot.

"""