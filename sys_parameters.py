
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:23:43 2022

@author: Akshay Baghmar
"""
#Delta t in seconds
delta_time = 1

"""
Basic Parameters
"""

road_lgth = 6000 

# Probability of calling 
probability = 0.083 #(Calculated with Delta T and Lamba for Marco and Small cells)

"""
Macro cell parameters
"""
#location in meters
bstn_M_x = 0
bstn_M_y = -500
#Frequency Mhz
fm_macro = 800
#ht of macro cell in mtrs
hm_macro = 60
#Macro cell EIRP in dBm
eirp_macro_cell = 57 
#Marco Cell channels
tchnl_macro = 20

"""
Small Cell parameters
"""
#location 
bstn_S_x = 0
bstn_S_y = 50
#Frequency Mhz
fm_small = 2000
#ht of small cell in mtrs
hm_small = 30
#Small cell EIRP in dBm
eirp_small_cell = 54
#Small Cell channels
tchnl_small = 20

"""
Mobile parameters
"""
#Mobile height in meters
hm_ue = 1
#Mobile Handoff margin db
Hom = 3
#Mobile threshold dbm
ue_thres = -102 
#Small cell optimum performance thershold
RSLopt_small = -70 
#Call rate Lambda calls/hour
call_rate = 3 / 3600

"""
User Parameter Road
"""
#Avg call duration in seconds
call_duration_road = 2 * 60
#User speed meters/ second
R_user_speed = 15

"""
User Parameter Park
"""
#Call rate per hour

#Avg call duration in hours/call
H_park = 2 / 60
#User speed meters/ second
P_user_speed = 2

#shadowing parameters 
shadowing_mean = 0 #shadowing mean
shadowing_std = 2 # shadowing standard deviation
shadowing_res = 10 # shadowing resolution in meters

