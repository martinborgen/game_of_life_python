# GAME OF LIFE, Martin juli 2020
import tkinter as tk
from tkinter import messagebox as popup
from tkinter import filedialog
import os


class Square(tk.Button):  # the squares in this Game of Life will be buttons, so that the user can select which one to start as alive
    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.col = col
        self.status = "dead"
        self.alive_neighbours = 0
        self.config(bg=self.icon(), command=lambda: self.change_state())

    # method that adds the cells neighbours to a list. intended to be called once at the beginning of the game.
    def add_neighbours(self, cell_list):
        neighbours = []
        for cell in cell_list:
            if cell.row == self.row and cell.col == self.col:
                continue
            if cell.row in range(self.row - 1, self.row + 2) and cell.col in range(self.col - 1, self.col + 2):
                neighbours.append(cell)
        self.neighbours = neighbours

    def check(self):  # checks the neighbours and counts how many are alive
        alive = 0
        for i in self.neighbours:
            if i.status == "alive":
                alive += 1
        self.alive_neighbours = alive

    def update(self):  # updates the cells status based on how many neighbours are alive
        if self.status == "alive":
            if self.alive_neighbours < 2 or self.alive_neighbours > 3:
                self.setstatus("dead")
        elif self.status == "dead" and self.alive_neighbours == 3:
            self.setstatus("alive")

    def icon(self):  # returns a colour based on the cell's state
        if self.status == "alive":
            return "red"
        else:
            return "grey"

    def change_state(self):  # toggles between the two states
        if self.status == "alive":
            self.status = "dead"
        else:
            self.status = "alive"
        self.config(bg=self.icon())

    def setstatus(self, status):  # sets a status and updates the cell
        self.status = status
        self.config(bg=self.icon())


