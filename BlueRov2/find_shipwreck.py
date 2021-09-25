#!/usr/bin/env python

#Rexrov placed in random spot told ship is somewhere in front of it
#up to 50 meters in front and 50 meters to the right

import rospy
import math
import message_filters
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from uuv_control_msgs.msg import TrajectoryPoint
from point import Point

#pose values
goal_angle = None
curr_angle = None

pose_x = None
pose_y = None
pose_z = None

#whether traveling to the right means positive or negative
travel_direction_positive = None

goal_x = None
goal_y = None
goal_z = None

lower_x = None
upper_x = None
lower_y = None
upper_y = None


#when trying to get left/right sonar onto ship
not_checked_behind = True
move_back_and_forth = 0
moving_forward = True


#ships dimensions
ship_x_length = 10.6858320413
ship_y_length = 22.5559060462
ship_height = 9.8181664295

#initial ship values
initial_ship_sonar_distance = None
ship_found = False
need_to_calculate_goal_angle = True

#ship measurements
left_side_of_boat = None
right_side_of_boat = None

tasks_completed = 0


def sonar_callback(sonar_front, sonar_left, sonar_back, sonar_right):
    global goal_x
    global goal_y
    global goal_z

    global goal_angle
    
    global move_back_and_forth
    global moving_forward

    global left_side_of_boat
    
    global initial_ship_sonar_distance
    global tasks_completed

    global ship_found
    global need_to_calculate_goal_angle

    global not_checked_behind

    pub = rospy.Publisher('/rexrov2/cmd_vel', Twist, queue_size=10)
    vel = Twist()

    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.z = 0


    #initialize sonar readings
    if initial_ship_sonar_distance == None:
        sonar_list = [sonar_front.range, sonar_left.range, sonar_back.range, sonar_right.range]
        initial_ship_sonar_distance = max(sonar_list)



    #determine if ship is in sights
    if not ship_found:
        initial_ship_contact = None

        x_adjustment = 0
        y_adjustment = 0

        #figure out which way each sonar is pointing
        if lower_x != None:
            if goal_x == lower_x:
                orientation = (3.14, -1.57, 0, 1.57)
            else:
                orientation = (0, 1.57, 3.14, -1.57)
        else:
            if goal_y == lower_y:                                                          
                orientation = (-1.57, 0, 1.57, 3.14)
            else:
                orientation = (1.57, 3.14, -1.57, 0)

        #if the front sonar sees ship
        if sonar_front.range < initial_ship_sonar_distance - 1.5:
            #establish where the point of contact is based on current orientation
            initial_ship_contact = Point(pose_x, pose_y, pose_z, sonar_front.range, math.pi / 6, orientation[0])
            current_orientation = orientation[0]
        elif sonar_left.range < initial_ship_sonar_distance - 1.5:
            initial_ship_contact = Point(pose_x, pose_y, pose_z, sonar_left.range, math.pi / 6, orientation[1])
            current_orientation = orientation[1]
        elif sonar_back.range < initial_ship_sonar_distance - 1.5:
            initial_ship_contact = Point(pose_x, pose_y, pose_z, sonar_back.range, math.pi / 6, orientation[2])
            current_orientation = orientation[2]
        elif sonar_right.range < initial_ship_sonar_distance - 1.5:
            initial_ship_contact = Point(pose_x, pose_y, pose_z, sonar_right.range, math.pi / 6, orientation[3])
            current_orientation = orientation[3]
        if initial_ship_contact != None:
            #make adjustments based off current orientation
            if current_orientation == 0:
                x_adjustment = 1.5
            elif current_orientation == 1.57:
                y_adjustment = 1.5
            elif current_orientation == 3.14:
                x_adjustment = -1.5
            elif current_orientation == -1.57:
                y_adjustment = -1.5
            goal_x = initial_ship_contact.x + x_adjustment
            goal_y = initial_ship_contact.y + y_adjustment
            goal_z = ship_height + 3 - 78
            rospy.logerr('SHIP FOUND!!')
            rospy.logerr('Traveling to: ' + str(goal_x) + ', ' + str(goal_y) + ', ' + str(goal_z))
            ship_found = True




    #main movement conditions for boustrephodon search pattern

    #sink
    if pose_z > goal_z + .2:
        #rospy.logfatal('sink')
        vel.linear.z = -2
    elif pose_z < goal_z - .2:
        #rospy.logfatal('sink')
        vel.linear.z = 2

    if not (curr_angle > goal_angle - .1 and curr_angle < goal_angle + .1):
        #rospy.loginfo('twist for: ' + str(goal_angle) + ' current: ' + str(curr_angle))
        if goal_angle - curr_angle > 0:
            vel.angular.z = .25
        else:
            vel.angular.z = -.25
        vel.linear.x = 0
        vel.linear.y = 0
    elif not ship_found:
        #if within goal pose
        if pose_x > goal_x - 1.5 and pose_x < goal_x + 1.5 and pose_y > goal_y - 1.5 and pose_y < goal_y + 1.5 and pose_z > goal_z - .2 and pose_z < goal_z + .2:
            rospy.logerr('done')
            vel.linear.x = 0
            vel.linear.y = 0
            vel.linear.z = 0
            vel.angular.z = 0

            if ship_found:
                at_ship = True

            #logic for where next goal is
            if lower_x != None:
                if goal_x == lower_x:
                    goal_x = upper_x
                else:
                    goal_x = lower_x
                if travel_direction_positive == True:
                    goal_y += 10
                else:
                    goal_y -= 10
            else:
                if goal_y == lower_y:
                    goal_y = upper_y
                else:
                    goal_y = lower_y
                if travel_direction_positive == True:
                    goal_x += 10
                else:
                    goal_x -= 10

            rospy.logerr('Next goal: ' + str(goal_x) + ', ' + str(goal_y))

        else:
            #move
            vel.linear.x = 3

    #once ship has been located start doing tasks
    else:
        #This is how to calculate what the sonar "should" read with nothing in the way
        #((pose_z - (-78)) / math.cos(math.pi / 6)) - 1

        #task 0: get to ship
        if tasks_completed == 0:
            vel.linear.x = 3
            if pose_x > goal_x - .5 and pose_x < goal_x + .5 and pose_y > goal_y - 1.5 and pose_y < goal_y + 1.5 and pose_z > goal_z - .2 and pose_z < goal_z + .2:
                rospy.loginfo("Task 0 completed. Reached initial boat contact point, twisting to 3.14")
                vel.linear.x = 0
                tasks_completed += 1
        #task 1: turn toward the west
        elif tasks_completed == 1:
            need_to_calculate_goal_angle = False
            goal_angle = 3.14
            tasks_completed += 1
        #task 2: move all the way to the left
        elif tasks_completed == 2:
            vel.linear.y = 3
            if left_side_of_boat == None:
                left_side_of_boat = pose_y
            if sonar_left.range < ((pose_z - (-78)) / math.cos(math.pi / 6)) - 1:
                if pose_y < left_side_of_boat:
                    left_side_of_boat = pose_y
                    rospy.loginfo('Left side of boat now: ' + str(left_side_of_boat))
                move_back_and_forth = 0
                if pose_x < goal_x - 3:
                    moving_forward = False
                if pose_x > goal_x + 3:
                    moving_forward = True
                if moving_forward:
                    vel.linear.x = 1.5
                else:
                    vel.linear.x = -1.5
            #stops seeing left
            else:
                if move_back_and_forth >= 2:
                    rospy.loginfo('Task 2 completed. Reached left point of ship: ' + str(left_side_of_boat))
                    vel.linear.y = 0
                    vel.linear.x = 0
                    tasks_completed += 1
                    goal_x = pose_x + 25
                    goal_y = left_side_of_boat + 6
                    rospy.loginfo("Traveling to: " + str(goal_x) + ',  ' + str(goal_y))
                if pose_x < goal_x - 3:
                    if moving_forward == True:
                        move_back_and_forth += 1
                        rospy.loginfo('Moved forward, checked ' + str(move_back_and_forth) + ' side(s)')
                    moving_forward = False
                elif pose_x > goal_x + 3:
                    if moving_forward == False:
                        move_back_and_forth += 1
                        rospy.loginfo('Moved back, checked ' + str(move_back_and_forth) + ' side(s)')
                    moving_forward = True
                if moving_forward:
                    vel.linear.x = 1.5
                else:
                    vel.linear.x = -1.5
        #move to the final location based on data gathered about boats location
        elif tasks_completed == 3:
            need_to_calculate_goal_angle = True
            vel.linear.x = 3
            if pose_x > goal_x - 1.5 and pose_x < goal_x + 1.5 and pose_y > goal_y - 1.5 and pose_y < goal_y + 1.5:
                need_to_calculate_goal_angle = False
                goal_angle = 3.14
                goal_z = -76
                rospy.logerr('Task 3 completed. In Final Place')
                tasks_completed += 1





    pub.publish(vel)




