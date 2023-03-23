# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 15:05:52 2022

@author: Akshay Baghmar
"""

import sys_parameters as para
import Modules_Project as mod
import numpy as np
import Users_Module as user
import time

start = time.time()

#==================================================================================
#Macro cell
#==================================================================================
num_channel_Active_macro = 0
num_call_attempt_macro = 0
num_call_established_success_macro = 0
num_success_call_macro = 0
num_success_handoff_out_Macro = 0
num_success_handoff_into_Macro = 0
num_potential_handoff_macro = 0
num_handoff_attempt_macro = 0
num_fail_handoff_into_Macro = 0
num_fail_handoff_out_Macro = 0
num_call_drop_low_sgnl_Macro = 0
num_call_blocked_capacity_macro = 0
num_call_drop_capacity_macro = 0
num_traffic_channel_macro = para.tchnl_macro
num_success_handoff_macro = 0
#=================================================================================
#Small Cell stats
#=================================================================================
num_channel_Active_small = 0
num_call_attempt_small = 0
num_call_established_success_small = 0
num_success_call_small = 0
num_success_handoff_out_small = 0
num_success_handoff_into_small = 0
num_potential_handoff_small = 0
num_handoff_attempt_small = 0
num_fail_handoff_into_Small = 0
num_fail_handoff_out_Small = 0
num_call_drop_low_sgnl_small = 0
num_call_drop_capacity_small = 0
num_call_blocked_capacity_small = 0
num_traffic_channel_small = para.tchnl_small

# Probability of making a call
probability = (para.call_rate * para.delta_time)

value = int(input("Enter total simulation time (in Hours) : "))
if value > 0:
    # Converting Hours to Seconds
    Ttotal = int(value * 3600)
else:
    print("Please enter positive values....!!!")
#print("Ttotal Set")

value = int(input("Enter number of users on Road : "))
NumUsersRoad = value
while value <= 0:
    value = int(
        input("Inavlid value. Try again,Please enter positive user Park values : "))
    NumUsersRoad = value
    
value = int(input("Enter number of users on Park : "))
NumUsersPark = value
while value <= 0 :
    value = int(input("Inavlid value. Try again,Please enter positive user Park values : "))
    NumUsersRoad = value
#print("Num user set")

# ==============================================================================
# Taking EIRP Macro cell details
# ==============================================================================
value = int(input("Enter EIRP for Marco cell : "))
EIRP_macro = value

value = int(input("Enter EIRP for Small cell : "))
EIRP_small = value
#print("EIRP set")
#====================================================================================
#Making User data base to store user details,will utilise to refer to UserId in main loop
#====================================================================================
userdata_park = []
ActiveUser_Park = []
InactiveUser_Park = []
ArchiveUser_Park = []
# First we will add all users as inactive and then check for calling users for that instance
for i in range (0,NumUsersPark):
    temp_user = user.user(i,0,0,0,para.P_user_speed)
    userdata_park.append(temp_user)
    InactiveUser_Park.append(i)
#print("Park User data is set") # For verification only
#print(userdata_park[6].x,userdata_park[6].y,userdata_park[6].angle)

# ==============================================================================
# Initializing data base for simulations
# ==============================================================================
# Making User data base to store user details,will utilise to refer to UserId in main loop
userdata_road = []
# As stated we need to track active , inactive calls and once call done add in archieve , Making a dict to track this
ActiveUser_Road = []
InactiveUser_Road = []
ArchiveUser_Road = []
# Making user details based on Number of road user inputs
# First we will add all users as inactive/add their details and then check for calling users for that instance
for i in range(0, NumUsersRoad):
    temp_user = user.user(i, 0, 0, 0, para.R_user_speed)
    userdata_road.append(temp_user)
    InactiveUser_Road.append(i)
#=================================================================================================
#simulation start
#=================================================================================================
for counter in range((Ttotal//para.delta_time)+1):
    # making a list of callers to tracker, it will get refreshed every iteration 
    caller_list = [] #For road
    #When simulation start First second (+1 second next) 
    #we will take care of active user, as we can calulcate updated x,y,angle and timer
    for userid in ActiveUser_Road:
        user_road = userdata_road[userid]
        #og_user_road_x = user_road.getx()
        serving_cell = user_road.getservingstation()
        updated_road_x = mod.updateposition_road(user_road,para.delta_time)
        #print("FOr user :",userid,"Original x was",og_user_road_x,"and updated x is",updated_road_x)
        user_road.updatelocation(updated_road_x, 0, 0) #updating the user location on road , # y and angle = 0 for road user
        #print("Updated x for user:",userid)
        active_calltime = user_road.getcalltimer() #getting call time
        #print("User id:",userid,"call time is:",active_calltime)
        update_calltime = active_calltime - para.delta_time #updating the call time
        user_road.setcalltimer(update_calltime)
        #print("User id:",userid,"updated call time is:",update_calltime)
        active_calltime = user_road.getcalltimer() #getting updated call time
        user_road_x = user_road.getx() # getting the updated road user details
        if active_calltime <= 0 or (user_road_x > 3000 or user_road_x < -3000):#Checking if user timer is done or out of area
            if serving_cell == 0: #means serving cell was macro cell
                #print("updating channel for Macro cell.line 248")
                num_traffic_channel_macro += 1 #Macro cell traffic is freed
                num_success_call_macro += 1 # updating the success call as mentioned in 2.b/c
            elif serving_cell == 1:
                num_traffic_channel_small += 1 # small cell traffic is freed
                #print("updating channel for small cell.line 248")
                num_success_call_small += 1 # updating the success call as mentioned in 2.b/c
            else:
                pass
            user_road.resetuser() #we need to reset the user data before moving to archive
            ActiveUser_Road.remove(userid) # Removing from active road user list
            ArchiveUser_Road.append(userid) # adding to active road user list
            
        else: #This means the call timer is active and user still on road
            #print("inside loop at line 253. Call still ongoing checking rsl for updated position")
            if serving_cell == 0: #Means server is Macro cell
                #print("Serving cell is 0 = Macro")
                rsl_server = mod.findRSL_Macro(user_road,para.bstn_M_x, para.bstn_M_y,EIRP_macro) 
                rsl_other = mod.findRSL_Small(user_road, para.bstn_S_x, para.bstn_S_y,EIRP_small)
                if rsl_server < para.ue_thres: #This means call is dropped
                    #print("RSL_Server < Threshold, call dropped")
                    num_call_drop_low_sgnl_Macro += 1 # updating call drop due to signal level
                    num_traffic_channel_macro += 1 # increasing channels in Macro cell
                    user_road.resetuser() #we need to reset the user data before moving to archive
                    ActiveUser_Road.remove(userid) # Removing from active road user list
                    ArchiveUser_Road.append(userid) # adding to active road user list
                else: #rsl_Server >= rsl threshold
                    #print("Server Macro RSL_Server >= RSL_threshold.line267")
                    if rsl_other > rsl_server + para.Hom:
                        #print("Inside loop at 269. rsl_other > rsl_server + para.Hom")
                        num_potential_handoff_macro += 1 # as mentioned an handoff attempt will be possible
                        if rsl_other >= para.RSLopt_small: # RSL_other means small cell so checking handover to small cell here
                            #print("inside loop 272. rsl_other >= para.RSLopt_small")
                            num_handoff_attempt_macro += 1
                            available_channel = num_traffic_channel_small # we will check the channel available in neighbor small cell
                            if available_channel > 0:
                                #print("inside loop 276. Channel available handing off to SMall cell")
                                updated_server = 1 
                                user_road.updateservingcell(updated_server) # we are setting small cell as new server for the user
                                num_traffic_channel_macro += 1
                                num_traffic_channel_small -= 1
                                num_success_handoff_out_Macro += 1
                                num_success_handoff_into_small += 1
                            else: # channel not available
                                num_fail_handoff_into_Small += 1
                                num_fail_handoff_out_Macro += 1
                            #end of this loop if available_channel > 0:
                        #end of this loop rsl_other >= para.RSLopt_small:
                    #end of this loop rsl_other > rsl_server + para.Hom
                #end of this loop sl_server < para.ue_thres:
                    
            elif serving_cell == 1: #serving cell is small cell
                #print("Serving cell is 1 = Small.line 288")
                rsl_server = mod.findRSL_Small(user_road, para.bstn_S_x, para.bstn_S_y, EIRP_small)
                rsl_other = mod.findRSL_Macro(user_road, para.bstn_M_x, para.bstn_M_y, EIRP_macro)
                if rsl_server < para.ue_thres: #This means call is dropped
                    #print("RSL_Server < Threshold, call dropped. line 292")
                    num_call_drop_low_sgnl_small += 1 # updating call drop due to signal level
                    num_traffic_channel_small += 1 # increasing channels in Macro cell
                    user_road.resetuser() #we need to reset the user data before moving to archive
                    ActiveUser_Road.remove(userid) # Removing from active road user list
                    ArchiveUser_Road.append(userid) # adding to active road user list
                elif rsl_server >= para.RSLopt_small:
                    #print("rsl_Server>=threshold. Hence passing handover steps.Line 299")
                    pass #No handover happens and pass the steps 
                else: #rsl_Server >= rsl threshold
                    #print("Inside loop 301. rsl_Server >= rsl threshold")
                    if rsl_other > rsl_server + para.Hom:
                        num_handoff_attempt_small += 1
                        available_channel = num_traffic_channel_macro # we check macro channel availabliltiy
                        if available_channel > 0: #Meaning Macro cell have channels to assign to this user
                            updated_server = 0 # chaning serving cell to 0 -> Macro cell
                            user_road.updateservingcell(updated_server)
                            num_traffic_channel_small += 1 #release small cell channel
                            num_traffic_channel_macro -= 1 #take Macro channel
                            num_success_handoff_out_small +=1
                            num_success_handoff_into_Macro +=1
                        else: #Channel is not available with Macro cell
                            num_fail_handoff_into_Macro +=1
                            num_fail_handoff_out_Small += 1
                        #end of this loop if available_channel > 0:
                    #end of this loop rsl_other >= para.RSLopt_small:
            #else:
            #    pass #end of this loop rsl_other > rsl_server + para.Hom
            #end of this loop sl_server < para.ue_thres:
        #end of this loop else: #This means the call timer is active and user still on road

    for userid in ActiveUser_Park:
        user_park = userdata_park[userid]
        serving_cell = user_park.getservingstation()
        active_calltime = user_park.getcalltimer()
        angle = user_park.getangle()
        updated_call_timer = active_calltime - para.delta_time
        user_park.updatetimer(updated_call_timer)
        updated_park_x = mod.updatepositionpark_x(user_park, para.delta_time)
        updated_park_y = mod.updatepositionpark_y(user_park, para.delta_time)
        updated_angle = mod.updateanglepark(updated_park_x, updated_park_y, angle)
        #print("UPdated angle:", updated_angle)
        #update user details for the users
        user_park.updatelocation(updated_park_x, updated_park_y, updated_angle)
        active_calltime = user_park.getcalltimer()
        if active_calltime < 0:
            #num_success_call += 1 # updating the success call as mentioned in 2.b/c
            if serving_cell == 0: #means serving cell was macro cell
                #print("updating channel for Macro cell.line 248")
                num_success_call_macro +=1
                num_traffic_channel_macro += 1 #Macro cell traffic is freed
            elif serving_cell == 1:
                num_traffic_channel_small += 1
                num_success_call_small += 1 # small cell traffic is freed
                #print("updating channel for small cell.line 248")
            #else:
            #    pass
            user_park.resetuser() #we need to reset the user data before moving to archive
            ActiveUser_Park.remove(userid) # Removing from active road user list
            ArchiveUser_Park.append(userid) # adding to active road user list
        else:#Means call is ongoing then we need to check other cases
            if serving_cell == 0:#this means serving cell is Macro
                rsl_server = mod.findRSL_Macro(user_park, para.bstn_M_x, para.bstn_M_y, EIRP_macro)
                rsl_other = mod.findRSL_Small(user_park, para.bstn_S_x, para.bstn_S_y, EIRP_small)
                if rsl_server < para.ue_thres: #call drop condition as stated in point d
                    num_call_drop_low_sgnl_Macro += 1
                    num_traffic_channel_macro += 1
                    user_park.resetuser() #we need to reset the user data before moving to archive
                    ActiveUser_Park.remove(userid) # Removing from active park user list
                    ArchiveUser_Park.append(userid) # adding to active road user list
                else:#rsl_Server >= rsl threshold
                    
                    if rsl_other > para.ue_thres + para.Hom: #potential handoff criteria
                        num_potential_handoff_macro += 1
                        if rsl_other >= para.RSLopt_small:
                            num_handoff_attempt_macro += 1 #handover is attempted now as rsl_other >= RSL_opt_small
                            available_channel = num_traffic_channel_small
                            if available_channel > 0:
                                updated_server = 1
                                user_park.updateservingcell(updated_server)
                                num_traffic_channel_macro += 1
                                num_traffic_channel_small -= 1
                                num_success_handoff_out_Macro += 1
                                num_success_handoff_into_small += 1
                            else:#handover fails, call will continue for next check next second
                                num_fail_handoff_into_Small += 1
                                num_fail_handoff_out_Macro += 1
                            #end of this loop if available_channel > 0:
                        #end of this loop rsl_other >= para.RSLopt_small:
                    #end of this loop rsl_other > rsl_server + para.Hom
                #end of this loop sl_server < para.ue_thres:
            
            elif serving_cell == 1: # that means serving cell is small cell
                rsl_server = mod.findRSL_Small(user_park, para.bstn_S_x, para.bstn_S_y, EIRP_small)
                rsl_other = mod.findRSL_Macro(user_park, para.bstn_M_x, para.bstn_M_y, EIRP_macro)
                if rsl_server < para.ue_thres: #This means call is dropped
                    num_call_drop_low_sgnl_small += 1 # updating call drop due to signal level
                    num_traffic_channel_small += 1 # increasing channels in small cell
                    user_park.resetuser()
                    user_park.resetuser() #we need to reset the user data before moving to archive
                    ActiveUser_Park.remove(userid) # Removing from active road user list
                    ArchiveUser_Park.append(userid) # adding to active road user list
                elif rsl_server >= para.RSLopt_small:
                    #print("rsl_Server>=threshold. Hence passing handover steps.Line 299")
                    pass #No handover happens and pass the steps
                else:#(removing elif rsl_server >= para.ue_thres:)
                    if rsl_other > rsl_server + para.Hom:
                        num_handoff_attempt_small += 1
                        available_channel = num_traffic_channel_macro # we check neighbor macro channel availabliltiy
                        if available_channel > 0:
                            #Means neighbor Macro cell have channel
                            updated_server = 0 # chaning serving cell to 0 -> Macro cell
                            user_park.updateservingcell(updated_server)
                            num_traffic_channel_small += 1 #release small cell channel
                            num_traffic_channel_macro -= 1 #take Macro channel
                            num_success_handoff_out_small +=1
                            num_success_handoff_into_Macro +=1
                        else: #Channel is not available with Macro cell
                            num_fail_handoff_into_Macro +=1
                            num_fail_handoff_out_Small += 1
                    #else:
                    #    pass
            #else:
            #    pass
            
    # ==================================================================================================================================
    # Calculating active users in Road for given second using the probability
    # ==================================================================================================================================
    for userid in InactiveUser_Road:
        user_road = userdata_road[userid]
        temp_callstatus = user_road.getcallstatus()
        temp_calltime = user_road.getcalltimer()
        n = np.random.uniform()
        if n < probability:
            # print(n) # For verification
            # temp_callstatus = 1 #0->Inactive,1->Active. So changing to 1 to mark active users in User data
            # user.setCallStatus(temp_callstatus)
            temp_x = np.random.uniform(-3000, 3000)
            user_road.updatelocation(temp_x, 0, 0)
            temp_calltime = np.random.exponential(para.call_duration_road)
            #print("Road call time generated is :",temp_calltime)
            user_road.setcalltimer(temp_calltime)
            #caller_list.append(userid)
            InactiveUser_Road.remove(userid)
            # print("Active list updated") #For verification
            # Making a temporary list for Active user:

        # for userid in ActiveUser_Road:
            #user_road = userdata_road[userid]
            # print("Userid",userid)
            rsl_macro = mod.findRSL_Macro(
                user_road, para.bstn_M_x, para.bstn_M_y, EIRP_macro)
            rsl_small = mod.findRSL_Small(
                user_road, para.bstn_S_x, para.bstn_M_y, EIRP_small)
            #print("rsl_macro is:", rsl_macro, "for userid:", userid)
            #print("rsl_small is:", rsl_small, "for userid:", userid)
            if rsl_macro > rsl_small:
                rsl_server = rsl_macro
                rsl_other = rsl_small
                user_road.updateservingcell(0)
                #print("Rsl server is macro cell", rsl_server,"for user id :", userid)
            else:
                pass

            if rsl_small > rsl_macro or rsl_small > para.RSLopt_small:
                rsl_server = rsl_small
                rsl_other = rsl_macro
                user_road.updateservingcell(1)
                #print("Rsl server is small cell",
                #      rsl_server, "for user id :", userid)
            else:
                pass

            if rsl_server < para.ue_thres:

                active_server = user_road.getservingstation()
                if active_server == 0:
                    num_call_drop_low_sgnl_Macro += 1
                    #print("I am dropping call due to low sgnl_macro_Cell for userid", userid)
                    user_road.resetuser()
                    caller_list.remove(userid)
                    ArchiveUser_Road.append(userid)
                else: #server is small cell
                    num_call_drop_low_sgnl_small += 1
                    #print("I am dropping call due to low sgnl_small_Cell for userid", userid)                        
                    user_road.resetuser()
                    caller_list.remove(userid)
                    ArchiveUser_Road.append(userid)

            else:  # loop for rsl_server>=rsl_threshold
                active_server = user_road.getservingstation()
                if active_server == 0:  # Means call is served by Macro cell
                    #print("as serving cell is 0 for user", userid,
                          #"I am checking Macro cell first")
                    num_call_attempt_macro += 1
                    avail_channel = num_traffic_channel_macro
                    if avail_channel > 0:
                        num_traffic_channel_macro -= 1
                        num_call_established_success_macro += 1
                        #print(
                         #   "I am establishing call on macro_Cell for userid", userid)
                        user_road.setCallStatus(1)
                        user_road.updateservingcell(0)
                        # adding user to a caller list
                        caller_list.append(userid)
                    # checking channels for Other cell (Macro cell here) Point 1.c.V.1,2
                    else: #Macro do not have the channel check small cell
                        rsl_server = rsl_other
                        if rsl_server >= para.ue_thres:
                            num_call_blocked_capacity_macro += 1
                            num_call_attempt_small += 1
                            avail_channel = num_traffic_channel_small
                            if avail_channel > 0:
                                num_traffic_channel_small -= 1
                                #print(
                                #    "No channel is Macro .I am establishing call on small_Cell for userid", userid)
                                num_call_established_success_small += 1
                                user_road.setCallStatus(1)
                                user_road.updateservingcell(1)
                                # adding user to a caller list
                                caller_list.append(userid)
                            else:
                                num_call_drop_capacity_macro += 1
                                #print(
                                #    "I am blocking call due to capacity issue in Macro cell for user", userid)
                                user_road.resetuser()
                                caller_list.remove(userid)
                                ArchiveUser_Road.append(userid)
                        else:
                            pass
                    
                else:  # active_server == 1
                    #print("as serving cell is 1 for user", userid,
                    #      "I am checking small cell first")
                    num_call_attempt_small += 1
                    avail_channel = num_traffic_channel_small
                    if avail_channel > 0:
                        #print(
                        #    "I am establishing call on small_Cell for userid", userid)
                        num_traffic_channel_small -= 1
                        num_call_established_success_small += 1
                        user_road.setCallStatus(1)
                        user_road.updateservingcell(1)
                        # adding user to a temp list to avoid iterating through same active users
                        caller_list.append(userid)
                    else:
                        # checking channels for Other cell (Macro cell here) Point 1.c.V.1,2
                        rsl_server = rsl_other
                        if rsl_server >= para.ue_thres:
                            avail_channel = num_traffic_channel_macro
                            num_call_blocked_capacity_small += 1
                            num_call_attempt_macro += 1
                            if avail_channel > 0:
                                #print("No channel is small .I am establishing call on macro_Cell for userid", userid)
                                    
                                num_traffic_channel_macro -= 1
                                num_call_established_success_macro += 1
                                user_road.setCallStatus(1)
                                user_road.updateservingcell(0)
                                # adding user to a temp list to avoid iterating through same active users
                                caller_list.append(userid)
                            else:
                                num_call_drop_capacity_small += 1
                                #print("I am blocking call due to capacity issue in Small cell for user", userid)
                                    
                                user_road.resetuser()
                                caller_list.remove(userid)
                                ArchiveUser_Road.append(userid)
                        else:
                            pass
                        
    caller_list_park = [] #For park
    for userid in InactiveUser_Park:
        #print("User id is" , userid)
        user_park = userdata_park[userid]
        temp_callstatus = user_park.getcallstatus()
        temp_calltime = user_park.getcalltimer()
        n = np.random.uniform()
        if n < probability: #calculating the callers
            #print(n) -> For verification
            #temp_callstatus = 1 #0 -> Inactive , 1 -> Active. So changing to 1 to mark active users in User data
            #user_park.setCallStatus(temp_callstatus)
            temp_x = np.random.uniform(-100,100) # Generating random X axis value for a user in park
            temp_y = np.random.uniform(0,100) #Generating random Y axis value for a user in park
            temp_angle = np.random.uniform(0,360) #generating random angle value for a user in Park
            temp_calltime = np.random.exponential(para.call_duration_road) # As mentioned passing 120 second average value
            #print("Park call time generated is :",temp_calltime)
            user_park.updatelocation(temp_x, temp_y, temp_angle) #Updating location details for inactive users
            user_park.setcalltimer(temp_calltime)
            caller_list_park.append(userid)
            InactiveUser_Park.remove(userid)
            #Finding RSL for the user 
            rsl_macro = mod.findRSL_Macro(
                user_park, para.bstn_M_x, para.bstn_M_y, EIRP_macro)
            rsl_small = mod.findRSL_Small(
                user_park, para.bstn_S_x, para.bstn_M_y, EIRP_small)
            #print("rsl_macro is:", rsl_macro, "for userid:", userid)
            #print("rsl_small is:", rsl_small, "for userid:", userid)
            if rsl_macro > rsl_small:
                rsl_server = rsl_macro
                rsl_other = rsl_small
                user_park.updateservingcell(0)
                #print("Rsl server is macro cell", rsl_server,"for user id :", userid)
            else:
                pass

            if rsl_small > rsl_macro or rsl_small > para.RSLopt_small:
                rsl_server = rsl_small
                rsl_other = rsl_macro
                user_park.updateservingcell(1)
                #print("Rsl server is small cell",
                #      rsl_server, "for user id :", userid)
            else:
                pass
            
            if rsl_server < para.ue_thres:
                active_server = user_park.getservingstation()
                if active_server == 0:
                    num_call_drop_low_sgnl_Macro += 1
                    #print("I am dropping call due to low sgnl_macro_Cell for userid", userid)
                    user_park.resetuser()
                    caller_list_park.remove(userid)
                    ArchiveUser_Park.append(userid)
                else:
                    num_call_drop_low_sgnl_small += 1
                    #print("I am dropping call due to low sgnl_small_Cell for userid", userid)
                    user_park.resetuser()
                    caller_list_park.remove(userid)
                    ArchiveUser_Park.append(userid)
            else:  # loop for rsl_server>=rsl_threshold
                active_server = user_park.getservingstation()
                if active_server == 0:  # Means call is served by Macro cell
                    #print("as serving cell is 0 for user", userid,
                          #"I am checking Macro cell first")
                    num_call_attempt_macro += 1
                    avail_channel = num_traffic_channel_macro
                    if avail_channel > 0:
                        num_traffic_channel_macro -= 1
                        num_call_established_success_macro += 1
                        #print(
                         #   "I am establishing call on macro_Cell for userid", userid)
                        user_park.setCallStatus(1)
                        user_park.updateservingcell(0)
                        # adding user to a caller list
                        #caller_list_park.append(userid)
                    # checking channels for Other cell (Macro cell here) Point 1.c.V.1,2
                    else: #Macro cell do not have channel , then need to check other cell (Small cell here)
                        rsl_server = rsl_other
                        if rsl_server >= para.ue_thres:
                            num_call_blocked_capacity_macro += 1
                            avail_channel = num_traffic_channel_small
                            if avail_channel > 0:
                                num_traffic_channel_small -= 1
                                #print(
                                #    "No channel is Macro .I am establishing call on small_Cell for userid", userid)
                                num_call_established_success_small += 1
                                user_park.setCallStatus(1)
                                user_park.updateservingcell(1)
                                # adding user to a caller list
                                #caller_list_park.append(userid)
                            else:
                                num_call_drop_capacity_macro += 1
                                #print(
                                #    "I am blocking call due to capacity issue in Macro cell for user", userid)
                                user_park.resetuser()
                                caller_list_park.remove(userid)
                                ArchiveUser_Park.append(userid)

                else:  # active_server == 1 that means server is small cell
                    #print("as serving cell is 1 for user", userid,
                    #      "I am checking small cell first")
                    num_call_attempt_small += 1
                    avail_channel = num_traffic_channel_small
                    if avail_channel > 0:
                        #print(
                        #    "I am establishing call on small_Cell for userid", userid)
                        num_traffic_channel_small -= 1
                        num_call_established_success_small += 1
                        user_park.setCallStatus(1)
                        user_park.updateservingcell(1)
                        # adding user to a temp list to avoid iterating through same active users
                        #caller_list_park.append(userid)
                    else:
                        # checking channels for Other cell (Macro cell here) Point 1.c.V.1,2
                        rsl_server = rsl_other
                        if rsl_server >= para.ue_thres:
                            num_call_blocked_capacity_small += 1
                            avail_channel = num_traffic_channel_macro
                            if avail_channel > 0:
                                #print("No channel is small .I am establishing call on macro_Cell for userid", userid)
                                num_traffic_channel_macro -= 1
                                num_call_established_success_macro += 1
                                user_park.setCallStatus(1)
                                user_park.updateservingcell(0)
                                # adding user to a temp list to avoid iterating through same active users
                                #caller_list_park.append(userid)
                            else:
                                num_call_drop_capacity_small += 1 #as call is blocked due to capacity issue in small cell
                                #print("I am blocking call due to capacity issue in Small cell for user", userid)
                                user_park.resetuser()
                                caller_list_park.remove(userid)
                                ArchiveUser_Park.append(userid)
                        else:
                            pass

    #Adding users to active list
    ActiveUser_Park.extend(caller_list_park)
    ActiveUser_Road.extend(caller_list)
    
    #Clearing archieve list and adding back to inactive user
    InactiveUser_Park.extend(ArchiveUser_Park)
    InactiveUser_Road.extend(ArchiveUser_Road)
    ArchiveUser_Park = []
    ArchiveUser_Road = []
#=====================================================================================
#Printing stats for each hour and final hour stats
#=====================================================================================   
    if counter > 0 and counter%3600 == 0:
        
        print("\n===============X Macro Cell Stats {0} {1} X================= ".format((counter//3600),"hours"))
        print("No. of active calls on Macro cell:", (para.tchnl_macro-num_traffic_channel_macro))
        print("No. of call attempts on Macro cell: ",num_call_attempt_macro)
        print("No. of calls successfully established on Macro cell: ",num_call_established_success_macro)
        print("No. of successful handoff out of Macro cell: ",num_success_handoff_out_Macro)
        print("No. of successful handoff into Macro cell: ",num_success_handoff_into_Macro)
        print("No. of call dropped due to capacity of Macro cell: ", num_call_drop_capacity_macro)
        print("No. of call blocked due to capacity in Macro cell: ",num_call_blocked_capacity_macro)
        print("No. of calls dropped due to low signal strength for Marco Cell: ",num_call_drop_low_sgnl_Macro)
        print("\n================Small Cell Stats {0} {1}================= ".format((counter//3600),"hours"))
        print("No. of active calls on Small cell:", (para.tchnl_small-num_traffic_channel_small))
        print("No. of call attempts on Small cell: ",num_call_attempt_small)
        print("No. of calls successfully established on Small cell: ",num_call_established_success_small)
        print("No. of successful handoff out of Small cell: ",num_success_handoff_out_small)
        print("No. of successful handoff into Small cell: ",num_success_handoff_into_small)
        print("No. of calls dropped due to low signal strength for Small Cell: ",num_call_drop_low_sgnl_small)
        print("No. of call blocked due to capacity in Small cell: ",num_call_blocked_capacity_small) 
        print("No. of call droppped due to capacity of Small cell: ", num_call_drop_capacity_small)
        #print("\n")
        print("================X End of {} (st/nd/rd/th) hours report X====================".format((counter//3600)))
    else:
        pass
#End of simulation loop
#==============================================================================================
end = time.time()
run_time = end - start
print("Total run time :", run_time)