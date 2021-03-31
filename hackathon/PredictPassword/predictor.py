''' Class that predicts a password based on the classifier. '''
class PasswordPredictor():

    def __init__(self, clf):
        self.clf = clf


    ''' Call the classifier to predict a key based on the frame. '''
    def predictKey(self, frame):
        return self.clf.predict([frame])


    ''' Read a flow of frame to build the secret password. '''
    def findPassword(self, frames_table, i):
        garbageKeys = ["NOKEY", "CTRL"]
        pwd = ""
        enter_block_size = 0
        cur_block_size = 1
        stop_block_size = 0
        last_key = "NOKEY"

        while i < frames_table.shape[0]:
            key = self.predictKey(frames_table.iloc[i])

            if key == "ENTER":
                enter_block_size += 1
            else:
                enter_block_size = 0

            if enter_block_size == 3:
                return pwd

            if key not in garbageKeys:
                if key != last_key:
                    stop_block_size += 1

                    if stop_block_size == 3:
                        if cur_block_size > 3:
                            pwd += last_key

                        cur_block_size = 1
                        last_key = key
                        stop_block_size = 0

                else:
                    stop_block_size = 0
                    cur_block_size += 1

            i += 1

        return pwd


    ''' Read a flow of frame and skip until the required key frame block. '''
    def skipUntilKey(self, pics_table, i, key):
        block_size = 0
        while i < pics_table.shape[0]:
            if self.predictKey(pics_table.iloc[i]) == key:
                block_size += 1
            else:
                block_size = 0

            if block_size == 3:
                return i
            i += 1

        # Couldn't find the required key:
        return -1


    ''' Skip the flow of frame until first CTRL frame block, return the index. '''
    def beginLogin(self, pics_table):
        return self.skipUntilKey(pics_table, 0, "CTRL")


    ''' Skip the flow of frame until no key frame block is detected, return the index. '''
    def endLogin(self, pics_table, i):
        return self.skipUntilKey(pics_table, i, "NOKEY")


    ''' Predict the password based on frame flow. '''
    def predictPassword(self, pics_table):
        i = self.beginLogin(pics_table)

        if i == -1:
            print("predictPassword: Could not find CTRL-ALT-SUPPR sequence.")
            return None

        i = self.endLogin(pics_table, i)

        if i == -1:
            print("predictPassword: Could not find CTRL-ALT-SUPPR sequence.")
            return None

        return self.findPassword(pics_table, i)
