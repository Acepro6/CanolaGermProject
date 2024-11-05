import json
import tkinter as tk

class Controller:
    # TODO : Finish Documentation!
    def __init__(self, model):
        self.model = model
        self.subscribers = []
        self.selected_geno = None
        self.selected_seed = 'A1'
        self.config = self.model.pull_config()

    def get_dataset_names(self):
        return self.model.get_dataset_names()

    def get_config(self):
        return self.config

    def get_seed(self, title, seed):
        return self.model.get_seed(title, seed)

    def get_genotype(self, title):
        return self.model.get_genotype(title)

    def export_germ(self):
        self.model.export_germ_data()

    def update_selected(self, selected):
        self.selected_geno = selected
        self.notify_subscribers()

    def update_seed(self, seed):
        self.selected_seed = seed
        self.notify_subscribers()

    def seed_down(self):
        print("Down Arrow Pressed")
        geno = self.model.genotype
        data_titles = list(geno.data.keys())
        idx = data_titles.index(self.selected_seed)
        self.selected_seed = data_titles[idx + 1]
        print(self.selected_seed)

    def seed_up(self):
        print("Up Arrow Pressed")
        geno = self.model.genotype
        data_titles = list(geno.data.keys())
        idx = data_titles.index(self.selected_seed)
        self.selected_seed = data_titles[idx - 1]
        print(self.selected_seed)

    def open_settings(self):
        window = tk.Tk()

        left_frame = tk.Frame(window)
        left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        smoothing_lambda = tk.Label(left_frame, text="Smoothing Lambda: ")
        crit_thresh = tk.Label(left_frame, text="Critical Threshold: ")
        low_thresh = tk.Label(left_frame, text="Lower Threshold: ")
        past_reach = tk.Label(left_frame, text="Threshold Look Ahead: ")
        bl_subset_replace = tk.Label(left_frame, text="BL Sub Replacement Line: ")
        bl_size_lim = tk.Label(left_frame, text="BL minimum data size: ")

        smoothing_lambda.grid(row=0, column=0)
        crit_thresh.grid(row=1, column=0)
        low_thresh.grid(row=2, column=0)
        past_reach.grid(row=3, column=0)
        bl_subset_replace.grid(row=4, column=0)
        bl_size_lim.grid(row=5, column=0)

        field_smoothing_lambda = tk.Entry(left_frame)
        field_crit_thresh = tk.Entry(left_frame)
        field_low_thresh = tk.Entry(left_frame)
        field_past_reach = tk.Entry(left_frame)
        field_bl_subset_replace = tk.Entry(left_frame)
        field_bl_size_lim = tk.Entry(left_frame)
        excel_dx_status = tk.BooleanVar()
        chk_button_Excel_dx = tk.Checkbutton(left_frame,
                                             text="Excel DX (Not Working)",
                                             variable=excel_dx_status,
                                             onvalue=True,
                                             offvalue=False
                                             )

        field_smoothing_lambda.insert(0, self.config['Smoothing Lambda'])
        field_crit_thresh.insert(0, self.config['Critical Threshold'])
        field_low_thresh.insert(0, self.config['Lower Threshold'])
        field_past_reach.insert(0, self.config['Past Threshold Reach'])
        field_bl_subset_replace.insert(0, self.config['BL Subset Replacement'])
        field_bl_size_lim.insert(0, self.config['BL Substitute Size Limit'])
        if self.config['Excel DX'] == True:
            chk_button_Excel_dx.select()
        elif self.config['Excel DX'] == False:
            chk_button_Excel_dx.deselect()

        field_smoothing_lambda.grid(row=0, column=1, padx="2.5", pady="2.5")
        field_crit_thresh.grid(row=1, column=1, padx="2.5", pady="2.5")
        field_low_thresh.grid(row=2, column=1, padx="2.5", pady="2.5")
        field_past_reach.grid(row=3, column=1, padx="2.5", pady="2.5")
        field_bl_subset_replace.grid(row=4, column=1, padx="2.5", pady="2.5")
        field_bl_size_lim.grid(row=5, column=1, padx="2.5", pady="2.5")
        chk_button_Excel_dx.grid(row=6, column=1, padx="2.5", pady="2.5")

        def apply_settings():
            self.config['Smoothing Lambda'] = field_smoothing_lambda.get()
            self.config['Critical Threshold'] = field_crit_thresh.get()
            self.config['Lower Threshold'] = field_low_thresh.get()
            self.config['Past Threshold Reach'] = field_past_reach.get()
            self.config['BL Subset Replacement'] = field_bl_subset_replace.get()
            self.config['BL Substitute Size Limit'] = field_bl_size_lim.get()
            self.config['Excel DX'] = excel_dx_status.get()

            with open('C:\\Users\\Fritzkea\\PycharmProjects\\CanolaGermProjectV4\\Model\\config.json', 'w') as config_file:
                json.dump(self.config, config_file)

            # Pull New Settings & Update UI
            self.model.update_config()
            self.notify_subscribers()

        apply_button = tk.Button(window, text='Apply', command=apply_settings)
        apply_button.pack(side=tk.BOTTOM, pady="2.5")

        window.mainloop()

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def notify_subscribers(self):
        for sub in self.subscribers:
            sub.update()
