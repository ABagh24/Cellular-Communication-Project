# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:25:28 2022
@author: Akshay Baghmar
"""


import sys_parameters as para
import Modules_Project as mod
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


#RSLs of Macro cell
d_road = np.arange(-3000,3001,1) #making array of each meter distance on Road
d = np.hypot(d_road ,500) #calculating distance between macro cell and road points
#converting d in Kms
d = d / 1000
#print(d)
rsl_macro = []
for i in d:
    PL50 = mod.prop_macro_cell(i,para.fm_macro) #callings Okamura Hata Function
    rsl_macro.append(PL50)
#print(rsl_macro)

#RSLs for Small cell
d_park = np.hypot(d_road,50) #calculating the distance between small cell and road points
#converting d_park in Kms
d_park = d_park / 1000
rsl_small = []
for i in d_park:
    PL50 = mod.prop_small_cell(i, para.fm_small) #Calling Cost231 function
    rsl_small.append(PL50)
#print(rsl_small)

#Defining GridSpec for the plots
plt.tight_layout()
gs = gridspec.GridSpec(2, 2)

#Defining the layout for plot
ax = plt.subplot(gs[0, :])
ax1 = plt.subplot(gs[1,0])
ax2= plt.subplot(gs[1,1])

#First Plot - Okamura hata and Cost 231 graph
plt.tight_layout()
ax.set_title('Only Propogation Loss')
ax.plot(rsl_macro,'r')
ax.plot(rsl_small,'b')
ax.set_xlabel("Distance(d) on road")
ax.set_ylabel("RSL")
ax.legend(("RSL_Macro","RSL_Small"),loc='upper right',fontsize=7)

#Calculation Second graph with shadowing for macro cell
shadow_val = mod.shadowing(0,2,6010)
idx = 0
for shadowKey in shadow_val:
   rsl_macro[idx] = rsl_macro[idx] + shadow_val[shadowKey]
   idx += 10 #added 10 so it increases by 10 value

#print(rsl_macro)
#RSL_macro with shadwoing and rsl_small cell as found with Cost231 function
plt.tight_layout()
#ax1.set_xlim([0,30])
#Plotting Macro cell graph - Propogation + Shadowing and Cost231 (Small cell)
ax1.set_title("Propgation with Shadowing")
ax1.plot(rsl_macro,'r')
ax1.plot(rsl_small,'b')
ax1.set_xlabel("Distance(d) on road")
ax1.set_ylabel("RSL")
ax1.legend(("RSL_Macro","RSL_Small"),loc='upper right', fontsize=5)

#Calculation Third graph with Shadowing + Fading


#Calculating 3rd Graph - 
#Macro Cell = Propogation + Shadowing + Fading
fading_val = []
n = 6001
for i in range(n):
    #calling fading function and this will generate 6000 fading_val for each meter on road
    fading_val.append(mod.fading(2, 10))
#print(fading_val)
#Adding fading value and rsl_macro (found in line 62, which is Okamura_Hata + Shadowing)
rsl_macro_all = []
for i in range(0, len(rsl_macro)):
    rsl_macro_all.append(rsl_macro[i] + fading_val[i])
#print(rsl_macro_all)

#Small cell = Propogation + Fading
rsl_small_all = []
fading_val_2 = []
n = 6001
#getting fading values for small cells , calling same fading function and generating random fading values
for i in range(n):
    #calling fading function and this will generate 6000 fading_val for each meter on road
    fading_val_2.append(mod.fading(2, 10))
#print(fading_val_2)
#Adding the RSL_small + Fading_values
for i in range(0, len(rsl_small)):
    rsl_small_all.append(rsl_small[i] + fading_val_2[i])
#print(rsl_small_all)
#Plotting thrid graph with all loss for both Macro cell (okamura hata+shadowing+fading) and small cells(Cost231+fading) 
plt.tight_layout()
#ax2.set_xlim([0,30])
#Plotting Graph 3 - Macro cell = Prop + shadowing + Fading and Small cell = Cost231+Fading
ax2.set_title("Including all loss")
ax2.plot(rsl_macro_all,'r')
ax2.plot(rsl_small_all,'b')
ax2.set_xlabel("Distance(d) on road")
ax2.set_ylabel("RSL",fontsize=9)
ax2.legend(("RSL_Macro","RSL_Small"),loc='upper right', fontsize=5)
