#!/usr/bin/env python3
import os
import re
import pandas as pd
import glob
import numpy as np

# Compile all binary files into one csv database.

def read_int(f):
    ba = bytearray(4)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.int32)
    return prm[0]
    
def read_double(f):
    ba = bytearray(8)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.double)
    return prm[0]

def read_double_tab(f, n):
    ba = bytearray(8*n)
    nr = f.readinto(ba)
    if nr != len(ba):
        return []
    else:
        prm = np.frombuffer(ba, dtype=np.double)
        return prm
    
def get_pics_from_file(filename):
    # Lecture du fichier d'infos + pics detectes (post-processing KeyFinder)
    print("Ouverture du fichier de pics "+filename)
    f_pic = open(filename, "rb")
    info = dict()
    info["nb_pics"] = read_int(f_pic)
    print("Nb pics par trame: " + str(info["nb_pics"]))
    info["freq_sampling_khz"] = read_double(f_pic)
    print("Frequence d'echantillonnage: " + str(info["freq_sampling_khz"]) + " kHz")
    info["freq_trame_hz"] = read_double(f_pic)
    print("Frequence trame: " + str(info["freq_trame_hz"]) + " Hz")
    info["freq_pic_khz"] = read_double(f_pic)
    print("Frequence pic: " + str(info["freq_pic_khz"]) + " kHz")
    info["norm_fact"] = read_double(f_pic)
    print("Facteur de normalisation: " + str(info["norm_fact"]))
    tab_pics = []
    pics = read_double_tab(f_pic, info["nb_pics"])
    nb_trames = 1
    while len(pics) > 0:
        nb_trames = nb_trames+1
        tab_pics.append(pics)
        pics = read_double_tab(f_pic, info["nb_pics"])
    print("Nb trames: " + str(nb_trames))
    f_pic.close()
    return tab_pics, info

def bin2csv():
    # ls data
    # put in []
    # [key, pic_1, pic_2, ...]
    # write_csv() into data/keys_freq.csv
    # 80% train, 20% validation

    data = {}
    data["key"] = []
    for i in range(1, 18):
        data["pic" + str(i)] = []

    for filename in glob.glob("./given_files/data/*.bin"):
        key = re.search("\_(.*)\.", filename).group(1)
        

        trames, _ = get_pics_from_file(filename)

        for pics in trames:
            data["key"].append(key)
            for i in range(0, 17):
                data["pic" + str(i + 1)].append(pics[i])
        break

    df = pd.DataFrame.from_dict(data)
    df.to_csv("keys_freq.csv", index=False)
                    




if __name__ == "__main__":
    bin2csv()
    
