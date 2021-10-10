#!/usr/bin/python3

import json, errno, re, fileinput

import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

from os import walk, path, makedirs
from subprocess import check_output, Popen, PIPE, TimeoutExpired
from lazyme.string import color_print
from collections import Counter
from shutil import *

from ebugs_refactor.err.exceptions import NoTestResultsError

from ebugs_refactor.settings.android import cs_aapt_path
from ebugs_refactor.settings.app_test import cs_monkey_seeds_events
from ebugs_refactor.settings.storage import cs_measure_file_prefix, cs_trace_file_prefix
from ebugs_refactor.settings.misc import cs_ignored_folders

csv_dtypes = {"Time  [ms]": float,
              "\"Battery Remaining (%) [%]\"": float,
              "Time  [ms]": float,
              "\"Battery Status\"": float,
              "Time  [ms]": float,
              "\"Screen Brightness\"": float,
              "Time  [ms]": float,
              "\"Battery Power* [uW] (Raw)\"": float,
              "\"Battery Power* [uW] (Delta)\"": float,
              "Time  [ms]": float,
              "\"GPU Frequency [KHz]\"": float,
              "Time  [ms]": float,
              "\"GPU Load [%]\"": float,
              "Time  [ms]": float,
              "\"CPU1 Frequency [kHz]\"": float,
              "Time  [ms]": float,
              "\"CPU2 Frequency [kHz]\"": float,
              "Time  [ms]": float,
              "\"CPU3 Frequency [kHz]\"": float,
              "Time  [ms]": float,
              "\"CPU4 Frequency [kHz]\"": float,
              "Time  [ms]": float,
              "\"CPU1 Load [%]\"": float,
              "Time  [ms]": float,
              "\"CPU2 Load [%]\"": float,
              "Time  [ms]": float,
              "\"CPU3 Load [%]\"": float,
              "Time  [ms]": float,
              "\"CPU4 Load [%]\"": float,
              "Time  [ms]": float,
              "\"Application State\"": float,
              "Description": str}


def print_i(message, end='\n', verbose=True):
    if verbose:
        color_print(message, color="blue", bold=True, end=end)


def print_w(message, end='\n', verbose=True):
    if verbose:
        color_print(message, color="yellow", end=end)


def print_e(message, end='\n', verbose=True):
    if verbose:
        color_print(message, color="red", bold=True, end=end)


def print_d(message, end='\n', flush=True, verbose=True):
    if verbose:
        print(message, end=end, flush=flush)


def compare(x, y, operator):
    if operator == "=":
        return x == y
    elif operator == "!=":
        return x != y
    elif operator == ">":
        return x > y
    elif operator == "<":
        return x < y
    elif operator == ">=":
        return x >= y
    elif operator == "<=":
        return x <= y
    else:
        return False


def run_command(command, dir=None, timeout=None):
    pipes = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, cwd=dir)
    try:
        std_out, std_err = pipes.communicate(timeout=timeout)
    except TimeoutExpired as e:
        return -9, "", "Command '" + command + "' timed out after " + str(timeout) + " seconds"
    else:
        return pipes.returncode, std_out.decode("UTF-8", errors="ignore"), std_err.decode("UTF-8", errors="ignore")


def git_clean(folder):
    git_folder = folder
    for root, dirs, files in walk(folder):
        if ".git" in dirs:
            git_folder = root
            break
    git_clean = run_command("git clean -df", dir=git_folder)
    git_clean = run_command("git checkout -- .", dir=git_folder)


def remove_ignored_folders(proj_folder):
    for root, dirs, files in walk(proj_folder):
        for d in dirs:
            if d in cs_ignored_folders:
                rmtree(path.join(root, d))
                return


def compare(x, y, operator):
    if operator == "=":
        return x == y
    elif operator == "!=":
        return x != y
    elif operator == ">":
        return x > y
    elif operator == "<":
        return x < y
    elif operator == ">=":
        return x >= y
    elif operator == "<=":
        return x <= y
    else:
        return False


def make_dir(dir, del_first=False):
    if path.exists(dir) and del_first:
        rmtree(dir)

    if not path.exists(dir):
        try:
            makedirs(dir)
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e


def save_text(content, file, append=False):
    if not path.exists(path.dirname(file)):
        try:
            makedirs(path.dirname(file))
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e

    if append:
        action = "a+"
    else:
        action = "w+"
    with open(file, action) as text_file:
        text_file.write(content)


def log_text(content, file, log=False):
    if not path.exists(path.dirname(file)):
        try:
            makedirs(path.dirname(file))
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e

    if log:
        save_text(content, file, append=True)


