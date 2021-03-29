import sys

import hackathon.DBManager.manager as db
import hackathon.DataAnalyser.analyser as analyser


''' Entry point of the project '''
def run():
    db_manager = db.DbManager()
    db_manager.openTable("data/keys_freq.csv")

    classifier = analyser.Classifier()
    print("Classifier is training on Train database ...")
    classifier.train(db_manager.train_pics, db_manager.train_keys)

    print("Classifier is predicting on Validation database ...")
    classifier.ConfusionMatrix(db_manager.valid_pics, db_manager.valid_keys)
    print("Done !")


run()
