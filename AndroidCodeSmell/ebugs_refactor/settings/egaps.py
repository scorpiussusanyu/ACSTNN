#!/usr/bin/python3

"""
EGAPs settings.
"""

"""
List of supported EGAPs.
"""
cs_EGAPs = ["DrawAllocation", "Wakelock", "Recycle", 
		 "ObsoleteLayoutParam", "ViewHolder", "HashMapUsage", 
		 "SensorLeak", "CameraLeak", "MediaLeak", 
		 "ExcessiveMethodCalls", "MemberIgnoringMethod"
		 ]


"""
Search keys of each EGAP, to be used by the filter operator.
"""
cs_EGAPs_keys = list(map(lambda i: ("l:"+i, int), cs_EGAPs))


"""
List of keys that can be used in the filter operator queries.
"""
cs_valid_keys = {"app id" : str, "folder" : str, "gradle" : bool, "return code" : int, "l:ALL" : int, "l:ANY" : int}
cs_valid_keys.update(cs_EGAPs_keys)
