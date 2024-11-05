import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from whittaker_eilers import WhittakerSmoother


class GraphFrame:
    def __init__(self, root, controller=None):
        """

        :param root: Requires parent window
        :param controller: Controller Module for MVC Architecture to communicate with the Model
        """
        self.master = root
        self.controller = controller
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update(self):
        # Reset View
        self.frame.destroy()
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figure_container = tk.Frame(self.frame)
        self.figure_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.genotype = self.controller.get_genotype(self.controller.selected_geno)
        self.seed = self.genotype.data[self.controller.selected_seed]

        # Combo Box Code
        def combobox_selected(event):
            self.figure_container.destroy()
            self.figure_container = tk.Frame(self.frame)
            self.controller.update_seed(seed_combobox.get())

        n = tk.StringVar()
        seed_combobox = ttk.Combobox(self.frame, width=15, textvariable=n)
        seed_combobox.pack(side=tk.TOP)
        seed_combobox.bind("<<ComboboxSelected>>", combobox_selected)
        seed_combobox['values'] = list(self.genotype.data.keys())

        self.graph()

    def graph(self):
        # Graphing Code
        config = self.controller.get_config()
        intercept_text = tk.StringVar()
        germ_time = tk.Label(self.figure_container, textvariable=intercept_text)
        germ_time.pack(side=tk.TOP)

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_title(self.controller.selected_seed)
        ax.set_xlabel = 'Hours'
        ax.set_ylabel = 'Data Values'
        ax.grid()

        x = self.seed.get_hrs()
        whittaker_smoother = WhittakerSmoother(lmbda=int(config['Smoothing Lambda']), order=2, data_length=len(self.seed.get_dx()))
        raw_y = self.seed.get_dx()
        y = whittaker_smoother.smooth(raw_y)
        crit_idx = self.seed.get_crit_idx()
        ax.plot(x, y)
        ax.plot(x, raw_y, color='blue', label='Raw dx', linewidth=0.5)

        try:
            # Get subsets
            slope_subset, hrs_subset, starting_index = self.seed.get_slope_regression()
            bl_subset, bl_hrs_subset = self.seed.get_baseline_regression()

            # Plot Data
            ax.plot(hrs_subset, y[starting_index: crit_idx + int(config['Past Threshold Reach'])], color='r', label='Germ Subset', linewidth=2)
            ax.plot(bl_hrs_subset, y[5:starting_index], color='yellow', label='Base Subset', linewidth=2)
            ax.plot(x, slope_subset, color='brown', label='Germ Regres.', linestyle='dashed')
            ax.plot(x, bl_subset, color='magenta', label='Base Regres.', linestyle='dashed')

            # Find Intercept of regression lines and save index value
            idx = np.argwhere(np.diff(np.sign(slope_subset - bl_subset))).flatten()
            ax.plot(x[idx], np.array(y)[idx], 'ko')

            x_y_intercept = self.seed.get_intercept()
            intercept_text.set(f"Est. Germ Time [HRS] : {str(x_y_intercept[0])}")
        except:
            print("Couldn't Graph Dormant or Dead Seeds")
            intercept_text.set(f"Est. Germ Time [HRS] : Dormant or Dead")

        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=self.figure_container)
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.figure_container)
        toolbar.update()

        canvas.get_tk_widget().pack()
        self.figure_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



