#!/usr/bin/python3

import os, itertools, time
from shutil import copytree, rmtree

from ebugs_refactor.err.exceptions import NoTestResultsError
from ebugs_refactor.tools.util import *
from ebugs_refactor.tools.gradle_util import *

import ebugs_refactor.operators.e_filter as flt
import ebugs_refactor.operators.e_refactor as rfc

from ebugs_refactor.settings.remote import *
from ebugs_refactor.settings.app_test import *
from ebugs_refactor.settings.storage import cs_measure_file_prefix, cs_trace_file_prefix, cs_trace_methods_file_prefix, \
    cs_monkey_stats_file_prefix, cs_local_apps_folder, cs_local_results_folder, cs_local_data_folder, cs_assets_folder, \
    cs_device_dir
from ebugs_refactor.settings.egaps import cs_EGAPs
from ebugs_refactor.settings.misc import cs_logging, cs_clean_local_apps_folder, cs_clean_local_data_folder

_finished_file = "log/finished.json"

verbose = True


def combo_to_queries(combination):
    queries = []
    for ebug in combination:
        query = ebug, ">", 0
        queries.append(query)
    return queries


def ebugs_combos(elems):
    all_combos = []
    for r in range(1, len(elems) + 1):
        for subset in itertools.combinations(elems, r):
            combo = []
            for s in subset:
                combo.append(s)
            combo.sort()
            all_combos.append(combo)

    return all_combos


def cool_down_phone(phone_usage_time):
    # Check if the phone is being under usage for too long, and if so let it rest
    # if phone_usage_time >= cs_phone_usage_threshold:
    if get_battery_level() < 100:
        print_i("\t\t»» Step 2.2.6 »» Cooling down phone", verbose=verbose)
        phone_usage_time = 0
        while get_battery_level() < 100:
            run_command(" ".join(["sleep", str(cs_recover_time)]))


def tear_down_app(scenarios, combo_id, combo_data, app_id, app_data, errors=None):
    if errors:
        app_data["errors"].append(errors)

    combo_data["apps"].append(app_data.copy())
    add_finished_scenario(scenarios, combo_id, app_id)
    save_json(scenarios, _finished_file)
    save_json(app_data, os.path.join(cs_local_results_folder, str(combo_id), str(app_id) + ".json"))  # backup


def fix_project_configs(project_folder, data, clean_first=True):
    gradlew_folder = os.path.dirname(data["gradle script"])

    if ("gradle" in data.keys()) and (data["gradle"]):
        if clean_first:
            git_clean(project_folder)
            remove_ignored_folders(project_folder)
        # To avoid issues with non-build files being included in the list of gradle files
        gradle_files = list(filter(lambda f: f.endswith("build.gradle"), data["gradle files"]))
        # Edit gradle build files
        transform_configs(gradle_files)
        if ("wrapper-properties" in data.keys()) and (all(os.path.isfile(f) for f in data["wrapper-properties"])):
            transform_wrapper(data["wrapper-properties"])
        else:
            # if the gradle wrapper folder does not exist, let's use
            # the default one contained in the assets folder
            cpt = cp_tree(os.path.join(cs_assets_folder, "gradle"), os.path.join(gradlew_folder, "gradle"))

        if "local-properties" in data.keys():
            transform_properties(data["local-properties"])


def fork_app_data(data, original, refactored, tracing):
    data_orig = data.copy()
    data_refac = data.copy()
    data_trace = data.copy()

    app_id = data["app id"]

    # change original
    data_orig["folder"] = original
    data_orig["gradle script"] = os.path.join(original, data_orig["gradle script"].split(app_id + "/")[1])
    gradle_files = []
    for f in data_orig["gradle files"]:
        gradle_files.append(os.path.join(original, f.split(app_id + "/")[1]))
    data_orig["gradle files"] = gradle_files
    if "wrapper-properties" in data_orig.keys():
        property_files = []
        for p in data_orig["wrapper-properties"]:
            property_files.append(os.path.join(original, p.split(app_id + "/")[1]))
        data_orig["wrapper-properties"] = property_files

    # change refactored
    data_refac["folder"] = refactored
    data_refac["gradle script"] = os.path.join(refactored, data_refac["gradle script"].split(app_id + "/")[1])
    gradle_files = []
    for f in data_refac["gradle files"]:
        gradle_files.append(os.path.join(refactored, f.split(app_id + "/")[1]))
    data_refac["gradle files"] = gradle_files
    if "wrapper-properties" in data_refac.keys():
        property_files = []
        for p in data_refac["wrapper-properties"]:
            property_files.append(os.path.join(refactored, p.split(app_id + "/")[1]))
        data_refac["wrapper-properties"] = property_files

    # change tracing
    data_trace["folder"] = tracing
    data_trace["gradle script"] = os.path.join(tracing, data_trace["gradle script"].split(app_id + "/")[1])
    gradle_files = []
    for f in data_trace["gradle files"]:
        gradle_files.append(os.path.join(tracing, f.split(app_id + "/")[1]))
    data_trace["gradle files"] = gradle_files
    if "wrapper-properties" in data_trace.keys():
        property_files = []
        for p in data_trace["wrapper-properties"]:
            os.path.join(tracing, p.split(app_id + "/")[1])
        data_trace["wrapper-properties"] = property_files

    return data_orig, data_refac, data_trace


