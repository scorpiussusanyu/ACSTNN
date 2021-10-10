#!/usr/bin/python

import os, re, fileinput

from shutil import copyfile
from ebugs_refactor.tools.util import Stack

from ebugs_refactor.settings.egaps import cs_EGAPs, cs_EGAPs_keys
from ebugs_refactor.settings.android import cs_gradle_plugin_version, cs_wrapper_version

#
def _get_compileSdk_versions():
	check_folder = os.path.join(os.environ["ANDROID_HOME"], "platforms")
	sdk_list = next(os.walk(check_folder))[1]
	sdk_list_ints = list(map(lambda i: i.split("-")[1], sdk_list))
	return (sdk_list_ints + sdk_list)

#
def _get_buildtools_versions():
	check_folder = os.path.join(os.environ["ANDROID_HOME"], "build-tools")
	tools_list = next(os.walk(check_folder))[1]
	tools_list.sort()
	return tools_list

#
_tokens_map = {
				"packageName" : "applicationId", 
				"testPackageName" : "testApplicationId", 
				"runProguard" : "minifyEnabled", 
				"packageNameSuffix" : "applicationIdSuffix", 
				"android\.plugin\.bootClasspath" : "android.bootClasspath", 
				"android\.plugin\.ndkFolder" : "android.plugin.ndkDirectory", 
				"zipAlign " : "zipAlignEnabled ", 
				"jniDebugBuild" : "jniDebuggable", 
				"renderscriptDebug " : "renderscriptDebuggable ", 
				"flavorGroups" : "flavorDimensions", 
				"renderscriptSupportMode " : "renderscriptSupportModeEnabled ", 
				"ProductFlavor\.renderscriptNdkMode" : "renderscriptNdkModeEnabled", 
				"InstrumentTest" : "androidTest", 
				"instrumentTestCompile" : "androidTestCompile",
}

#
def fix_config_values(line):
	line_clear = re.sub(r"[ \t]", "", line)
	m = re.match(r"classpath[\'\"]com.android.tools.build:gradle(.+)[\'\"]", line_clear)
	if m:
		# SPECIAL CASE: edit the classpath value in the main build file
		return re.sub(r"[\'\"](.+)[\'\"]", r"'com.android.tools.build:gradle:"+cs_gradle_plugin_version+"'", line) + "\n"

	m = re.match(r"([ \t]*)(compileSdkVersion|targetSdkVersion)([ =])[\'\"]?(\d+)[\'\"]?", line)
	if m:
		old_version = m.group(4)
		supported_versions = _get_compileSdk_versions()
		if (old_version in supported_versions):
			return line
		else:
			return m.group(1) + m.group(2) + m.group(3) + min(supported_versions) + "\n"

	m = re.match(r"([ \t]*)(buildToolsVersion)([ =]+)[\'\"]?(.+)[\'\"]?", line)
	if m:
		old_version = m.group(4)
		supported_versions = _get_buildtools_versions()
		if old_version in supported_versions:
			return line
		else:
			best_version = supported_versions[0]
			for i in supported_versions:
				if i > old_version:
					best_version = i
					break
			return m.group(1) + m.group(2) + m.group(3) + "'" + best_version + "'\n"

	return line

#
def update_tokens(line):
	line_clear = re.sub(r"[ \t]", "", line)
	for t,n in _tokens_map.items():
		if re.match(r""+t+"(.+)$", line_clear):
			return re.sub(r""+t, r""+n, line)
	return line

