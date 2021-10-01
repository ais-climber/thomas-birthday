# Present
# Author: Caleb Kisby
# Date: Jul.25.15
# 
# Represents a present event in a birthday game.

from event import *

class Present(Event):
    def __init__(self, init_root, init_canvas, image, animations, init_x1, init_y1, init_x2, init_y2, player):
        """
        Initializes and draws the present.  Sets the present movement.
        """
        super().__init__(init_root, init_canvas, image, animations, init_x1, init_y1, init_x2, init_y2, tag="points")
        
        self._player = player
        
        # Set the speed to 8 to make the movement seem natural.
        self._speed = 8
        
        # Set the amount of time to move the balloon up once.
        self._wait = 50
        
        self._root.after(self._wait, self.move_loop)    
    
    def move_loop(self):
        """
        A helper method which moves the present upwards until the present touches
        a "cleanup" tagged object.
        """
        if(self.collision_detect(UP, "cleanup")):
            self.erase_event()
        elif(self.collision_detect_surround("player")):
            self._player.update_points(self._player._points+10)
        else:
            self.move(UP)
            self._root.after(self._wait, self.move_loop)