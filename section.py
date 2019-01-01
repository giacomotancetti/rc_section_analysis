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
        xv.append(round(float(l_rows[i+j+1]),3))
    
    yv=[]     
    for i in pos_v:
        j=0
        while l_rows[i+j]!="20":
            j=j+1        
        yv.append(round(float(l_rows[i+j+1]),3))
    
    # define list of vertex coordiantes
    pts=[]
    for i in range(len(xv)):
        pts.append([xv[i],yv[i]])
    
    # calculate area of concrete cross section
    def area(pts):
        if pts[0] != pts[-1]:
            pts = pts + pts[:1]
        x = [ c[0] for c in pts ]
        y = [ c[1] for c in pts ]
        s = 0
        for i in range(len(pts) - 1):
            s += x[i]*y[i+1] - x[i+1]*y[i]
        return s/2
    
    # calculate position of centroid of concrete cross section
    def centroid(pts):
        if pts[0] != pts[-1]:
            pts = pts + pts[:1]
        x = [ c[0] for c in pts ]
        y = [ c[1] for c in pts ]
        sx = sy = 0
        a = area(pts)
        for i in range(len(pts) - 1):
            sx += (x[i] + x[i+1])*(x[i]*y[i+1] - x[i+1]*y[i])
            sy += (y[i] + y[i+1])*(x[i]*y[i+1] - x[i+1]*y[i])
        return sx/(6*a), sy/(6*a)
 
    # calculate inertia of concrete cross section
    def inertia(pts): 
        if pts[0] != pts[-1]:
            pts = pts + pts[:1]
        x = [ c[0] for c in pts ]
        y = [ c[1] for c in pts ]
        sxx = syy = sxy = 0
        a = area(pts)
        cx, cy = centroid(pts)
        for i in range(len(pts) - 1):
            sxx += (y[i]**2 + y[i]*y[i+1] + y[i+1]**2)*(x[i]*y[i+1] - x[i+1]*y[i])
            syy += (x[i]**2 + x[i]*x[i+1] + x[i+1]**2)*(x[i]*y[i+1] - x[i+1]*y[i])
            sxy += (x[i]*y[i+1] + 2*x[i]*y[i] + 2*x[i+1]*y[i+1] + x[i+1]*y[i])*(x[i]*y[i+1] - x[i+1]*y[i])
        return sxx/12 - a*cy**2, syy/12 - a*cx**2, sxy/24 - a*cx*cy
    
    # calculate principal inertia and orientation of principal axis
    def principal(Ixx, Iyy, Ixy):
        avg = (Ixx + Iyy)/2
        diff = (Ixx - Iyy)/2      # signed
        I1 = avg + sqrt(diff**2 + Ixy**2)
        I2 = avg - sqrt(diff**2 + Ixy**2)
        theta = atan2(-Ixy, diff)/2
        return I1, I2, theta
    
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