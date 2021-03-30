import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class DbManager():

    ''' Open the DB and split into train/valid table. '''
    def openTable(self, data_path):
        table = pd.read_csv(data_path)

        keys_table = table[['key']].dropna()
        pics_table = table.loc[:, table.columns != 'key'].dropna()
        # ratio for splitting is about 70%/30%.
        self.train_pics, self.valid_pics, self.train_keys, self.valid_keys = train_test_split(
                pics_table, keys_table, test_size=0.3)

        self.table = table



    ''' Close the DB and flush all remaining data '''
#    def closeTable(self):
#        self.table.close()


# Example of table managment:

#def randomSelection5(table):
#    table_height = table.shape[0]
#    rand_vect = np.random.randint(0, table_height, size=5)
#
#    return table.loc[rand_vect]
#
#
#def midAgeMenFilter(table):
#    return table[(table.sex == 'male') & (table.age >= 30) & (table.age <= 50)]

