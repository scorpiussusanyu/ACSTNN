#!/usr/bin/python3

"""
Local storage settings.
"""

"""
Path to a local folder where the code of each application under test 
is going to be temporarily stored after being forked into 3 versions.
"""
cs_local_apps_folder = "/home/marco/temp_apps"


"""
Path to a local folder where the results of each EGAP combination will 
be stored.
"""
cs_local_results_folder = "/home/marco/coevolgy_res"


"""
Path to a local folder where the results of all tests executed in an 
application will be stored.
"""
cs_local_data_folder = "/home/marco/coevolgy_res/apps_data"


"""
Path to a local folder where the assets used by the refactor and filter 
operators are stored.
"""
cs_assets_folder = "/home/marco/repos/greens/co-evolgy/EBugsRefactor/assets"


"""
Path to the location in the device where the test results are stored.
"""
cs_device_dir = "/mnt/sdcard/trepn"

## Generic filenames

"""
Abstract filename to store, for each app, the results of the 
miner operator.
"""
cs_lint_result_file = "{}-lint-ebugs.json"


"""
Filename used by the filter operator to store the overall 
results of EGAPs found. 
"""
cs_agg_result_file = "agg_EGAPs.json"


## File Prefixs

"""
Prefix for the energy measurement files.
"""
cs_measure_file_prefix = "measureTrace"


"""
Prefix for the EGAP tracing files.
"""
cs_trace_file_prefix = "traces"


"""
Prefix for the monkey events files.
"""
cs_monkey_stats_file_prefix = "statsMonkey"


"""
Prefix for the method tracing files.
"""
cs_trace_methods_file_prefix = "methodTraces"
