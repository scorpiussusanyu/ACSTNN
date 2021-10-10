#!/usr/bin/python3

from os import path, walk
from shutil import move

issue_chars_map = {"." : "_", " " : "", "-" : "__"}

def replace_issue_chars(path):
	new_path = path
	for a, b in issue_chars_map.items():
		new_path = new_path.replace(a, b)

	return new_path

def fix_folder_names(main_folder):
	if any(i in path.basename(main_folder) for i in issue_chars_map.keys()):
		new_main_folder = path.join(path.dirname(main_folder), 
									replace_issue_chars(path.basename(main_folder))
									)
	else:
		new_main_folder = main_folder

	to_fix = []
	for root, dirs, files in walk(main_folder):
		if any(i in root for i in issue_chars_map.keys()):
			to_fix.insert(0, root)  # inserting at positing '0' assures that the 
									# first folder to fix is the deepest folder.

	fixed = []
	for f in to_fix:
		root_dir = path.dirname(f)
		dir_name = path.basename(f)
		new_name = replace_issue_chars(dir_name)
		dst = path.join(root_dir, new_name)
		move(f, dst)
		fixed.insert(0, {"before" : f, "after" : dst})

	return new_main_folder, fixed

# all the strings in `files` are paths to files, never folders.
def get_fixed_file_paths(root, files):
	res = []
	for file in files:
		f = file.replace(root, "")
		root_dir = path.dirname(f)
		file_name = path.basename(f)
		res.append(path.join(root + replace_issue_chars(root_dir), file_name))

	return res

# CAUTION: this method should only be used in a controlled way, to undo a previous 
# operation performed by `fix_folder_names`
def undo_fix_folder_names(data):
	for d in data:
		if ("before" in d.keys()) and ("after" in d.keys()):
			move(d["after"], d["before"])

