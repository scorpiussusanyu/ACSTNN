import matplotlib as mpl
import matplotlib.pyplot as plt
import requests
def pic1():
    # 设置图片大小
    plt.figure(figsize=(10, 8))

    # 生成数据
    labels = ['成功', '失败']
    data = [1, 18, 25, 27, 31, 49, 50, 50, 52, 79, 101, 118, 127, 179, 281, 293, 446, 614, 754, 1137]
    t = sum(data)
    data = [i / t for i in data]
    yellow, blue = "#FF8C00", "#4169E1"
    colors1 = [yellow] * 4 + [blue] + [yellow] * 6 + [blue] * 4 + [yellow, blue, yellow, blue, blue]
    colors2 = [yellow] * 10 + [blue, yellow] + [blue] * 8
    colors0 = [yellow] * 20

    params = {
        "autopct": '%3.1f%%',
        "startangle": 180,
        "textprops": {'color': 'w'},
        "wedgeprops": {'width': 0.3, "linewidth": 1.5, 'edgecolor': 'w'},
        "counterclock": False,
    }
    wedges0, texts0, autotexts0 = plt.pie(data,
                                          autopct=params["autopct"],
                                          radius=1.3,
                                          # pctdistance=0.9,
                                          colors=colors0,
                                          startangle=params["startangle"],
                                          textprops=params["textprops"],
                                          wedgeprops=params["wedgeprops"],
                                          counterclock=params["counterclock"]
                                          )

    # 外环
    wedges1, texts1, autotexts1 = plt.pie(data,
                                          autopct=params["autopct"],
                                          radius=0.95,
                                          # pctdistance=0.7,
                                          colors=colors1,
                                          startangle=params["startangle"],
                                          textprops=params["textprops"],
                                          wedgeprops=params["wedgeprops"],
                                          counterclock=params["counterclock"]
                                          )

    # 内环
    wedges2, texts2, autotexts2 = plt.pie(data,
                                          autopct=params["autopct"],
                                          radius=0.6,
                                          # pctdistance=0.75,
                                          colors=colors2,
                                          startangle=params["startangle"],
                                          textprops=params["textprops"],
                                          wedgeprops=params["wedgeprops"],
                                          counterclock=params["counterclock"]
                                          )

    plt.rcParams['font.family']=['SimHei']
    plt.rcParams['font.size'] = '17'
    # 图例
    plt.legend([wedges1[0], wedges1[4]],
               labels,
               fontsize=23,
               title_fontsize=23,
               title='检测评价',
               loc='lower right',
               shadow=True,
               bbox_to_anchor=(1.15, -0.06))
    label_fontsize=30
    plt.text(0, 0, "aDoctor", fontsize=label_fontsize, verticalalignment="center", horizontalalignment="center")
    plt.annotate('', xy=(0.3, 0.3), xytext=(0, 0.05),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.text(1.2, -0.7, "Paprika", fontsize=label_fontsize, verticalalignment="center", horizontalalignment="center")
    plt.annotate('', xy=(0.6, -0.4), xytext=(1.2, -0.68), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.text(-1.1, -1, "Droidlens", fontsize=label_fontsize, verticalalignment="center", horizontalalignment="center")
    plt.annotate('', xy=(-1, -0.7), xytext=(-1.1, -0.95), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    # 设置文本样式
    plt.setp(autotexts0, size=20, weight='bold', alpha=0)
    plt.setp(autotexts1, size=20, weight='bold', alpha=0)
    plt.setp(autotexts2, size=20, weight='bold', alpha=0)
    plt.tight_layout()
    plt.savefig('temp.pdf', bbox_inches='tight')
    plt.show()


def pic2():
    # 设置图片大小
    plt.figure(figsize=(10, 8))

    # 生成数据
    labels = ['success', 'failure']
    data = [20] * 18
    t = sum(data)
    data = [i / t for i in data]
    yellow, blue = "#FF8C00", "#4169E1"
    colors1 = [yellow] * 15 + [blue] * 3
    colors2 = [yellow] * 4 + [blue] * 14
    colors0 = [yellow] * 18

    params = {
        "labels": ["IGS", "LIC", "MIM", "NLMR", "HMU",
                   "DTWC", "IDFAP", "UC", "ISQ", "LT",
                   "SL", "DW", "PD", "RAM", "DR",
                   "HBR", 'HSS', "SCC"],
        "autopct": '%3.1f%%',
        "startangle": 180,
        "textprops": {'color': 'black'},
        "wedgeprops": {'width': 0.3, "linewidth": 1.5, 'edgecolor': 'w'},
        "counterclock": False,
    }
    wedges0, texts0 = plt.pie(data,
                              labels=params["labels"],
                              autopct=None,
                              radius=1.3,
                              labeldistance=0.85,
                              colors=colors0,
                              startangle=params["startangle"],
                              textprops=params["textprops"],
                              wedgeprops=params["wedgeprops"],
                              counterclock=params["counterclock"]
                              )

    # 外环
    wedges1, texts1, autotexts1 = plt.pie(data,
                                          autopct=params["autopct"],
                                          radius=0.95,
                                          # pctdistance=0.7,
                                          colors=colors1,
                                          startangle=params["startangle"],
                                          textprops=params["textprops"],
                                          wedgeprops=params["wedgeprops"],
                                          counterclock=params["counterclock"]
                                          )

    # 内环
    wedges2, texts2, autotexts2 = plt.pie(data,
                                          autopct=params["autopct"],
                                          radius=0.6,
                                          # pctdistance=0.75,
                                          colors=colors2,
                                          startangle=params["startangle"],
                                          textprops=params["textprops"],
                                          wedgeprops=params["wedgeprops"],
                                          counterclock=params["counterclock"]
                                          )

    # 图例
    plt.legend([wedges1[0], wedges1[-1]],
               labels,
               fontsize=13,
               title_fontsize=13,
               title='Detection Evaluation',
               loc='lower right',
               shadow=True,
               bbox_to_anchor=(1.2, 0.01))
    plt.text(0, 0, "Paprika", fontsize=16, verticalalignment="center", horizontalalignment="center")
    plt.annotate('', xy=(0.3, 0.3), xytext=(0, 0.05),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.text(1.2, -0.8, "aDoctor", fontsize=16, verticalalignment="center", horizontalalignment="center")
    plt.annotate('', xy=(0.6, -0.4), xytext=(1.2, -0.75), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
    plt.text(-1.1, -1, "Droidlens", fontsize=16, verticalalignment="center", horizontalalignment="center")
    plt.annotate('', xy=(-1, -0.7), xytext=(-1.1, -0.95), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    # 设置文本样式
    plt.setp(texts0, size=15)
    plt.setp(autotexts1, size=15, weight='bold', alpha=0)
    plt.setp(autotexts2, size=15, weight='bold', alpha=0)
    plt.savefig('temp.pdf', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    pic1()
