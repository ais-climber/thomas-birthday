# Menu Manager
# Author: Caleb Kisby
# Date: Jun.3.15
# 
# Manages the menus in a birthday game.

import tkinter as tk
from event import *
from player import *
from maps import *
from generator import *

class MenuManager():
    def __init__(self, init_root, init_canvas, image_path,
        tile_length, canvas_width, canvas_height):
        """
        Sets the parameter attributes of the menu.
        """
        self._root = init_root
        self._canvas = init_canvas
        self._image_path = image_path
        self._map_list = Maps(self._root, self._canvas, [self._image_path])
        
        self._obstacle_generator = Generator(self._root, self._canvas, 0, 
            0, 0, 0, 0, None)
        self._player = ""
        
        self._tile_length = tile_length
        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
        
        self._name_entry = ""
    
    def game_state(self, event):
        """
        Initializes all objects needed for a birthday game.
        """
        # Unbind the 'any' key check.
        self._root.unbind("<Key>")
        
        # Remove all start menu items from the canvas.
        self._canvas.delete(tk.ALL)
        
        # Redraw the map.
        self._map_list = Maps(self._root, self._canvas, [self._image_path])
        
        # Create the player.
        path = "graphics/spritesets/"
        player_animation_lst = [path+"thomas1.gif",
                    path+"thomas2.gif",
                    path+"thomas1.gif",
                    path+"thomas3.gif"]
        self._player = Player(self._root, self._canvas, player_animation_lst[0],
                player_animation_lst,
                128, 128, 128+64, 128+96)
    
        # Create a demo wall.
        self._canvas.create_rectangle(0,0, 2*self._tile_length,self._tile_length*self._canvas_height, 
                    outline="", fill="", tags="wall")
        self._canvas.create_rectangle((self._canvas_width-2)*self._tile_length,0, self._canvas_width*self._tile_length,self._tile_length*self._canvas_height, 
                    outline="", fill="", tags="wall")
        self._canvas.create_rectangle(0,self._canvas_height*self._tile_length, 
                    self._canvas_width*self._tile_length,self._tile_length*self._canvas_height+8, 
                    outline="", fill="", tags="wall")
        self._canvas.create_rectangle(2*self._tile_length,0, (self._canvas_width-2)*self._tile_length,1, 
                    outline="", fill="", tags="cleanup")
        
        # Schedule the creation of obstacles.
        self._obstacle_generator = Generator(self._root, self._canvas, self._tile_length, 
            2*self._tile_length, self._tile_length*(self._canvas_height-1),
            (self._canvas_width-2)*self._tile_length, self._tile_length*self._canvas_height, self._player)
        self._obstacle_generator._continue = True
        
        # Schedule an occasional check for the end of the game.
        self._root.after(100, self.is_game_over)
    
    def is_game_over(self):
        """
        A helper function which calls the game over menu when the
        game is over.
        """
        if(self._player._health <= 0):
            self.game_over_menu()
            return
        self._root.after(100, self.is_game_over)
    
    def call_start_menu(self, event):
        self.start_menu()
    
    def start_menu(self):
        """
        Displays a menu which prompts the user to press Return.
        """
        # Clear the canvas and redraw the map.
        self._canvas.delete(tk.ALL)
        self._map_list = Maps(self._root, self._canvas, [self._image_path])
        
        self._canvas.create_text(self._canvas_width*self._tile_length/2,
                    self._canvas_height*self._tile_length/2-128,
                    text="Happy Birthday, Thomas!", 
                    fill="white", font=("Arial", 36))
        self._canvas.create_text(self._canvas_width*self._tile_length/2,
                    self._canvas_height*self._tile_length/2+64,
                    text="Press Enter to begin.", 
                    fill="white", font=("Arial", 24))
        self._canvas.create_text(2, self._canvas_height*self._tile_length-20,
                    text="Art by Amanda Kisby, Programming by Caleb Kisby, Tested by Ruth(ie) Kisby", 
                    fill="white", font=("Arial", 12), anchor=tk.NW)
        self._canvas.create_text(1024-2, 2,
                    text="Collect presents!", 
                    fill="white", font=("Arial", 16), anchor=tk.NE)
        self._canvas.create_text(1024-2, 30+2,
                    text="Avoid popping your birthday balloons!", 
                    fill="white", font=("Arial", 16), anchor=tk.NE)
        
        # Bind any key to begin the game.
        self._root.bind("<Return>", self.game_state)
    
    def game_over_menu(self):
        """
        Displays a game over menu.  Opens the scoreboard after a key is pressed.
        """
        # Unbind key presses.
        self._up_id = self._root.unbind("<Up>")
        self._down_id = self._root.unbind("<Down>")
        self._left_id = self._root.unbind("<Left>")
        self._right_id = self._root.unbind("<Right>")
        
        # Unbind key releases.
        self._root.unbind("<KeyRelease-Up>")
        self._root.unbind("<KeyRelease-Down>")
        self._root.unbind("<KeyRelease-Left>")
        self._root.unbind("<KeyRelease-Right>")
        
        self._obstacle_generator._continue = False
        self._player._animate_flag = False
        
        self._player.set_speed(0)
        self._player._STAHP = True
        
        self._canvas.delete(tk.ALL)
        self._map_list = Maps(self._root, self._canvas, [self._image_path])
        
        # Stop player and obstacles from flying uncontrollably off of the screen.
        self._canvas.create_rectangle(0,0, self._tile_length*self._canvas_width,self._tile_length*self._canvas_height, 
                    outline="", fill="", tags="cleanup")
        
        # Display game over screen.  Wait for keypress.
        self._canvas.create_text(self._canvas_width*self._tile_length/2,
                    self._canvas_height*self._tile_length/2-32,
                    text="Game Over", 
                    fill="white", font=("Arial", 36))
        self._canvas.create_text(self._canvas_width*self._tile_length/2,
                    self._canvas_height*self._tile_length/2+32,
                    text="Press Enter to continue.", 
                    fill="white", font=("Arial", 24))
        self._root.bind("<Return>", self.name_entry_menu)
    
    def name_entry_menu(self, event):
        """
        Allows the player to enter a 3 letter name for the scoreboard.
        """
        self._root.unbind("<Return>")
        self._canvas.delete(tk.ALL)
        self._map_list = Maps(self._root, self._canvas, [self._image_path])
        
        self._canvas.create_text(self._canvas_width*self._tile_length/2,
                    self._canvas_height*self._tile_length/2-16,
                    text="Please type your name below", 
                    fill="white", font=("Arial", 24))
        self._canvas.create_text(self._canvas_width*self._tile_length/2,
                    self._canvas_height*self._tile_length/2+16,
                    text="and press Enter.", 
                    fill="white", font=("Arial", 24))
        
        self._name_entry = tk.Entry(self._root, background="white", font=("Arial", 20))
        self._name_entry.place(relx=1024/2, rely=640/2)
        self._name_entry.pack()
        
        self._root.bind("<Return>", self.scoreboard_menu)
    
    def scoreboard_menu(self, event):
        """
        Displays the scoreboard.  Opens the start menu after a key is pressed.
        """
        self._root.unbind("<Return>")
        self._canvas.delete(tk.ALL)
        self._map_list = Maps(self._root, self._canvas, [self._image_path])
        
        self.update_scoreboard(self._name_entry.get(), self._player._points)
        self._name_entry.destroy()
        self._canvas.create_text(384, 96,
                    text="High Scores", 
                    fill="white", font=("Arial", 24), anchor=tk.NW)
        
        score_file = open("saves/scoreboard.txt", 'r')
        y_pos = 128+32
        for line in score_file:
            self._canvas.create_text(384, y_pos,
                    text=line.rstrip("\n"), 
                    fill="white", font=("Arial", 24), anchor=tk.NW)
            y_pos += 32
        
        self._canvas.create_text(384,
                    self._canvas_height*self._tile_length-32,
                    text="Press Enter to continue.", 
                    fill="white", font=("Arial", 20), anchor=tk.NW)
        self._root.bind("<Return>", self.call_start_menu)
    
    def update_scoreboard(self, new_name, new_score):
        """
        Updates the scoreboard.txt file with a new score new_score and name new_name.
        """
        file = open("saves/scoreboard.txt", 'r')
        scores = []
        flag = False
        for line in file:
            tup = (line.split("\t")[0], line.split("\t")[1])
            if((new_score > int(tup[1])) and not(flag)):
                scores.append((new_name, str(new_score)+"\n"))
                flag = True
            
            scores.append(tup)
        if(flag):
            scores.pop()
        
        file = open("saves/scoreboard.txt", 'w')
        for score_tup in scores:
            file.write(score_tup[0] + "\t" + score_tup[1])