import tkinter as tk
from a1_state import State
from a3_agent import Agent
import tkinter.font as tkfont
from a4_game import IsHinger, IsValidMove

# turn = 0
move_count = 0



# Example grid to initialise the State
initial_grid = [
    [2, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 2, 0, 1],
    [0, 0, 0, 1, 0]
]

state = State(initial_grid)
buttons = []

# player_types = [0, 1]  # default Human vs Agent

# agent = Agent((state.rows, state.cols), "Echo")


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

board_frame = tk.Frame(root, bg=BOARD_BG, padx=20, pady=20)
board_frame.grid(row=1, column=0, padx=50)

sidebar = tk.Frame(root,bg=SIDEBAR_COLOUR, padx=20, pady=20)
sidebar.grid(row=1, column=1, sticky="n", padx=6)

title_font = tkfont.Font(family="Helvetica", size=30, weight="bold")
subtitle_font = tkfont.Font(family="Helvetica", size=19)

title = tk.Label(header, text="B1 - Hinger",bg=BG, font=title_font)
title.pack(pady=(0,5))

subtitle = tk.Label(header, text="Instructions: Click a cell to remove a counter! The first player to make a move on a hinger wins the game!",bg=BG, font=subtitle_font)
subtitle.pack()

status_label = tk.Label(sidebar, text="Turn: Human", pady=10, bg=SIDEBAR_COLOUR )
status_label.pack()

moves_label = tk.Label(sidebar, text="Moves: 0", bg=SIDEBAR_COLOUR)
moves_label.pack()

history_box = tk.Listbox(sidebar, height=12, width=20, bg=HISTORY_COLOUR, bd=0)
history_box.pack()


mode_var = tk.StringVar(value="Human vs Agent")

mode_frame = tk.Frame(sidebar, bg=SIDEBAR_COLOUR, pady=10)
mode_frame.pack()
tk.Label(mode_frame, text="Select Mode:", bg=SIDEBAR_COLOUR).pack(anchor="w")

modes = ["Human vs Human", "Human vs Agent", "Agent vs Agent"]
for m in modes:
    tk.Radiobutton(mode_frame, text=m, variable=mode_var, value=m, bg=SIDEBAR_COLOUR).pack(anchor="w")



def on_click(r, c):
    global turn, move_count
      # Ignore clicks if current player is an agent
    # if player_types[turn] == 1:
    #     return
  

    if not IsValidMove(state, r, c):
        print(f"Illegal move at ({r},{c})")
        return

    was_hinger = IsHinger(state, r, c)


    #make move, and update grid? 
    if state.grid[r][c] > 0:
        state.grid[r][c] -= 1
        buttons[r][c].config(text=str(state.grid[r][c]), bg=CELL_BG)
        print(f"Button clicked at ({r}, {c}) -> New value : {state.grid[r][c]}")
        print(state)
    else:
        print(f"Cell ({r}, {c}) is already empty!")
    
 
    move_count += 1
    moves_label.config(text=f"Moves: {move_count}")
    # history_box.insert(tk.END, f"Player {turn+1} moved at ({r},{c})")

    # # Check hinger
    # if was_hinger:
    #     end_game(f"Player {turn+1} HIT A HINGER AND WINS!")
    #     return

    # # Check draw
    # if all(state.grid[row][col] == 0 for row in range(state.rows) for col in range(state.cols)):
    #     end_game("DRAW! All counters removed.")
    #     return

    # Switch turn
    # turn = 1 - turn
    # status_label.config(text=f"Turn: Player {turn+1}")

    # # Automatic agent move if next turn is agent
    # if player_types[turn] == 1:
    #     root.after(500, agent_move)
# ---------------------------
# Agent logic
# # ---------------------------
# agent = Agent((state.rows, state.cols), "Echo")

# def agent_move():
#     global turn
#     # Agent uses minimax
#     _, move = agent.move(state, 'minimax')
#     if move:
#         on_click(*move)


# def get_player_types():
#     mode = mode_var.get()
#     if mode == "Human vs Human":
#         return [0, 0]
#     elif mode == "Human vs Agent":
#         return [0, 1]
#     elif mode == "Agent vs Agent":
#         return [1, 1]



# ---------------------------
# Start Game Button
# ---------------------------
# def start_game():
#     global player_types, turn, move_count
#     player_types = get_player_types()
#     turn = 0
#     move_count = 0

#     # Reset board display
#     for r in range(state.rows):
#         for c in range(state.cols):
#             buttons[r][c].config(
#                 text=str(state.grid[r][c]),
#                 bg=CELL_BG,
#                 state="normal"
#             )
#     status_label.config(text=f"Turn: Player {turn+1}")
#     moves_label.config(text=f"Moves: {move_count}")
#     history_box.delete(0, tk.END)

#     # If first turn is agent, start automatic move
#     if player_types[turn] == 1:
#         root.after(500, agent_move)

# tk.Button(sidebar, text="Start Game", command=start_game, bg="#9DCFF5").pack(pady=10)


root.configure(bg=BG)
board_frame.configure(bg=BOARD_BG, relief="groove", bd=6)

# def end_game(message):
#     """End the game: disable all buttons and show message"""
#     for row in buttons:
#         for btn in row:
#             btn.config(state="disabled")
#     status_label.config(text=message)


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




