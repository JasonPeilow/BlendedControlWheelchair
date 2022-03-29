#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__________________________________________________________________________________________________
Brief Description
__________________________________________________________________________________________________

This is the sole teloperation script, which is used for study_a and study_c (Blended Control).
There is basic speed selection and forward / rotation functionality. The input source for these
control methods is a wired Xbox 360 Controller.
__________________________________________________________________________________________________
1. Imported Clients and Packages
__________________________________________________________________________________________________

rospy is the client library for ros python. The action library provides the ability to broadcast
and listen for goals from the action server/client. These goals are set using the
MoveBaseGoal library and are then communicated to the action server using MoveBaseAciton. This
is passed as an arguement through the SimpleActionClient from the actionlib library.
"""

import rospy

from geometry_msgs.msg import Twist     # (ROS.org, 2014)
from sensor_msgs.msg import Joy         # (ROS.org, 2019)
#from sensor_msgs.msg import LaserScan  # (ROS.org, 2019)


class Teleoperation:
    def __init__(self):
        """
        __________________________________________________________________________________________
        2. The Teleoperation Class
        __________________________________________________________________________________________

        The node is initialised as 'teleop_pure' which is what this consists of: only teleop.
        There is no autonomous travel within this script, but there is some simple object detect
        functions for information purposes only. This is in the form of a simple laser scan in the
        local vicinity. This can be noted in the 'scan_callback' and LaserScan subscriber. One
        other subsciber, also part of the sensor_msgs package, would be Joy. This will enable
        input from an xbox controller and publish the commands as twist messages for the robot
        to act upon. mps / metres per second is set at zero, with the option to alter speed by
        increments of 25%. This can reach a maximum of 2 metres per second (4 miles per hour),
        which is the max speed of the Jazzy 6 wheelchair. The rotation of the robot is set at
        1 radian per second, which is also the maximum rotation speed of the Jazzy 6. This means
        the robot would take 3 seconds to perform a 180 degree (approx) turn. Finally, variables
        have been set for the vertical and horizontal functionality of the xbox left thumbstick.

        """
        # (ROS.org, 2019)

        rospy.init_node("teleop_pure") # initialise the teleop node

        self.pub_teleop = rospy.Publisher("base_controller/command", Twist, queue_size=10) # publish twist msgs
        self.sub_teleop = rospy.Subscriber("joy", Joy, self.teleop_callback) # subscribe to joy
        #self.sub_lasers = rospy.Subscriber("scan", LaserScan, self.scan_callback)

        rate = rospy.Rate(50)   # move this?

        self.mps = 0.0          # metres per second
        self.rad = 1.0          # radians per second

        self.left_vert = 1      # set 1 for vertical movement on left Xbox joystick
        self.left_hrzn = 0      # set 0 for horizontal movement on left Xbox joystick

        self.twist = Twist()    # create an object to pass twist messages

        rate.sleep()
        rospy.spin()

    def teleop_callback(self, control):
        """
        __________________________________________________________________________________________
        3. Commanding Velocity and Speed Selection
        __________________________________________________________________________________________

        Simple teleoperation functionality. The left thumbstick enables the usage of forward and
        rotational velocities to the robot and provides functionality to 6 of the xbox buttons.
        The four 'letter' based buttons (A, B, X and Y) are used to select 1 of 4 speed settings.
        It is understood that the Jazzy 6 has ten speed settings, but that is not convinient for
        the controller layout and may prove an uneccessary distraction for users. Other than
        these speed settings, the 'shoulder' or 'bumper' buttons, LB and RB, provide a braking
        mechanism for the robot.

        """
        if control.buttons[3]: # Xbox Control Button: Y
            self.mps = 2.0
            print("Speed setting 100%")

        elif control.buttons[2]: # Xbox Control Button: X
            self.mps = 1.5
            print("Speed setting 75% ")

        elif control.buttons[1]: # Xbox Control Button: B
            self.mps = 1.0
            print("Speed setting 50%")

        elif control.buttons[0]: # Xbox Control Button: A
            self.mps = 0.5
            print("Speed setting 25%")

        if control.buttons[4] or control.buttons[5]: # Xbox Shouler Bumpers: Left[4] & Right [5]
            self.mps = 0.0
            print("Regenerative Brake: Active")

        self.twist.linear.x = control.axes[self.left_vert] * self.mps   # forward velocity
        self.twist.angular.z = control.axes[self.left_hrzn] * self.rad  # rotate robot at 1 rps

        self.pub_teleop.publish(self.twist)

        # (Fairchild and Harman, 2017, 355-366)


        """
        def scan_callback(self, detect):
            __________________________________________________________________________________________________
            4. Environment Scan
            __________________________________________________________________________________________________

            These laser msgs do not inform the robot to use any obstacle avoidance in a reactive sense etc and
            are, more, for the benefit of the user. This is just to inform them, by simple message, that the
            powered wheelchair is nearing an object or is very close to colliding with something.

            if detect.ranges[40] < 1.5:
                print(detect)
                rospy.loginfo('LEFT: Nearing object...')
            if detect.ranges[40] < 0.3:
                print(detect)
                rospy.loginfo('LEFT: COLLISION!!!')
            if detect.ranges[229] > 1.5:
                print(detect)
                rospy.loginfo('FRONT: Nearing object...')
            if detect.ranges[229] > 0.3:
                print(detect)
                rospy.loginfo('FRONT: COLLISION!!!')
            if detect.ranges[599] > 1.5:
                print(detect)
                rospy.loginfo('RIGHT: Nearing object...')
            if detect.ranges[599] > 0.3:
                print(detect)
                rospy.loginfo('RIGHT: COLLISION!!!')

            # (The Construct, 2017)
            # (RISC Labs, 2018)
            # (riskhaust, 2018)

       """


if __name__ == '__main__':
    """
    ______________________________________________________________________________________________
    5. Execution
    ______________________________________________________________________________________________

    Simple execution, which is slightly different to ROS spin, but has the same general function.
    The class 'Teleoperation' will continue to be executed until an interupt (CTRL + C) is used.
    Some basic commands print to the log to indicate the 'start' and 'end' of the process.

    """
    try:
        rospy.loginfo('Start Teleoperation...')
        Teleoperation()
    except rospy.ROSInterruptException:
        rospy.loginfo('End Teleoperation...')


"""
__________________________________________________________________________________________________
References
__________________________________________________________________________________________________

