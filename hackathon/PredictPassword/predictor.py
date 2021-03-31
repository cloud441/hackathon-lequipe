''' Class that predicts a password based on the classifier. '''
class PasswordPredictor():

    def __init__(self, clf):
        self.clf = clf


    ''' Call the classifier to predict a key based on the frame. '''
    def predictKey(self, frame):
        return self.clf.predict([frame])


    ''' Read a flow of frame to build the secret password. '''
    # idea: detect ENTER in the end
    def findPassword(self, frames_table, i):
        garbageKeys = ["NOKEY", "CTRL"]
        pwd = ""

        while i < frames_table.shape[0]:
            key = self.predictKey(frames_table.iloc[i])

            if key == "ENTER":
                return pwd
            if key not in garbageKeys:
                pwd += key

            i += 1

        return pwd


    ''' Read a flow of frame and skip until the required key frame. '''
    def skipUntilKey(self, pics_table, i, key):
        while i < pics_table.shape[0]:
            if self.predictKey(pics_table.iloc[i]) == key:
                return i
            i += 1

        # Couldn't find the required key:
        return -1


    ''' Skip the flow of frame until first CTRL frame, return the index. '''
    def beginLogin(self, pics_table):
        return self.skipUntilKey(pics_table, 0, "CTRL")


    ''' Skip the flow of frame until no key frame is detected, return the index. '''
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
