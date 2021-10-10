#!/usr/bin/python3

import os, re
import xml.etree.ElementTree as ET

from lazyme.string import color_print

from ebugs_refactor.tools.util import *
from ebugs_refactor.tools.gradle_util import *

from ebugs_refactor.settings.egaps import cs_EGAPs;
from ebugs_refactor.settings.misc import cs_clean_repo_first, cs_ignored_folders;
from ebugs_refactor.settings.storage import cs_lint_result_file, cs_assets_folder;

# If set to "False", the results will be stored in separate files, 
# one per project, as the analysis goes.
# It set to "True", all the results will be stored in the same file.
_save_all = False

def parse_lint_bugs(files):
	ebugs_dict = {}
	
	for file in files:
		tree = ET.parse(file)
		root = tree.getroot()
	
		for child in root:
			att = child.attrib
			if "id" in att.keys():
				val = att['id']
				if val in cs_EGAPs:
					if val in ebugs_dict:
						ebugs_dict[val] += 1
					else:
						ebugs_dict[val] = 1
	return ebugs_dict

def lint(id, gradle_script, folder):
	ebugs = {}
	run_command(" ".join(["chmod", "755", gradle_script]))
	command = " ".join([gradle_script, "-p", folder, 'clean', 'build', 'lint'])
	returncode, std_out, std_err = run_command(command)

	if returncode != 0:
		# an error happened!
		print("[ERROR] : " + id)
	else:
		# no errors
		lint_xml = []
		for line in std_out.split("\n"):
			m = re.match("Wrote XML report to", line)
			if m:
				file = re.split(r"to file:(\/\/)?|to ", line)[-1]
				lint_xml.append(file.replace("%20", " "))
		ebugs = parse_lint_bugs(lint_xml)

		if len(std_err):
			print("[WARNING] : " + id)
			# return code is 0 (no error), but we have
			# something on std_err. Maybe we want to 
			# log it or something
	#
	return ebugs, returncode, std_err

def save_projects(projects, out_folder):
	result_dict = {}
	result_dict['projects'] = projects
	result_file = os.path.join(out_folder, cs_lint_result_file.format("ALL"))
	
	save_json(result_dict, result_file)


def save_project_json(project, out_folder):
	result_file = os.path.join(out_folder, cs_lint_result_file.format(project["app id"]))

	save_json(project, result_file)

def mine_app(tag, folder, assets_folder, output_folder="output_detector"):
	data = {}
	data['app id'] = tag
	data['folder'] = folder
	data['gradle files'] = []
	data['wrapper-properties'] = []
	found_gradlew = False
	gradlew_file = ""
	gradlew_folder = ""

	# lets reset the repo first
	if cs_clean_repo_first:
		git_clean(folder)

	for root, dirs, files in os.walk(folder):
		if any(ig in root for ig in cs_ignored_folders):
			continue
		for f in files:
			if f == "build.gradle":
				filename = os.path.join(root, f)
				data['gradle files'].append(filename)
			elif (not found_gradlew) and (f == "gradlew"):
				filename = os.path.join(root, f)
				gradlew_file = os.path.join(root, f)
				gradlew_folder = root
				found_gradlew = True
			elif f == "gradle-wrapper.properties":
				data['wrapper-properties'].append(os.path.join(root, f))
			elif f == "local.properties":
				data['local-properties'] = os.path.join(root, f)

	if os.path.isfile(gradlew_file):
		data['gradle'] = True
		data['gradle script'] = gradlew_file
		# Edit gradle build files
		transform_configs(data['gradle files'])
		if 'wrapper-properties' in data.keys():
			transform_wrapper(data['wrapper-properties'])
		else:
			# if the gradle wrapper folder does not exist, let's use 
			# the default one contained in this folder
			cpt = copytree(os.path.join(assets_folder, "./gradle"), os.path.join(gradlew_folder, "gradle"))

		if 'local-properties' in data.keys():
			transform_properties(data['local-properties'])
		try:
			ebugs_dict, returncode, errors = lint(tag, gradlew_file, gradlew_folder)
			data['return code'] = returncode
			data['errors'] = errors
			data['lint'] = {}
			if returncode == 0:
				data['lint'] = ebugs_dict
		except Exception as e:
			raise e
		finally:
			# Reset gradle build files to previous (backup) version
			to_reset = data['gradle files']
			if 'wrapper-properties' in data.keys():
				to_reset += data['wrapper-properties']
			if 'local-properties' in data.keys():
				to_reset.append(data['local-properties'])
			reset_configs(to_reset)
			
	else:
		data['gradle'] = False
		data['gradle script'] = ""

	save_project_json(data, output_folder)

	return data

def mine_apps(main_folder, assets_folder, output_folder="output_detector"):
	root, dirs, files = next(os.walk(main_folder))
	projects = [(d, os.path.join(root, d)) for d in dirs]

	projects_data = []
	make_dir(output_folder)

	for tag, folder in projects:
		data = mine_app(tag, folder, assets_folder, output_folder)
		projects_data.append(data)
	
	if _save_all:
		save_projects(projects_data, output_folder)

	return 0
	