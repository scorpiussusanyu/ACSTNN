# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/07/16
@Description: 
"""
from time import sleep
from appium_script.tools import log
from multiprocessing import Value
import os


def manual(apk_name: str, version: int):
    from appium_script.script import setting
    app_package = setting.APKS[apk_name]["appPackage"]
    log_dir = os.path.join(setting.BASE_DIR, apk_name, str(version))
    lock = Value('i', 1)
    log.start_log(app_package, lock, log_dir)
    sleep(2)
    input("等待指令》》》")
    lock.value = 0
    sleep(5)
    print("  %-s  的  %s  版本测试完成" % (apk_name, setting.VERSIONS[version]))


if __name__ == "__main__":
    # manual("Tasks", 7)
    # manual("TrebleShot", 7)
    # manual("AnkiDroid", 7)
    # manual("AuroraStore", 7)
    # manual("Download Navi", 7)
    # manual("F-Droid", 7)
    # manual("GitNex", 7)
    manual("AnkiDroid", 0)
    # manual("Materialistic", 7)
    # manual("NextCloud", 7)
