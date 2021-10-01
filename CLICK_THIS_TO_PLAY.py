# Main
# Author: Caleb Kisby
# Date: Jun.3.15
# 
# Tests the level generator, object movement, and key presses.

from menu_manager import *
import tkinter as tk

def main():
    # Set arbitrary game dimensions.
    tile_length = 64 #Tile length
    canvas_width = 16 #Canvas' width in tiles
    canvas_height = 10 #Canvas' height in tiles
    
    # Draw the canvas.
    root = tk.Tk()
    canvas = tk.Canvas(width=tile_length * canvas_width,
            height=tile_length*canvas_height, 
            background="black")
    canvas.pack()
    root.resizable(width=0, height=0)
    
    # Initialize the menu manager and start the game state.
    menu_manager = MenuManager(root, canvas, "graphics/maps/sample_map.gif",
                    tile_length, canvas_width, canvas_height)
    menu_manager.start_menu()
    
    root.mainloop()

if __name__ == "__main__":
    main()
