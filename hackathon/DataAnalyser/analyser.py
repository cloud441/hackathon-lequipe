from pandas.plotting import scatter_matrix
from sklearn.decomposition import svm, metrics
from numpy.random import randint


class Classifier():

    ''' Train the classifier on pics/key train table. '''
    def train(self, pics_tables, key_tables, gamma):
        clf = svm.SVC(gamma=gamma)
        clf.fit(pics_tables, key_tables)

        self.clf = clf


    ''' Predict the key according to the pic values. '''
    def predict(self, pics_tables):
        return self.clf.predict(pics_tables)


    ''' Print Confusion Matrix to verify classifier model on validation database.
        The mean confusion Matrix is printed. '''
    def ConfusionMatrix(self, table):
        rand_validator = table[randint(0, table.shape[0])]
        key, pics_values = rand_validator[0], rand_validator[1:]

        disp_mat = metrics.plot_confusion_matrix(self.clf, key, pics_values)
