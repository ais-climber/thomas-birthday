# Event
# Author: Caleb Kisby
# Date: Jun.2.15
# 
# Represents a general event in a general adventure game.

import tkinter as tk

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Event:
    def __init__(self, init_root, init_canvas, image, animations,
             init_x1, init_y1, init_x2, init_y2, tag="NONE"):
        """
        Initializes the event with a Tkinter canvas and initial coordinates (x1, y1) and (x2, y2) given.
        """
        self._root = init_root
        self._canvas = init_canvas
        self._speed = 16
        self._pos = (init_x1, init_y1, init_x2, init_y2)
        self._frame = tk.PhotoImage(file=image)
        self._animations = [tk.PhotoImage(file=path) for path in animations]
        self._tag = tag
        self._STAHP = False
        
        # Draws the event onto the canvas.
        self._image = self._canvas.create_image(self._pos[0], self._pos[1],
                            image=self._frame, anchor=tk.NW, tags=self._tag)
    
    def get_canvas(self):
        """
        Publicizes the Tkinter canvas associated with the event.
        """
        return self._canvas
    
    def get_speed(self):
        """
        Publicizes the speed of the event.
        """
        return self._speed
    
    def get_pos(self):
        """
        Publicizes the position of the event.
        """
        return self._pos
    
    def get_frame(self):
        """
        Publicizes the current frame of the event.
        """
        return self._frame
    
    def get_animations(self):
        """
        Publicizes the current set of animations of the event.
        """
        return self._animations
    
    def set_canvas(self, a_canvas):
        """
        Sets the Tkinter canvas associated with the event to a_canvas.
        """
        self._canvas = a_canvas
    
    def set_speed(self, a_speed):
        """
        Sets the speed to a_speed, given that a_speed is an integer n>=0.
        """
        if a_speed >= 0:
            self._speed = a_speed
    
    def set_pos(self, x1, y1, x2, y2):
        """
        Updates the position of the event with coordinates (x1, y1), (x2, y2), given that any coordinate c>=0.
        """
        if ((x1 >= 0) and (x2 >= 0) and (y1 >= 0) and (y2 >= 0)):
            self._pos = (x1, y1, x2, y2)
    
    def set_frame(self, a_frame):
        """
        Updates the frame of the event with a_frame.
        """
        self._frame = a_frame
    
    def set_animations(self, animation_lst):
        """
        Updates the animations of the event with animation_lst.
        """
        self._animations = [tk.PhotoImage(item) for item in animation_lst]
    
    def draw_event(self):
        """
        Draws the event onto a Tkinter canvas.
        """
        self._canvas.delete(self._image)
        self._image = self._canvas.create_image(self._pos[0], self._pos[1],
                            image=self._frame, anchor=tk.NW, tags=self._tag)
    def erase_event(self):
        """
        Erases the event from a Tkinter canvas.
        Saves some memory, but does not eliminate the class completely.
        Also may be used to make events temporarily hidden.
        """
        self._canvas.delete(self._image)
        
    def collision_detect(self, direction, tag):
        """
        Returns true if there is another event with tag touching self in a direction.
        """
        # Find the overlap between self and any events in direction.
        overlap = self._canvas.find_overlapping(self._pos[0] + direction[0],
                            self._pos[1] + direction[1],
                            self._pos[2] + direction[0],
                            self._pos[3] + direction[1])
        for event in overlap:
            if self._canvas.itemcget(event, "tags") == tag:
                return True
        return False
    
    def collision_detect_surround(self, tag):
        """
        Returns true if there is another event with tag touching self.  Direction independent.
        """
        # Find the overlap between self and any events.
        overlap = self._canvas.find_overlapping(self._pos[0], self._pos[1], self._pos[2], self._pos[3])
        
        for event in overlap:
            if self._canvas.itemcget(event, "tags") == tag:
                return True
        return False
    
    def get_collision(self, tag):
        """
        Returns a list of events colliding with tag touching self.  Direction independent.
        """
        ret = []
        overlap = self._canvas.find_overlapping(self._pos[0], self._pos[1], self._pos[2], self._pos[3])
        
        for event in overlap:
            if self._canvas.itemcget(event, "tags") == tag:
                ret.append(event)
        return ret
    
    def move(self, direction):
        """
        Redraws the event in the given direction if there is no event blocking the player.
        """
        if not(self.collision_detect(direction, "wall")):
            # Set new positions.
            self.set_pos(self._pos[0] + (self._speed * direction[0]), 
                     self._pos[1] + (self._speed * direction[1]), 
                          self._pos[2] + (self._speed * direction[0]), 
                     self._pos[3] + (self._speed * direction[1]))
        
            # Redraw the event with the new directions.
            if(not(self._STAHP)):
                self.draw_event()
        else:
            return

