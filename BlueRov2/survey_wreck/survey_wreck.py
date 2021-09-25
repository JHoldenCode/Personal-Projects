#!/usr/bin/env python

import rospy
import math
import message_filters
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from uuv_control_msgs.msg import TrajectoryPoint
from point import Point

survey_grid = []

curr_angle = 0
goal_angle = 0
pose_x = -64
pose_y = -25
pose_z = -60
goal_x = -16
goal_y = -25
final_x = -16
final_y = -57
#square from (-64, -25) to (-16, -57)
#cell size of ~1x2



def refine_grid():
    global survey_grid

    refined_grid = []

    for i in survey_grid:
        if i.z > -78:
            refined_grid.append(i)

    return refined_grid



def sonar_callback(sonar0, sonar2):
    global survey_grid
    global goal_angle
    global pose_y
    global goal_x
    global goal_y


    pub = rospy.Publisher('/rexrov2/cmd_vel', Twist, queue_size=10)
    vel = Twist()

    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.z = 0

    #for while True loop
    i = 0


    if not (curr_angle > goal_angle - .1 and curr_angle < goal_angle + .1):
        rospy.loginfo('twist for: ' + str(goal_angle) + ' current: ' + str(curr_angle))
        if goal_angle - curr_angle > 0:
            vel.angular.z = .25
        else:
            vel.angular.z = -.25
        vel.linear.x = 0
        vel.linear.y = 0
        vel.linear.z = 0
    else:
        #if within goal pose
        if pose_x > goal_x - 1.5 and pose_x < goal_x + 1.5 and pose_y > goal_y - 1.5 and pose_y < goal_y + 1.5:
            rospy.logerr('done')
            vel.linear.x = 0
            vel.linear.y = 0
            vel.linear.z = 0
            vel.angular.z = 0
            if goal_x == final_x and goal_y == final_y:
                rospy.logfatal('congrats')
                for dot in survey_grid:
                    dot.display_point()
                print('**************')
                refined_grid = refine_grid()
                for dot_refined in refined_grid:
                        dot_refined.display_point()
                print('-------------')
                while True:
                    i = i + 1
            else:
                #logic for where next goal is
                if pose_x > -25:
                    if (-goal_y - 1) % 4 == 0: 
                        goal_y = goal_y - 2
                    else:
                        goal_x = -64
                else:
                    if (-goal_y - 1) % 4 == 0:
                        goal_x = -16 
                    else:
                        goal_y = goal_y - 2
                        
                rospy.logerr('Next goal: ' + str(goal_x) + ', ' + str(goal_y))
        else:
            #move
            vel.linear.x = 3

        #gather data
        if pose_x % 1 < 0.075 and pose_x > -62 and pose_x < -18:
            rospy.loginfo('node: ' + str(int(pose_x)))
            #change to equal point on map instead of sonar range
            if pose_x <= -39:
                orientation = 0
                if goal_x > -39:
                    rospy.loginfo('USING FRONT SONAR')
                    survey_grid.append(Point(pose_x, pose_y, pose_z, sonar0.range, math.pi / 6, orientation))
                else:
                    rospy.loginfo('USING BACK SONAR')
                    survey_grid.append(Point(pose_x, pose_y, pose_z, sonar2.range, math.pi / 6, orientation))
            else:
                orientation = 3.14
                if goal_x <= -39:
                    rospy.loginfo('USING FRONT SONAR')
                    survey_grid.append(Point(pose_x, pose_y, pose_z, sonar0.range, math.pi / 6, orientation))
                else:
                    rospy.loginfo('USING BACK SONAR')
                    survey_grid.append(Point(pose_x, pose_y, pose_z, sonar2.range, math.pi / 6, orientation))
            
        #sink
        if pose_z > -58:
            #rospy.logfatal('sink')
            vel.linear.z = -2
        elif pose_z < -62:
            #rospy.logfatal('sink')
            vel.linear.z = 2
    
        
    pub.publish(vel)




def pose_callback(pose):
    global goal_angle
    global curr_angle
    global pose_x
    global pose_y
    global pose_z

    pose_x = pose.pose.position.x
    pose_y = pose.pose.position.y
    pose_z = pose.pose.position.z

    t3 = 2.0 * (pose.pose.orientation.w * pose.pose.orientation.z + pose.pose.orientation.x * pose.pose.orientation.y)
    t4 = 1.0 - 2.0 * (pose.pose.orientation.y * pose.pose.orientation.y + pose.pose.orientation.z * pose.pose.orientation.z)
    curr_angle = math.atan2(t3, t4)

    x_dist = goal_x - pose_x
    y_dist = goal_y - pose_y

    if x_dist < 1 and x_dist > -1:
        if y_dist > 1:
            goal_angle = 1.57
        elif y_dist < 1:
            goal_angle = -1.57
    elif y_dist < 1 and y_dist > -1:
        if x_dist > 1:
            goal_angle = 0
        elif x_dist < 1:
            goal_angle = 3.14
    elif x_dist >= 0 and y_dist >= 0:
        goal_angle = math.atan(y_dist / x_dist)
    elif x_dist < 0 and y_dist >= 0:
        goal_angle = 3.14 - math.atan(y_dist / (-x_dist))
    elif x_dist < 0 and y_dist < 0:
        goal_angle = -1 * (3.14 - math.atan((-y_dist) / (-x_dist)))
    else:
        goal_angle = -1 * math.atan((-y_dist) / x_dist)
    

    #rospy.loginfo(x_dist)
    #rospy.loginfo(y_dist)
    #rospy.loginfo(goal_angle)
    #rospy.loginfo(curr_angle)


    #fix 2nd and 3rd quadrant turn
    if (curr_angle > 1.57 or curr_angle < -1.52) and (goal_angle > 1.57 or goal_angle < -1.52):
        if curr_angle < -1.52:
            curr_angle = curr_angle + 6.28
        if goal_angle < -1.52:
            goal_angle = goal_angle + 6.28




def survey():
    rospy.init_node('survey', anonymous=True)

    rospy.Subscriber('/rexrov2/dp_controller/reference', TrajectoryPoint, pose_callback)

    sonar0 = message_filters.Subscriber('/rexrov2/dvl_sonar0', Range)
    sonar2 = message_filters.Subscriber('/rexrov2/dvl_sonar2', Range)

    ts = message_filters.TimeSynchronizer([sonar0, sonar2], 10)
    ts.registerCallback(sonar_callback)

    rospy.spin()




if __name__ == '__main__':
    try:
        survey()
    except rospy.ROSInterruptException:
        pass
