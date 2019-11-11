# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 15:15:35 2019

@author: Tobias's PC
"""

class Functions:
    
    def sumSquares(point):
        """
        returns the sum of the squares of the coordinates of point (the square of the distance to the origin)
        defined for any dimension
        
        Inputs:
            point:[float] = an array representing the point to be evaluated. Size should match self.dimdom
        """
            
        val=0
        for x in point:
            val+=x**2
        return val
    
    def oneKThing(point):
        """
        returns the sum of each coordinate mod 1000 times the square of the coordinate plus the absolute value of the coordinate divided by 1000
        defined for any dimension
        
        Inputs:
            point:[float] = an array representing the point to be evaluated. Size should match self.dimdom
        """
        d=0
        for c in point:
            d+=(c%1000)*(c**2)+abs(c/100)
        return d