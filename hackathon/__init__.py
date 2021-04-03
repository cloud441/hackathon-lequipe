from data.bin2csv import bin2df
import hackathon.DBManager.manager as db
import hackathon.DataAnalyser.analyser as analyser
import hackathon.PredictPassword.predictor as predictor

confusion_msg = "You couldn't build your confusion matrix with loaded model because of random \
train/valid database spliting (confusion matrix could be on trained value)."
password_bin = "./data/given_files/data/pics_LOGINMDP.bin"


''' Entry point of the project '''
def run(argv):
    if len(argv) != 2:
        print("Error: Invalid nb of parameter, 1 (train or detect) is required.")
        return

    # Load the database:
    db_manager = db.DbManager()
    db_manager.openTable("data/keys_freq.csv")
    classifier = analyser.Classifier()

    # Train the SVM classifier on frame database:
    if argv[1] == 'train':
        print("Classifier is training on Train database ...")
        classifier.train(db_manager.train_frames, db_manager.train_keys)

    # Try to determine the password based on the input frame:
    elif argv[1] == 'detect':
        print("Classifier is loading the model ...")
        if not classifier.loadModel():
            return

        print("Loading the password frame ...")
        pwd_frame = bin2df(password_bin)

        predict = predictor.PasswordPredictor(classifier)
        print("Searching password...")
        password = predict.predictPassword(pwd_frame)

        if not password:
            print("Could not find any password in the frame.")
        else:
            print("password is found:\n%s" %password)

    # Bad command option case:
    else:
        print("Error: Invalid parameter '%s'\nvalid parameters are 'train' and 'detect'" %argv[1])
        return

    # In train case, the model is validated by analysing the confusion matrix:
    if argv[1] == 'train':
        print("Classifier is computing the validation score ...")
        classifier.validationScore(db.manager.valid_frames, db_manager.valid_keys)
        print("Classifier is predicting on Validation database ...")
        classifier.confusionMatrix(db_manager.valid_frames, db_manager.valid_keys)