def save_json(json_dict, file):
    if not path.exists(path.dirname(file)):
        try:
            makedirs(path.dirname(file))
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e

    with open(file, 'w+') as fp:
        json.dump(json_dict, fp, indent=4, sort_keys=True)


def load_json(file):
    d = {}
    with open(file, "r")  as f:
        d = json.load(f)
    return d


def cp_tree(src, dst):
    if path.exists(dst):
        rmtree(dst)
    copytree(src, dst)


def files_by_type(dir_path, suffix, name_only=False):
    lst = []
    for root, dirs, files in walk(dir_path):
        for file in files:
            if file.endswith(suffix):
                if name_only:
                    lst.append(re.sub(dir_path, '', path.join(root, file)))
                else:
                    lst.append(path.join(root, file))
    return lst


def files_by_name(dir_path, name, name_only=False):
    lst = []
    for root, dirs, files in walk(dir_path):
        for file in files:
            if file == name:
                if name_only:
                    lst.append(re.sub(dir_path, '', path.join(root, file)))
                else:
                    lst.append(path.join(root, file))
    return lst


def start_measures():
    trepn_init = "adb shell am startservice --user 0 com.quicinc.trepn/.TrepnService"
    start_measure_command = "adb shell am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value \"1\" -e com.quicinc.Trepn.UpdateAppState.Value.Desc \"started\""

    run_command(trepn_init)
    run_command(
        "adb shell am broadcast -a com.quicinc.trepn.start_profiling -e com.quicinc.trepn.database_file \"myfile\"")
    run_command("sleep 5")
    run_command(start_measure_command)


def stop_measures(seed, index, expected_repeats=1):
    stop_measure_command = "adb shell am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value \"0\" -e com.quicinc.Trepn.UpdateAppState.Value.Desc \"stopped\""
    run_command(stop_measure_command)

    if expected_repeats == 1:
        output_file = cs_measure_file_prefix + str(seed)
    else:
        output_file = cs_measure_file_prefix + str(seed) + "_" + str(index)

    run_command("adb shell am broadcast -a com.quicinc.trepn.stop_profiling")
    run_command("sleep 5")
    run_command(
        "adb shell am broadcast -a com.quicinc.trepn.export_to_csv -e com.quicinc.trepn.export_db_input_file \"myfile\" -e com.quicinc.trepn.export_csv_output_file \"" + output_file + "\"")

    # to disable all possible monkeys that can still be running:
    run_command(
        "adb shell ps | grep \"com.android.commands.monkey\" | grep -v \"grep\" | awk '{print $2}' | xargs -I{} adb shell kill -9 {}")


def clean_measure_tool_files(device_dir):
    run_command('adb shell "rm -rf ' + device_dir + '/*.db"')
    run_command('adb shell "rm -rf ' + device_dir + '/*.db-shm"')
    run_command('adb shell "rm -rf ' + device_dir + '/*.db-wal"')
    run_command('adb shell "rm -rf ' + device_dir + '/*.csv"')
    run_command('adb shell "rm -rf ' + device_dir + '/trepn_state"')


def force_stop_app(package_name):
    run_command("adb shell input keyevent \"KEYCODE_HOME\"")
    run_command("adb shell input keyevent \"KEYCODE_BACK\"")
    run_command("adb shell am force-stop " + package_name)
    run_command("adb shell pm clear " + package_name)


def package_name_from_apk(apk_path):
    ret_code, s_out, s_err = run_command(cs_aapt_path + " dump badging " + apk_path + " | grep \"package: name\"")
    if (ret_code == 0) and (s_out != ""):
        for o in s_out.split(" "):
            m = re.match(r"name='(.+)'", o)
            if m:
                return m.group(1)
    else:
        return ""


def get_battery_level():
    ret_code, out, err = run_command("adb shell dumpsys battery | grep level")
    if ret_code == 0:
        out_splited = out.replace(" ", "").split(":")
        if (len(out_splited) == 2):
            try:
                level = int(out_splited[1])
                return level
            except ValueError as e:
                return 100  # if we can't get the value for some reason, let's assume its 100 (full battery)
    else:
        return 100  # if we can't get the value for some reason, let's assume its 100 (full battery)


