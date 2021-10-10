#!/bin/bash

echo "[DrawAllocation]"; python ebugs_filter.py "(l:DrawAllocation, >, 0)" -o l:DrawAllocation; echo "- - - - - -"
echo "[ExcessiveMethodCalls]"; python ebugs_filter.py "(l:ExcessiveMethodCalls, >, 0)" -o l:ExcessiveMethodCalls; echo "- - - - - -"
echo "[HashMapUsage]"; python ebugs_filter.py "(l:HashMapUsage, >, 0)" -o l:HashMapUsage; echo "- - - - - -"
echo "[ObsoleteLayoutParam]"; python ebugs_filter.py "(l:ObsoleteLayoutParam, >, 0)" -o l:ObsoleteLayoutParam; echo "- - - - - -"
echo "[Recycle]"; python ebugs_filter.py "(l:Recycle, >, 0)" -o l:Recycle; echo "- - - - - -"
echo "[ViewHolder]"; python ebugs_filter.py "(l:ViewHolder, >, 0)" -o l:ViewHolder; echo "- - - - - -"
echo "[Wakelock]"; python ebugs_filter.py "(l:Wakelock, >, 0)" -o l:Wakelock; echo "- - - - - -"
echo "[InternalGetter]"; python ebugs_filter.py "(l:InternalGetter, >, 0)" -o l:InternalGetter; echo "- - - - - -"
echo "[CameraLeak]"; python ebugs_filter.py "(l:CameraLeak, >, 0)" -o l:CameraLeak; echo "- - - - - -"
echo "[SensorLeak]"; python ebugs_filter.py "(l:SensorLeak, >, 0)" -o l:SensorLeak; echo "- - - - - -"
echo "[MediaLeak]"; python ebugs_filter.py "(l:MediaLeak, >, 0)" -o l:MediaLeak; echo "- - - - - -"


