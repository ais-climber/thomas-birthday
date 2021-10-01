# Player
# Author: Caleb Kisby
# Date: Jun.3.15
# 
# Represents a player event in a general adventure game.

from event import *

class Balloon(Event):
    def __init__(self, init_root, init_canvas, image, animations, init_x1, init_y1, init_x2, init_y2, player):
        """
        Initializes and draws the balloon.  Sets the balloon movement.
        """
        super().__init__(init_root, init_canvas, image, animations, init_x1, init_y1, init_x2, init_y2, tag="damage")
        
        self._player = player
        
        # Set the speed to 8 to make the movement seem natural.
        self._speed = 8
        
        # Set the amount of time to move the balloon up once.
        self._wait = 100
        
        self._root.after(self._wait, self.move_loop)    
    
    def move_loop(self):
        """
        A helper method which moves the balloon upwards until the balloon touches
        a "cleanup" tagged object.
        """
        if(self.collision_detect(UP, "cleanup")):
            self.erase_event()
        elif(self.collision_detect_surround("player")):
            self._player.update_health(self._player._health-1)
        else:
            self.move(UP)
            self._root.after(self._wait, self.move_loop)
