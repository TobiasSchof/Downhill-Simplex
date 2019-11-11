# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:21:13 2019

@author: Tobias's PC
"""

from Support import Polytope, Vertex
import time

class Simplex:      
    """
    Runs a downhill simplex on a function from R^n to R^1
    """
    
    def __init__(self, function, dimension, startPoint, startDelta):
        """
        Constructor for Simplex
        
        Inputs:
            function:Function = the function to be minimized
            dimension:int = the dimension of the domain of the function
            startPoint:Tuple = the coordinates of a point to base the start of the simplex on
            startDelta:float = the maximum distance any point in the starting polytope should be from [startPoint]
        Parameters:
            evaluate:Function = the function to be minimized
            dim:int = the dimension of the domain of the function
            sp:Tuple = the coordinates to base the start of the simplex on
            sd:float = the distance any point in the starting polytope should be from startPoint
        """
        self.evaluate=function
        self.dim=dimension
        self.sp=startPoint
        self.sd=startDelta
        
    def step(self, polytope):
        """
        Performs one step of the simplex
        
        Input:
            polytope:Polytope = the polytope being manipulted by the simplex
        """
        alpha=1 #the reflection factor
        gamma=2 #the expansion factor
        rho=.5 #the contraction factor
        sigma=.5 #the shrink factor
        
        #finds the point that is a reflection of our worst point over the centroid
        temp=[]
        for x in range(0, self.dim):
            temp.append(polytope.centroid[x]+alpha*(polytope.centroid[x]-polytope.vertices[-1].coord[x]))
            
        #calculate how good the reflected point is
        temp=Vertex(tuple(temp), self.evaluate(temp))
            
        #tracks whether we need to do a shrink
        shrink=False
        
        #if the reflected point is better than or as good as our best point, expand and check whether expansion is better
        if temp.value <= polytope.vertices[0].value:
            expand=[]
            for x in range(0, self.dim):
                expand.append(polytope.centroid[x]+gamma*(temp.coord[x]-polytope.centroid[x]))
            expval=self.evaluate(expand)
            if expval < temp.value:
                temp=Vertex(tuple(expand), expval)
                
        #if the reflected point is worse than our second worst point, contract
        elif temp.value >= polytope.vertices[-2].value:
            contraction=[]
            for x in range(0, self.dim):
                contraction.append(polytope.centroid[x]+rho*(polytope.vertices[-1].coord[x]-polytope.centroid[x]))
            conval=self.evaluate(contraction)
            #if contraction is better than our reflection and our worse point, use that
            if conval < temp.value and conval < polytope.vertices[-1].value:
                temp=Vertex(tuple(contraction), conval)
            #if contraction is not better and our reflected point is worse or equal to our worst point, shrink
            elif temp.value >= polytope.vertices[-1].value:
                shrink=True
        
        #if we're not shrinking, we put our new point in the list, recalculate delta and the centroid
        if (not shrink) and temp.value < polytope.vertices[-1].value:
            polytope.insert(temp)
            
        #if we are supposed to shrink, shrink
        else:
            polytope.shrink(sigma, self.evaluate)
           
    def randRun(self, trials, minimum, termination):
        """
        Runs this simplex (trials) times, starting with coordinates determined by the generate() function, terminating each simplex when a point is found within (termination) of (minimum)
        Note: a theoretical minimum must be known for the function that is being minimized. If none is known, a personalized implementation with a different termination condition can be made using the step() function
        
        Inputs:
            trials:int = the number of trials that should be run
            minimum:float = the theoretical minimum of the function being minimized
            termination:float = the unit distance that determines how close the simplex should get to the minimum before it terminates
        Output:
            [String] = a list of Strings, each of which contain the best vertex from a trial
        """
        #start a timer
        startT=time.time()
        
        mins=[]
        
        for x in range(0, trials):
            #make a polytope
            poly=Polytope.generate(self.dim, self.evaluate, self.sp, self.sd)
            check=[]
            while abs(poly.vertices[0].value-minimum) > abs(termination):
                self.step(poly)
                #stuck check for oneKThing
                if len(check)<(2*self.dim+1):
                    check.insert(0,poly.vertices[0].value)
                else:
                    if check[-1]-poly.vertices[0].value < .1*(check[-1]-(minimum+termination)):
                        print("check: %s, best: %f"%(check, poly.vertices[0].value))
                        check=[]
                        poly=Polytope.generate(self.dim, self.evaluate, poly.vertices[0].coord, 2*poly.delta[0])
                        check.append(poly.vertices[0].value)
                        print("retry")
                        for v in poly.vertices:
                            print(v)
                    else:
                        check.insert(0,poly.vertices[0].value)
                        check.pop()

                print("best: %s"%poly.vertices[0])
                
            print("done with number %d." %x)
            mins.append(poly.vertices[0])
            
        endT=time.time()
        elapsed=endT-startT
        
        print("It took %s seconds to run %d trials within %f units of the minimum." %(elapsed, trials, termination))
        return mins