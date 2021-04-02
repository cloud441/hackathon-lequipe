from joblib import Parallel, delayed
import numpy as np
import pandas as pd

BLK_SIZE = 6

''' Class that predicts a password based on the classifier. '''
class PasswordPredictor():

    def __init__(self, clf):
        self.clf = clf


    ''' Call the classifier to predict a key based on the frame. '''
    def predictKey(self, frame):
        return self.clf.predict([frame])

    def predictKeys(self, frames):
        l = frames.values.tolist()
        results = Parallel(n_jobs=-1, verbose=1)(delayed(self.clf.predict)([l[i]]) for i in range(frames.shape[0]))
        return np.vstack(results).flatten()


    ''' Read a flow of frame to build the secret password. '''
    def findPassword(self, keys, i):
        garbageKeys = ["NOKEY", "CTRL"]
        pwd = ""
        enter_blk_size = 0
        cur_blk_size = 1
        stop_blk_size = 0
        last_key = "NOKEY"

        while i < keys.shape[0] and enter_blk_size != BLK_SIZE:
            key = keys[i]
            enter_blk_size = (enter_blk_size + 1) if key == "ENTER" else 0

            if key not in garbageKeys:
                if key != last_key:
                    stop_blk_size += 1

                    if stop_blk_size == BLK_SIZE:
						# save previous key
                        if cur_blk_size > BLK_SIZE:
                            pwd += last_key

						# we have a new block
                        cur_blk_size = 1
                        last_key = key
                        stop_blk_size = 0

                else:
                    stop_blk_size = 0
                    cur_blk_size += 1

            i += 1

        return pwd


    ''' Read a flow of frame and skip until the required key frame block. '''
    def skipUntilKey(self, keys, i, key):
        block_size = 0
        while i < keys.shape[0]:
            block_size = (block_size + 1) if keys[i] == key else 0

            if block_size == BLK_SIZE:
                return i
            i += 1

        # Could not find the required key:
        return -1


    ''' Skip the flow of frame until first CTRL frame block, return the index. '''
    def beginLogin(self, keys):
        return self.skipUntilKey(keys, 0, "CTRL")


    ''' Skip the flow of frame until no key frame block is detected, return the index. '''
    def endLogin(self, keys, i):
        return self.skipUntilKey(keys, i, "NOKEY")


    ''' Predict the password based on frame flow. '''
    def predictPassword(self, pics_table):
        keys = self.predictKeys(pics_table)
        i = self.beginLogin(keys)

        if i == -1:
            print("predictPassword: Could not find CTRL-ALT-SUPPR sequence.")
            return None

        i = self.endLogin(keys, i)

        if i == -1:
            print("predictPassword: Could not find CTRL-ALT-SUPPR sequence.")
            return None

        return self.findPassword(keys, i)
