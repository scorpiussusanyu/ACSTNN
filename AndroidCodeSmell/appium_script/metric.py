# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/07/21
@Description: 
"""
from appium_script.tools import util
from appium_script.tools.util import run_command
import collections
import traceback
import csv


class Metric:
    def __init__(self):
        self.content = collections.defaultdict(int)
        self.writer = None

    def init_writer(self, file):
        self.writer = csv.writer(file)

    def write_header(self):
        self.writer.writerow(self.content.keys())

    def write_val(self):
        self.writer.writerow(self.content.values())


class CPU(Metric):
    def __init__(self):
        super().__init__()
        self.pre_cpu = 0
        self.pre_proc = 0

    def parse(self, pid: str):
        self.parse_cpu()
        self.parse_proc(pid)

    # 2s收集一次
    def parse_cpu(self):
        command = "adb shell cat /proc/stat"
        data = run_command(command)[1]
        index = data.find("\r\n")
        data = data[5:index]
        data = data.split(' ')
        data = data[1:]
        """user, nice, system, idle, iowait, irq, softirq, steal, guest, guest time"""
        total_time = sum(eval(i) for i in data)
        self.content['delat_cpu'] = total_time - self.pre_cpu
        self.pre_cpu = total_time

    def parse_proc(self, pid: str):
        try:
            command = "adb shell cat /proc/%s/stat" % pid
            data = run_command(command)[1].split()[13:17]
            """user, system, children user, children system"""
            for i in range(4):
                data[i] = int(data[i])
            total_time = sum(data)
            self.content['delat_proc'] = total_time - self.pre_proc
            self.pre_proc = total_time
            self.content['cpu_occupation'] = 100 * self.content['delat_proc'] / self.content['delat_cpu']
            self.content["proc_user"] = data[0]
            self.content["proc_sys"] = data[1]
            self.content["proc_cuser"] = data[2]
            self.content["proc_csys"] = data[3]
        except IndexError as e:
            print(e)
            print("Proc CPU异常\n" + str(data))

    def __str__(self):
        return "proc user time: %d jiffies,\n" \
               "proc system time: %d jiffies,\n" \
               "proc children user time: %d jiffies,\n" \
               "proc children system time: %d jiffies,\n" \
               "delat proc time: %d jiffies,\n" \
               "cpu occupation: %f%"


class GC(Metric):
    # 结束时收集

    def parse(self, pre_data: str):
        try:
            beg = pre_data.find("Done Dumping histograms") + len("Done Dumping histograms\r\n")
            end = pre_data.find("Total blocking GC time: ", beg)
            end = pre_data.find("\r\n", end)
            pre_data = pre_data[beg:end]
            data = pre_data.split("\r\n")
            t = data[0].split()
            self.content["paused_sum"] = util.convert_time(t[4])
            self.content["paused_min"] = util.convert_time(t[-5].split('-')[0])
            self.content["paused_avg"] = util.convert_time(t[-3])
            self.content["paused_max"] = util.convert_time(t[-1])
            t = data[2].split()
            self.content["copying_freed_objects"] = int(t[3])
            self.content["copying_freed_size"] = util.convert_size(t[-1])

            # t = data[3].split()
            # self.content["copying_throughput_objects"] = int(t[-3][:-2])
            # self.content["copying_throughput_size"] = util.convert_size(t[-1][:-2])

            self.content["mean_throughput_size"] = util.convert_size(data[8][data[8].rfind(' ') + 1:][:-2])
            self.content["mean_throughput_objects"] = eval(data[9].split()[-2])
            self.content["total_allocations"] = eval(data[10][data[10].rfind(' ') + 1:])
            self.content["total_allocated_size"] = util.convert_size(data[11][data[11].rfind(' ') + 1:])
            self.content["total_freed_size"] = util.convert_size(data[12][data[12].rfind(' ') + 1:])
            self.content["total_waiting"] = util.convert_time(data[-5][data[-5].rfind(' ') + 1:])
            self.content["total_count"] = int(data[-4][data[-4].rfind(' ') + 1:])
            self.content["total_time"] = util.convert_time(data[-3][data[-3].rfind(' ') + 1:])
            self.content["mean_time"] = self.content["total_time"] / self.content["total_count"]
            self.content["total_blocking_count"] = int(data[-2][data[-2].rfind(' ') + 1:])
            t = data[-1][data[-1].rfind(' ') + 1:]
            self.content["total_blocking_time"] = util.convert_time(t) if t != "0" else t
        except Exception as e:
            print(e)
            traceback.print_exc()
            print("GC异常\n" + pre_data)

    def __str__(self):
        return "concurrent copying paused: copying paused: Sum: %fms, Min: %fms, Max: %fms, Avg: %fms\n" \
               "concurrent copying time: total: %fms, mean: %fms\n" \
               "concurrent copying freed: %d objects, %fMB\n" \
               "concurrent copying throughput: %d/s, %fMB/s\n" \
               "Mean GC throughput: %d/s, %fMB/s\n" \
               "Total allocated: %d, %fMB\n" \
               "Total freed: %fMB\n" \
               "Total time waiting for GC to complete: %fms\n" \
               "Total GC count: %d\n" \
               "Total blocking GC count: %d\n" \
               "Total blocking GC time: %f" \
               % (self.content["paused_sum"], self.content["paused_min"], self.content["paused_max"],
                  self.content["paused_avg"], self.content["total_time"], self.content["mean_time"],
                  self.content["copying_freed_objects"], self.content["copying_freed_size"],
                  self.content["copying_throughput_objects"], self.content["copying_throughput_size"],
                  self.content["mean_throughput_objects"], self.content["mean_throughput_size"],
                  self.content["total_allocations"], self.content["total_allocated_size"],
                  self.content["total_freed_size"], self.content["total_waiting"], self.content["total_count"],
                  self.content["total_blocking_count"], self.content["total_blocking_time"]
                  )


class Memory(Metric):
    # 2s更新一次
    def parse(self, data: str):
        beg = data.find("\n        TOTAL") + len("\n        TOTAL")
        end = data.find("\r\n", beg)
        result = data[beg:end].split()
        self.content['pss'], self.content['private_dirty'] = eval(result[0]), eval(result[1])
        self.content['private_clean'], self.content['swap_dirty'] = eval(result[2]), eval(result[3])

    def __str__(self):
        return "Pss: %dKB, Private Dirty: %dKB, Private CLean: %dKB, Swap Dirty: %dKB" % \
               (self.content['pss'], self.content['private_dirty'], self.content['private_clean'],
                self.content['swap_dirty'])


class Frame(Metric):
    # 默认2s拉取一次，配合reset严格限制拉取区间
    def parse(self, data: str):
        try:
            beg = data.find("Total frames rendered:")
            end = data.find("HISTOGRAM", beg) - 2
            data = data[beg:end].split("\r\n")
            self.content["count"] = int(data[0][data[0].rfind(' ') + 1:])
            self.content["delay_count"] = int(data[1].split()[-2])
            self.content["fps"] = self.content["count"] // 2
            self.content["missed_vsync"] = int(data[6][data[6].rfind(' ') + 1:])
            self.content["high_input_latency"] = int(data[7][data[7].rfind(' ') + 1:])
            self.content["slow_ui_thread"] = int(data[8][data[8].rfind(' ') + 1:])
            self.content["slow_bitmap_uploads"] = int(data[9][data[9].rfind(' ') + 1:])
            self.content["slow_issue_draw_command"] = int(data[10][data[10].rfind(' ') + 1:])
            self.content["frame_deadline_missed"] = int(data[11][data[11].rfind(' ') + 1:])
        except ValueError as e:
            print(e)
            print("Frame收集异常\n" + str(data))

    def __str__(self):
        return "Total frames rendered: %d\nDelay frames: %d\nFPS: %dfps\nNumber Missed Vsync: %d\n" \
               "Number High input latency: %d\nNumber Slow UI thread: %d\nNumber Slow bitmap uploads: %d\n" \
               "Number Slow issue draw commands: %d\nNumber Frame deadline missed: %d" % \
               (self.content["count"], self.content["delay_count"], self.content["fps"], self.content["missed_vsync"],
                self.content["high_input_latency"], self.content["slow_ui_thread"],
                self.content["slow_bitmap_uploads"], self.content["slow_issue_draw_command"],
                self.content["frame_deadline_missed"])


class Battery(Metric):
    # 传感器状态主动更新，进程状态被动更新，100ms更新一次

    def parse(self, data: str):
        beg = data.find("Estimated power use (mAh):\r\n") + len("Estimated power use (mAh):\r\n")
        end = data.find("\r\n", beg)
        # end = data.find("\r\n\r\n", beg)
        data = data[beg:end].split()
        self.content["computed_drain"] = float(data[4][:-1])

    def __str__(self):
        return "Computed drain: %s" % self.content["computed_drain"]