def run_and_measure(package_name, seed, measure, timeout, repeats, out_folder):
    for r in range(repeats):
        print_d(".", end="", verbose=verbose)
        run_command("adb shell \"echo " + str(seed) + " > " + os.path.join(cs_device_dir, "MonkeySeed") + "\"")

        start_app(package_name)  # for now, let's just ignore the output from the method (return code & output)
        if measure:
            start_measures()

        ret_code, s_out, s_err = run_monkey(seed, cs_throttle, cs_pct_activity_events, package_name, cs_monkey_events,
                                            timeout=timeout)
        if not measure:
            save_text(s_out, os.path.join(out_folder, cs_monkey_stats_file_prefix + str(seed)))

        if ret_code == -9:
            # timeout occured. force kill the monkey processes
            run_command(
                "adb shell ps | grep \"com.android.commands.monkey\" | grep -v \"grep\" | awk '{print $2}' | xargs -I{} adb shell kill -9 {}")

        if measure:
            stop_measures(seed, r, expected_repeats=repeats)
    print_d(" ", end="", verbose=verbose)


# builds the app, and runs the monkey tests.
# if everything goes well, a pair (return code, list of pulled files) is returned.
# it an error occurs, it returns a pair (return code, error).
# TODO: add more exceptions for things that can go wrong in running all the commands.
def test_app(data, data_folder, tag, measure=True, repeats=1):
    out_folder = os.path.join(data_folder, tag)
    # before running anything, let's make sure there is no previous result files in the device folder
    r, o, e = run_command("adb shell ls " + cs_device_dir)
    prev_dev_files = list(filter(lambda f: re.match(
        r"(" + cs_measure_file_prefix + "|" + cs_trace_file_prefix + "|" + cs_trace_methods_file_prefix + ").+", f),
                                 o.split("\n")))
    prev_dev_files = list(map(lambda x: os.path.join(cs_device_dir, x.replace("\r", "")), prev_dev_files))

    if (not cs_replace_test_results) and (os.path.exists(out_folder)):
        prev_out_files = [f for f in os.listdir(out_folder) if os.path.isfile(os.path.join(out_folder, f))]
        if len(prev_out_files) > 0:
            # if there are previous results files, and the indication is to
            # maintain them, then use these instead of running tests again.
            prev_out_files = list(map(lambda i: os.path.join(out_folder, i), prev_out_files))
            return 0, prev_out_files

    if (len(prev_dev_files) > 0) and verbose:
        print_d("\t\t\t* Removing previous result files")
    for f in prev_dev_files:
        run_command("adb shell rm -rf " + f)

    make_dir(out_folder)
    gradle_script = data["gradle script"]
    proj_folder = os.path.dirname(gradle_script)

    run_command("chmod 755 " + gradle_script)
    print_d("\t\t\t* Building/Installing", verbose=verbose)
    command = " ".join([gradle_script, "-p", proj_folder, "assembleDebug", 'installDebug'])
    returncode, std_out, std_err = run_command(command)
    if returncode != 0:
        # an error occured while building/installing!
        return returncode, "Error while building or installing: \n" + std_err
    else:
        try:
            # get the package name
            apk = list(filter(lambda x: "-unaligned" not in x, files_by_type(proj_folder, ".apk")))[0]
            package_name = package_name_from_apk(apk)

            print_d("\t\t\t* Running tests [package=" + package_name + "]", verbose=verbose)

            # grant the package write/read permissions
            run_command("adb shell pm grant " + package_name + " android.permission.READ_EXTERNAL_STORAGE")
            run_command("adb shell pm grant " + package_name + " android.permission.WRITE_EXTERNAL_STORAGE")

            # execute the tests
            print_d("\t\t\t\t", end=" ")
            for seed in cs_monkey_seeds:
                run_and_measure(package_name, seed, measure, cs_monkey_timeout, repeats, out_folder)
            print()

            # clear and uninstall the app
            run_command("adb shell pm clear " + package_name)
            run_command("adb shell am force-stop " + package_name)
            run_command("adb uninstall " + package_name)

            # pull files from device, and remove them from the device afterwards
            r, o, e = run_command("adb shell ls " + cs_device_dir)
            pulled_files = list(filter(lambda f: re.match(
                r"(" + cs_measure_file_prefix + "|" + cs_trace_file_prefix + "|" + cs_trace_methods_file_prefix + ").+",
                f), o.split("\n")))
            pulled_files = list(map(lambda x: os.path.join(cs_device_dir, x.replace("\r", "")), pulled_files))
            for f in pulled_files:
                pull_cmd = " ".join(["adb", "pull", f, out_folder])
                run_command(pull_cmd)
                run_command("adb shell rm -rf " + f)

            monkey_stats_file = os.path.join(out_folder, cs_monkey_stats_file_prefix + str(seed))
            if (not measure) and (os.path.isfile(monkey_stats_file)):
                pulled_files.append(monkey_stats_file)

        except IndexError as e:
            return 1, "APK file not generated"

    return 0, list(map(lambda i: i.replace(cs_device_dir, out_folder), pulled_files))


