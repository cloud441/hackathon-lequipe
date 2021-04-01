# hackathon-lequipe
Git repository of Hackathon 2021 (Energy Data Hack) with "L'equipe" team.

# Pull the database:

```
$ git lfs pull data/keys_freq.csv
```

## Run the project (on Linux):

```
$ virtualenv Hackathon_env 
$ source Hackathon/bin/activate
$ pip install -r requirements.txt
$ chmod 755 run.py
$ ./run.py [train/load]
```
train: Train de classifier model and print the result confusion matrix.
        (also save the model in data/clf_model.sav)

detect: Load the classifier model for key prediction, and try to solve the login and
        the password saved in bin file: data/given_files/data/pics_LOGINMDP.bin
