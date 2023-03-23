# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 09:11:53 2022

@author: Akshay Baghmar
"""

import numpy as np
from math import log10
import sys_parameters as para
from math import sin,cos,sqrt
import Users_Module as user_mod

#Making function to convert value to db (useful for fading)
def convert2db(val):
    y = 10 * log10(val)
    return y

#Macro cell Okamura hata propogration function
def prop_macro_cell(d,fm_macro):
    d = d / 1000
    Ahm = (1.1 * log10(fm_macro) - 0.7) * para.hm_ue - (1.5 * log10(fm_macro) - 0.8)
    pl50 = 69.55 + 26.16 * log10(fm_macro) - (13.82*log10(para.hm_macro)) + (44.9-6.55*log10(para.hm_macro))*log10(d)- Ahm
    #print("Ploss is:",pl50)
    return pl50

#Cost231
def prop_small_cell(d,fm_small):
    d = d / 1000
    Ahm = (1.1 * log10(fm_small) - 0.7) * 1 - (1.5 * log10(fm_small) - 0.8)
    pl50 = 46.3 + 33.9*log10(fm_small)-13.82*log10(para.hm_small)+(44.9 -6.55*log10(para.hm_small))*log10(d)-Ahm
    return pl50 

#Shadowing its will make a dictionary of value associated with every 10 meters on road
def shadowing (mean,sigma,size): 
    #Created random normal values for shadowing , Mean = 0, Stnd d = 2, size = 600
    shadow_val = np.random.normal(mean,sigma,size)
    #print(len(shadow_val))
    #print(type(shadow_val))
    return shadow_val

#Defining Fading fuction : It will calculate the second deepest fade.
def fading(sigma,size):
    #Used Rayleigh function (standard deviation.,size)
    y = np.random.rayleigh(sigma,size)
    y = np.sort(y) 
    ray_sqr = y ** 2
    #print(ray_sqr)
    #getting the second deepest value, throwing(ignoring)first deepest fade, 
    #converting to db by calling covert2db function
    fade1db = convert2db(ray_sqr[1])
    return fade1db

def updateposition_road(userid,deltaT):
    temp_x = userid.getx()
    temp_direction = userid.getdirection()
    temp_speed =userid.getspeed()
    if temp_direction == 0:
        x1 = temp_x + (temp_speed*deltaT)
    else:
        x1 = temp_x - (temp_speed*deltaT)
    return x1
    
def updatepositionpark_x(userid,deltaT):
    temp_user_angle = userid.getangle()
    temp_user_x = userid.getx()
    speed = userid.getspeed()
    if temp_user_angle is not None:
        x1 = temp_user_x + (speed*deltaT*cos(temp_user_angle))
        return x1
    return temp_user_x    

def updatepositionpark_y(userid,deltaT):
    temp_user_angle = userid.getangle()
    speed = userid.getspeed()
    temp_user_y = userid.gety()
    if temp_user_angle is not None:  
        y1 = temp_user_y + (speed*deltaT*sin(temp_user_angle))
        return y1
    return temp_user_y

def updateanglepark(x,y,angle):
    #print(angle,angle+180.0,angle+180) #for checking
    #If user in park goes out of park or reaches border, change the angle
    if (x <= -100):
        angle = (angle+180)%360
        return angle
    else:
        pass
    if (y >= 100):
        angle = (angle+180)%360
        return angle
    else:
        pass
    if (y <= 0):
        angle = (angle+180)%360
        return angle
    else:
        pass
    if (x >= 100):
        angle = (angle+180)%360
        return angle
    else:
        pass
    return angle


def findRSL_Macro(userid,bstn_x,bstn_y,eirp_macro):
    temp_user_x = userid.getx()
    temp_user_y = userid.gety()
    d = sqrt((temp_user_x-bstn_x)**2 + (temp_user_y - bstn_y)**2)
    #print("x cordinate is :",temp_user_x, "Y cordinate is:", temp_user_y,"distance is:",d)
    ploss = prop_macro_cell(d, para.fm_macro)
    shadow_aray = shadowing(para.shadowing_mean, para.shadowing_std, para.road_lgth//para.shadowing_res)
    index = int(temp_user_x // para.shadowing_res) #
    #print("Shadowing index is:",index)
    shadow_val = shadow_aray[index]
    #print("Shadowing Value is:", shadow_val)
    fad_loss = fading(2,10)
    #print("Fading value is:" , fad_loss)
    rsl_macro = eirp_macro - ploss + fad_loss + shadow_val #RSL macro cell
    return rsl_macro
    
def findRSL_Small(userid,bstn_x,bstn_y,eirp_small):
    temp_user_x = userid.getx() # Get user X cords
    temp_user_y = userid.gety() #Get user Y cords
    d = sqrt((temp_user_x-bstn_x)**2 + (temp_user_y - bstn_y)**2) #Cal Distance
    #print("x cordinate is :",temp_user_x, "Y cordinate is:", temp_user_y,"distance is:",d)
    ploss = prop_small_cell(d,para.fm_small)
    fad_loss = fading(2,10) # getting fading 2nd deepest fade
    rsl_small = eirp_small - ploss + fad_loss # calculating RSL for small cell
    return rsl_small


