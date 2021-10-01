# Player
# Author: Caleb Kisby
# Date: Jun.3.15
# 
# Represents a player event in a general adventure game.

from menu_manager import *
from event import *
from tkinter import NW

class Player(Event):
    def __init__(self, init_root, init_canvas, image, animations, init_x1, init_y1, init_x2, init_y2):
        """
        Initializes and draws the player.  Sets key press checks.
        """
        super().__init__(init_root, init_canvas, image, animations, init_x1, init_y1, init_x2, init_y2, tag="player")
        
        # A simple attribute which toggles animation.
        self._toggle = 0
        self._animate_flag = True
        
        # A simple attribute which controls the amount of time to change the frame.
        self._wait = 500
        
        # Attributes to monitor the player's health and points.
        self._health = 3
        self._health_events = []
        self._points = 0
        self._score_name = ""
        self._points_display = self._canvas.create_text(896, 0, 
                    text=str(self._points), fill="white", font=("Arial", 24), anchor=NW)
        self.update_health(self._health)
        self.update_points(self._points)
        
        # These attributes keep track of direction keys being held.
        self._hold_up = False
        self._hold_down = False
        self._hold_left = False
        self._hold_right = False
        
        # Bind key presses.
        self._up_id = self._root.bind("<Up>", self.key_up)
        self._down_id = self._root.bind("<Down>", self.key_down)
        self._left_id = self._root.bind("<Left>", self.key_left)
        self._right_id = self._root.bind("<Right>", self.key_right)
        
        # Bind key releases.
        self._root.bind("<KeyRelease-Up>", self.stop_up)
        self._root.bind("<KeyRelease-Down>", self.stop_down)
        self._root.bind("<KeyRelease-Left>", self.stop_left)
        self._root.bind("<KeyRelease-Right>", self.stop_right)
        
        # Schedule animation.
        self._root.after(self._wait, self.change_frame)
    
    # Change frame method is used to animate the player.
    def change_frame(self):
        if(self._animate_flag):
            self.set_frame(self._animations[self._toggle])
            self.draw_event()
            
            # Update the next frame.
            if(self._toggle >= 3):
                self._toggle = 0
            else:
                self._toggle += 1
            
            # Reschedule animation.
            self._root.after(self._wait, self.change_frame)
    
    def update_health(self, new_health):
        """
        A helper function which updates the health given an amount of health new_health.
        This function also redraws the health events.
        """
        self._health = new_health
        for event in self._health_events:
            event.erase_event()
        
        self._health_events = [Event(self._root, self._canvas, "graphics/spritesets/life1.gif", [],
                        0, 64*pos, 0, 64*(pos+1)) for pos in range(0, new_health)]
    
    def update_points(self, new_points):
        """
        A helper function which updates the points given an amount of points new_points.
        This function also redraws the point count.
        """
        self._points = new_points
        
        if((self._points % 500 == 0) and (self._points != 0)):
            self.update_health(self._health+1)
        
        self._canvas.delete(self._points_display)
        self._points_display = self._canvas.create_text(896, 0, 
                    text=str(self._points), fill="white", font=("Arial", 24), anchor=NW)
    
    # Moving methods move the player until they are interrupted.
    def move_up(self):
        if self._hold_up:
            self.move(UP)
            self._root.after(50, self.move_up)
    
    def move_down(self):
        if self._hold_down:
            self.move(DOWN)
            self._root.after(50, self.move_down)
    
    def move_left(self):
        if self._hold_left:
            self.move(LEFT)
            self._root.after(50, self.move_left)
    
    def move_right(self):
        if self._hold_right:
            self.move(RIGHT)
            self._root.after(50, self.move_right)
    
    # Stop methods interrupt the move methods.
    def stop_up(self, event):
        self._hold_up = False
        self._up_id = self._root.bind("<Up>", self.key_up)
    
    def stop_down(self, event):
        self._hold_down = False
        self._down_id = self._root.bind("<Down>", self.key_down)
    
    def stop_left(self, event):
        self._hold_left = False
        self._left_id = self._root.bind("<Left>", self.key_left)
    
    def stop_right(self, event):
        self._hold_right = False
        self._right_id = self._root.bind("<Right>", self.key_right)
    
    # Keypress methods respond to key presses.
    def key_up(self, event):
        self._hold_up = True
        self._root.unbind("<Up>", self._up_id)
        self.move_up()
    
    def key_down(self, event):
        self._hold_down = True
        self._root.unbind("<Down>", self._down_id)
        self.move_down()
    
    def key_left(self, event):
        self._hold_left = True
        self._root.unbind("<Left>", self._left_id)
        self.move_left()
    
    def key_right(self, event):
        self._hold_right = True
        self._root.unbind("<Right>", self._right_id)
        self.move_right()
