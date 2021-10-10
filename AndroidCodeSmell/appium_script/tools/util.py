# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/07/21
@Description: 
"""
from subprocess import Popen, PIPE, TimeoutExpired
import os

size_table = ("bytes", "KB", "MB", "GB")
time_table = ("us", "ms", "s")


def run_command(command: str, dir=None, timeout=None):
    pipes = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, cwd=dir)
    try:
        std_out, std_err = pipes.communicate(timeout=timeout)
    except TimeoutExpired as e:
        return -9, "", "Command '" + command + "' timed out after " + str(timeout) + " seconds"
    else:
        return pipes.returncode, std_out.decode("UTF-8", errors="ignore"), std_err.decode("UTF-8", errors="ignore")


def creat_file(path: str):
    if os.path.exists(path) and os.path.isfile(path):
        return True
    else:
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, 'w'):
            pass
        return True


def convert_size(origin: str, target="KB") -> float:
    target_index = size_table.index(target)
    index = split_number(origin)
    origin_index = size_table.index(origin[index:])
    result = float(origin[:index])
    result *= 1024 ** (origin_index - target_index)
    return result


def convert_time(origin: str, target="ms") -> float:
    target_index = time_table.index(target)
    index = split_number(origin)
    origin_index = time_table.index(origin[index:])
    result = float(origin[:index])
    result *= 1000 ** (origin_index - target_index)
    return result


def split_number(origin: str) -> int:
    index = -1
    while index > -len(origin):
        if '0' <= origin[index - 1] <= '9':
            break
        index -= 1
    return index
