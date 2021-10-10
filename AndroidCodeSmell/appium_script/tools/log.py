# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/07/21
@Description: 
"""
from appium_script.tools import util
from appium_script import metric
from multiprocessing import Process
import jpype
import os
import time


def get_pid(package_name: str) -> str:
    command = "adb shell ps | findstr %s" % package_name
    result = util.run_command(command)[1]
    pid = result.split()[1]
    return pid


def log_gc_anr(lock, pid: str, freq: int, log_dir: str):
    clean_command = "adb shell rm /data/anr/*"
    log_command = "adb shell kill -3 %s" % pid
    ls_command = "adb shell ls /data/anr/"
    print("启动GC收集：")
    util.run_command(clean_command)

    log_file_path = os.path.join(log_dir, "gc.csv")
    util.creat_file(log_file_path)
    log_file = open(log_file_path, "w", newline='')
    gc = metric.GC()
    gc.init_writer(log_file)
    flag = 1
    print("GC收集启动成功：")
    while lock.value:
        time.sleep(freq - 1)
        util.run_command(log_command)
        time.sleep(1)
        file_name = util.run_command(ls_command)[1].strip().split("\r\n")[-1]
        command = "adb shell cat /data/anr/%s" % file_name
        content = util.run_command(command)[1]
        util.run_command(clean_command)
        if content != "":
            gc.parse(content)
            if flag:
                gc.write_header()
                flag = 0
            gc.write_val()
    log_file.close()
    print("*" * 50)
    print("%s  收集完毕" % log_file_path)


def log_gc_logcat(pid: str, timestamp: str, log_dir: str):
    log_command = "adb shell logcat -b main -t '%s.000' --pid=%s > %s" % \
                  (timestamp, pid, os.path.join(log_dir, "gc.txt"))
    util.run_command(log_command)


def log_battery(lock, package_name: str, freq: int, log_dir: str):
    reset_command = "adb shell dumpsys batterystats --reset"
    util.run_command(reset_command)
    log_command = "adb shell dumpsys batterystats %s" % package_name
    battery = metric.Battery()
    # while lock.value:
    time.sleep(freq)
    result = util.run_command(log_command)[1]
    battery.parse(result)
    print(battery)


def log_cpu_top(pid: str, package_name: str, log_dir: str):
    log_command = "adb shell top -p %s -n 1 | findstr %s" % (pid, package_name)
    util.run_command(log_command)
    time.sleep(3)


def log_cpu_proc(lock, pid: str, freq: int, log_dir: str):
    # 默认2s更新一次
    print("启动CPU收集：")
    log_file_path = os.path.join(log_dir, "cpu.csv")
    util.creat_file(log_file_path)
    log_file = open(log_file_path, "w", newline='')
    cpu = metric.CPU()
    cpu.init_writer(log_file)
    cpu.parse(pid)
    cpu.write_header()
    print("CPU收集启动成功：")
    while lock.value:
        time.sleep(freq)
        cpu.parse(pid)
        cpu.write_val()
    log_file.close()
    print("*" * 50)
    print("%s  收集完毕" % log_file_path)


def log_memory(lock, pid: str, freq, log_dir: str):
    print("启动Memory收集：")  # KB
    log_command = "adb shell dumpsys meminfo %s" % pid
    log_file_path = os.path.join(log_dir, "memory.csv")
    util.creat_file(log_file_path)
    log_file = open(log_file_path, "w", newline='')
    memory = metric.Memory()
    memory.init_writer(log_file)
    flag = 1
    print("Memory收集启动成功：")
    while lock.value:
        time.sleep(freq)
        content = util.run_command(log_command)[1]
        try:
            memory.parse(content)
            if flag:
                memory.write_header()
                flag = 0
            memory.write_val()
        except Exception as e:
            print(e)
            print("Memory异常:\t" + content)

    log_file.close()
    print("*" * 50)
    print("%s  收集完毕" % log_file_path)


def log_frame(lock, pid: str, freq: int, log_dir: str):
    print("启动Frame收集：")
    command = "adb shell dumpsys gfxinfo %s reset" % pid
    util.run_command(command)
    log_file_path = os.path.join(log_dir, "frame.csv")
    util.creat_file(log_file_path)
    log_file = open(log_file_path, "w", newline='')
    frame = metric.Frame()
    flag = 1
    frame.init_writer(log_file)
    print("Frame收集启动成功：")
    while lock.value:
        time.sleep(freq)
        content = util.run_command(command)[1]
        frame.parse(content)
        if flag:
            frame.write_header()
            flag = 0
        frame.write_val()
    log_file.close()
    print("*" * 50)
    print("%s  收集完毕" % log_file_path)


def log_energy(lock, package_name, log_dir):
    print("启动Energy收集：")
    jar_dir = "E:/PycharmProjects/AndroidCodeSmell/appium_script/lib"
    jar_path = ""
    for jar in os.listdir(jar_dir):
        jar_path += os.path.join(jar_dir, jar) + ";"
    jvm_path = "D:/Java/jdk-8_x86/jre/bin/server/jvm.dll"
    jpype.startJVM(jvm_path, "-ea", "-Xms128m", "-Xmx256m", f"-Djava.class.path={jar_path}")
    java_class = jpype.JClass("Main")
    profiler = java_class.getInstance()
    profiler.setTargetPackage(package_name)
    print("Energy收集启动成功：")
    while lock.value:
        continue
    profiler.save()
    profiler.stop()
    jpype.shutdownJVM()


def start_log(package_name, lock, log_dir, freq=2):
    print("开始启动日志记录：")
    pid = get_pid(package_name)
    Process(target=log_frame, args=(lock, pid, freq, log_dir)).start()
    Process(target=log_cpu_proc, args=(lock, pid, freq, log_dir)).start()
    Process(target=log_memory, args=(lock, pid, freq, log_dir)).start()
    Process(target=log_gc_anr, args=(lock, pid, freq, log_dir)).start()
    Process(target=log_energy, args=(lock, package_name, log_dir)).start()


if __name__ == "__main__":
    # lock = Value('i', 1)
    # Process(target=func, args=(lock, 1)).start()
    # Process(target=func, args=(lock, -1)).start()
    # for i in range(10):
    #     print("main %d" % i)
    #     time.sleep(1)
    # lock.value = 0
    # util.creat_file("C:/Users/MaoMorn/Desktop/a/test.txt")
    pid = "25319"
    # log_dir = "C:/Users/MaoMorn/Desktop/test"
    log_dir = "C:\\Users\\MaoMorn\\Desktop\\test"
    print("log")
    # Process(target=log_frame, args=(lock, pid, 2, log_dir)).start()
    # Process(target=log_cpu_proc, args=(lock, pid, 2, log_dir)).start()
    # Process(target=log_memory, args=(lock, pid, 2, log_dir)).start()
    # Process(target=log_gc_anr, args=(lock, pid, 2, log_dir)).start()
    # for i in range(10):
    #     print(i)
    #     time.sleep(1)
    # lock.value = 0