def add_permissions(permissions, manifest):
    try:
        # ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
        tree = ET.parse(manifest)
        root = tree.getroot()
        namespace1 = 'xmlns:ns0="http://schemas.android.com/apk/res/android"'
        namespace2 = 'xmlns:android="http://schemas.android.com/apk/res/android"'
        if (namespace1 not in ET.tostring(root).decode("UTF-8")) and (
                namespace2 not in ET.tostring(root).decode("UTF-8")):
            root.attrib["xmlns:android"] = "http://schemas.android.com/apk/res/android"
    except ET.ParseError as e:
        return 1

    used_perm = []
    for perm in root.iter("uses-permission"):
        used_perm += perm.attrib.values()

    for p in permissions:
        if p not in used_perm:
            new_perm = ET.SubElement(root, "uses-permission")
            new_perm.attrib = {"android:name": p}

    tree.write(manifest)
    # fix the namespace problem
    with fileinput.FileInput(manifest, inplace=True, backup='.bck') as f:
        for line in f:
            new_line = re.sub(r"xmlns:ns0", r"xmlns:android", line)
            new_line = re.sub(r"ns0:", r"android:", new_line)
            print(new_line, end='')
    return 0


def count_occurences(lst, within_list=None):
    res = []
    if type(lst) is dict:
        count = lst

    elif type(lst) is list:
        count = Counter(lst)

    for k, v in count.items():
        if within_list and k in within_list:
            res.append({"name": k, "count": v})
        if within_list == None:
            res.append({"name": k, "count": v})

    return res


def has_all_refactorings(transformed, refactorings):
    trans_names = []
    for t in transformed:
        if "name" in t.keys():
            trans_names.append(t["name"])
    return all(i in trans_names for i in refactorings)


def is_scenario_tested(scenarios, combo_id, app_id):
    for s in scenarios["finished"]:
        if all(i in s.keys() for i in ["id", "apps"]):
            if (s["id"] == combo_id) and (app_id in s["apps"]):
                return True
    return False


def is_combo_done(scenarios, combo_id):
    for s in scenarios["finished"]:
        if all(i in s.keys() for i in ["id", "apps", "status"]):
            if (s["id"] == combo_id) and (s["status"] == "done"):
                return True
    return False


def add_finished_scenario(scenarios, combo_id, app_id):
    if len(scenarios["finished"]) == 0:
        if len(app_id) > 0:
            app_list = [app_id]
        else:
            # no app_id was provided, meaning this is a combo with no apps.
            app_list = []
        scenarios["finished"] = [{"id": combo_id, "apps": app_list, "status": "ongoing"}]

    added = False
    for s in scenarios["finished"]:
        if all(i in s.keys() for i in ["id", "apps"]):
            if s["id"] == combo_id:
                if len(app_id) > 0:
                    s["apps"].append(app_id)
                added = True

    if not added:
        if len(app_id) > 0:
            app_list = [app_id]
        else:
            # no app_id was provided, meaning this is a combo with no apps.
            app_list = []
        scenarios["finished"].append({"id": combo_id, "apps": app_list})


def mark_combo_finished(scenarios, combo_id):
    marked = False
    for s in scenarios["finished"]:
        if s["id"] == combo_id:
            s["status"] = "done"
            marked = True


def start_app(package):
    start_app_cmd = "adb shell monkey -p {} 1".format(package)

    run_command("adb shell input keyevent \"KEYCODE_HOME\"")
    run_command("adb shell input keyevent \"KEYCODE_BACK\"")
    run_command("adb shell settings put system screen_brightness 0")
    ret_code, s_out, s_err = run_command(start_app_cmd)
    run_command("sleep 3")

    return ret_code, s_out, s_err


def run_monkey(monkey_seed, event_throttle, activity_events_pct, package, num_events, timeout=None):
    """
    monkey_cmd = "adb shell monkey -s {} -v --throttle {} --pct-appswitch {} -p {} --pct-syskeys 0 {}".format(monkey_seed,
                                                                                                              event_throttle,
                                                                                                              activity_events_pct,
                                                                                                              package,
                                                                                                              num_events)

    ret_code, s_out, s_err = run_command(monkey_cmd, timeout=timeout)
    """
    for i, e in enumerate(cs_monkey_seeds_events[monkey_seed]):
        cmd = " ".join(["adb shell input", e])
        ret_code, s_out, s_err = run_command(cmd, timeout=timeout)
        run_command("sleep 0.3")

    force_stop_app(package)
    return ret_code, s_out, s_err


def get_monkey_event_percentages(monkey_out):
    res = {}
    consider_lines = False
    for l in monkey_out:
        if ("Event percentages:" in l):
            consider_lines = True
        elif (":Switch:" in l):
            consider_lines = False
        elif consider_lines:
            key_val = re.sub(r"//|%| ", "", l).split(":")
            key = key_val[0]
            val = key_val[1]
            res[key] = (float(val)) / 100

    return res


