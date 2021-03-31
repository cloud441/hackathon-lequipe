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

    # init function of the class
    def __init__(self, string_to_analyse):
        self.string_to_analyse = string_to_analyse

    # return the len of the string_to_analyse
    def len_of_password(self):
        return self.string_to_analyse

    # retrun the neme char of the string
    #
    # -1 is the error code when we are out of range
    def char_n_of_password(self, n):

        if (n < len(self.string_to_analyse)):
            return self.string_to_analyse[n]
        else:
            print("Error : you want the", n, "eme char of password but passsword have only", len(self.string_to_analyse), "char.")
            return -1

    # main function to analyse the password
    # 
    # return : a list of all possible password
    def analyse_the_password(self):
        password_in = self.string_to_analyse
        password_out = [[]]

        shift = False

        list_of_5_letter_key = ["\n","","Shift"," "]
        list_of_4_letter_key = ["CTRL"]

        i = 0
        while (i < len(password_in)):
            next_letter = analyse_next_lettre(password_in, i)
            
            if (next_letter == -2):
                print("Error in analyse_the_password because we are out of range")
            elif (next_letter == -1):
                if (len(password_out[-1]) != 0):
                    password_out[-1] = password_out[-1][0:-2]
            elif (next_letter == "Shift"):
                shift = True
            elif (next_letter == "ctrl" or next_letter == "\n"):
                password_out.append([])
            else:
                if (shift):
                    password_out[-1] = password_out[-1] + next_letter.upper()
                else:
                    password_out[-1] = password_out[-1] + next_letter
            
            if (next_letter in list_of_4_letter_key):
                i += 4
            elif (next_letter in list_of_5_letter_key):
                i += 5
            else:
                i += 1
        
        return password_out
            