def main(apps_data_folder, ignored_combos=[]):
    # Initial configurations
    make_dir(cs_local_apps_folder)
    make_dir(cs_local_results_folder)
    make_dir("log")
    finished_scenarios = {"finished": []}
    if os.path.isfile(_finished_file):
        finished_scenarios = load_json(_finished_file)

    all_infos = []
    phone_usage_time = 0

    # Step 1: generate set of possible combinations of ebugs
    print_i("# Step 1 # Generating eBugs combinations", verbose=verbose)
    elems = list(map(lambda i: "l:" + i, cs_EGAPs))
    combos = ebugs_combos(elems)

    print_i("# Step 2 # Puting combinations through the pipeline:", verbose=verbose)

    # Step 2: put each combination through the pipeline
    for i, combo in enumerate(combos):
        refactorings = list(map(lambda x: x.split(":")[1], combo))
        combo_tag = "_".join(refactorings)
        if (combo_tag in ignored_combos) or (is_combo_done(finished_scenarios, combo_tag)):
            print_i("  # Combo (" + str(i + 1) + ") " + str(combo) + " already tested or marked ignorable")
            continue

        combo_info = {}
        combo_info["id"] = i
        combo_info["tag"] = combo_tag
        combo_info["eBugs"] = refactorings
        combo_info["status"] = "ongoing"

        # Pipeline Structure:
        #	$2.1 » get the list of apps with that combination
        print_i("  # Combo (" + str(i + 1) + ") of " + str(len(combos)) + ": " + str(combo), verbose=verbose)
        print_i("\t» Step 2.1 » Filtering apps with combination", verbose=verbose)
        apps = flt.fetch_apps(apps_data_folder, combo_to_queries(combo))
        combo_info["apps"] = []
        if len(apps) == 0:
            # This particular combination has no apps
            print_w("\t  » Combination " + str(combo) + " not in any app. Skipping...", verbose=verbose)
            add_finished_scenario(finished_scenarios, combo_tag, "")
            mark_combo_finished(finished_scenarios, combo_tag)
            save_json(finished_scenarios, _finished_file)
            continue

        #   $2.2 » retrieve the apps from the server
        print_i("\t» Step 2.2 » Getting and testing each app", verbose=verbose)
        for j, app in enumerate(apps):
            app_id = app["app id"]
            print_i("\t  » App " + str(j + 1) + " of " + str(len(apps)) + ": " + app_id, verbose=verbose)

            # check if this particular app in this combo was already tested
            if is_scenario_tested(finished_scenarios, combo_tag, app_id):
                # it was, so we'll load the already obtained results
                app_info = load_json(os.path.join(cs_local_results_folder, str(combo_tag), str(app_id) + ".json"))
                combo_info["apps"].append(app_info.copy())
                continue

            count_refactorings = count_occurences(app["lint"], refactorings)
            app_info = {"id": app_id,
                        "errors": [],
                        "detected eBugs": count_refactorings.copy(),
                        "transformed eBugs": [],
                        "tests": []}

            temp_app_folder = os.path.join(cs_local_apps_folder, app_id)
            make_dir(temp_app_folder)
            temp_data_folder = os.path.join(cs_local_data_folder, combo_tag, app_id, "data")
            make_dir(temp_data_folder, del_first=cs_replace_test_results)
            copy_cmd = "scp -r " + cs_remote + ":" if cs_remote else "cp -r "
            cmd = copy_cmd + os.path.join(cs_remote_apps_folder, app_id) + " _original"
            # """
            if not os.path.exists(os.path.join(temp_app_folder, "_original")):
                ret_code, s_out, s_err = run_command(cmd, dir=temp_app_folder, timeout=cs_remote_copy_timeout)
                if ret_code != 0:
                    print_e("An error occured at copying app '" + app_id + "' from server '" + cs_remote + "'")
                    print("- - - - - - - - - -")
                    print(s_err)
                    app_info["errors"].append(" ".join(["[original]", s_err]))
                    combo_info["apps"].append(app_info.copy())
                    log_text(app_id + "\n", os.path.join("log", "failed_scp.log"), log=cs_logging)
                    continue
            # """
            #   $2.2.1 » create 3 versions of the app: original, refactored and trace
            versions = {"original": os.path.join(temp_app_folder, "_original"),
                        "refactored": os.path.join(temp_app_folder, "_refactored"),
                        "tracing": os.path.join(temp_app_folder, "_tracing")}
            print_i("\t\t»» Step 2.2.1 »» Creating 3 testable versions", verbose=verbose)

            app_orig, app_refac, app_trace = fork_app_data(app, versions["original"],
                                                           versions["refactored"],
                                                           versions["tracing"])

            print_d("\t\t  => original", verbose=verbose)
            fix_project_configs(versions["original"], app_orig)

            cp_tree(versions["original"], versions["refactored"])
            cp_tree(versions["original"], versions["tracing"])

            print_d("\t\t  => refactored", verbose=verbose)
            ret, out = rfc.refactor_app(app_refac, refactorings, tracing=False)
            if ret != 0:
                print_w("\t\t  [refactored] Unexpected error occured while refactoring", verbose=verbose)
                tear_down_app(finished_scenarios, combo_tag, combo_info, app_id, app_info, errors="[refactored] " + out)
                continue
            if (len(out) == 0) or not has_all_refactorings(out, refactorings):
                print_w("\t\t  [refactored] Skipping app without expected transformations performed", verbose=verbose)
                app_info["transformed eBugs"] = out.copy()
                tear_down_app(finished_scenarios, combo_tag, combo_info, app_id, app_info)
                continue

            print_d("\t\t  => tracing", verbose=verbose)
            ret, out = rfc.refactor_app(app_trace, refactorings, tracing=True)
            if ret != 0:
                print_w("\t\t  [tracing] Unexpected error occured while refactoring", verbose=verbose)
                tear_down_app(finished_scenarios, combo_tag, combo_info, app_id, app_info, errors="[tracing] " + out)
                continue
            # if we reach this point, it means `out` is the list of transformed refactorings
            refactor_trace = out
            app_info["transformed eBugs"] = refactor_trace.copy()

            #   $2.2.2 » run the monkey tests for each app versions
            print_i("\t\t»» Step 2.2.2 »» Running monkey tests", verbose=verbose)

            print_d("\t\t  => original", verbose=verbose)
            start_time = time.time()
            ret, out_orig = test_app(app_orig, temp_data_folder, "original", repeats=cs_measure_repeats)
            phone_usage_time += (time.time() - start_time)
            cool_down_phone(phone_usage_time)
            if ret != 0:
                tear_down_app(finished_scenarios, combo_tag, combo_info, app_id, app_info,
                              errors="[EXEC] [original]" + out_orig)
                continue

            print_d("\t\t  => refactored", verbose=verbose)
            start_time = time.time()
            ret, out_refac = test_app(app_refac, temp_data_folder, "refactored", repeats=cs_measure_repeats)
            phone_usage_time += (time.time() - start_time)
            cool_down_phone(phone_usage_time)
            if ret != 0:
                tear_down_app(finished_scenarios, combo_tag, combo_info, app_id, app_info,
                              errors="[EXEC] [refactored]" + out_refac)
                continue

            print_d("\t\t  => tracing", verbose=verbose)
            start_time = time.time()
            ret, out_trace = test_app(app_trace, temp_data_folder, "tracing", measure=False)
            phone_usage_time += (time.time() - start_time)
            cool_down_phone(phone_usage_time)
            if ret != 0:
                tear_down_app(finished_scenarios, combo_tag, combo_info, app_id, app_info,
                              errors="[EXEC] [tracing]" + out_trace)
                continue

            #   $2.2.3 » parse gain values
            print_i("\t\t»» Step 2.2.3 »» Parsing results", verbose=verbose)
            orig_files = out_orig.copy()
            orig_files.sort()
            for f in orig_files:
                remove_tables(f, 0, 2, 3)  # to maintain only the consumptions table
            refac_files = out_refac.copy()
            refac_files.sort()
            for f in refac_files:
                remove_tables(f, 0, 2, 3)  # to maintain only the consumptions table
            trace_files = out_trace.copy()
            trace_files.sort()

            for test_seed in cs_monkey_seeds:
                orig_csvs = get_seed_result_files(orig_files, test_seed, cs_measure_file_prefix)
                refac_csvs = get_seed_result_files(refac_files, test_seed, cs_measure_file_prefix)
                trace_file = get_seed_trace_file(trace_files, test_seed, cs_trace_file_prefix)

                methods_trace = count_occurences(
                    read_lines(get_seed_trace_file(trace_files, test_seed, cs_trace_methods_file_prefix)))
                monkey_stats_content = read_lines(
                    get_seed_trace_file(trace_files, test_seed, cs_monkey_stats_file_prefix))
                monkey_stats = get_monkey_event_percentages(monkey_stats_content)

                traces = []

                try:
                    time_o, energy_o = test_results2(orig_csvs, ["Time  [ms]", "Battery Power* [uW] (Raw)"], app_id,
                                                     test_seed)
                    time_r, energy_r = test_results2(refac_csvs, ["Time  [ms]", "Battery Power* [uW] (Raw)"], app_id,
                                                     test_seed)
                except NoTestResultsError as e:
                    log_text(" ".join([app_id, ":", str(test_seed) + "\n"]), os.path.join("log", "failed_seeds.log"),
                             log=cs_logging)
                    continue  ## TODO: instead, maybe we could try to re-run the test without results,
                    ## but carefully, since nothing guarantees it won't fail again.
                try:
                    with open(trace_file, "r") as fp:
                        lines = list(map(lambda l: l.replace("\n", ""), fp.readlines()))
                        traces = count_occurences(lines, refactorings)
                except FileNotFoundError as e:
                    traces = []

                # (Do this differently)
                # if the combo under test has the eBug "ObsoleteLayoutParam", we will assume that all
                # refactored eBugs were executed, since we cannot trace XML transformations
                if "ObsoleteLayoutParam" in refactorings:
                    traces += refactor_trace.copy()
                app_info["tests"].append({"seed": test_seed,
                                          "original": {"time": time_o, "consumption": energy_o},
                                          "refactored": {"time": time_r, "consumption": energy_r},
                                          "traces": traces.copy(),
                                          "method calls": methods_trace.copy(),
                                          "monkey stats": monkey_stats.copy()
                                          })

            #   $2.2.4 » store the results
            print_i("\t\t»» Step 2.2.4 »» Storing results", verbose=verbose)

            tear_down_app(finished_scenarios, combo_tag, combo_info, app_id, app_info)

            #   $2.2.5 » clear local apps folder
            print_i("\t\t»» Step 2.2.5 »» Clearing temporary files", verbose=verbose)

            if cs_clean_local_apps_folder:
                rmtree(temp_app_folder)

        save_json(combo_info,
                  os.path.join(cs_local_results_folder, "combos", "_".join(combo_info["eBugs"]) + ".json"))  # backup
        all_infos.append(combo_info.copy())
        mark_combo_finished(finished_scenarios, combo_tag)
        save_json(finished_scenarios, _finished_file)

    # save all results in a file (might take a while...)
    save_json(all_infos, os.path.join(cs_local_results_folder, "combos", "all_combos.json"))
    # all done! let's remove temporary files
    if cs_clean_local_apps_folder:
        rmtree(cs_local_apps_folder)

    if cs_clean_local_data_folder:
        rm_tree(cs_local_data_folder)


if __name__ == '__main__':
    machine = "all"
    to_be_ignored = []
    try:
        with open(os.path.join(".ignorable", machine + ".txt"), "r") as fp:
            lines = fp.read().splitlines()
            to_be_ignored = lines.copy()
    except FileNotFoundError as e:
        to_be_ignored = []

    apps_data_folder = "/home/marco/repos/greens/co-evolgy/EBugsRefactor/output_detector"
    main(apps_data_folder, ignored_combos=to_be_ignored)
