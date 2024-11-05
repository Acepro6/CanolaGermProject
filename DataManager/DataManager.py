import glob
import os.path
import tkinter.filedialog
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfile

# TODO : Finish Documentation

class DataManager:
    """

    """
    def __init__(self):
        """

        """
        # Data Manager basically only needs to know where to find the data that has already been activated!
        # self.dataset_directories = []
        self.active_directory = self._openFile()
        self.active_data = self._loadAllData(self.active_directory)

    def export_germ_times(self, data):
        path = tkinter.filedialog.askdirectory(title="Save Germ Data")
        datatoexcel = pd.ExcelWriter(path + "\\" + 'germdata_' + str(0) + '.xlsx')

        for title in list(data.keys()):
            df = pd.DataFrame.from_dict(data[title], orient='index')
            df.to_excel(datatoexcel, sheet_name=title)

        datatoexcel.close()
        print('Data has been exported to ' + path)

    def _openFile(self):
        return tkinter.filedialog.askdirectory(title="Open Excel Data")

    def _loadAllData(self, path):
        all_files = glob.glob(path + "/*.xlsx")
        li = {}
        for filename in all_files:
            title = os.path.basename(filename)
            df = self._createDataframe(filename)
            li[title] = df

        return li
    def _storeData(self, df):
        fname = asksaveasfile(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        df.to_excel(fname)

    def _createDataframe(self, filename):
        df = pd.read_excel(
            filename,
            header=21,
            usecols="E,G:BB"
        )

        return df

    def load_new_data(self):
        # Get file PATH
        file = self._openFile()

        ###########################################################
        # Load Data into a Pandas Dataframe
        # Scheme:
        #  +------------------------------------+
        #  |   P1       P5      P9       P13    |
        #  |   P2       P6      P10      P14    |
        #  |   P3       P7      P11      P15    |
        #  |   P4       P8      P12      P16    |
        #  +------------------------------------+
        ###########################################################

        # Load and Convert Data to Pandas Dataframe
        df = self._createDataframe(file)
        title = os.path.basename(file)
        self.active_data[title] = df






