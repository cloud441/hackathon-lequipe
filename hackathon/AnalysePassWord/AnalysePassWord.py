
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