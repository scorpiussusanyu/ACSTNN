# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/07/23
@Description: 
"""
from appium import webdriver
from appium_script.tools import log
from multiprocessing import Value
from time import sleep
import os


def swipeUp(driver, t=500, n=1):
    '''向上滑动屏幕'''
    l = driver.get_window_size()
    x1 = l['width'] * 0.5  # x坐标
    y1 = l['height'] * 0.75  # 起始y坐标
    y2 = l['height'] * 0.25  # 终点y坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t)


def swipeDown(driver, t=500, n=1):
    '''向下滑动屏幕'''
    l = driver.get_window_size()
    x1 = l['width'] * 0.5  # x坐标
    y1 = l['height'] * 0.25  # 起始y坐标
    y2 = l['height'] * 0.75  # 终点y坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t)


def swipLeft(driver, t=500, n=1):
    '''向左滑动屏幕'''
    l = driver.get_window_size()
    x1 = l['width'] * 0.75
    y1 = l['height'] * 0.5
    x2 = l['width'] * 0.25
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t)


def swipRight(driver, t=500, n=1):
    '''向右滑动屏幕'''
    l = driver.get_window_size()
    x1 = l['width'] * 0.25
    y1 = l['height'] * 0.5
    x2 = l['width'] * 0.75
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t)


def anki_droid(driver: webdriver):
    # 添加
    # 搜索
    # 学习
    # 遍历
    pass


def aurora_store(driver: webdriver):
    # 搜索
    # 下载
    # 遍历
    pass


def download_navi(driver: webdriver):
    # 搜索
    # 下载
    # 遍历
    pass


def f_droid(driver: webdriver):
    # 搜索
    # 下载
    # 遍历
    pass


def git_nex(driver: webdriver):
    # 遍历设置
    # 创建仓库
    # 创建文件
    pass


def glucosio(driver: webdriver):
    # 遍历
    # 创建reminder
    # 创建病例
    pass


def materialistic(driver: webdriver):
    # 遍历
    # 评论
    # 查看
    pass


def next_cloud(driver: webdriver):
    # 遍历
    # 下载
    # 上传
    pass


def tasks(driver: webdriver):
    # 遍历
    # 新建
    # 搜索
    pass


def treble_shot(driver: webdriver):
    # 遍历
    # 发送
    # 搜索
    pass


def main(apk_name: str, version: int):
    from appium_script.script import setting
    app_package = setting.APKS[apk_name]["appPackage"]
    app_activity = setting.APKS[apk_name]["appActivity"]
    script = setting.APKS[apk_name]["script"]
    log_dir = os.path.join(setting.BASE_DIR, str(version))
    setting.DESIRED_CAPS['appPackage'] = app_package
    setting.DESIRED_CAPS['appActivity'] = app_activity
    driver = webdriver.Remote(setting.REMOTE_HOST, setting.DESIRED_CAPS)
    lock = Value('i', 1)
    # log.start_log(app_package, lock, log_dir)
    script(driver)
    lock.value = 0
    sleep(5)
    driver.quit()
    print("  %-s  的  %s  版本测试完成" % (apk_name, setting.VERSIONS[version]))
