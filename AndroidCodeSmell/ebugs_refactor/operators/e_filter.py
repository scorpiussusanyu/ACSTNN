#!/usr/bin/python3

import os

from ebugs_refactor.tools.util import load_json, compare

from ebugs_refactor.settings.egaps import cs_EGAPs_keys


def get_files(folder):
	json_files = []
	for root, folders, files in os.walk(folder):
		for f in files:
			if f.endswith(".json"):
				json_files.append(os.path.join(root, f))

	return json_files

def load_dict(file):
	return load_json(file)

def check_queries(app_dict, queries):
	for key, cond, val in queries:
		if key.startswith("l:"):
			if "lint" not in app_dict.keys():
				return False
			k = key.split(":")[1]
			lint_elem = app_dict["lint"]
			if k == "ALL":
				has_all_ebugs = len(lint_elem) == len(cs_EGAPs_keys)
				if has_all_ebugs:
					return all(compare(lint_elem[e], val, cond) for e in cs_EGAPs_keys)
				else:
					return False
			if k == "ANY":
				return compare(len(lint_elem), val, cond)

			if (k not in lint_elem.keys()):
				if (val == 0) and (cond == "="):
					continue
				else:
					return False

			if (not compare(lint_elem[k], val, cond)):
				return False
		elif not compare(app_dict[key], val, cond):
			return False

	return True


def fetch_apps(folder, queries):
	json_files = get_files(folder)
	app_dicts = list(map(lambda f : load_dict(f), json_files))
	filtered = list(filter(lambda d : check_queries(d, queries), app_dicts))

	return filtered
