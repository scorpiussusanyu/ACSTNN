# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/01/08
@Description: 
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import csv
import collections
from brokenaxes import brokenaxes
import matplotlib.font_manager as fm
from matplotlib.ticker import MultipleLocator

number_java = {'2048': 3, 'Shaarlier': 54, 'BeHe Explorer': 76, 'NetworkTools': 81, 'ToneDef': 95, 'Ouroboros': 147,
               'Lightning': 150, 'Terminal Emulator': 152, 'Birthday Calendar': 158, 'JumpGo': 237, 'EP Mobile': 304,
               'Glucosio': 356, 'GPSLogger': 383, 'Owncloud': 539, 'AnkiDroid': 844, 'Materialistic': 881,
               'Nextcloud': 1338, 'K-9 Mail': 1844, 'Xabber': 2263, 'Signal Private Messenger': 3411}


def annular_chart():
    plt.figure(figsize=(10, 8))

    # 生成数据
    total = 0
    for i in number_java:
        total += number_java[i]
    data = []
    for i in number_java:
        data.append(number_java[i] / total)
    colors = ["darkorange", "royalblue"]
    paprika = [colors[0], colors[0], colors[0], colors[0], colors[1],
               colors[0], colors[0], colors[0], colors[0], colors[0],
               colors[0], colors[1], colors[1], colors[1], colors[1],
               colors[0], colors[1], colors[0], colors[1], colors[1]]
    paprika_labels = ["Paprika"]
    paprika_labels.extend([""] * (len(paprika) - 1))
    aDoctor = [colors[0], colors[0], colors[0], colors[0], colors[0],
               colors[0], colors[0], colors[0], colors[0], colors[0],
               colors[1], colors[0], colors[1], colors[1], colors[1],
               colors[1], colors[1], colors[1], colors[1], colors[1]]
    aDoctor_labels = ["aDoctor"]
    aDoctor_labels.extend([""] * (len(aDoctor) - 1))
    props = {
        "wedgeprops": {'width': 0.25, 'edgecolor': 'w'},
        "counterclock": False,
        "startangle": 180,
        "autopct": '%3.1f%%',
    }
    # 外环
    wedges1, texts1, autotexts1 = plt.pie(data,
                                          autopct=props["autopct"],
                                          radius=1,
                                          pctdistance=0.85,
                                          colors=paprika,
                                          startangle=props["startangle"],
                                          counterclock=props["counterclock"],
                                          wedgeprops=props["wedgeprops"],
                                          # labels=paprika_labels
                                          )

    # 内环
    wedges2, texts2, autotexts2 = plt.pie(data,
                                          autopct=props["autopct"],
                                          radius=0.7,
                                          pctdistance=0.75,
                                          colors=aDoctor,
                                          startangle=props["startangle"],
                                          counterclock=props["counterclock"],
                                          wedgeprops=props["wedgeprops"],
                                          # labels=aDoctor_labels
                                          )

    plt.rcParams['font.family'] = ['SimHei']
    # 图例
    plt.legend([wedges1[0], wedges1[4]],
               ['成功', '失败'],
               shadow=True,
               fontsize=12,
               title='检测评价',
               bbox_to_anchor=(0.85, 0.22))
    plt.text(0, 0, "aDoctor", fontsize=15, verticalalignment="top", horizontalalignment="right")
    plt.annotate('', xy=(0.4, 0.4), xytext=(0, 0), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.text(-0.8, -0.8, "Paprika", fontsize=15, verticalalignment="top", horizontalalignment="right")
    plt.annotate('', xy=(-0.6, -0.6), xytext=(-0.8, -0.8), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    # 设置文本样式
    plt.setp(autotexts1, alpha=0)
    plt.setp(autotexts2, alpha=0)

    plt.savefig("examples.pdf")
    plt.show()
    plt.close()


def annular_chart_smell_types():
    plt.figure(figsize=(10, 8))

    # 生成数据
    data = [1 / 18] * 18
    colors = ["darkorange", "royalblue"]
    paprika = [colors[0]] * 4 + [colors[1]] * 14
    aDoctor = [colors[0]] * 15 + [colors[1]] * 3
    droidlens = [colors[0]] * 18
    labels = ["IGS", "LIC", "MIM", "NLMR", "HMU",
              "DTWC", "IDFAP", "UC", "ISQ", "LT",
              "SL", "DW", "PD", "RAM", "DR",
              "HBR", "HSS", "SCC"]
    props = {
        "x": data,
        "autopct": '%3.1f%%',
        "startangle": 180,
        "counterclock": False,
        "wedgeprops": {'width': 0.2, 'edgecolor': 'w'}
    }
    # 内环
    wedges1, texts1, autotexts1 = plt.pie(
        radius=0.5,
        colors=paprika,
        x=props["x"],
        autopct=props["autopct"],
        startangle=props["startangle"],
        counterclock=props["counterclock"],
        wedgeprops=props["wedgeprops"],
    )

    # 中环
    wedges2, texts2, autotexts2 = plt.pie(
        radius=0.75,
        colors=aDoctor,
        x=props["x"],
        autopct=props["autopct"],
        startangle=props["startangle"],
        counterclock=props["counterclock"],
        wedgeprops=props["wedgeprops"],
    )
    # 外环
    wedges3, texts3, autotexts3 = plt.pie(
        radius=1,
        colors=droidlens,
        labels=labels,
        labeldistance=0.85,
        x=props["x"],
        autopct=props["autopct"],
        startangle=props["startangle"],
        counterclock=props["counterclock"],
        wedgeprops=props["wedgeprops"],
    )
    plt.setp(texts3, fontsize=16)
    plt.rcParams['font.family'] = ['SimHei']
    plt.rcParams['font.size'] = '17'
    # 图例
    plt.legend([wedges1[0], wedges1[4]],
               ['成功', '失败'],
               shadow=True,
               fontsize=19,
               title_fontsize=19,
               title='支持性评价',
               bbox_to_anchor=(0.8, 0.22))

    # 设置文本样式
    plt.setp(autotexts1, alpha=0)
    plt.setp(autotexts2, alpha=0)
    plt.setp(autotexts3, alpha=0)
    label_fontsize = 23
    plt.text(0.15, 0, "Paprika", fontsize=label_fontsize, verticalalignment="top", horizontalalignment="right")
    plt.annotate('', xy=(-0.3, 0.3), xytext=(0, 0), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.text(1.2, -0.6, "aDoctor", fontsize=label_fontsize, verticalalignment="top", horizontalalignment="right")
    plt.annotate('', xy=(0.5, -0.3), xytext=(0.9, -0.57), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.text(-0.8, -0.8, "Droidlens", fontsize=label_fontsize, verticalalignment="top", horizontalalignment="right")
    plt.annotate('', xy=(-0.6, -0.7), xytext=(-0.8, -0.8), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.tight_layout()
    plt.savefig("examples.pdf", bbox_inches='tight')
    plt.show()
    plt.close()


def failed2Paprika():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\RQ1_2_1.csv"
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    csv_file.close()
    smells = {}
    for i in data:
        for j in i:
            if j == "app_name":
                smells[i[j]] = 0
                continue
            smells[i["app_name"]] += int(i[j])
            if j == "NLMR":
                break
    # print(smells)
    plt.rcParams['font.family'] = ['SimHei']
    plt.rcParams['font.size'] = '12'
    drawing_x = []
    drawing_y = []
    for i in smells:
        drawing_x.append(i)
        drawing_y.append(smells[i])

    # plt.gca().xaxis.set_major_locator(MultipleLocator(1.5))

    plt.plot(drawing_x, drawing_y, marker='o', linewidth=2)
    plt.plot(drawing_x, [0] * len(drawing_y), marker='o', linewidth=2)
    plt.gcf().set_size_inches(10, plt.gcf().get_size_inches()[1])

    plt.legend(labels=["Droidlens", "Paprika"], fontsize=17)
    plt.xlabel("安卓应用", fontsize=17)
    plt.ylabel("检出异味数量", fontsize=17)
    plt.xticks(fontsize=17,rotation=-7)
    plt.yticks(fontsize=17)
    plt.tight_layout()
    plt.savefig("examples.pdf", bbox_inches='tight')
    plt.show()


def failed2aDoctor():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\RQ1_2_2.csv"
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    csv_file.close()
    smells = {}
    for i in data:
        for j in i:
            if j == "app_name":
                smells[i[j]] = 0
                continue
            smells[i["app_name"]] += int(i[j])
    # print(smells)
    drawing_x = []
    drawing_y = []
    plt.rcParams['font.family'] = ['SimHei']
    plt.rcParams['font.size'] = '17'
    for i in smells:
        drawing_x.append(i)
        drawing_y.append(smells[i])
    plt.plot(drawing_x, drawing_y, marker='o', linewidth=2)
    plt.plot(drawing_x, [0] * len(drawing_y), marker='o', linewidth=2)
    plt.gcf().set_size_inches(11, plt.gcf().get_size_inches()[1])
    plt.legend(labels=["Droidlens", "aDoctor"])
    plt.xlabel("安卓应用")
    plt.ylabel("检出异味数量")
    plt.xticks(rotation=-9)
    plt.tight_layout()
    plt.savefig("examples.pdf", bbox_inches='tight')
    plt.show()


def test():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\RQ2_1.csv"
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    csv_file.close()
    smells = collections.defaultdict(int)
    for i in data:
        for j in i:
            if j == "app_name":
                continue
            smells[j] += int(i[j])
    # print(smells)
    column = []
    temp = {}
    row = []
    for i in smells:
        if smells[i] == 0 or smells[i] > 300:
            temp[i] = smells[i]
        else:
            row.append(i)
            column.append(smells[i])
        print(smells[i])
    width = 0.20
    plt.ylim([0, 30])
    # # figsize = (10, 8)  # 调整绘制图片的比例
    plt.bar(row, column, width, color="#87CEFA")  # 绘制柱状图
    plt.xlabel('Smell Types')  # x轴
    plt.ylabel('Number detected')  # y轴
    plt.yticks()
    # # plt.savefig('test.png', dpi=400)  # 保存图像，dpi可以调整图像的像素大小
    plt.savefig("examples.pdf", bbox_inches='tight')
    plt.show()
    print(temp)


def box1():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\RQ3_1.csv"
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    csv_file.close()
    droidlens = collections.defaultdict(list)
    for i in data:
        for j in i:
            if j == "app_name":
                continue
            else:
                if i[j] == "":
                    i[j] = 0
                else:
                    i[j] = int(i[j])
                droidlens[j].append(i[j])
    # print(droidlens)
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\paprika.csv"
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    csv_file.close()
    paprika = collections.defaultdict(list)
    for i in data:
        for j in i:
            if j == "app_name":
                continue
            else:
                if i[j] == "":
                    i[j] = 0
                else:
                    i[j] = int(i[j])
                paprika[j].append(i[j])
    # print(paprika)
    tool_key = "工具"
    smells = [i for i in droidlens]
    droidlens = [droidlens[i] for i in droidlens]
    paprika = [paprika[i] for i in paprika]
    tools = ["Droidlens"] * len(droidlens[0])
    tools.extend(["Paprika"] * len(paprika[0]))
    droidlens[0].extend(paprika[0])
    droidlens[1].extend(paprika[1])
    droidlens[2].extend(paprika[2])
    droidlens[3].extend(paprika[3])
    data = {
        smells[0]: droidlens[0],
        smells[1]: droidlens[1],
        smells[2]: droidlens[2],
        smells[3]: droidlens[3],
        tool_key: tools
    }
    # print(droidlens)
    # print(paprika)
    plt.rcParams['font.family'] = ['SimHei']
    plt.rcParams['font.size'] = '17'
    df = pd.DataFrame(data)
    df_melt = df.melt(id_vars=tool_key, value_vars=smells, var_name="columns")
    # = sns.boxplot(data=)
    # sns.boxplot(data=data, x="Smells Types", y="Number Detected")
    # plt.show()
    sns.boxplot(data=df_melt, hue=tool_key, x="columns", y="value", flierprops={'marker': '+', "markersize": 6})
    plt.xlabel("安卓代码异味类型")
    plt.ylabel("异味数量")
    plt.tight_layout()
    plt.savefig("examples.pdf")
    plt.show()


def box2():
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\RQ3_2_aDocotor.csv"
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    csv_file.close()
    aDoctor = collections.defaultdict(list)
    for i in data:
        for j in i:
            if j == "app_name":
                continue
            else:
                if i[j] == "":
                    i[j] = 0
                else:
                    i[j] = int(i[j])
                aDoctor[j].append(i[j])
    # print(aDoctor)
    path = "C:\\Users\\MaoMorn\\Desktop\\android\\results\\RQ3_2_Droidlens.csv"
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    data = []
    for row in csv_reader:
        data.append({x: row[x] for x in row})
    csv_file.close()
    droidlens = collections.defaultdict(list)
    for i in data:
        for j in i:
            if j == "app_name":
                continue
            else:
                if i[j] == "":
                    i[j] = 0
                else:
                    i[j] = int(i[j])
                droidlens[j].append(i[j])
    # print(droidlens)

    smells = [i for i in aDoctor]
    aDoctor = [aDoctor[i] for i in aDoctor]
    droidlens = [droidlens[i] for i in droidlens]
    tools = ["Droidlens"] * len(droidlens[0])
    tools.extend(["aDoctor"] * len(aDoctor[0]))
    for i in range(len(droidlens)):
        droidlens[i].extend(aDoctor[i])
    tool_key = "工具"
    data = {tool_key: tools}
    for i in range(len(smells)):
        data[smells[i]] = droidlens[i]
    # print(aDoctor)
    # print(droidlens)
    df = pd.DataFrame(data)
    df_melt = df.melt(id_vars=tool_key, value_vars=smells, var_name="columns")
    # = sns.boxplot(data=)
    # sns.boxplot(data=data, x="Smells Types", y="Number Detected")
    # plt.show()
    plt.rcParams['font.family'] = ['SimHei']
    plt.rcParams['font.size'] = '17'
    sns.boxplot(data=df_melt, hue=tool_key, x="columns", y="value", flierprops={'marker': '+', "markersize": 6})
    plt.xlabel("安卓代码异味类型")
    plt.ylabel("检出异味数量")
    plt.tight_layout()
    plt.savefig("examples.pdf", bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    # failed2Paprika()
    # failed2aDoctor()
    # annular_chart()
    # test()
    annular_chart_smell_types()
    # box2()