class Board():  # Class containing the board, a list of all cells, and the methods to update all cells.
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game of Life")
        self.board_field = tk.Frame(self.root)
        self.board_field.grid(row=1, column=1)
        self.side = tk.StringVar()
        self.playing = False

        self.cell_list = []
        self.board_list = []

        self.side_menu = tk.Frame(self.root)
        self.side_menu.grid(row=1, column=2)
        self.side_entry = tk.Entry(self.side_menu, textvariable=self.side)
        self.side_entry.pack()
        self.side_confirm_button = tk.Button(
            self.side_menu, text="create board/change size", command=lambda: self.create_board(self.side.get()))
        self.side_confirm_button.pack()
        self.advance_button = tk.Button(
            self.side_menu, text="Advance state", command=lambda: self.refresh())
        self.advance_button.pack()
        self.play_button = tk.Button(
            self.side_menu, text="Play/Pause", command=lambda: self.play_toggle())
        self.play_button.pack()
        self.clear_button = tk.Button(
            self.side_menu, text="Clear", command=lambda: self.clear())
        self.clear_button.pack()
        self.save_button = tk.Button(self.side_menu, text="Save state", command=lambda: self.save_state(
            tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save state of board", filetypes=(("text files", ".txt"),))))
        self.save_button.pack()
        self.load_button = tk.Button(self.side_menu, text="Load state", command=lambda: self.load_state(
            tk.filedialog.askopenfilename(initialdir=os.getcwd(), title="Load a saved state", filetypes=(("text files", ".txt"),))))
        self.load_button.pack()

        self.shift_field = tk.Frame(self.side_menu)
        self.shift_field.pack()
        self.shift_up_button = tk.Button(
            self.shift_field, text="up", command=lambda: self.shift_state("up"))
        self.shift_up_button.grid(row=0, column=1)
        self.shift_down_button = tk.Button(
            self.shift_field, text="down", command=lambda: self.shift_state("down"))
        self.shift_down_button.grid(row=2, column=1)
        self.shift_right_button = tk.Button(
            self.shift_field, text="right", command=lambda: self.shift_state("right"))
        self.shift_right_button.grid(row=1, column=2)
        self.shift_left_button = tk.Button(
            self.shift_field, text="left", command=lambda: self.shift_state("left"))
        self.shift_left_button.grid(row=1, column=0)

    # returns a specific cell instance based on the (row, col) arguments [int]
    def cell(self, row, col):
        for i in self.cell_list:
            if i.row == row and i.col == col:
                return i

    # advances the board one step, by calling the relevant methods in the cells. Must be run as separate loops.
    def refresh(self):
        alive = 0
        for i in self.cell_list:
            i.check()
        for i in self.cell_list:
            i.update()
            if i.status == "alive":
                alive += 1
        if alive == 0 and self.playing == True:
            self.play_toggle()

    def play_toggle(self):  # toggles the self.playing bool, and the relevant buttons, starts the play_func if it's not running
        if self.playing == False:
            self.playing = True
            self.advance_button.config(state="disabled")
            self.play_func()
        else:
            self.playing = False
            self.advance_button.config(state="active")

    def play_func(self):  # calls the refresh method every second if playing == True
        if self.playing == True:
            self.root.after(1000, self.play_func)
            self.refresh()

    def clear(self):  # clears all cells. Will pause if playing.
        if self.playing == True:
            self.play_toggle()
        self.playing = False
        self.advance_button.config(state="active")
        for i in self.cell_list:
            i.status = "dead"
            i.config(bg=i.icon())

    # saves the state of all cells in the board to a .txt file.
    def save_state(self, filename):
        if self.playing == True:
            self.play_toggle()
        if filename == "":
            return
        state = ""
        for row in self.board_list:
            for col in row:
                state += "{} ".format(col.status)
            state += "\n"
        save_to_file(filename, state)

    # loads a previously saved state from a .txt file. Promts to create a larger board if the save is a larger board than the current.
    def load_state(self, filename):
        if self.playing == True:
            self.play_toggle()
        if filename == "":
            return
        loaded = read_from_file(filename)
        if len(loaded) > len(self.board_list):
            size_answer = popup.askyesnocancel(
                message="The saved state is larger than the current board, \nwould you like to create a board of the same size({})?".format(len(loaded)))
            if size_answer == True:
                self.create_board(len(loaded))
            elif size_answer == None:
                return
        for i in self.cell_list:
            if i.status == "alive":
                clear_answer = popup.askyesnocancel(
                    message="Clear the current board before loading?")
                if clear_answer == True:
                    self.clear()
                    break
                elif clear_answer == None:
                    return
                else:
                    break
        state = []
        for i in loaded:
            state.append(i.split())
        for row_n, row in enumerate(state):
            if row_n > len(self.board_list) - 1:
                break
            for col_n, col in enumerate(row):
                if col_n > len(self.board_list[row_n]) - 1:
                    break
                self.board_list[row_n][col_n].setstatus(col)

    # shifts the state of the board by one step in the direction "str". Only one direction at a time.
    def shift_state(self, dir):
        if self.playing == True:
            self.play_toggle()
        oldstate = []
        for row in self.board_list:
            r = []
            for col in row:
                r.append(col.status)
            oldstate.append(r)
        self.clear()

        row_shift = 0
        col_shift = 0
        if dir == "up":
            row_shift = -1
        elif dir == "down":
            row_shift = 1
        elif dir == "right":
            col_shift = 1
        elif dir == "left":
            col_shift = -1

        for row_n, row in enumerate(oldstate):
            if row_n + row_shift not in range(len(self.board_list)):
                continue
            for col_n, col in enumerate(row):
                if col_n + col_shift not in range(len(self.board_list[row_n])):
                    continue
                self.board_list[row_n + row_shift][col_n +
                                                   col_shift].setstatus(col)

    # creates a square board with side length given in the entry field, checks if it's an int, removes the old board if there is one.
    def create_board(self, side):
        if self.playing == True:
            self.play_toggle()
        try:
            side = int(side)
        except ValueError:
            popup.showerror("Error", "Please enter an integer")
            return

        if len(self.cell_list) > 0:
            for i in self.cell_list:
                i.destroy()
        cell_list = []  # will become a continuous list of all cells
        board_list = []  # will become a list of all cells ordered by [row][column]
        for row in range(side):
            r = []
            for col in range(side):
                square = Square(row, col, self.board_field, width=3)
                square.grid(row=row, column=col)
                cell_list.append(square)
                r.append(square)
            board_list.append(r)
        self.cell_list = cell_list
        self.board_list = board_list
        for cell in self.cell_list:
            cell.add_neighbours(self.cell_list)


# writes data to a file. If data is a list, it gives each element a new line.
def save_to_file(filename, data):
    savefile = open(filename, "w")
    if isinstance(data, list):
        for i in data:
            savefile.write("{}\n".format(i))
    else:
        savefile.write(data)


# reads data from a file, returns a list of lines, each line is .strip()ped.
def read_from_file(filename):
    readfile = open(filename, "r").readlines()
    tmp = []
    for i in readfile:
        tmp.append(i.strip())
    return tmp


board = Board()

tk.mainloop()
