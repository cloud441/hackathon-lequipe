import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


''' Class that manages train/validation frame database. '''
class DbManager():

    ''' Open the DB and split into train/valid table. '''
    def openTable(self, data_path):
        table = pd.read_csv(data_path)

        # clean table in case of incomplete frame selection:
        keys_table = table[['key']].dropna()
        frames_table = table.loc[:, table.columns != 'key'].dropna()

        # ratio for splitting is about 70%/30%.
        self.train_frames, self.valid_frames, self.train_keys, self.valid_keys = train_test_split(
                frames_table, keys_table, test_size=0.3)

        self.table = table
