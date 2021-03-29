import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




''' Open the DB and lightly clean it '''
def openTable(data_path):
    table = pd.read_csv(data_path)
    # drop line with none value for a column:
    #table = table.dropna(axis=1)

    return table


''' Close the DB and flush all remaining data '''
def closeTable(table):
    table.close()


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

