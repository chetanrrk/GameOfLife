#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:55:00 2020

@author: chetanrupakheti
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

images=[]

class Grid:
    def __init__(self,dim,pixel,out=None):
        self.dim=dim
        self.grid=np.zeros(dim*dim)
        self.pixel=pixel
        self.fout=out
        if self.fout: self.fout=open(out,"w")
        
    def initGrid(self):
        alive=0
        dead=0
        for i in range(len(self.grid)):
            if np.random.randint(2):
                self.grid[i]=self.pixel    
                alive+=1
            else:dead+=1
        self.grid = np.reshape(self.grid,(self.dim,self.dim))
        return alive,dead
    
    def getNeighbors(self,i,j): ### pass cell with i,j index
        """
        if min(i-1,j-1)<0 or max(i+1,j+1)>=self.dim: return [] ### out of bounds
        else: return [self.grid[i-1,j-1],self.grid[i-1,j],self.grid[i-1,j+1],
                self.grid[i,j-1],self.grid[i,j+1],
                self.grid[i+1,j-1],self.grid[i+1,j],self.grid[i+1,j+1]]
        """

        if i==0: 
            if j>0 and j<self.dim-1:
                return [self.grid[i,j-1],self.grid[i,j+1],
                self.grid[i+1,j-1],self.grid[i+1,j],self.grid[i+1,j+1]]
            elif j==self.dim-1:
                return [self.grid[i,j-1],self.grid[i+1,j-1],self.grid[i+1,j]]
            else:return [self.grid[i,j+1],self.grid[i+1,j],self.grid[i+1,j+1]]
        elif j==0:
            if i>0 and i<self.dim-1:
                return [self.grid[i-1,j],self.grid[i-1,j+1],self.grid[i,j+1],
                    self.grid[i+1,j],self.grid[i+1,j+1]]
            elif i==self.dim-1:
                return [self.grid[i-1,j],self.grid[i-1,j+1],self.grid[i,j+1]]
        elif i==self.dim-1:
            if j<self.dim-1:
                return [self.grid[i-1,j-1],self.grid[i-1,j],self.grid[i-1,j+1],
                        self.grid[i,j-1],self.grid[i,j+1]]
            elif j== self.dim-1:
                return [self.grid[i-1,j-1],self.grid[i-1,j],
                        self.grid[i,j-1]]
        elif j==self.dim-1:
            return [self.grid[i-1,j-1],self.grid[i-1,j],
                self.grid[i,j-1],self.grid[i+1,j-1],self.grid[i+1,j]]
        else: return [self.grid[i-1,j-1],self.grid[i-1,j],self.grid[i-1,j+1],
                self.grid[i,j-1],self.grid[i,j+1],
                self.grid[i+1,j-1],self.grid[i+1,j],self.grid[i+1,j+1]]
        

    def applyRules(self,cell,neighbors):
        aliveNeighbors=0
        deadNeighbors=0
        for n in neighbors:
            if n>0.0:aliveNeighbors+=1
            else:deadNeighbors+=1
            
        """
        rules1: dead cell with 3 alive neighbors becomes alive
        rules2: alive cell with 2 or 3 alive neighbors becomes alive
        rules3: else cell becomes or remain dead
        """
        if cell==0.0 and aliveNeighbors==3: ##rule 1
            cell= self.pixel
        elif cell>0.0 and (aliveNeighbors==2 or aliveNeighbors==3): ##rule 2
            cell=self.pixel
        else: ##rule 3
            cell=0.0
        return cell  
            
    ### print helper function
    def _printGrid(self):
        for i in range(self.dim):
            for j in range(self.dim):
                print self.grid[i][j],
                print>>self.fout,self.grid[i][j],
            print
            print>>self.fout,""
        
    def countAlive(self):
        alive=0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.grid[i][j]>0:
                    alive+=1
        return alive           
                    
    def simulate(self,iters):
        images=[]
        for i in range(iters):
            result=[]
            if self.fout:
                print "=============iter"+str(i)+"=============\n"
                print>>self.fout,"=============iter"+str(i)+"=============\n"
            for j in range(self.dim):
                for k in range(self.dim):
                    neighbors = self.getNeighbors(j,k)
                    if len(neighbors) > 0:
                        cell = self.applyRules(self.grid[j][k],neighbors)
                        result.append(cell)
                    else:result.append(self.grid[j][k])
            
            if np.sum(result)==0:
                print "no alive cells"
                images.append(self.grid)
                break
            ###update the grid at the end
            self.grid=np.reshape(result,(self.dim,self.dim))
            
            #aliveCount = self.countAlive()
            #print "alive,dead",aliveCount,(self.dim*self.dim)-aliveCount
            #self._printGrid()
            
            images.append(self.grid)
            
        if self.fout: self.fout.close()    
        return images

def animate(frame):
    image.set_array(images[frame])
        

if __name__=="__main__":
    pixel=5
    size=20
    out=None
    iterations=500
    g = Grid(size,pixel,out)

    alive,dead = g.initGrid()

    print "inital alive,dead",alive,dead
    images = g.simulate(iterations) ### 10 iterations
        
    # starting to plot
    fig, ax = plt.subplots(1, figsize=(1, 1))
    # Stretch to fit the whole plane
    fig.subplots_adjust(0, 0, 1, 1)
    # Remove bounding line
    ax.axis("off")

    # Initialise our plot. Make sure we set vmin and vmax!
    image = ax.imshow(images[0], vmin=0, vmax=1)
    
    
    anim = animation.FuncAnimation(
        #Matplotlib Figure object
        fig,
        # The function that does the updating of the Figure
        animate,
        # Frame information (here just frame number)
        np.arange(len(images)),
        # Extra arguments to the animate function
        fargs=[],
        # Frame-time in ms; i.e. for a given frame-rate x, 1000/x
        interval=1000/5
    )
    
    #anim.save("gol.mp4",dpi=10) ### movie doesn't work
    
    anim.save ('./GOL/game_of_life.gif', writer = "imagemagick",fps=100)
    
    