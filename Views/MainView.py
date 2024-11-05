import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Controller.Controller import Controller
from Views.SelectionFrame import SelectionFrame
from Views.GraphFrame import GraphFrame


class MainView:
    def __init__(self, root, controller=None):
        """
        Init for Primary View of the app
        :param root: Requires parent window
        :param controller: Controller Module for MVC Architecture
        """
        # Variables:
        self.germ_truth_table = {
            '6deg 200excel_1.xlsx': {
                "A1": 47.5,
                "B1": 114.3,
                "C1": 0.0,
                "D1": 78.9,
                "E1": 0.0,
                "F1": 49.6,
                "F2": 49.3,
                "E2": 29.2,
                "D2": 37.3,
                "C2": 75.6,
                "B2": 72.9,
                "A2": 38.6,
                "A3": 38.3,
                "B3": 34.4,
                "C3": 53.5,
                "D3": 41.8,
                "E3": 36.3,
                "F3": 5.25,
                "F4": 56.8,
                "E4": 0.0,
                "D4": 29.5,
                "C4": 0.0,
                "B4": 70.4,
                "A4": 55.5,
                "A5": 0.0,
                "B5": 41.5,
                "C5": 44.1,
                "D5": 49.4,
                "E5": 53.5,
                "F5": 47.6,
                "F6": 45.2,
                "E6": 41.1,
                "D6": 40.1,
                "C6": 0.0,
                "B6": 45.3,
                "A6": 33.6,
                "A7": 42.8,
                "B7": 38.9,
                "C7": 0.0,
                "D7": 51.6,
                "E7": 61.6,
                "F7": 46.2,
                "F8": 0.0,
                "E8": 38.9,
                "D8": 39.0,
                "C8": 0.0,
                "B8": 86.8,
                "A8": 43.6

            },
            '6deg 200excel_2.xlsx': {
                "A1": 0.0,
                "B1": 48.2,
                "C1": 40.6,
                "D1": 49.6,
                "E1": 101.7,
                "F1": 45.7,
                "F2": 62.7,
                "E2": 42.1,
                "D2": 48.5,
                "C2": 0.0,
                "B2": 53.0,
                "A2": 78.4,
                "A3": 66.2,
                "B3": 38.3,
                "C3": 0.0,
                "D3": 37.9,
                "E3": 44.3,
                "F3": 21.4,
                "F4": 35.5,
                "E4": 55.0,
                "D4": 43.40,
                "C4": 28.3,
                "B4": 31.9,
                "A4": 0.0,
                "A5": 41.6,
                "B5": 40.9,
                "C5": 43.3,
                "D5": 0.0,
                "E5": 71.1,
                "F5": 83.9,
                "F6": 129.1,
                "E6": 41.9,
                "D6": 0.0,
                "C6": 0.0,
                "B6": 51.0,
                "A6": 71.2,
                "A7": 122.5,
                "B7": 100.8,
                "C7": 30.2,
                "D7": 0.0,
                "E7": 70.4,
                "F7": 121.5,
                "F8": 0.0,
                "E8": 0.0,
                "D8": 103.8,
                "C8": 0.0,
                "B8": 0.0,
                "A8": 0.0
            },
            '6deg 200excel_3.xlsx': {
                "A1": 68.8,
                "B1": 120.5,
                "C1": 0.0,
                "D1": 48.8,
                "E1": 68.2,
                "F1": 74.1,
                "F2": 0.0,
                "E2": 51.2,
                "D2": 65.4,
                "C2": 51.4,
                "B2": 41.1,
                "A2": 0.0,
                "A3": 101.6,
                "B3": 0.0,
                "C3": 0.0,
                "D3": 123.6,
                "E3": 0.0,
                "F3": 0.0,
                "F4": 44.0,
                "E4": 48.5,
                "D4": 0.0,
                "C4": 42.6,
                "B4": 0.0,
                "A4": 71.9,
                "A5": 17.6,
                "B5": 54.2,
                "C5": 53.1,
                "D5": 46.5,
                "E5": 154.4,
                "F5": 0.0,
                "F6": 52.6,
                "E6": 0.0,
                "D6": 57.3,
                "C6": 48.9,
                "B6": 0.0,
                "A6": 52.3,
                "A7": 42.0,
                "B7": 0.0,
                "C7": 0.0,
                "D7": 0.0,
                "E7": 17.3,
                "F7": 58.7,
                "F8": 0.0,
                "E8": 78.8,
                "D8": 0.0,
                "C8": 41.9,
                "B8": 65.3,
                "A8": 59.4
            },
            '6deg 200excel_4.xlsx': {
                "A1": 69.0,  # Take less on the top                 [1.28 error] not bad though         GREAT
                "B1": 54.6,  # Pretty Much Spot on                  [0.89 error]                        GREAT
                "C1": 0.0,   # N/A
                "D1": 69.2,  # Take more on the bottom              [42.09 error]                       FAIL    *
                "E1": 46.8,  # Take more on the bottom              [2.40 error]                        GOOD
                "F1": 67.3,  # Take less on the bottom              [1.54 error] not bad though         GREAT
                "F2": 81.9,  # Take more on the bottom              [13.13 error]                       BAD     *
                "E2": 0.0,   # N/A
                "D2": 90.4,  # Take less on the bottom              [2.02 error]                        GOOD
                "C2": 61.9,  # Not to bad, but take more bottom?    [2.67 error]                        GOOD
                "B2": 80.1,  # Pretty much spot on                  [0.25 error]                        GREAT
                "A2": 63.9,  # Take less on the bottom              [3.16 error]                        AVERAGE *
                "A3": 0.0,   # N/A
                "B3": 65.3,  # Pretty munch spot on                 [0.55 error]                        GREAT
                "C3": 67.4,  # Take more on the top                 [3.15 error]                        AVERAGE *
                "D3": 0.0,   # N/A
                "E3": 91.3,  # Take less on the top                 [2.92 error]                        GOOD
                "F3": 0.0,   # N/A
                "F4": 37.2,  # Less on bottom, or more on top       [1.53 error] not bad though         GREAT
                "E4": 56.4,  # Pretty Much spot on                  [0.68 error]                        GREAT
                "D4": 0.0,   # N/A
                "C4": 100.2, # Not Sure                             [2.80 error]                        GOOD
                "B4": 63.0,  # Take more on the top                 [2.26 error]                        GOOD
                "A4": 0.0,   # N/A
                "A5": 41.2,  # Pretty much spot on                  [0.51 error]                        GREAT
                "B5": 62.2,  # SPOT ON!                             [0.04 error]                        GREAT
                "C5": 42.6,  # Pretty much spot on                  [0.91 error]                        GREAT
                "D5": 138.4, # Pretty much spot on (lil messy)      [0.68 error]                        GREAT
                "E5": 62.9,  # Could take off the bottom            [0.16 error]                        GREAT
                "F5": 64.5,  # Pretty much spot on                  [0.75 error]                        GREAT
                "F6": 40.7,  # TOTAL MESS!                          [42.67 error]                       FAIL
                "E6": 0.0,   # N/A
                "D6": 0.0,   # N/A
                "C6": 28.3,  # Bigger baseline, take more off top   [2.84 error]                        GOOD
                "B6": 0.0,   # N/A
                "A6": 0.0,   # N/A
                "A7": 68.5,  # Pretty much spot on                  [0.78 error]                        GREAT
                "B7": 63.3,  # Pretty much spot on                  [0.45 error]                        GREAT
                "C7": 41.2,  # SPOT ON!                             [0.01 error]                        GREAT
                "D7": 0.0,   # N/A
                "E7": 57.1,  # Take more on bottom                  [1.13 error]                        GREAT
                "F7": 55.2,  # SPOT ON!                             [0.01 error]                        GREAT
                "F8": 0.0,   # N/A
                "E8": 55.4,  # Pretty much spot on                  [0.32 error]                        GREAT
                "D8": 80.6,  # Take less on bottom                  [1.26 error]                        GREAT
                "C8": 153.3, # Take more on bottom, messy           [10.71 error]                       FAIL
                "B8": 108.7, # Take less on the top                [0.74 error]                        GREAT
                "A8": 0.0    # N/A
                             # SPOT ON!         =>  x/48   total =  144.45
                             # less bottom      =>  x/48
                             # more bottom      =>  x/48
                             # baseline issue   =>  x/48
                             # less on top      =>  x/48
                             # more on top      =>  x/48
            }
        }

        # Set Root Window
        self.master = root
        self.controller = controller

        # Setup Right Frame
        self.GraphFrame = GraphFrame(root, controller)
        self.controller.add_subscriber(self.GraphFrame)

        # Setup Left Frame
        self.SelectionFrame = SelectionFrame(root, controller)
        self.controller.add_subscriber(self.SelectionFrame)

        # Bindings
        self.master.bind('<Up>', self.up)
        self.master.bind('<Left>', self.up)
        self.master.bind('<Down>', self.down)
        self.master.bind('<Right>', self.down)

    def update(self):
        self.GraphFrame.selected_geno = self.controller.selected_geno

    def export(self):
        self.controller.export_germ()

    def up(self, event):
        self.controller.seed_up()
        self.GraphFrame.update()

    def down(self, event):
        self.controller.seed_down()
        self.GraphFrame.update()

def main():
    """
    Testing Function
    """
    root = tk.Tk()
    app = MainView(root)

if __name__ == '__main__':
    main()
