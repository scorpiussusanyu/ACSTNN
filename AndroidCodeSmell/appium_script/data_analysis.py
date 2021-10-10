# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time:  2020/12/30
@Description: 
"""
import openpyxl

import cliffsDelta
from appium_script.script import setting
import os
import csv
import scipy.stats
import math

target_versions = ['0', '1', '2', '3', '7']
metric_files = ["%s_energy.csv", "cpu.csv", "frame.csv", "memory.csv"]
app_file_number = {'Glucosio': 162, 'Download Navi': 197, 'TrebleShot': 215, 'Materialistic': 305, 'AuroraStore': 323,
                   'F-Droid': 335, 'GitNex': 346, 'AnkiDroid': 372, 'NextCloud': 907, 'Tasks': 1312}


def cpu(path):
    sum_data, count = 0, 0
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            t = int(row['delat_proc'])
            if t > 0:
                count += 1
                sum_data += t
    print(sum_data // count)
    return None


def frame():
    data = {}
    for apk_name in setting.APKS:
        # print(apk_name)
        base_path = os.path.join(setting.BASE_DIR, apk_name)
        data[apk_name] = {}
        for version in target_versions:
            sum_fps, count_fps = 0, 0
            sum_delay, count_delay = 0, 0
            dir_path = os.path.join(base_path, version)
            path = os.path.join(dir_path, "frame.csv")
            with open(path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        t = eval(row["fps"])
                        sum_fps += t
                        count_fps += 1
                    except:
                        continue
                    try:
                        t = eval(row["delay_count"])
                        sum_delay += t
                        count_delay += 1
                    except:
                        continue
            try:
                data[apk_name][version] = {}
                data[apk_name][version]["delay"] = sum_delay / count_delay
                data[apk_name][version]["fps"] = sum_fps / count_fps
            except ZeroDivisionError:
                print(apk_name + " " + version)
    return data


def memory():
    data = {}
    for apk_name in setting.APKS:
        # print(apk_name)
        base_path = os.path.join(setting.BASE_DIR, apk_name)
        data[apk_name] = {}
        for version in target_versions:
            sum_data, count = 0, 0
            dir_path = os.path.join(base_path, version)
            path = os.path.join(dir_path, "memory.csv")
            with open(path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        t = eval(row["pss"])
                        sum_data += t
                        count += 1
                    except:
                        continue
            try:
                data[apk_name][version] = {"memory": sum_data / count}
            except ZeroDivisionError:
                print(apk_name + " " + version)
    return data


def energy():
    data = {}
    for apk_name in setting.APKS:
        data[apk_name] = {}
        # print(apk_name)
        base_path = os.path.join(setting.BASE_DIR, apk_name)
        energy_path = "%s_Energy.csv" % setting.APKS[apk_name]['appPackage']
        for version in target_versions:
            dir_path = os.path.join(base_path, version)
            energy_file = os.path.join(dir_path, energy_path)
            sum_data, count = 0, 0
            with open(energy_file) as file:
                reader = csv.reader(file)
                for row in reader:
                    for i in row:
                        try:
                            t = int(i)
                            sum_data += t
                            count += 1
                        except:
                            continue
            data[apk_name][version] = {"energy": sum_data / count}
    return data


def gc():
    data = {}
    for apk_name in setting.APKS:
        # print(apk_name)
        base_path = os.path.join(setting.BASE_DIR, apk_name)
        data[apk_name] = {}
        for version in target_versions:
            sum_data, count = 0, 0
            dir_path = os.path.join(base_path, version)
            path = os.path.join(dir_path, "gc.csv")
            with open(path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        t = eval(row["paused_avg"])
                        sum_data += t
                        count += 1
                    except:
                        continue
            try:
                data[apk_name][version] = {"gc": sum_data / count}
            except ZeroDivisionError:
                print(apk_name + " " + version)
    return data


def latex_table(data: dict):
    attrs = list(list(data.values())[0].values())[0].keys()
    for attr in attrs:
        s_table = ""
        for app in app_file_number:
            s_table += app
            for version in target_versions:
                s_table += "&%.3f" % data[app][version][attr]
            s_table += "\\\\\n\\hline\n"
        print(attr)
        print(s_table)


def latex_table(data: dict):
    attrs = list(list(data.values())[0].values())[0].keys()
    for attr in attrs:
        s_table = ""
        data_format = "&%.2f"
        if attr == "memory":
            data_format = "&%.0f"
        for app in app_file_number:
            s_table += app
            for version in target_versions:
                s_table += data_format % data[app][version][attr]
            s_table += "\\\\\n\\hline\n"
        print(attr)
        print(s_table)


def save_result(data, file_path):
    # 新建文件和表格
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    header = ["应用", "0", "1", "2", "3", "7"]
    attrs = list(list(data.values())[0].values())[0].keys()
    for attr in attrs:
        sheet.append([])
        sheet.append([])
        sheet.append([attr])
        sheet.append(header)
        for app in app_file_number:
            row = [app,
                   data[app]["0"][attr],
                   data[app]["1"][attr],
                   data[app]["2"][attr],
                   data[app]["3"][attr],
                   data[app]["7"][attr]]
            sheet.append(row)
    wb.save(file_path)  # 保存文件，注意以xlsx为文件扩展名


def save_data():
    energy_data = energy()
    # print(energy_data)
    gc_data = gc()
    # print(gc_data)
    frame_data = frame()
    # print(frame_data)
    memory_data = memory()
    # print(memory_data)
    result_path = "C:\\Users\\MaoMorn\\Desktop\\refactor\\analysis_result.xlsx"
    save_result(energy_data, result_path)
    save_result(gc_data, result_path)
    save_result(frame_data, result_path)
    save_result(memory_data, result_path)


def get_metric_path(apk_name, version, metric):
    base_path = os.path.join(setting.BASE_DIR, apk_name)
    dir_path = os.path.join(base_path, version)
    result = ""
    if metric == "energy":
        result = os.path.join(dir_path, "%s_Energy.csv" % setting.APKS[apk_name]['appPackage'])
    elif metric == "delay_count" or metric == "fps":
        result = os.path.join(dir_path, "frame.csv")
    else:
        result = os.path.join(dir_path, metric + ".csv")
    return result


def get_data(apk_name, version, metric):
    metric_path = get_metric_path(apk_name, version, metric)
    result = []
    with open(metric_path) as file:
        if metric == "energy":
            reader = csv.reader(file)
            for row in reader:
                for i in row:
                    try:
                        t = int(i)
                        result.append(t)
                    except:
                        continue
        else:
            reader = csv.DictReader(file)
            attr = metric
            if metric == "gc":
                attr = "paused_avg"
            elif metric == "memory":
                attr = "pss"
            for row in reader:
                try:
                    t = eval(row[attr])
                    result.append(t)
                except:
                    continue
    return result


def delta_all(metric):
    combs = [["0", "1"], ["0", "2"], ["0", "3"], ["0", "7"]]
    result = {}
    for apk_name in setting.APKS:
        app_data = {}
        for version in target_versions:
            app_data[version] = get_data(apk_name, version, metric)
        result[apk_name] = {}
        for comb in combs:
            s_comb = str(comb)
            # value = cliffsDelta.cliffsDelta(app_data[comb[0]], app_data[comb[1]])
            t1, t2 = app_data[comb[0]], app_data[comb[1]]
            t1, t2 = sum(t1) / len(t1), sum(t2) / len(t2)
            value = (t2 - t1) / t1 * 100
            result[apk_name][s_comb] = value
    for apk_name in app_file_number:
        print(apk_name)
        for comb in combs:
            s_comb = str(comb)
            print("%s :  %s" % (s_comb, result[apk_name][s_comb]))
    delta2latex(result)


def delta2latex(data):
    combs = {"['0', '1']": "$V_0V_1$", "['0', '2']": "$V_0V_2$",
             "['0', '3']": "$V_0V_3$", "['0', '7']": "$V_0V_4$"}
    s = ""
    for comb in combs:
        s += combs[comb]
        for app_name in app_file_number:
            # t = "%.3f" % data[app_name][comb][0]
            t = data[app_name][comb]
            if abs(t) > 20:
                t = t / (10 ** (len("%.0f" % abs(t)) - 1))
            t = "%.2f" % t
            # tag = data[app_name][comb][1]
            # \textbf
            # if tag == "small":
            #     t = "\\textbf{%s(S)}" % t
            # elif tag == "medium":
            #     t = "\\textbf{%s(M)}" % t
            # elif tag == "large":
            #     t = "\\textbf{%s(L)}" % t
            s += "&" + t
        s += "\\\\\n\\hline\n"
    print(s)
    # s += app_name
    # for comb in combs:
    #     s_comb = str(comb)
    #     tag = data[app_name][s_comb][1]
    #     s += "&%.3f" % data[app_name][s_comb][0]
    #     if tag == "small":
    #         s += "(S)"
    #     elif tag == "medium":
    #         s += "(M)"
    #     elif tag == "large":
    #         s += "(L)"
    # s += "\\\\\n\\hline\n"


def delta_all_metric(app_name):
    # combs = [["7", "1"], ["7", "2"], ["7", "3"]]
    combs = [["1", "2"], ["1", "3"], ["2", "3"], ["7", "1"], ["7", "2"], ["7", "3"]]
    attrs = ["gc", "memory", "delay_count", "fps", "energy"]
    result = {}
    for metric in attrs:
        result[metric] = {}
        data = {}
        for version in target_versions:
            data[version] = get_data(app_name, version, metric)
        for comb in combs:
            s_comb = str(comb)
            value = cliffsDelta.cliffsDelta(data[comb[0]], data[comb[1]])
            result[metric][s_comb] = value
    for metric in result:
        print(metric)
        print(result[metric])
    metrics2latex(result)


def metrics2latex(data):
    # combs = {"['7', '1']": "$V_4V_1$", "['7', '2']": "$V_4V_2$", "['7', '3']": "$V_4V_3$"}
    combs = {"['1', '2']": "$V_1V_2$","['1', '3']": "$V_1V_3$","['2', '3']": "$V_2V_3$",
             "['7', '1']": "$V_4V_1$", "['7', '2']": "$V_4V_2$", "['7', '3']": "$V_4V_3$"}
    metrics = {"energy", "fps", "delay_count", "memory", "gc"}
    s = ""
    for comb in combs:
        s += combs[comb]
        for metric in metrics:
            t = "%.3f" % data[metric][comb][0]
            tag = data[metric][comb][1]
            if tag == "small":
                t = "\\textbf{%s(S)}" % t
            elif tag == "medium":
                t = "\\textbf{%s(M)}" % t
            elif tag == "large":
                t = "\\textbf{%s(L)}" % t
            s += "&" + t
        s += "\\\\\n\\hline\n"
    print(s)


def task_analysis(app_name):
    apk_name = "Tasks"
    combs = [["0", "1"], ["0", "2"], ["0", "3"], ["0", "7"], ["7", "1"], ["7", "2"], ["7", "3"]]

    base_path = os.path.join(setting.BASE_DIR, apk_name)
    energy_path = "%s_Energy.csv" % setting.APKS[apk_name]['appPackage']
    data = {}
    for version in target_versions:
        dir_path = os.path.join(base_path, version)
        energy_file = os.path.join(dir_path, energy_path)
        version_data = []
        with open(energy_file) as file:
            reader = csv.reader(file)
            for row in reader:
                for i in row:
                    try:
                        t = int(i)
                        version_data.append(t)
                    except:
                        continue
        data[version] = version_data

    result = {}
    for comb in combs:
        s_comb = str(comb)
        result[s_comb] = []
        # value = scipy.stats.wilcoxon(data[comb[0]], data[comb[1]])
        # result[s_comb].append(value[1])
        value = cliffsDelta.cliffsDelta(data[comb[0]], data[comb[1]])
        result[s_comb].append(value)
    for comb in result:
        print(comb)
        print(result[comb])


if __name__ == "__main__":
    # delta_all("delay_count")
    # delta_all("fps")
    # delta_all("energy")
    # delta_all("memory")
    # delta_all("fps")
    # energy_data = energy()
    # print(energy_data)
    # gc_data = gc()
    # print(gc_data)
    # frame_data = frame()
    # print(frame_data)
    # memory_data = memory()
    # print(memory_data)
    # latex_table(gc_data)
    # latex_table(memory_data)
    # latex_table(frame_data)
    # latex_table(energy_data)

    delta_all_metric("NextCloud")
# delta_all_metric("GitNex")

# NextCloud
# GitNex
