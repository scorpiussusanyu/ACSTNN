# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2018/08/26
@Description: 从APK中读取应用的基本信息
"""

import os
import re
import shutil
import subprocess


# 检查apk版本号等信息
def get_app_base_info(parm_aapt_path, parm_apk_path):
    cmd = '%s dump badging "%s"' % (parm_aapt_path, parm_apk_path)  # 使用命令获取版本信息  aapt命令介绍可以相关博客
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # proc.wait()
    data = proc.communicate()[0]
    output = data.decode("utf-8")  # 执行命令，并将结果以字符串方式返回
    # print(output)
    match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output)
    if not match:
        print(output)
        raise Exception("can't get packageinfo")
    result = {}
    # application-label:'Adobe Acrobat'
    result['name'] = re.compile("application-label:'((((?!')\S)| )*)'").search(output).group(1)
    result['packageName'] = match.group(1)
    result['versionCode'] = match.group(2)
    result['versionName'] = match.group(3)
    result['sdkVersion'] = re.compile("sdkVersion:'(\d*)'").search(output).group(1)
    result['targetSdkVersion'] = re.compile("targetSdkVersion:'(\d*)'").search(output).group(1)
    # print(u" 包名：%s \n 版本号：%s \n 版本名称：%s " % (result['packagename'], result['versionCode'], result['versionName']))
    return result


def read_rsa(keytool_path, apk_path):
    result = {}
    cmd = 'keytool -printcert -jarfile "%s"' % apk_path
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # proc.wait()
    data = proc.communicate()[0]
    output = data.decode("gbk")  # 执行命令，并将结果以字符串方式返回
    # print(output)
    try:
        result['developer'] = re.compile("所有者: [A-Z]*=((((?!,)\S)| )*)").search(output).group(1)
    except (IndexError, AttributeError):
        result['developer'] = "No Name"
    result['sha256'] = re.compile("SHA256: (\S{95})").search(output).group(1)
    return result


def search_apk(base_path, apk_list):
    if os.path.isdir(base_path):
        file_list = os.listdir(base_path)
        for file in file_list:
            file_path = os.path.join(base_path, file)
            search_apk(file_path, apk_list)
    else:
        if base_path.endswith(".apk"):
            apk_list.append(base_path)
    # for i in os.listdir(base_path):
    #     if i in ['Birthday Calendar', 'Signal Private Messenger', "materialistic", 'Glucosio']:
    #         t = base_path + "\\" + i
    #         for j in os.listdir(t):
    #             apk_list.append(t + "\\" + j)


def command_line(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    flag = 0
    if len(proc.stderr.read()):
        flag = 1
    # return subprocess.check_output(cmd)
    proc.wait()
    # data = proc.communicate()[0]
    # print(data.decode('gbk'))
    # print(proc.returncode)
    return proc.returncode or flag


def file_creation():
    apks_dir = "E:\\硕士研究\\SoftwareTest\\20个软件"
    keytool_path = "D:\\Android\\Android Studio\\jre\\bin\\keytool.exe"  # keytool工具地址
    aapt_path = "D:\\Android\\sdk\\build-tools\\27.0.3\\aapt.exe"  # aapt工具地址
    apk_list = []
    search_apk(apks_dir, apk_list)
    count = 0
    for apk_path in apk_list:
        result = {}
        try:
            result.update(get_app_base_info(aapt_path, apk_path))
        except:
            continue
        count += 1
        csv_path = "E:\\硕士研究\\SoftwareTest\\20个软件测试结果\\Doridlens\\" + result["name"] + ".csv"
        print(csv_path)
        # shutil.rmtree(csv_path)  # 删除非空文件夹
        # os.makedirs(csv_path)
        open(csv_path, "w").close()
    print(count)


def paprika_test():
    apks_dir = "C:\\Users\\MaoMorn\\Desktop\\android\\as"
    # apks_dir = "E:\\硕士研究\\SoftwareTest\\20个软件\\gpslogger_v96"
    # apks_dir = "E:\\硕士研究\\SoftwareTest\\20个软件\\2048_2.08"
    apk_path = "E:\\硕士研究\\SoftwareTest\\SampleAPP\\app-release.apk"  # apk地址
    keytool_path = "D:\\Android\\Android Studio\\jre\\bin\\keytool.exe"  # keytool工具地址
    aapt_path = "D:\\Android\\sdk\\build-tools\\27.0.3\\aapt.exe"  # aapt工具地址
    paprika_jar = "E:\\Data\\MasterTimes\\Study\\SoftwareTest\\paprika\\GeoffreyHecht\\paprika-master\out\\artifacts\\Paprika_jar\\Paprika.jar"
    doridlens_jar = ".\\lib\\doridlens.jar"
    """================================================================================================================="""
    android_jars_path = "D:\\Android\\sdk\\platforms"
    base_path = "C:\\Users\\MaoMorn\\Desktop\\android\\paprika"
    category = "TestApp"
    download = 100
    date = "2017-01-001 10:23:39.050315"
    rating = 100
    size = 1024
    unsafe = "unsafe"
    apk_list = []
    search_apk(apks_dir, apk_list)
    count = 0
    failed_list = []
    for apk_path in apk_list:
        result = {}
        try:
            result.update(read_rsa(keytool_path, apk_path))
            result.update(get_app_base_info(aapt_path, apk_path))
        except:
            continue
        count += 1
        # db_path = base_path + result["name"] + "_" + result["versionName"] + ".db"
        db_path = apk_path.replace("as", "paprika").replace(".apk", ".db")
        # print()
        # csv_path = "E:\\硕士研究\\SoftwareTest\\20个软件测试结果\\" + result["name"] + "_" + result[
        #     "versionName"] + "\\doridlens\\\\"
        # csv_path = "E:\\硕士研究\\SoftwareTest\\20个软件测试结果\\aDoctor\\" + result["name"] + ".csv"
        csv_path = db_path[:-3] + "\\\\"
        # print(csv_path)
        # shutil.rmtree(csv_path)  # 删除非空文件夹
        # os.makedirs(csv_path)  # 创建目录
        data = (apk_path, android_jars_path, db_path, result["name"], result["packageName"], result["sha256"],
                result["developer"],
                category, download, date, rating, size)
        # print(result["name"]+"  "+result["packageName"])
        print(result["name"] + ";" + result["sdkVersion"] + ";" + result["targetSdkVersion"])
        # analyse = 'analyse "%s" -a "%s" -db "%s" -n "%s" -p "%s" -k %s -dev "%s" -cat "%s" -nd %d -d "%s" -r %d -s %d -u -omp -f' % data
        analyse = 'analyse "%s" -a "%s" -db "%s" -n "%s" -p "%s" -k %s -dev "%s" -cat "%s" -nd %d -d "%s" -r %d -s %d -u "unsafe" -omp True' % data
        # query = 'query -db "%s" -d  -r ALLAP -c "%s"' % (data[2], csv_path)
        query = 'query -db "%s" -d TRUE -r ALLAP -c "%s"' % (data[2], csv_path)
        # print(('*' + str(count)) * 10)
        print(analyse)
        # print(query)
        cmd = "java -jar %s %s" % (paprika_jar, analyse)
        # cmd = "java -jar %s %s" % (doridlens_jar, analyse)
        print(cmd)

        if command_line(cmd):
            # print(apk_path)
            failed_list.append(apk_path)
            continue
        cmd = "java -jar %s %s" % (paprika_jar, query)
        print(cmd)
        print(result["name"])
        command_line(cmd)
    print(count)
    print(failed_list)


def droidlens_test():
    apks_dir = "C:\\Users\\MaoMorn\\Desktop\\android\\as"
    keytool_path = "D:\\Android\\Android Studio\\jre\\bin\\keytool.exe"  # keytool工具地址
    aapt_path = "D:\\Android\\sdk\\build-tools\\27.0.3\\aapt.exe"  # aapt工具地址
    doridlens_jar = ".\\lib\\doridlens.jar"
    """================================================================================================================="""
    android_jars_path = "D:\\Android\\sdk\\platforms"
    base_path = "C:\\Users\\MaoMorn\\Desktop\\android\\droidlens2"
    category = "TestApp"
    download = 100
    date = "2017-01-001 10:23:39.050315"
    rating = 100
    size = 1024
    unsafe = "unsafe"
    apk_list = []
    search_apk(apks_dir, apk_list)
    count = 0
    failed_list = []
    for apk_path in apk_list:
        result = {}
        try:
            result.update(read_rsa(keytool_path, apk_path))
            result.update(get_app_base_info(aapt_path, apk_path))
        except:
            continue
        count += 1
        db_path = apk_path.replace("as", "droidlens2").replace(".apk", ".db")
        csv_path = db_path[:-3] + "\\\\"
        data = (apk_path, android_jars_path, db_path, result["name"], result["packageName"], result["sha256"],
                result["developer"],
                category, download, date, rating, size)
        print(result["name"] + ";" + result["sdkVersion"] + ";" + result["targetSdkVersion"])
        analyse = 'analyse "%s" -a "%s" -db "%s" -n "%s" -p "%s" -k %s -dev "%s" -cat "%s" -nd %d -d "%s" -r %d -s %d -u -omp -f' % data
        query = 'query -db "%s" -d  -r ALLAP -c "%s"' % (data[2], csv_path)
        # print(analyse)
        # print(query)
        cmd = "java -jar %s %s" % (doridlens_jar, analyse)
        print(cmd)
        # if command_line(cmd):
        #     # print(apk_path)
        #     failed_list.append(apk_path)
        #     continue
        cmd = "java -jar %s %s" % (doridlens_jar, query)
        print(result["name"])
        # command_line(cmd)
        print(cmd)
    print(count)
    print(failed_list)


if __name__ == '__main__':
    # paprika_test()
    droidlens_test()
    failed = ['C:\\Users\\MaoMorn\\Desktop\\android\\apks\\AnkiDroid\\AnkiDroid-2.10alpha3.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\AnkiDroid\\AnkiDroid-2.10alpha30.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\AnkiDroid\\AnkiDroid-2.9.1.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\GPSLogger\\gpslogger-102.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\GPSLogger\\gpslogger-103-weekrollover.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\GPSLogger\\gpslogger-103.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\JumpGo\\JumpGo.Dev.4.4.1.0-dev.01.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\JumpGo\\JumpGo.v4.4.0.24.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\K-9 Mail\\k9-5.700.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\K-9 Mail\\k9-5.703.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\Lightning\\acr.browser.lightning_100.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\Lightning\\acr.browser.lightning_101.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\NetworkTools\\AndroidNetworkTools0.4.5.2.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\NetworkTools\\AndroidNetworkTools0.4.5.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\nextcloud\\nextcloud-30090090.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\nextcloud\\nextcloud-30090190.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\nextcloud\\nextcloud-30090290.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\NextINpact\\app-release2.3.2.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\owncloud\\owncloud2.13.1.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\owncloud\\owncloud2.14.1.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\owncloud\\owncloud_2.13.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\Shaarlier\\Shaarlier_v1.6.1.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\Terminal Emulator\\jackpal.androidterm_42.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\Terminal Emulator\\Term-1.0.65.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\ToneDef\\ToneDef-18.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\ToneDef\\ToneDef-19.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\ToneDef\\ToneDef-20.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\xabber\\xabber0.9.30.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\xabber\\xabber1.0.30.apk',
              'C:\\Users\\MaoMorn\\Desktop\\android\\apks\\xabber\\xabber644.apk']
    # ['Birthday Calendar','Signal Private Messenger',"materialistic",'Glucosio']
    # file_creation()
