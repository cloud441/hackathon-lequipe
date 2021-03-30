from numpy.random import randint
from pandas.plotting import scatter_matrix
from sklearn import svm, metrics
import matplotlib.pyplot as plt
import pickle

clf_model_file = 'data/clf_model.sav'


class Classifier():

    ''' Train the classifier on pics/key train table. '''
    def train(self, pics_tables, key_tables, gamma=None):
        clf = svm.SVC(gamma=gamma, verbose=True) if gamma else svm.SVC(verbose=True)
        clf.fit(pics_tables, key_tables.values.ravel())

        with open(clf_model_file, 'wb') as f:
            pickle.dump(clf, f)
        self.clf = clf


    def loadModel(self):
        try:
            with open(clf_model_file, 'rb') as f:
                self.clf = pickle.load(f)
            return True

        except (OSError, IOError) as e:
            print("%s not found, you have not trained your classifier model yet." %clf_model_file)
            return False




    ''' Predict the key according to the pic values. '''
    def predict(self, pics_tables):
        return self.clf.predict(pics_tables)


    ''' Print Confusion Matrix to verify classifier model on validation database.
        The mean confusion Matrix is printed. '''
    def ConfusionMatrix(self, valid_pics, valid_keys):
        disp_mat = metrics.plot_confusion_matrix(self.clf, valid_pics, valid_keys)
        disp_mat.figure_.suptitle("Confusion Matrix")

        print(f"Confusion Matrix: \n{disp_mat.confusion_matrix}")
        plt.savefig("confusion_matrix.png")
