def analyse_next_lettre(string, index):
    # function that analyse and return the letter
    # in position index in string
    len_string = len(string)
    
    # if index out of range return the error code -2
    if (index > len_string):
        return -2
    # if hotkey can't be present just retrun the next letter
    elif (index + 4 > len_string):
        return string[index]
    # test all hotkey
    else:
        if (index + 5 > len_string):
            next_4_char = len_string[index:index+4]
            if (next_4_char == "CTRL"):
                return "CTRL"
            else:
                return string[index]
        else:
            next_5_char = len_string[index:index+5]
            if (next_5_char == "SPACE"):
                return " "
            elif (next_5_char == "SHIFT"):
                return "Shift"
            elif (next_5_char == "SUPPR"):
                return -1
            elif (next_5_char == "NOKEY"):
                return ""
            elif (next_5_char == "ENTER"):
                return "\n"
            else:
                return string[index]

class AnalysePassword():

    def __init__(self, string_to_analyse):
        self.string_to_analyse = string_to_analyse

    def len_of_password(self):
        return self.string_to_analyse

    def char_n_of_password(self, n):

        if (n < len(self.string_to_analyse)):
            return self.string_to_analyse[n]
        else:
            print("Error : you want the", n, "eme char of password but passsword have only", len(self.string_to_analyse), "char.")
            return -1