# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:27:46 2019

@author: Tobias's PC
"""

import random, math

class Polytope:
    """
    Defines a polytope in n-dimensional space with vertices evaluated by a function from R^n to R^1
    """
    
    def __init__(self, points):
        """
        Constructor for Polytope
        
        Inputs:
            points:[Vertex] = a list of n-dimensional tuples that represent the vertices of the Polytope
        Parameters:
            vertices:[Vertex] = a list populated with Vertex objects sorted by their value
            centroid:Tuple = the center of this polytope
            delta:[float, Vertex, Vertex] = the maximum distance between any two vertices of this polytope stored with the two vertices determining delta
        """
        
        self.vertices=points
        
        #make sure that our vertices are sorted by value
        self.vertices.sort(key=lambda x: x.value)
        
        #finds the centroid
        c=[]
        for i in range(0, len(self.vertices[0].coord)):
            c.append(0)
            for t in self.vertices:
                c[i]+=t.coord[i]
            c[i]=c[i]/len(self.vertices)
            
        self.centroid=tuple(c)
        
        #finds delta, comparing each vertex once and updating delta if a larger distance is found
        self.delta=[0,0,0]
        for p1 in range(0, len(self.vertices)):
            for p2 in range(p1+1, len(self.vertices)):
                distance=self.vertices[p1].distance(self.vertices[p2])
                if distance > self.delta[0]:
                    self.delta[0]=distance
                    self.delta[1]=self.vertices[p1]
                    self.delta[2]=self.vertices[p2]
                    
    def insert(self, vertex):
        """
        Replaces the worst vertex in this polytope with the input polytope, updates delta and the centroid
        
        Input:
            vertex:Vertex = the vertex to be included in the polytope
        """
        #update the centroid
        cent=[]
        for i in range(0, len(self.centroid)):
            cent.append(self.centroid[i]-(self.vertices[-1].coord[i]/len(self.vertices))+(vertex.coord[i]/len(self.vertices)))
        self.centroid=tuple(cent)
        
        #find the largest delta between the point being inserted and all the other points
        updated=False
        ndelta=[0,0,0]
        for v in self.vertices[:-1]:
            distance=vertex.distance(v)
            if distance>ndelta[0]:
                ndelta[0]=distance
                ndelta[1]=vertex
                ndelta[2]=v

        #if this new delta proves to be larger than the previous delta, update delta
        if ndelta[0]>self.delta[0]:
            self.delta=ndelta  
            updated=True
                
        #if our new point didn't give us a new delta and the old delta involved the point we're removing, calculate the new delta
        if (not updated) and (self.delta[1]==self.vertices[-1] or self.delta[2]==self.vertices[-1]):
            #start with the largest delta that involves the point to be added
            self.delta=ndelta
            
            #see if any two points besides the worse point have a larger delta
            for i in range(0, len(self.vertices)-1):
                for x in range(i+1, len(self.vertices)-1):
                    distance=self.vertices[i].distance(self.vertices[x])
                    if distance > self.delta[0]:
                        self.delta[0]=distance
                        self.delta[1]=self.vertices[i]
                        self.delta[2]=self.vertices[x]
        
        #insert the new vertex into the sorted list    
        self.vertices=Polytope.__intinsert(vertex, self.vertices[:-1])
                
    def __intinsert(point, vertices):
        """
        A helper method for insert. Not meant for external use.
        Inserts the point into the sorted list vertices
        
        Inputs:
            point:Vertex = the point to be inserted
            vertices:[Vertex] the sorted list that our point is to be added to
            
        Outputs:
            [Tuple] = the sorted list with the inputted point added
        """
        #recursive catch
        if len(vertices)==0:
            return [point]
        
        mid=int(len(vertices)/2)
        if(vertices[mid].value > point.value):
            return Polytope.__intinsert(point, vertices[:mid])+vertices[mid:]
        elif(vertices[mid].value < point.value):
            return vertices[:mid+1]+Polytope.__intinsert(point, vertices[mid+1:])
        else:
            return vertices.insert(mid, point)
        
    def shrink(self, sigma, evaluate):
        """
        Shrinks the polytope around the best vertex (by a factor of sigma), updates delta and the centroid
        
        Inputs:
            sigma:float = the shrinking factor
            evaluate:Function = the evaluating function. Should take a dim-dimensional vector and return a float
        """
        temp=[]
        temp.append(self.vertices[0])
        cent=list(self.vertices[0].coord)
        
        #replace every vertex besides the best with the vertex shrunk towards the best point
        for v in self.vertices[1:]:
            p=[]
            for i in range(0, len(v.coord)):
                p.append(self.vertices[0].coord[i]+sigma*(v.coord[i]-self.vertices[0].coord[i]))
                cent[i]+=p[i]
            temp.append(Vertex(tuple(p), evaluate(p)))
            
        #set the centroid
        for i in range(0, len(cent)):
            cent[i]=cent[i]/len(temp)
        self.centroid=tuple(cent)
        
        #set delta
        ndelta=[0,0,0]
        for i in range(0, len(temp)):
            for x in range(i+1, len(temp)):
                distance=temp[i].distance(temp[x])
                if distance > ndelta[0]:
                    ndelta[0]=distance
                    ndelta[1]=temp[i]
                    ndelta[2]=temp[x]
                    
        self.delta=ndelta
            
        self.vertices=temp
        
        #make sure that our vertices are sorted
        for i in range(0, len(self.vertices)):
            while (i-1)>=0 and self.vertices[i].value<self.vertices[i-1].value:
                temp=self.vertices[i-1]
                self.vertices[i-1]=self.vertices[i]
                self.vertices[i]=temp
        
    def generate(dim, evaluate, point, delta):
        """
        generates a dim-dimensional polytope with random vertices sorted in ascendind order by the value returned by evaluate at each point
        
        Inputs:
            dim:int = the dimension of the space the polytope is to exist in
            evaluate:Function = a function that takes in a dim-dimensional vector and returns a float. Using this polytope in simplex will minimize the values of this function
            point:Tuple = the coordinates of a point to start with
            delta:float = the distance from (point) that new points should be within
        Output:
            Polytope = the polytope generated
        """
        
        #make a polytope including the inputted point and a collection of points within delta of that point
        #may have to put an upper/lower bound on how much of the delta each coordinate gets
        start=[list(point)]*(dim+1)
        for p in range(1, len(start)):
            dist=delta
            for i in range(0, dim):
                shift=random.randrange(0, math.ceil(100000*dist))/100000
                dist=(dist**2-shift**2)**(.5)
                start[p][i]+=random.randrange(-1,2,2)*shift
            start[p]=Vertex(tuple(start[p]), evaluate(start[p]))
        start[0]=Vertex(tuple(point), evaluate(point))
        
        return Polytope(start)
        
class Vertex:
    """
    Defines a vertex to be used in the Polytope class. Stores a tuple of coordinates and the value of that tuple via the simplex's function
    """
    
    def __init__(self, coordinate, value):
        """
        Constructor for Vertex
        
        Inputs:
            coordinate:Tuple = the coordinates of the vertex
            value:float = the value of this vertex by an evaluating function
        Parameters:
            self.coord:Tuple = the coordinates of the vertex
            self.value:float = the value of this vertex by an evaluating function
        """
        self.coord=coordinate
        self.value=value
        
    def distance(self, v2):
        """
        Returns the Euclidean distance between this vertex and the point that is passed in.
        
        Inputs:
            v2:Vertex = The vertex that this vertex is being compared to. Must be the same dimension as this vertex.
        Outputs:
            float = the distance between this vertex and the point passed in.
        """
        
        if not len(v2.coord)==len(self.coord):
            raise Exception("Dimension mismatch. Input is %d dimensions while this vertex is made of a point of %d dimensions." %len(v2.coord),len(self.coord))
            
        d=0
        for i in range(0, len(self.coord)):
            d+=(self.coord[i]-v2.coord[i])**2
            
        return d**(1/2)
    
    def __repr__(self):
        """
        String representation of vertex is the tuple followed by a colon followed by the vertex's value
        """
        rep="("
        for x in self.coord:
            rep=rep+"%.4f, "%x
            
        rep=rep[0:-2]+"):%.4f"%self.value
            
        return rep
            
        