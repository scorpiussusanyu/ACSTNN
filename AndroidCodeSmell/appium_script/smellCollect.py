# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time:  2021/3/10
@Description: 
"""
import os
import csv

app_names = ["AnkiDroid", "AuroraStore", "Download Navi", "F-Droid", "GitNex", "Glucosio",
             "Materialistic", "NextCloud", "Tasks", "TrebleShot"]
app_file_number = {'Glucosio': 162, 'Download Navi': 197, 'TrebleShot': 215, 'Materialistic': 305, 'AuroraStore': 323,
                   'F-Droid': 335, 'GitNex': 346, 'AnkiDroid': 372, 'NextCloud': 907, 'Tasks': 1312}


def data_statistics_Droidlens():
    path = "C:\\Users\\MaoMorn\\Desktop\\refactor\\Droidlens"
    smells = {'IDFP': 0, 'IGS': 0, 'MIM': 0}
    data = []
    for file_name in os.listdir(path):
        app_name = file_name[:-4]
        data.append({"app_name": app_name})
        for i in smells:
            data[-1][i] = smells[i]
        file_path = path + "\\" + file_name
        file = open(file_path)
        f_csv = csv.DictReader(file)
        for row in f_csv:
            for i in smells:
                if row.get(i) is not None:
                    data[-1][i] += (int(row[i]) > 0)
        file.close()
    for i in data:
        print(i)
    headers = [i for i in data[0]]
    csv_file = open("./data/droidlens_source_files.csv", "w", newline='')
    csv_writer = csv.DictWriter(csv_file, headers)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    # for i in apks.items():
    #     print(i)
    csv_file.close()


def collectJava():
    path = "C:\\Users\\MaoMorn\\Desktop\\refactor"
    backup = {}
    for app_name in app_names:
        # os.mkdir(paprika_path + "\\" + i)
        # os.mkdir(adoctor_path + "\\" + i)
        app_path = path + "\\" + app_name
        number = 0
        for root, dirname, filenames in os.walk(app_path):
            for filename in filenames:
                if filename.endswith(".java"):
                    number += 1
        # backup[i] = number / 3
        backup[app_name] = number
    backup = [(x, backup[x]) for x in backup]
    backup.sort(key=lambda x: x[1])
    total = 0
    apps = {}
    for app_name in backup:
        total += app_name[1]
        apps[app_name[0]] = app_name[1]
        print(app_name)
    # print(total)
    print(apps)


def collect_HMU(app_dir):
    dir_path = ""
    if app_dir:
        dir_path = app_dir
    count = 0
    file_count = 0
    backup = open("./data/backup", "w")
    for root, dirname, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(".java"):
                file_path = root + "\\" + filename
                file = open(file_path, 'r', encoding="utf-8")
                flag = 0
                while 1:
                    try:
                        line = file.readline()
                        if line:
                            t = line.count("new HashMap")
                            if t > 0:
                                count += t
                                if flag == 0:
                                    flag = 1
                                    file_count += 1
                                    print(file_path)
                        else:
                            break
                    except UnicodeDecodeError:
                        pass
                        # print(file_path)
                file.close()
    backup.close()
    print("num of HMU : %d" % count)
    print("num of files : %d" % file_count)
    return count


import os
import csv


def repo_stat():
    base_dir = "F:\\repo_android\\result"
    smells = {"LIC": 0, "IGS": 0, "MIM": 0}
    smell_files = {"LIC": 0, "IGS": 0, "MIM": 0}
    files = []
    count = 0
    for s in os.listdir(base_dir):
        java_path = os.path.join(base_dir, s)
        with open(java_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                files.append(row["Class"])
                count += 1
                flag = 0
                for smell in smells:
                    t = int(row[smell])
                    if t > 0:
                        flag = 1
                        smells[smell] += t
                        smell_files[smell] += 1
                if flag > 0:
                    # files.append(row["Class"])
                    pass

    with open("./data/backup.txt", 'w') as backup:
        for t in files:
            backup.write(t + "\n")
    print(len(files))
    print(smell_files)
    for smell in smell_files:
        print("NO_%s: %d" % (smell, count - smell_files[smell]))
    print(smells)


if __name__ == "__main__":
    # data_statistics_Droidlens()
    # collectJava()
    # collect_HMU("F:\\repo_android\\media\\marco\\Elements\\sources\\success")

    repo_stat()
