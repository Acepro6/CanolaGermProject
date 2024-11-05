import json

import DataManager.DataManager as dm
import numpy as np
from Utilities import Calculator, GenotypeData


class Model:
    def __init__(self):
        self.dm = dm.DataManager()
        self.raw_data = self.dm.active_data
        self.genotype = None
        self.config = self.pull_config()

    # GETTERS
    def get_seed(self, title, seed):
        temp = self.get_genotype(title)
        seed_data = temp.data[seed]
        return seed_data

    def get_genotype(self, title):
        if title is None:
            return None
        self.genotype = GenotypeData.GenotypeData(title, self.raw_data[title], self.config)
        return self.genotype

    def get_dataset_names(self):
        return self.dm.active_data.keys()

    def get_config(self):
        return self.config

    def pull_config(self):
        with open('C:\\Users\\Fritzkea\\PycharmProjects\\CanolaGermProjectV4\\Model\\config.json', 'r') as config_file:
            config = json.load(config_file)

        return config

    def update_config(self):
        with open('C:\\Users\\Fritzkea\\PycharmProjects\\CanolaGermProjectV4\\Model\\config.json', 'r') as config_file:
            config = json.load(config_file)

        self.config = config

    # UTILITY METHODS
    def export_germ_data(self):
        """
        Sends over data (NOT raw_data OR pd.df), made up of genotype and seed ADT objects
        """
        germ_data = {}

        for dataset in list(self.raw_data.keys()):
            temp = self.get_genotype(dataset)
            sub_data = {}
            for seed in temp.data.keys():
                if seed == 'HRS':
                    continue

                if temp.data[seed].get_intercept() == 0:
                    sub_data[seed] = {
                        'Germtime': 'N/A',
                        'Slope Coefficient': 'N/A',
                        'OCR Average': temp.data[seed].get_OCR_avg()
                    }
                else:
                    sub_data[seed] = {
                        'Germtime': temp.data[seed].get_intercept()[0],
                        'Slope Coefficient': temp.data[seed].get_coefficient(),
                        'OCR Average' : temp.data[seed].get_OCR_avg()
                    }


            germ_data[dataset] = sub_data

        # TODO : SEND DATA OBJECTS TO DATA MANAGER FOR EXPORT! DON'T FORGET!
        self.dm.export_germ_times(germ_data)


def main():
    """
    TESTING FUNCTION
    """
    model = Model()
    print(model.dm.active_data.keys())
    print(model.genotypes.keys())
    print(model.genotypes['2024_1.xlsx'].data['A1'].get_title())
    print(model.genotypes['2024_1.xlsx'].data['A1'].get_data())
    print(model.genotypes['2024_1.xlsx'].data['A1'].get_intercept())
    print(model.genotypes['2024_1.xlsx'].data['A1'].get_baseline_regression())
    print(model.genotypes['2024_1.xlsx'].data['A1'].get_slope_regression())


if __name__ == '__main__':
    main()
