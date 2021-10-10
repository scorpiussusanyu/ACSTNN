# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/07/23
@Description: 
"""
from appium_script.script import script

DESIRED_CAPS = dict(platformName='android',
                    deviceName="MI NOTE LTE",
                    appPackage="com.morn.myapplication",
                    appActivity='com.morn.myapplication.MainActivity',
                    automationName="UiAutomator2",
                    resetKeyBoard=True,
                    skipDeviceInitialization=True,
                    skipServerInstallation=True,
                    skipUnlock=True,
                    unicodeKeyBoard=True,
                    skipLogcatCapture=True,
                    noReset=True)

REMOTE_HOST = 'http://localhost:4723/wd/hub'

VERSIONS = {
    0: "Origin",
    1: 'IGS',
    2: 'MIM',
    3: 'HMU',
    4: 'HMU & IGS',
    5: 'HMU & MIM',
    6: 'IGS & MIM',
    7: 'ALL'}

BASE_DIR = "C:\\Users\\MaoMorn\\Desktop\\refactor"

APKS = {
    "AnkiDroid": {
        "appPackage": "com.ichi2.anki",
        "appActivity": "com.ichi2.anki.IntentHandler",
        "script": script.anki_droid
    },
    "AuroraStore": {
        "appPackage": "com.aurora.store",
        "appActivity": "com.aurora.store.ui.single.activity.SplashActivity",
        "script": script.aurora_store
    },
    "Download Navi": {
        "appPackage": "com.tachibana.downloader",
        "appActivity": "com.tachibana.downloader.ui.main.MainActivity",
        "script": script.anki_droid
    },
    "F-Droid": {
        "appPackage": "org.fdroid.basic.debug",
        "appActivity": "org.fdroid.fdroid.views.main.MainActivity",
        "script": script.anki_droid
    },
    "GitNex": {
        "appPackage": "org.mian.gitnex",
        "appActivity": "org.mian.gitnex.activities.MainActivity",
        "script": script.anki_droid
    },
    "Glucosio": {
        "appPackage": "org.glucosio.android.daily",
        "appActivity": "org.glucosio.android.activity.SplashActivity",
        "script": script.anki_droid
    },
    "Materialistic": {
        "appPackage": "io.github.hidroh.materialistic",
        "appActivity": "io.github.hidroh.materialistic.LauncherActivity",
        "script": script.anki_droid
    },
    "NextCloud": {
        "appPackage": "com.nextcloud.client",
        "appActivity": "com.owncloud.android.ui.activity.FileDisplayActivity",
        "script": script.anki_droid
    },
    "Tasks": {
        "appPackage": "org.tasks.debug",
        "appActivity": "com.todoroo.astrid.activity.MainActivity",
        "script": script.anki_droid
    },
    "TrebleShot": {
        "appPackage": "com.genonbeta.TrebleShot.debug",
        "appActivity": "com.genonbeta.TrebleShot.activity.HomeActivity",
        "script": script.anki_droid
    }
}
