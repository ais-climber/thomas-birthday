# Maps
# Author: Caleb Kisby
# Date: Jun.4.15
# 
# A class which stores a collection of map images for a general adventure game.

import tkinter as tk

class Maps:
    def __init__(self, root, canvas, init_maps):
        """
        Initializes and populates a list of map image file paths from init_maps.
        """
        self._root = root
        self._canvas = canvas
        self._maps_list = []
        self.add_maps(init_maps)
        self._current_image = tk.PhotoImage(file=self._maps_list[0])
        self._current = self._canvas.create_image(0,0, image=self._current_image, anchor=tk.NW)
    
    def add_maps(self, a_maps_list):
        """
        Appends each item in a_maps_list to self._maps_list
        """
        for map in a_maps_list:
            self._maps_list.append(map)
    
    def display_map(self, index):
        """
        Deletes the current map and replaces it with the map at index.
        """
        self._canvas.delete(self._current)
        self._current_image = tk.PhotoImage(file=self._maps_list[index])
        self._current = self._canvas.create_image(0,0, image=self._current_image, anchor=tk.NW)