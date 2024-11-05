import pandas as pd
from Utilities import SeedData

class GenotypeData:
    def __init__(self, title, df: pd.DataFrame, config):
        # Data Variables
        self.title = title
        self.columns = []
        self.hours = df['HRS']
        self.config = config
        self.data = self.generate_seeds(df)

    def generate_seeds(self, df: pd.DataFrame):
        seed_columns = {}
        for seed in df:
            if seed == 'HRS':
                continue
            self.columns.append(seed)
            seed_columns[seed] = SeedData.SeedData(seed, self.hours, df[seed], self.config)

        return seed_columns
