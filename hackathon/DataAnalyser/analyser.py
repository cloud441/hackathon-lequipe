from numpy.random import randint
from pandas.plotting import scatter_matrix
from sklearn import svm, metrics
import matplotlib.pyplot as plt
import pickle


clf_model_file = 'data/clf_model.sav'


''' Class that wraps SVM classifier and ML tools. '''
class Classifier():

    ''' Train the classifier on frame/key train table. '''
    def train(self, frames_table, keys_table, gamma=None):
        clf = svm.SVC(gamma=gamma, verbose=True) if gamma else svm.SVC(verbose=True)
        clf.fit(frames_table, keys_table.values.ravel())

        with open(clf_model_file, 'wb') as f:
            pickle.dump(clf, f)
        self.clf = clf


    ''' Load the SVM model saved during last training. '''
    def loadModel(self):
        try:
            with open(clf_model_file, 'rb') as f:
                self.clf = pickle.load(f)
            return True

        except (OSError, IOError) as e:
            print("%s not found, you have not trained your classifier model yet." %clf_model_file)
            return False




    ''' Predict the key according to the frame values. '''
    def predict(self, frames_table):
        return self.clf.predict(frames_table)


    ''' Build and save Confusion Matrix to verify classifier model on validation database. '''
    def confusionMatrix(self, valid_frames, valid_keys):
        disp_mat = metrics.plot_confusion_matrix(self.clf, valid_frames, valid_keys)
        disp_mat.figure_.suptitle("Confusion Matrix")

        print(f"Confusion Matrix: \n{disp_mat.confusion_matrix}")
        plt.savefig("confusion_matrix.png")