#
def transform_configs(files):
	lowest_minSdkVersion = 0
	lib_files = []

	for file in files:
		try:
			# First, backup the files
			backup = file + ".bak"
			copyfile(file, backup)
	
			# Then, edit the lint options
			with open(file, 'r') as f:
				content = f.readlines()
				new_content = []
				repositories = []
	
				context = Stack()
				ident = "    "
				ident_level, brackets = 0, 0
				is_lib, changed_lint = False, False
				minSdkVersion, appcompat = None, False
				lint_checks = "check \"" + "\", \"".join(cs_EGAPs) + "\"\n"
				default_config_line = -1
				# not gonna use for now
				#dex_options = "preDexLibraries = false\njavaMaxHeapSize \"2g\"\n"
	
				i = 0
				for l in content:
					line = fix_config_values(update_tokens(l))
					line_clear = re.sub(r"[ \t]", "", line)
	
					if re.match(r"applyplugin:([\"\'])(com.android.library|android-library)([\"\'])", line_clear):
						is_lib = True
					elif is_lib and re.match(r"applicationId(.+)", line_clear):
						# Lib projects don't have `applicationId`. Remove it.
						continue
	
					if re.match(r"repositories{(.+)}$", line_clear):
						# [Special Case]
						# in the same line, the 'repositories' group is defined with one repository; 
						new_content.append((ident*ident_level) + "repositories{\n")
						ident_level += 1
						new_content.append((ident*ident_level) + "jcenter()\n")
						new_content.append((ident*ident_level) + "mavenCentral()\n")
						ident_level -= 1
						new_content.append((ident*ident_level) + "}\n")
						i += 4
						continue
					elif re.match(r"repositories{?", line_clear):
						repositories.append({"line" : i, "names" : []})
					elif re.match(r"jcenter\(\)", line_clear):
						repositories[-1]["names"].append("jcenter()")
					elif re.match(r"mavenCentral\(\)", line_clear):
						repositories[-1]["names"].append("mavenCentral()")
					elif re.match(r"compile([\"\'])com.android.support:appcompat-v7:(.+)([\"\'])", line_clear):
						appcompat = True
					elif re.match(r"defaultConfig{?$", line_clear):
						default_config_line = i
					
					match_minsdk = re.match(r"minSdkVersion(.+)", line_clear)
					if match_minsdk:
						minSdkVersion = {"line" : i, "version" : match_minsdk.group(1)}
						if is_lib:
							lib_files.append(file)
							try:
								minsdk = int(minSdkVersion["version"])
								lowest_minSdkVersion = max(lowest_minSdkVersion, minsdk)
							except ValueError as e:
								pass
	
					if re.match(r"android{?$", line_clear):
						# Inside android block
						context.push("android")
						ident_level += 1
	
					if ("{" in line_clear):
						ident_level += 1
						brackets += 1
					if ("}" in line_clear):
						ident_level -= 1
						brackets -= 1
	
					if (context.peek() == "android"):
						if (re.match(r"lintOptions{?$", line_clear)):
							context.push("lint")
	
						elif (re.match(r"lintOptions{(.+)}$", line_clear)):
							# lintOptions block in a single line. 
							# Ignore and add it in the end
							continue
	
						elif (re.match(r"lintOptions{(.+)$", line_clear)):
							# Inside lintOptions block, but it 
							# has stuff after the opening bracket
							new_content.append((ident*ident_level) + "lintOptions {\n")
							ident_level += 1
							new_content.append((ident*ident_level) + lint_checks)
							new_content.append((ident*ident_level) + "abortOnError false\n")
							ident_level -= 1
							changed_lint = True
							i += 3
	
					elif (context.peek() == "lint") and (not re.match(r"\{$", line_clear)):
						# Inside lintOptions block
						if not changed_lint:
							new_content.append((ident*ident_level) + lint_checks)
							new_content.append((ident*ident_level) + "abortOnError false\n")
							changed_lint = True
							i += 2
	
					if (re.match(r"(.*)}$", line_clear)) and (not context.isEmpty()):
						if context.peek() == "android" and brackets != 0:
							new_content.append(line)
							i += 1
							continue
						else:
							end_context = context.pop()
							if end_context == "lint":
								line = ((ident * ident_level)+ "}\n")
		
							elif (end_context == "android") and (not changed_lint) and (brackets == 0):
								# We never entered lintOptions block,
								# because there was no such block.
								# Let's add the lint options
								new_content.append((ident * ident_level) + "lintOptions {\n")
								new_content.append((ident * (ident_level + 1))+ lint_checks)
								new_content.append((ident * (ident_level + 1))+ "abortOnError false\n")
								new_content.append((ident * ident_level) + "}\n")
								changed_lint = True
								i += 4
	
					if (context.peek() != "lint") or (not changed_lint):
						new_content.append(line)
						i += 1
	
			# now let's see if the repositories are correct
			line_inc = 0
			for r in repositories:
				i = r["line"]
				n = r["names"]
				if "jcenter()" not in n:
					new_content.insert((line_inc+i+1), "    jcenter()\n")
					line_inc += 1
				if "mavenCentral()" not in n:
					new_content.insert((line_inc+i+1), "    mavenCentral()\n")
					line_inc += 1
	
			if appcompat:
				if minSdkVersion and minSdkVersion["version"] < "7":
					index = minSdkVersion["line"] + line_inc + 1
					line = new_content[index]
					new_content[index] = re.sub(r"(minSdkVersion)(.+)", r"\1 7", line)
				elif (not minSdkVersion) and (default_config_line > -1):
					index = default_config_line + line_inc + 1
					new_content.insert(index, "        minSdkVersion 7\n")
	
			with open(file, 'w') as f:
				for l in new_content:
					f.write("%s" % l)
		except FileNotFoundError as e:
			continue	# something strangely wrong happened. 
						# The file, previous detected as existing, now was not found.

	# final check: verify if the minSdkVersion variable is set to 
	# the higher or equal to the maximum value detected in the libs.

	min_sdk = lowest_minSdkVersion
	min_sdk_regex = "(" + "|".join(list(map(str, range(1, min_sdk)))) + ")[ \t]*$"
	for file in files:
		if file not in lib_files:
			try:
				with fileinput.FileInput(file, inplace=True, backup='.bck') as f:
					for line in f:
						print(re.sub(r"([ \t]*minSdkVersion)[ \t]+"+min_sdk_regex, r"\1 "+str(lowest_minSdkVersion), line), end='')
			except FileNotFoundError as e:
				continue

