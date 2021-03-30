
class PasswordPredictor():

    def __init__(self, clf):
        self.clf = clf


    def predictKey(self, row):
        return self.clf.predict([row])


    """ idea: detect ENTER in the end"""
    def findPassword(self, pics_table, i):
        garbageKeys = ["NOKEY", "CTRL"]
        
        passwd = ""
        while i < pics_table.shape[0]:
            key = self.predictKey(pics_table.iloc[i])
            
            if key == "ENTER":
                return passwd
            elif key not in garbageKeys:
                passwd += key
            
            i += 1

        return passwd


    def skipUntilKey(self, pics_table, i, key):
        while i < pics_table.shape[0]:
            if self.predictKey(pics_table.iloc[i]) == key:
                return i
            i += 1

        # Could not find key
        return -1


    """ idea: detect only CTRL, when not pressed anymore it is passwd"""
    def beginLogin(self, pics_table):
        return self.skipUntilKey(pics_table, 0, "CTRL")


    def endLogin(self, pics_table, i):
        return self.skipUntilKey(pics_table, i, "NOKEY")


    def predictPassword(self, pics_table):
        
        i = self.beginLogin(pics_table)
        
        if i == -1:
            print("predictPassword: Could not find CTRL-ALT-SUPPR sequence.")
        
        i = self.endLogin(pics_table, i)
        
        if i == -1:
            print("predictPassword: Could not find CTRL-ALT-SUPPR sequence.")

        return self.findPassword(pics_table, i)