def remove_tables(file, *idxs):
    indexes = list(idxs)
    indexes.sort()

    lines = []
    with open(file, "r") as f:
        lines = f.readlines()

    split_indexes = []
    for i, l in enumerate(lines):
        if l == "\n":
            split_indexes.append(i)

    tables = np.split(lines, split_indexes)
    for e, i in enumerate(indexes):
        if (i - e) < len(tables):
            del tables[(i - e)]

    content = ""
    for r in tables:
        content += "".join(list(r))
    with open(file, "w") as f:
        f.write(content)


# returns the energy consumption value (in Joules, by default) and the elapsed time (in seconds, by default),
# calculated from a list of timestamps (in ms) and power values (in mW).
def energy_consumed(timestamps, powers, ret_energy=1, ret_time=1):
    elapsed_time = (timestamps[-1] - timestamps[0]) / 1000
    pairs = list(zip(timestamps, powers))

    res, last = 0, None
    for t, p in pairs:
        #		if p == 0:
        #			continue  # to ignore measures with power = 0
        if last:
            last_time, last_power = last
            val = ((t - last_time) / 1000) * (((last_power + p) / 2) / 1000)
            res += val

        last = t, p

    return (elapsed_time * ret_time), (res * ret_energy)


def filter_df_rows(df, column_name, values):
    return df.loc[df[column_name].isin(values)]


def df_power_time_rows(df, columns=None):
    fdf = filter_df_rows(df, "Application State", [1, 2])
    try:
        last_index = list(fdf[(fdf["Application State"] == 2)].index)[0]
        fdf = fdf.drop(fdf[(fdf.index > last_index)].index)
        if (not columns) or (type(columns) is not list):
            return fdf
        else:
            if any(c not in fdf.columns for c in columns):
                return fdf
            else:
                return fdf[columns]
    except IndexError as e:
        raise e


def test_results2(files, cols, app, seed):
    try:
        res_energy = []
        res_time = []
        for file in files:
            df = pd.read_csv(file, dtype=csv_dtypes)
            fdf = df_power_time_rows(df, columns=cols)
            timestamps = list(fdf[fdf.columns[0]])
            powers = list(fdf[fdf.columns[1]])
            # Power values are in uW, and timestamps are in ms.
            # Normalize...
            powers = [p / 1000 for p in powers]
            # return the calculated energy and elapsed time values (in ms and mJ, respectively)
            time, energy = energy_consumed(timestamps, powers, ret_time=1000, ret_energy=1000)
            res_energy.append(energy)
            res_time.append(time)
        return res_time, res_energy
    except IndexError as e:
        raise NoTestResultsError(app, seed)
    except FileNotFoundError as e:
        raise NoTestResultsError(app, seed)  # return -1, -1


def test_results(file, cols, app, seed):
    try:
        df = pd.read_csv(file, dtype=csv_dtypes)
        fdf = df_power_time_rows(df, columns=cols)
        timestamps = list(fdf[fdf.columns[0]])
        powers = list(fdf[fdf.columns[1]])
        # Power values are in uW, and timestamps are in ms.
        # Normalize...
        powers = [p / 1000 for p in powers]
        # return the calculated energy and elapsed time values (in ms and mJ, respectively)
        return energy_consumed(timestamps, powers, ret_time=1000, ret_energy=1000)
    except pd.errors.EmptyDataError as e:
        raise NoTestResultsError(app, seed)
    except IndexError as e:
        raise NoTestResultsError(app, seed)
    except FileNotFoundError as e:
        raise NoTestResultsError(app, seed)  # return -1, -1


def get_seed_result_files(files, seed, prefix):
    res = []
    for f in files:
        file_name = path.basename(f)
        if (file_name.startswith(prefix + str(seed) + "_") or (file_name == prefix + str(seed) + ".csv")):
            res.append(f)
    return res


def get_seed_trace_file(files, seed, prefix):
    for f in files:
        file_name = path.basename(f)
        if (file_name.startswith(prefix + str(seed) + "_") or (file_name == prefix + str(seed))):
            return f
    return ""


def read_lines(file):
    try:
        with open(file, "r") as fp:
            lines = list(map(lambda l: l.replace("\n", ""), fp.readlines()))
            return lines
    except FileNotFoundError as e:
        return []


# dump and die
def dd(var):
    print(var)
    exit(0)


class Stack:
    def __init__(self):
        self._storage = []

    def isEmpty(self):
        return len(self._storage) == 0

    def push(self, p):
        self._storage.append(p)

    def pop(self):
        return self._storage.pop()

    def peek(self):
        if len(self._storage) == 0:
            return ""
        else:
            return self._storage[-1]