GvdHoorn (2019) joy. ROS Wiki. Open Robotics. Available from
http://wiki.ros.org/joy [accessed 15 April 2020].

ROS.org (2014) geometry_msgs. ROS Wiki. Open Robotics. Available from
http://wiki.ros.org/geometry_msgs [accessed 15 April 2020].

Fairchild, C. and Harman, T.L. (2017) Ros Robotics By Example, 2nd Edition.
Birmingham, UK: Packt Publishing Ltd.

Packt Publishing (2017) Turtlesim_joy_code. PacktPublishing. Available from
https://github.com/PacktPublishing/ROS-Robotics-By-Example-Second-Edition/tree/master/Chapter08/
Turtlesim_joy_code [accessed 15 April 2020].

The Construct (2017) [ROS Q&A] 031 – How to read LaserScan data (ROS python). Alberto Ezquerro.
Available from http://www.theconstructsim.com/read-laserscan-data/ [accessed 15 April 2020].

Mohamed Abdelkader (2018) ROS Basics. RISC Labs. Available from
https://risc.readthedocs.io/1-ros-basics.html [accessed 15 April 2020].

Kuat Telegenov (2018) ros-basics. risckaust. Available from
https://github.com/risckaust/risc-documentations/blob/master/src/ros-basics/mini_project.py
[accessed 15 April 2020].

"""