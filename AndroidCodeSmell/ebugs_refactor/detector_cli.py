#!/usr/bin/python3

import ebugs_refactor.operators.e_detector as dtc

from ebugs_refactor.tools.util import run_command, print_e

from ebugs_refactor.settings.remote import cs_remote, cs_remote_apps_folder, cs_remote_copy_timeout
from ebugs_refactor.settings.storage import cs_local_apps_folder, cs_assets_folder

def list_remote_apps():
	app_list = []
	
	list_cmd = "ssh " + cs_remote + " ls -l "+ cs_remote_apps_folder +" | grep -v total"
	ret_code, s_out, s_err = run_command(list_cmd, timeout=cs_remote_copy_timeout)
	if ret_code != 0:
		print_e("An error occured while listing the apps in server '" + cs_remote + "'")
		print("- - - - - - - - - -")
		print(s_err)
	else:
		lines = s_out.split("\n")
		for l in lines:
			app_tag = l.split(" ")[-1]
			if app_tag != "":
				app_list.append(app_tag)

	return app_list

def get_app(app_id):
	scp_cmd = "scp -r " + cs_remote + ":"
	cmd = scp_cmd + os.path.join(cs_remote_apps_folder, app_id) + " " + app_id
	ret_code, s_out, s_err = run_command(cmd, dir=cs_local_apps_folder, timeout=cs_remote_copy_timeout)

	if ret_code != 0:
		print_e("An error occured at copying app '" + app_id + "' from server '" + cs_remote + "'")
		print("- - - - - - - - - -")
		print(s_err)
	
	return ret_code

if __name__ == '__main__':
	if not cs_remote:
		# Detector will only run if the apps 
		# are stored in the same machine.
		dtc.mine_apps(cs_remote_apps_folder, cs_assets_folder, output_folder="gh_detector")
	else:
		app_list = list_remote_apps()
		for app in apps:
			scp_status = get_app(app)
			if scp_status == 0:
				dtc.mine_app(app, os.path.join(cs_local_apps_folder, app), cs_assets_folder)
