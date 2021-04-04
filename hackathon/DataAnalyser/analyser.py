from joblib import Parallel, delayed
from numpy.random import randint
from pandas.plotting import scatter_matrix
from sklearn import svm, metrics
import matplotlib.pyplot as plt
import numpy as np
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


    ''' Call the predict method on all keys according to frame values. '''
    def predictKeys(self, frames_tables):
        frames_list = frames_tables.values.tolist()
        # We compute all prediction with multi-threading approach to gain time:
        results = Parallel(n_jobs=-1, verbose=1)(delayed(self.predict)([frames_list[i]]) for i in range(frames_tables.shape[0]))
        return np.vstack(results).flatten()

    ''' Compute the model validation score on Validation Database. '''
    def validationScore(self, valid_frames, valid_keys):
        predicted_keys = self.predictKeys(valid_frames)
        return metrics.accuracy_score(valid_keys, predicted_keys)


    ''' Build and save Confusion Matrix to verify classifier model on validation database. '''
    def confusionMatrix(self, valid_frames, valid_keys):
        disp_mat = metrics.plot_confusion_matrix(self.clf, valid_frames, valid_keys)
        disp_mat.figure_.suptitle("Confusion Matrix")

        print(f"Confusion Matrix: \n{disp_mat.confusion_matrix}")
        plt.savefig("confusion_matrix.png")
