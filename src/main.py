import tkinter as tk
from chess_gui import ChessGUI

def start_game():
    root = tk.Tk()
    root.geometry("420x480")
    root.resizable(False, False)
    chess_gui = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_game()
