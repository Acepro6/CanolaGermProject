import tkinter as tk


class SelectionFrame:
    def __init__(self, root, controller=None):
        """

        :param root: Requires parent window
        :param controller: Controller Module for MVC Architecture to communicate with the Model
        """
        self.master = root
        self.controller = controller
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

        self.selected_geno = self.controller.selected_geno

        self.update()

    def update(self):
        # Reset View
        self.frame.destroy()
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

        list_box = tk.Listbox(self.frame, selectmode=tk.SINGLE)
        index = 0
        elements = self.controller.get_dataset_names()
        for name in elements:
            list_box.insert(index, name)
            index += 1
        list_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Button Code
        def item_selected():
            # Pass selected dataset to controller
            self.controller.update_selected(list_box.get(list_box.curselection()))

        def export():
            self.controller.export_germ()

        def settings():
            self.controller.open_settings()

        export_button = tk.Button(self.frame, text='Export Data', command=export)
        export_button.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        selection_button = tk.Button(self.frame, text='Select', command=item_selected)
        selection_button.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        settings_button = tk.Button(self.frame, text='Settings', command=settings)
        settings_button.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
