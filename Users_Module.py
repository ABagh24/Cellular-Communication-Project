# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21  11:37:12 2022

@author: Akshay Baghmar
"""
#================================================
#Making a class to save user data such as X,Speed
#===============================================

import sys_parameters as para

class user:
    
    def __init__(self,userid,x,y,angle,speed):
        self.userid = userid
        self.x = x
        self.y = y
        self.angle = angle
        self.speed=speed
        #self.location = 0 #-> 0 for road and 1 for park
        self.calltimer = 0
        self.servingstation = None #0 for Marco and 1 for Small cell 
        self.callStatus = 0 #0 inactive and 1 as active
        #Creating direction for road user so they can move to furthest point on the road
        if y == 0 and angle == 0:
            # 0 => W -> E and 1 => E -> W
            if self.x < 0:
                self.direction = 0
            else:
                self.direction = 1

#Defining function to make details callable 
    def getuserid(self):
        return self.userid
    
    def getcallstatus(self):
        return self.callStatus
    
    def getx(self):
        return self.x
    
    def gety(self):
        return self.y
    
    def getangle(self):
        return self.angle
    
    def updateangle(self,angle):
        if angle is not None:
            self.angle = angle
            return self.angle
        return self.angle
    
    def getcalltimer(self):
        return self.calltimer
    
    def getservingstation(self):
        return self.servingstation 
    
    def setCallStatus(self,status):
        self.callStatus = status
    
    def setcalltimer(self,timer):
        self.calltimer = timer
        return self.calltimer
    
    def updatex(self,x):
        self.x = x
        return self.x
    
    def updatey(self,y):
        self.y = y
        return self.y
    
    def getdirection(self):
        return self.direction
    
    def updateservingcell(self,servcell):
        self.servingstation = servcell
        return self.servingstation

    def getspeed(self):
        return self.speed

    def updatelocation(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle
        return self.x,self.y,self.angle
    
    def updatetimer(self,call_timer):
        self.calltimer = call_timer - para.delta_time
        return self.calltimer
    
    def setlocation(self,loc):
        self.location = loc
        return self.location
    
    def resetuser(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.calltimer = 0
        self.servingstation = None #0 for Marco and 1 for Small cell 
        self.callStatus = 0
        return 
    

    
    
        
        
    