#
def transform_wrapper(files):
	for file in files:
		# First, backup the files
		backup = file + ".bak"
		copyfile(file, backup)
	
		with open(file, "r") as f:
			content = f.readlines()
			new_content = []
	
			for i, line in enumerate(content):
				if re.match(r"(.*)distributionUrl(.+)", line):
					line = re.sub(r"(.+)=(.+)", r"\1=http://services.gradle.org/distributions/gradle-"+cs_wrapper_version+"-all.zip", line)
				new_content.append(line)
		
		with open(file, 'w') as f:
			for l in new_content:
				f.write("{}".format(l))

#
def transform_properties(file):
	try:
		with fileinput.FileInput(file, inplace=True, backup='.bak') as f:
			for line in f:
				print(re.sub(r"(^sdk.dir.+$)", r"#\1", line), end='')
	except FileNotFoundError as e:
		return

#
def reset_configs(files):
	for file in files:
		backup = file + ".bak"
		try:
			copyfile(backup, file)
		except FileNotFoundError as e:
			return

#
def include_project(file, proj):
	if os.path.isfile(file):
		with fileinput.FileInput(file, inplace=True, backup='.bck') as f:
			for line in f:
				print(re.sub(r"(include .+)", r"\1, ':"+ proj +"'", line), end='')
	else:
		with open(file, "w") as f:
			f.write("include \':"+ proj +"\'")

#
def include_compile_project(file, proj, lib_version=None):
	is_app, has_depends, has_missing_lib = False, False, False
	insert_at = -1
	new_lines = []
	if os.path.isfile(file):
		with open(file, "r") as f:
			lines = f.readlines()
			for i, l in enumerate(lines):
				if re.match(r"^[ \t]*compile[ \t]+([\"\'])" + proj + r":(.+)([\"\'])", l):
					has_missing_lib = True

				if insert_at < 0:
					if re.match(r"^[ \t]*apply plugin.+", l):
						is_app = True
					if re.match(r"^[ \t]*dependencies.+", l) and is_app:
						has_depends = True
					if has_depends and re.match(r".+\{", l) and is_app:
						insert_at = i+1
				new_lines.append(l)

		if lib_version and has_missing_lib:
			return

		if is_app: 
			if lib_version:
				include_str = "    compile '" + proj + ":" + lib_version + "'\n"
			else:
				include_str = "    compile project(':"+ proj +"')\n"
			if has_depends and insert_at > 0:
				new_lines.insert(insert_at, include_str)
			else:
				new_lines.append("\n")
				new_lines.append("dependencies {\n")
				new_lines.append("    compile project(':"+ proj +"')\n")
				new_lines.append("}\n")
		with open(file, "w") as f:
			for l in new_lines:
				f.write("{}".format(l))

#
def lowest_sdk_version(files):
	all_versions = [18]
	for file in files:
		try:
			with open(file, "r") as f:
				lines = f.readlines()
				for line in lines:
					m = re.match(r"[ \t]*minSdkVersion[ \t]+([0-9]+)[\t ]*", line)
					if m:
						try:
							all_versions.append(int(m.group(1)))
						except ValueError as e:
							continue
		except FileNotFoundError as e:
			continue

	return min(all_versions)

#
def fix_min_sdk_version(file, version):
	v = str(version)
	if os.path.isfile(file):
		with fileinput.FileInput(file, inplace=True, backup='.bck') as f:
			for line in f:
				print(re.sub(r"([ \t]*minSdkVersion)[ \t]+.+", r"\1 "+v, line), end='')
	else:
		print("### Damm, it's not a file:", file)
