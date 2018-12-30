#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 21:51:17 2018

@author: giacomo
"""
import math
import numpy as np

path="/home/giacomo/Documents/script_python/section/sez.dxf"

def Read_dxf(path):
    l_rows_clear=[]
    f=open(path)
    l_rows=f.readlines()
    f.close()
    
    for item in l_rows:        
        l_rows_clear.append(item.strip())    
    return(l_rows_clear)
    
def Find_steel(l_rows):
    pos=[i for i,item in enumerate(l_rows) if item=="STEEL"]
    # find position of 0 marker immediately preceding the "STEEL" string
    pos_0=[]
    for i in pos:
        j=0
        while l_rows[i-j]!="0":
            j=j+1
            pos_0_i=i-j
            if l_rows[i-j]=="0" and l_rows[pos_0_i+1]=="CIRCLE":
                pos_0.append(pos_0_i)
    xg=[]
    for i in pos_0:
        j=0
        while l_rows[i+j]!="10":
            j=j+1
        
        xg.append(l_rows[i+j+1])
    
    yg=[]
    for i in pos_0:
        j=0
        while l_rows[i+j]!="20":
            j=j+1
        
        yg.append(l_rows[i+j+1])
        
    area=[]
    for i in pos_0:
        j=0
        while l_rows[i+j]!="40":
            j=j+1     
        area.append(math.pi*float(l_rows[i+j+1])**2)
        
    return(xg,yg,area)
    
def FindConcrete(l_rows):
    pos=[i for i,item in enumerate(l_rows) if item=="CONCRETE"]
    # find position of 0 marker immediately preceding the "CONCRETE" string
    pos_0=[]
    for i in pos:
        j=0
        while l_rows[i-j]!="0":
            j=j+1
            pos_0_i=i-j
            if l_rows[i-j]=="0" and l_rows[pos_0_i+1]=="POLYLINE":
                pos_0.append(pos_0_i)
    # find position of "0" marker immediately preceding the 
    # "VERTEX" string
    pos_v=[]
    for i in pos_0:
        j=0
        while l_rows[i+j]!="SEQEND":
            j=j+1
            if l_rows[i+j]=="VERTEX":
                pos_v.append(i+j-1)
    # find coordinates of vertex 
    xv=[]
    for i in pos_v:
        j=0
        while l_rows[i+j]!="10":
            j=j+1        
        xv.append(float(l_rows[i+j+1]))
    
    yv=[]     
    for i in pos_v:
        j=0
        while l_rows[i+j]!="20":
            j=j+1        
        yv.append(float(l_rows[i+j+1]))
    
    # calculate area of concrete section
    def PolyArea(x,y):
        return (0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1))))
    
    area= PolyArea(xv,yv)
    
class SteelBar:
    def __init__(self,area,xg,yg):
        self.area=area
        self.xg=xg
        self.yg=yg
        
class Concrete:
    def __init__(self,area,xg,yg):
        self.area=area
        self.xg=xg
        self.yg=yg       


if __name__=="__main__":
    
    l_rows=Read_dxf(path)
    xg=Find_steel(l_rows)[0]
    yg=Find_steel(l_rows)[1]
    area=Find_steel(l_rows)[2]

    # create list of SteelBars instances
    par=[]
    for i in range(0,len(area)):
        par.append([area[i],xg[i],yg[i]])    
        steelBars=[SteelBar(i[0],i[1],i[2]) for i in par]