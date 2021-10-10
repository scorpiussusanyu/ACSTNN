#!/usr/bin/python3

"""
Miscellaneous settings.
"""

"""
If set to 'True', any repository folder will be clean before 
running any operation on the files. In other words, the command 
`git clean -df; git checkout -- .` will be executed.
"""
cs_clean_repo_first = True


"""
If set to 'True', the temporary folder of each application under 
test will be removed after the test results are generated and 
stored, hence reducing the number of disk writes and used disk space.
Setting it to 'False' preserves the code of all 3 versions of an 
application, so it is possible to later compare the differences
"""
cs_clean_local_apps_folder = False


"""
Is set to 'True', the raw/untreated result files of each application 
tested for each EGAP combination will be removed after the JSON result 
files are generated, hence reducing the percentage of disk used.
"""
cs_clean_local_data_folder = False


"""
If set to 'True', the output from the operators will be logged in 
different files, inside the 'log' folder.
"""
cs_logging = True


"""
List of folders that may be contained in an Android application 
source folder structure, and should be ignored by all the operators.
"""
cs_ignored_folders = ["_TRANSFORMED_"]