def pose_callback(pose):
    global goal_angle
    global curr_angle

    global pose_x
    global pose_y
    global pose_z

    global travel_direction_positive

    global goal_x
    global goal_y
    global goal_z

    global lower_x
    global upper_x
    global lower_y
    global upper_y

    pose_x = pose.pose.position.x
    pose_y = pose.pose.position.y
    pose_z = pose.pose.position.z

    t3 = 2.0 * (pose.pose.orientation.w * pose.pose.orientation.z + pose.pose.orientation.x * pose.pose.orientation.y)
    t4 = 1.0 - 2.0 * (pose.pose.orientation.y * pose.pose.orientation.y + pose.pose.orientation.z * pose.pose.orientation.z)
    curr_angle = math.atan2(t3, t4)

    if goal_x == None:
        goal_z = pose_z

        #set up direction of travel
        if (curr_angle > 1.47 and curr_angle < 1.67) or curr_angle > 3 or curr_angle < -3:
            travel_direction_positive = True
        else:
            travel_direction_positive = False

        #set up bounds for search area
        if (curr_angle > 1.47 and curr_angle < 1.67) or (curr_angle > -1.67 and curr_angle < -1.47):
            goal_x = pose_x
            if curr_angle > 1.47 and curr_angle < 1.67:
                goal_y = pose_y + 50
                lower_y = pose_y
                upper_y = goal_y
            else:
                goal_y = pose_y - 50
                lower_y = goal_y
                upper_y = pose_y
        else:
            goal_y = pose_y
            if curr_angle > -.5 and curr_angle < .5:
                goal_x = pose_x + 50
                lower_x = pose_x
                upper_x = goal_x
            else:
                goal_x = pose_x - 50
                lower_x = goal_x
                upper_x = pose_x

    x_dist = goal_x - pose_x
    y_dist = goal_y - pose_y


    if need_to_calculate_goal_angle:
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





def find():
    rospy.init_node('find_shipwreck', anonymous=True)

    rospy.Subscriber('/rexrov2/dp_controller/reference', TrajectoryPoint, pose_callback)

    sonar0 = message_filters.Subscriber('/rexrov2/dvl_sonar0', Range)
    sonar1 = message_filters.Subscriber('/rexrov2/dvl_sonar1', Range)
    sonar2 = message_filters.Subscriber('/rexrov2/dvl_sonar2', Range)
    sonar3 = message_filters.Subscriber('/rexrov2/dvl_sonar3', Range)

    ts = message_filters.TimeSynchronizer([sonar0, sonar1, sonar2, sonar3], 10)
    ts.registerCallback(sonar_callback)

    rospy.spin()




if __name__ == '__main__':
    try:
        find()
    except rospy.ROSInterruptException:
        pass

