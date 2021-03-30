import hackathon.DBManager.manager as db
import hackathon.DataAnalyser.analyser as analyser
import hackathon.PredictPassword.predictor as predictor
from data.bin2csv import bin2df

# Error output of confusion matrix invalid call
confusion_msg = "You couldn't build your confusion matrix with loaded model because of random \
train/valid database spliting (confusion matrix could be on trained value)."


''' Entry point of the project '''
def run(argv):
    if len(argv) != 2:
        print("Error: Invalid nb of parameter, 1 (train, load or detect) is required.")
        return

    db_manager = db.DbManager()
    db_manager.openTable("data/keys_freq.csv")
    classifier = analyser.Classifier()

    if argv[1] == 'train':
        print("Classifier is training on Train database ...")
        classifier.train(db_manager.train_pics, db_manager.train_keys)

    elif argv[1] == 'load':
        print("Classifier is loading the model ...")
        if not classifier.loadModel():
            return
    
    elif argv[1] == 'detect':

        # Load classifier
        if not classifier.loadModel():
            print("Could not load classifier model.")
            return

        # Load pics_tables
        bin_path = "./data/given_files/data/pics_LOGINMDP.bin"
        df = bin2df(bin_path)
        

        predict = predictor.PasswordPredictor(classifier)
        print("Searching password...")

        password = predict.predictPassword(df)
        if not password:
            print("Could not find any password.")
        else:
            print("Found password: %s" %password)
        return
        

    else:
        print("Error: Invalid parameter '%s'\nvalid parameter are 'train', 'load' and detect" %argv[1])
        return

    if argv[1] == 'load':
        print(confusion_msg)
        return

    print("Classifier is predicting on Validation database ...")
    classifier.ConfusionMatrix(db_manager.valid_pics, db_manager.valid_keys)
    print("Done !")
