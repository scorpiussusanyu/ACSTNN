#!/usr/bin/python3

import os

from shutil import copytree, rmtree

from ebugs_refactor.tools.util import run_command, save_text, count_occurences, files_by_type, files_by_name, log_text, add_permissions
from ebugs_refactor.tools.issues_fix import fix_folder_names, undo_fix_folder_names, get_fixed_file_paths
from ebugs_refactor.tools.gradle_util import include_project, include_compile_project, fix_min_sdk_version, lowest_sdk_version

from ebugs_refactor.settings.refactor import *
from ebugs_refactor.settings.android import cs_android_sdk_path
from ebugs_refactor.settings.misc import cs_logging
from ebugs_refactor.settings.storage import cs_assets_folder


TRACE_FLAG = 2000
NO_TRACE_FLAG = 1000

# problems with this method: is still not generalized to transform XML.
#   at the time, we assume that if a XML transformation is required, is the 'ObsoleteLayoutParam' only.
def refactor_app(data, refactorings, tracing=False):
	contains_XML = False
	if "ObsoleteLayoutParam" in refactorings:
		# this is a special case: a XML refactoring
		ref = list(filter(lambda x : x != "ObsoleteLayoutParam", refactorings))
		contains_XML = True
	else:
		ref = refactorings
	ref = list(map(lambda x : "--refactorings "+ x +"Refactoring", ref))

	refactor_trace = []
	proj_folder = os.path.dirname(data["gradle script"])
	root_folder = os.path.dirname(proj_folder)

	# Preliminary step - build the app, so the code generated can also be analyzed
	run_command("chmod 755 " + data["gradle script"])
	build_command = " ".join([data["gradle script"], "-p", proj_folder, 'clean', 'build'])
	returncode, std_out, std_err = run_command(build_command)
	for apk in list(filter(lambda x : "-unaligned" not in x, files_by_type(proj_folder, ".apk"))):
		os.remove(apk)
	# TODO: maybe do some checks with the return code and outputs?

	# First, put .project and .classpath in the correct place
	compile_version = "25"  # for now, let's use the same Android API version as reference (7.1)
	content = cs_eclipse_classpath.format(os.path.basename(proj_folder), cs_android_sdk_path, compile_version)
	save_text(content, os.path.join(root_folder, ".classpath"))
	save_text(cs_eclipse_project, os.path.join(root_folder, ".project"))

	# $? - Intermediate step: fix potencial known issues
	#     issue #1: folder names must not contain dots (.), or AutoRefactor will not work with them
	proj_folder, folders_fixed = fix_folder_names(proj_folder)
	fixed_gradle_files = get_fixed_file_paths(root_folder, data["gradle files"])  ##  because of issue #1 Intermidiate Step)
	
	# include support-v4 lib if not existing (com.android.support:support-v4:19.+)
	for f in fixed_gradle_files:
		include_compile_project(f, "com.android.support:support-v4", lib_version="19.+")

	# Second, run AutoRefactor
	cmd = "./" + cs_autorefactor_cli + " apply --project " + os.path.join(root_folder, ".project") + " " + " ".join(ref)
	if tracing:
		#run_command("export COEVOLOGY_OP=" + str(TRACE_FLAG))
		os.environ["COEVOLOGY_OP"] = str(TRACE_FLAG)
	else:
		#run_command("export COEVOLOGY_OP=" + str(NO_TRACE_FLAG))
		os.environ["COEVOLOGY_OP"] = str(NO_TRACE_FLAG)

	ret_code, s_out, s_err = 0, "", ""
	if len(ref) > 0:
		ret_code, s_out, s_err = run_command(cmd, dir=cs_autorefactor_folder)

	if tracing:
		cmd = "./" + cs_autorefactor_cli + " apply --project " + os.path.join(root_folder, ".project") + " --refactorings TraceMethodsRefactoring"
		ret, o, e = run_command(cmd, dir=cs_autorefactor_folder)
		ret_code += ret
		s_out += o
		s_err += e

		# if this is a tracing project, we must add write/read permissions to the manifests
		all_manifests = files_by_name(proj_folder, "AndroidManifest.xml")
		permissions = ["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.READ_EXTERNAL_STORAGE"]
		for m in all_manifests:
			add_permissions(permissions, m)

		# Add the 'Trace EBugs' project to the project (and update all necessary files)
		copytree(os.path.join(cs_assets_folder, "_co-evolgy"), (os.path.join(proj_folder, "_co-evolgy")))
		gradle_settings = os.path.join(proj_folder, "settings.gradle")
		include_project(gradle_settings, "_co-evolgy")
		for f in fixed_gradle_files:
			include_compile_project(f, "_co-evolgy")
		fix_min_sdk_version(os.path.join(proj_folder, "_co-evolgy", "build.gradle"), lowest_sdk_version(fixed_gradle_files))
		
	if contains_XML:
		all_layouts = list(filter(lambda f : "layout/" in f, files_by_type(proj_folder, ".xml")))
		refactor_count = 0
		for l in all_layouts:
			ret, o, e = run_command("android-view-refactor --refactor " + l)
			ret_code += ret
			s_out += o
			s_err += e
			refactor_count += e.count("Warning:")
		if refactor_count > 0:
			refactor_trace.append({"name" : "ObsoleteLayoutParam", "count" : refactor_count})

	# Finally, go through the list of performed transformations
	refact_trace_file = os.path.join(cs_autorefactor_folder, "refactorings.trace")
	try:
		with open(refact_trace_file, "r") as fp:
			lines = list(map(lambda l : l.replace("\n", ""), fp.readlines()))
			refactor_trace += count_occurences(lines, refactorings)
		os.remove(refact_trace_file)
	except FileNotFoundError as e:
		pass

	# undo all previous fixes, so it does not mess with the following steps.
	undo_fix_folder_names(folders_fixed)

	# Extra: log the events for future debug
	log_content = "< " + data["app id"] + " >\n" + s_out + "\n" + s_err + "\n«««««««« »»»»»»»»\n\n"
	log_text(log_content, os.path.join("log", "refactor.log"), log=cs_logging)
	
	# REMOVE LATER: test if the app can be built; return != 0 if it doesn't
	"""
	assemble_command = " ".join([data["gradle script"], "-p", proj_folder, 'assembleDebug'])
	ret, o, e  = run_command(assemble_command)
	ret_code += ret
	s_out += o
	s_err += e
	"""

	if ret_code != 0:
		return ret_code, s_err
	
	return ret_code, refactor_trace