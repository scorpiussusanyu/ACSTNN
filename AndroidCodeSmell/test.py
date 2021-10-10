# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2018/09/26
@Description: 
"""
import os
import re
import shutil
import csv
import collections

number_java = {'2048': 3, 'Shaarlier': 54, 'BeHe Explorer': 76, 'NetworkTools': 81, 'ToneDef': 95, 'NextINpact': 113,
               'Ouroboros': 147, 'Lightning': 150, 'Terminal Emulator': 152, 'Birthday Calendar': 158, 'JumpGo': 237,
               'EP Mobile': 304, 'Glucosio': 356, 'GPSLogger': 383, 'Owncloud': 539, 'GnuCash': 548, 'AnkiDroid': 844,
               'Materialistic': 881, 'SoundWaves': 1318, 'Nextcloud': 1338, 'K-9 Mail': 1844, 'Xabber': 2263,
               'Signal Private Messenger': 3411}


def collectJava():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\source"
    apps_directory = os.listdir(path)
    backup = {}
    for i in apps_directory:
        # os.mkdir(paprika_path + "\\" + i)
        # os.mkdir(adoctor_path + "\\" + i)
        app_path = path + "\\" + i
        number = 0
        for root, dirname, filenames in os.walk(app_path):
            for filename in filenames:
                if filename.endswith(".java"):
                    number += 1
        # backup[i] = number / 3
        backup[i] = number
    backup = [(x, backup[x]) for x in backup]
    backup.sort(key=lambda x: x[1])
    total = 0
    apps = {}
    for i in backup:
        total += i[1]
        apps[i[0]] = i[1]
        print(i)
    # print(total)
    print(apps)


def directory_for_Paprika():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\as"
    apps_directory = os.listdir(path)
    paprika_path = "C:\\Users\\MaoMorn\\Desktop\\android\\droidlens2_apkcsv"
    # paprika_path = "C:\\Users\\MaoMorn\\Desktop\\android\\paprika"
    for i in apps_directory:
        app_path = path + "\\" + i
        for j in os.listdir(app_path):
            file = paprika_path + "\\" + i
            if not os.path.exists(file):
                os.mkdir(file)
            file1 = file + "\\" + j[:-4]
            file2 = file + "\\" + j[:-4] + ".db"
            # os.remove(file)
            # shutil.rmtree(file)
            os.mkdir(file1)
            os.mkdir(file2)
            print(file1)
            print(file2)


def directory_for_aDoctor():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\source"
    apps_directory = os.listdir(path)
    adoctor_path = "C:\\Users\\MaoMorn\\Desktop\\android\\aDoctor"
    for i in apps_directory:
        app_path = path + "\\" + i
        for j in os.listdir(app_path):
            if j.endswith(".zip"):
                continue
            file = adoctor_path + "\\" + i
            if not os.path.exists(file):
                os.mkdir(file)
            file += "\\" + j
            # shutil.rmtree(file)
            print(file)
            open(file, "w").close()
    failed = "C:\\Users\\MaoMorn\\Desktop\\android\\source\\AnkiDroid\\Ank-2.10alpha30C:\\Users\\MaoMorn\\Desktop\\android\\source\\AnkiDroid\\Anki-2.10alpha3C:\\Users\\MaoMorn\\Desktop\\android\\source\\AnkiDroid\\Anki-2.9.1C:\\Users\\MaoMorn\\Desktop\\android\\source\\EP Mobile\\epmobile-2.20C:\\Users\\MaoMorn\\Desktop\\android\\source\\EP Mobile\\epmobile-2.21C:\\Users\\MaoMorn\\Desktop\\android\\source\\EP Mobile\\epmobile-2.22C:\\Users\\MaoMorn\\Desktop\\android\\source\\GnuCash\\gnucash-2.2.0C:\\Users\\MaoMorn\\Desktop\\android\\source\\GnuCash\\gnucash-2.3.0C:\\Users\\MaoMorn\\Desktop\\android\\source\\GnuCash\\gnucash-2.4.0C:\\Users\\MaoMorn\\Desktop\\android\\source\\GPSLogger\\gpslogger-102C:\\Users\\MaoMorn\\Desktop\\android\\source\\GPSLogger\\gpslogger-103C:\\Users\\MaoMorn\\Desktop\\android\\source\\GPSLogger\\gpslogger-104C:\\Users\\MaoMorn\\Desktop\\android\\source\\K-9 Mail\\k-9-5.600C:\\Users\\MaoMorn\\Desktop\\android\\source\\K-9 Mail\\k-9-5.700C:\\Users\\MaoMorn\\Desktop\\android\\source\\K-9 Mail\\k-9-5.703C:\\Users\\MaoMorn\\Desktop\\android\\source\\nextcloud\\nextcloud-3.9.0C:\\Users\\MaoMorn\\Desktop\\android\\source\\nextcloud\\nextcloud-3.9.1C:\\Users\\MaoMorn\\Desktop\\android\\source\\nextcloud\\nextcloud-3.9.2C:\\Users\\MaoMorn\\Desktop\\android\\source\\owncloud\\owncloud-2.13C:\\Users\\MaoMorn\\Desktop\\android\\source\\owncloud\\owncloud-2.13.1C:\\Users\\MaoMorn\\Desktop\\android\\source\\owncloud\\owncloud-2.14.1C:\\Users\\MaoMorn\\Desktop\\android\\source\\SoundWaves\\SoundWaves-380C:\\Users\\MaoMorn\\Desktop\\android\\source\\SoundWaves\\SoundWaves-390C:\\Users\\MaoMorn\\Desktop\\android\\source\\SoundWaves\\SoundWaves-424C:\\Users\\MaoMorn\\Desktop\\android\\source\\ToneDef\\ToneDef-18C:\\Users\\MaoMorn\\Desktop\\android\\source\\WebApps\\WebApps-2.20C:\\Users\\MaoMorn\\Desktop\\android\\source\\WebApps\\WebApps-2.22C:\\Users\\MaoMorn\\Desktop\\android\\source\\WebApps\\WebApps-2.23C:\\Users\\MaoMorn\\Desktop\\android\\source\\xabber\\xabber-0.9.30bC:\\Users\\MaoMorn\\Desktop\\android\\source\\xabber\\xabber-1.0.30C:\\Users\\MaoMorn\\Desktop\\android\\source\\xabber\\xabber-2.6.6"


def copy_directort():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\source"
    target = "C:\\Users\\MaoMorn\\Desktop\\android\\as"
    for i in os.listdir(path):
        t = target + "\\" + i
        if not os.path.exists(t):
            os.mkdir(t)
            print(t)


def data_statistics_paprika():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\paprika"
    backup = []
    # smells = collections.defaultdict(int)
    apks = {}
    for app in os.listdir(path):
        version = path + "\\" + app
        smells = collections.defaultdict(int)
        for ver in os.listdir(version):
            if ver.endswith(".db"):
                continue
            temp = version + "\\" + ver
            files = os.listdir(temp)
            if len(files) == 0:
                backup.append(ver)
            else:
                for f in files:
                    if f.endswith("ARGB8888.csv") or f.endswith("BLOB.csv") or f.endswith("CC.csv") or f.endswith(
                            "SAK.csv") or f.endswith("LM.csv"):
                        continue
                    smell = f[f.rindex("_") + 1:-4]
                    file_path = temp + "\\" + f
                    csv_file = open(file_path)
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        smells[smell] += 1
                    smells[smell] -= 1
                    csv_file.close()
            apks[app] = smells
    print(backup)
    print(len(backup))
    data = []
    for i in apks:
        data.append(dict())
        data[-1]["app_name"] = i
        for j in apks[i]:
            data[-1][j] = apks[i][j]
    for i in data:
        print(i)
    # print(data)
    headers = [i for i in data[0]]
    csv_file = open(".\\res\\paprika.csv", "w", newline='')
    csv_writer = csv.DictWriter(csv_file, headers)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    # for i in apks.items():
    #     print(i)
    csv_file.close()


def data_statistics_droidlens2():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\droidlens2"
    backup = []
    # smells = collections.defaultdict(int)
    apks = {}
    for app in os.listdir(path):
        version = path + "\\" + app
        smells = collections.defaultdict(int)
        for ver in os.listdir(version):
            if ver.endswith(".db"):
                continue
            temp = version + "\\" + ver
            files = os.listdir(temp)
            if len(files) == 0:
                backup.append(ver)
            else:
                for f in files:
                    if f.endswith("ARGB8888.csv") or f.endswith("BLOB.csv") or f.endswith("CC.csv") or f.endswith(
                            "SAK.csv") or f.endswith("LM.csv"):
                        continue
                    smell = f[f.rindex("_") + 1:-4]
                    file_path = temp + "\\" + f
                    csv_file = open(file_path)
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        smells[smell] += 1
                    smells[smell] -= 1
                    csv_file.close()
            apks[app] = smells
    print(backup)
    print(len(backup))
    data = []
    for i in apks:
        data.append(dict())
        data[-1]["app_name"] = i
        for j in apks[i]:
            data[-1][j] = apks[i][j]
    for i in data:
        print(i)
    # print(data)
    headers = [i for i in data[0]]
    csv_file = open(".\\res\\droidlens_apk.csv", "w", newline='')
    csv_writer = csv.DictWriter(csv_file, headers)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    # for i in apks.items():
    #     print(i)
    csv_file.close()


def data_statistics_aDoctor():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\aDoctor"
    data = [['DTWC', 0], ['DR', 0], ['DW', 0], ['IDFP', 0], ['IDS', 0], ['ISQLQ', 0], ['IGS', 0], ['LIC', 0], ['LT', 0],
            ['MIM', 0], ['NLMR', 0], ['PD', 0], ['RAM', 0], ['SL', 0], ['UC', 0]]
    smells = {'DTWC': 0, 'DR': 0, 'DW': 0, 'IDFP': 0, 'IDS': 0, 'ISQLQ': 0, 'IGS': 0, 'LIC': 0, 'LT': 0,
              'MIM': 0, 'NLMR': 0, 'PD': 0, 'RAM': 0, 'SL': 0, 'UC': 0}
    data = []
    for app in os.listdir(path):
        version = path + "\\" + app
        data.append({"app_name": app})
        for i in smells:
            data[-1][i] = smells[i]
        count = 0
        for f in os.listdir(version):
            file_path = version + "\\" + f
            file = open(file_path)
            f_csv = csv.DictReader(file)
            for row in f_csv:
                count += 1
                for i in smells:
                    data[-1][i] += int(row[i])
            file.close()
        else:
            if count == 0:
                data[-1].clear()
                data[-1]["app_name"] = app
    for i in data:
        print(i)
    headers = [i for i in data[0]]
    csv_file = open(".\\res\\aDoctor.csv", "w", newline='')
    csv_writer = csv.DictWriter(csv_file, headers)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    # for i in apks.items():
    #     print(i)
    csv_file.close()


def data_statistics_Droidlens():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\Droidlens"
    data = [['DTWC', 0], ['DW', 0], ['IDFP', 0], ['IDS', 0], ['ISQLQ', 0], ['IGS', 0], ['LIC', 0], ['LT', 0],
            ['MIM', 0], ['NLMR', 0], ['PD', 0], ['RAM', 0], ['SL', 0], ['UC', 0], ['DR', 0], ['SC', 0]]
    smells = {'DTWC': 0, 'DW': 0, 'IDFP': 0, 'IDS': 0, 'ISQLQ': 0, 'IGS': 0, 'LIC': 0, 'LT': 0,
              'MIM': 0, 'NLMR': 0, 'PD': 0, 'RAM': 0, 'SL': 0, 'UC': 0, 'DR': 0, 'SC': 0}
    data = []
    for app in os.listdir(path):
        version = path + "\\" + app
        data.append({"app_name": app})
        for i in smells:
            data[-1][i] = smells[i]
        count = 0
        for f in os.listdir(version):
            file_path = version + "\\" + f
            file = open(file_path)
            f_csv = csv.DictReader(file)
            for row in f_csv:
                count += 1
                for i in smells:
                    if row.get(i) is not None:
                        data[-1][i] += (int(row[i]) > 0)
            file.close()
        else:
            if count == 0:
                data[-1].clear()
                data[-1]["app_name"] = app
    for i in data:
        print(i)
    headers = [i for i in data[0]]
    csv_file = open(".\\res\\droidlens_source_files.csv", "w", newline='')
    csv_writer = csv.DictWriter(csv_file, headers)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    # for i in apks.items():
    #     print(i)
    csv_file.close()


def sort_data():
    file_path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\paprika.csv"
    file = open(file_path)
    csv_reader = csv.DictReader(file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    file.close()
    data.sort(key=lambda x: number_java[x["app_name"]])
    for i in data:
        print(i)
    file = open(file_path, "a+", newline='')
    csv_headers = [i for i in data[0]]
    csv_writer = csv.DictWriter(file, csv_headers)
    csv_writer.writerows(data)
    file.close()


def read_csv():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\ApplicationList.csv"
    file = open(path)
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        print(row["Name"] + "&" + row["Number of Files"] + "&" + row["Versions"] + "&" + row[
            "Downloads"] + "\\\\")
    file.close()


import ebugs_refactor.tools.util as util
import time
if __name__ == "__main__":
    util.start_measures()
    for i in range(10):
        time.sleep(1)
        print(i)
    util.stop_measures("test", 0)
    # read_csv()
# print("aDoctor")
# data_statistics_aDoctor()
# print("Droidlens:")

# collectJava()
# sort_data()

# copy_directort()
# directory_for_Paprika()
# import read_apk
# read_apk.droidlens_test()
# data_statistics_paprika()
# data_statistics_droidlens2()
# data_statistics_aDoctor()
# data_statistics_Droidlens()
