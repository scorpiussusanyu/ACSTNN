#!/usr/bin/python3

"""
Android settings.
"""

"""
Gradle plugin supported version.
"""
cs_gradle_plugin_version = "2.2.1" # TODO: this value can be increased (test first)


"""
Gradle wrapper supported version.
"""
cs_wrapper_version = "2.14.1" # TODO: this value can be increased (test first)


"""
Path to the Android SDK home folder. Typically, this value is the 
same as the one defined in the environment variable $ANDROID_HOME.
"""
cs_android_sdk_path = "/home/marco/android-sdk-linux"


"""
Path to the Android aapt tool, which is used to detect the package 
out of an application's apk file.
"""
cs_aapt_path = cs_android_sdk_path + "/build-tools/27.0.0/aapt"
