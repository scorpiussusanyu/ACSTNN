#!/usr/bin/python3

import os, re, argparse
import xml.etree.ElementTree as ET

from subprocess import check_output, Popen, PIPE
from lazyme.string import color_print

import ebugs_refactor.operators.e_filter as flt

from ebugs_refactor.settings.egaps import cs_EGAPs_keys, cs_valid_keys
from ebugs_refactor.settings.storage import cs_agg_result_file
from ebugs_refactor.tools.util import save_json


def tp_triple(string):
	pair_match = re.match(r"\(([^\(\)]+) *, *(=|>|<|>=|<=|!=) *, *([^\(\)]+)\)", string)
	if not pair_match :
		msg = "'{}' is not a valid triple '(key, condition, value)'".format(string)
		raise argparse.ArgumentTypeError(msg)
	
	key, cond, val = pair_match.group(1), pair_match.group(2), pair_match.group(3)
	if key not in cs_valid_keys.keys():
		possible_values = sorted(list(cs_valid_keys.keys()))
		msg = "'{}' is not a valid key. Possible values: {}".format(key, possible_values)
		raise argparse.ArgumentTypeError(msg)

	
	f = cs_valid_keys[key]
	if f is bool:
		if val in ["True", "true", "T", "t", "Y", "y", "Yes", "yes", "1"]:
			value = True
		elif val in ["False", "false", "F", "f", "N", "n", "No", "no", "0"]:
			value = False
		else:
			msg = "'{}' must be a boolean value.".format(value)
			raise argparse.ArgumentTypeError(msg)
	else:
		# either a string or an integer
		try:
			value = f(val)
		except ValueError as e:
			msg = "'{}' must be an integer value.".format(value)
			raise argparse.ArgumentTypeError(msg)
	
	return key, cond, value

def validate_output(output):
	for o in output:
		if o not in cs_valid_keys.keys():
			msg = "{} is not a valid key, and so it can't be print as output".format(o)
			raise argparse.ArgumentTypeError(msg)

def aggregate_lint_info(app_dicts, output):
	print("# of matches:", len(app_dicts))
	result = {}
	lint_output = list(filter(lambda i: i.startswith("l:"), output))
	result.update(list(map(lambda l: (l.split(":")[1], []), lint_output)))
	
	for app in app_dicts:
		for out in sorted(output):
			if (out.startswith("l:")) and ("lint" in app.keys()):
				lint_key = out.split(":")[1]
				if lint_key in app["lint"].keys():
					val = app["lint"][lint_key]
					result[lint_key].append(val)

	save_json(result, os.path.join("output", cs_agg_result_file))

def print_outputs(app_dicts, output):
	print("# of matches:", len(app_dicts))
	print()
	if len(output) != 0:
		if "l:ALL" in output:
			# if we want to print ALL the info about detected eBugs, we need to check 
			# if ALL eBugs keys are in the output list, and add the ones missing...
			for j, t in cs_EGAPs_keys:
				if j not in output:
					output.append(j)
			# ... and remove the reference to ALL eBugs
			output.remove("l:ALL")

		for i, app in enumerate(app_dicts):
			print("\t[Match {}]".format(i+1))
			for out in sorted(output):
				if (out.startswith("l:")) and ("lint" in app.keys()):
					lint_key = out.split(":")[1]
					if lint_key in app["lint"].keys():
						k = out.replace("l:", "> eBug ")
						val = app["lint"][lint_key]
						print("\t", k, "->", val)
				else:
					k = out
					val = app[out]
					print("\t", k, "->", val)
			print()


def main(folder, queries, output, agg=False):
	filtered = flt.fetch_apps(folder, queries)
	
	if agg:
		aggregate_lint_info(filtered, output)
	else:
		print_outputs(filtered, output)	

if __name__ == "__main__":
	data_folder = "/home/marco/repos/greens/co-evolgy/EBugsRefactor/output_detector"
	valid_out_keys = cs_valid_keys.copy()
	del valid_out_keys["l:ANY"]

	parser = argparse.ArgumentParser(description="A filter tool for the eBugs lint analysis.")
	parser.add_argument("queries", metavar="Q", type=tp_triple, nargs="+", 
						help="The list of triples in the form '(key, condition, value)' used to query the "+
						"information. `key` is the name of the attribute to check, `condition` is a boolean "+
						"operator (=, !=, >, <, >=, <=), and `value` is the value to compare with. Example: "+
						"`ebugs_filter.py \"(l:Wakelock, >=, 1)\"` will look for apps with at least 1 \"Wakelock\" eBug ")
	parser.add_argument("--out", "-o", metavar="o", nargs="+", default=list(valid_out_keys.keys()), 
						help="The list of attributes to be printed to output. ")
	parser.add_argument("--agg-lint", "-al", action="store_true",
						help="Aggregate the information about the eBugs detected with lint. "+
						"Example: `ebugs_filter.py \"(l:Wakelock, >=, 1)\" -al` will look for apps with "+
						"at least 1 \"Wakelock\" eBug, and from the matched apps it will check how many times "+
						"each existing eBug appears in each app. If we combine this with --output, it will only "+
						"display the information about the eBugs listed there.")

	args = parser.parse_args()
	validate_output(args.out)

	main(data_folder, args.queries, args.out, agg=args.agg_lint)
