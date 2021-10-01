# Player
# Author: Caleb Kisby
# Date: Jun.3.15
# 
# Represents a player event in a general adventure game.

from balloon import *
from present import *
from random import choice, randint

class Generator():
    def __init__(self, init_root, init_canvas, tile_size, init_x1, init_y1, init_x2, init_y2, player):
        """
        Schedules the main event generation loop.
        """
        # Set a flag to stop the generator.
        self._continue = False
        
        # Set the parameter attributes.
        self._root = init_root
        self._canvas = init_canvas
        self._tile_size = tile_size
        self._player = player
        
        self._x1 = init_x1
        self._y1 = init_y1
        self._x2 = init_x2
        self._y2 = init_y2
        
        # Set the wait time in-between each generated event.
        self._wait = 3000
        
        # Keep track of the total events generated.
        self._total_generated = 0
        
        # Set the minimum random value for each event to be generated.
        self._present_bound = 95.0
        self._balloon_bound = 85.0
        
        self._root.after(int(self._wait), self.event_generation)
    
    def event_generation(self):
        """
        Creates an amount of obstacles dependent on the current level.
        """
        if(self._continue):
            path = "graphics/spritesets/"
            x_positions = [self._x1+(self._tile_size*shift) for shift in range(0, int((self._x2-128)/64))]
            
            for position in x_positions:
                decision = randint(1, 100)
                # decision will be set for a 'pity present' every 50 generations.
                if(self._total_generated % 15 == 0): decision = 100
                
                # Determine the event to generate.
                if(decision >= self._present_bound):
                    imgs = [path+"present1.gif", path+"present2.gif"]
                    Present(self._root, self._canvas, choice(imgs), [],
                        position, self._y1, position+48, self._y1+48, self._player)
                    self._total_generated += 1
                elif(decision >= self._balloon_bound):
                    imgs = [path+"balloon1.gif", path+"balloon2.gif"]
                    Balloon(self._root, self._canvas, choice(imgs), [],
                        position, self._y1, position+48, self._y1+48, self._player)
                    self._total_generated += 1
        
            # Update the difficulty of each round depending on the total events generated.
            if(self._present_bound < 98):
                self._present_bound += 0.05
            if(self._balloon_bound > 20):
                self._balloon_bound -= 0.05
            if(self._wait >= 1000):
                self._wait -= 1
            
            # Continue loop.
            self._root.after(int(self._wait), self.event_generation)