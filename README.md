# hackathon-lequipe
Git repository of Hackathon 2021 (Energy Data Hack) with "L'equipe" team.

# Pull the database:

```
$ git lfs pull data/keys_freq.csv
```

## Run the project:

```
$ chmod 755 run.py
$ ./run.py [train/load]
```
train: Train de classifier model and print the result confusion matrix.
        (also save the model in data/clf_model.sav)

load: Load the classifier model for key prediction.
