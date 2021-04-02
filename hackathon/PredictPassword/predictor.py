BLK_SIZE = 6

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
        enter_blk_size = 0
        cur_blk_size = 1
        stop_blk_size = 0
        last_key = "NOKEY"

        while i < frames_table.shape[0] and enter_blk_size != BLK_SIZE:
            key = self.predictKey(frames_table.iloc[i])

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
    def skipUntilKey(self, pics_table, i, key):
        block_size = 0
        while i < pics_table.shape[0]:
            if self.predictKey(pics_table.iloc[i]) == key:
                block_size += 1
            else:
                block_size = 0

            if block_size == BLK_SIZE:
                return i
            i += 1

        # Could not find the required key:
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
