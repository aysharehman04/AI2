import tkinter as tk
from a1_state import State
from a3_agent import Agent
import tkinter.font as tkfont






# Example grid to initialise the State
initial_grid = [
    [2, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 2, 0, 1],
    [0, 0, 0, 1, 0]
]

state = State(initial_grid)
buttons = []

def on_click(r, c):
    #make move, and update grid? 
    if state.grid[r][c] > 0:
        state.grid[r][c] -= 1
        buttons[r][c].config(text=str(state.grid[r][c]), bg=CELL_BG)
        print(f"Button clicked at ({r}, {c}) -> New value : {state.grid[r][c]}")
        print(state)
    else:
        print(f"Cell ({r}, {c}) is already empty!")

root = tk.Tk()
root.geometry('1020x700') 

root.title("B1 Hinger Game")
BG = "#FBFF91"
BOARD_BG = "#9DCFF5"
CELL_BG = "#FCC5F7"
COUNTER_COLOUR = "#2b8cc4"
HINGER_COLOUR = "#ff6b6b"
EMPTY_COLOUR = "#e8e8e8"
SIDEBAR_COLOUR = "#D1FCC5"
HISTORY_COLOUR = "#E1FFD9"


header = tk.Frame(root, bg=BG, pady=10, padx=60)
header.grid(row=0, column=0, columnspan=2, sticky="ew")

board_frame = tk.Frame(root, bg=BOARD_BG, padx=50, pady=50)
board_frame.grid(row=1, column=0, padx=50)

sidebar = tk.Frame(root,bg=SIDEBAR_COLOUR, padx=20, pady=20)
sidebar.grid(row=1, column=1, sticky="n", padx=6)

title_font = tkfont.Font(family="Helvetica", size=30, weight="bold")
subtitle_font = tkfont.Font(family="Helvetica", size=19)

title = tk.Label(header, text="B1 — Hinger",bg=BG, font=title_font)
title.pack(pady=(0,5))

subtitle = tk.Label(header, text=" Instructions: Click a cell to remove a counter! The first player to make a move on a hinger wins the game!",bg=BG, font=subtitle_font)
subtitle.pack()

status_label = tk.Label(sidebar, text="Turn: Human", pady=10, bg=SIDEBAR_COLOUR )
status_label.pack()

moves_label = tk.Label(sidebar, text="Moves: 0", bg=SIDEBAR_COLOUR)
moves_label.pack()

history_box = tk.Listbox(sidebar, height=12, width=20, bg=HISTORY_COLOUR, bd=0)
history_box.pack()


root.configure(bg=BG)
board_frame.configure(bg=BOARD_BG, relief="groove", bd=6)




for r in range(state.rows):
    row_buttons = []
    for c in range(state.cols):
        cell_frame = tk.Frame(board_frame, bg=CELL_BG, padx=1, pady=1)
        cell_frame.grid(row=r, column=c, padx=4, pady=4)

        lbl = tk.Label(
            cell_frame,
            text=str(state.grid[r][c]),
            bg=CELL_BG,          
            fg="black",
            width= 9,            
            height=5,             
            font=("Helvetica", 18, "bold"),
            bd=0,
            relief="flat"
        )
        lbl.pack(expand=True, fill="both")

        # bind click to label (use lambda to capture r,c)
        lbl.bind("<Button-1>", lambda e, r=r, c=c: on_click(r, c))

        row_buttons.append(lbl)
        # btn = tk.Button(
        #     cell_frame, 
        #     width=8,
        #     height=4,
        #     bg=CELL_BG,
        #     activebackground="#F8B7F0",
        #     text=str(state.grid[r][c]),
        #     command=lambda r=r ,c=c: on_click(r,c),
        #     highlightthickness=0,
        #     relief="solid"
        # )
        # btn.grid(row=r, column=c,padx=4, pady=4)
        # row_buttons.append(btn)
    buttons.append(row_buttons)




root.mainloop()




