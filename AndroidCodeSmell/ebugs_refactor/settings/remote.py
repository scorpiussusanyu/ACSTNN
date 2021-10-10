#!/usr/bin/python3

"""
Remote storage settings.
"""

"""
Username and IP of where the applications are stored, expressed 
in the same way as in a typical SSH conection. 
If this value is empty ("") or None, the framework will assume 
the applications are stored in the same machine.
"""
cs_remote = "" #"greenlab@192.168.69.162"


"""
Remote folder path, located in @cs_remote, where the applications 
are stored.
"""
cs_remote_apps_folder = "/home/marco/tests/android-robotium" #"/media/data/android_apps/success"


"""
Timeout value, in milliseconds, for a remote copy (using `scp`).
"""
cs_remote_copy_timeout = 900 # 15 minutes