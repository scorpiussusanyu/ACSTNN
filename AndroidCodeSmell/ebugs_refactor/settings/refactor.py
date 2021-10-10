#!/usr/bin/python3

"""
Refactor tool settings.
"""

cs_autorefactor_folder = "/home/marco/repos/_forked_/AutoRefactorCli/"
cs_autorefactor_cli = "cli/target/autorefactor/bin/autorefactor"


"""
String value that goes into the .classpath file, 
needed by AutoRefactor.
"""
cs_eclipse_classpath = """<?xml version="1.0" encoding="UTF-8"?>
<classpath>
	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8"/>
	<classpathentry kind="src" path="{}"/>
	<classpathentry kind="lib" path="{}/platforms/android-{}/android.jar"/>
	<classpathentry kind="output" path="bin"/>
</classpath>
"""

"""
String value that goes into the .project file, 
needed by AutoRefactor.
"""
cs_eclipse_project = """<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
	<name>ProjUT</name>
	<comment></comment>
	<projects>
	</projects>
	<buildSpec>
		<buildCommand>
			<name>org.eclipse.jdt.core.javabuilder</name>
			<arguments>
			</arguments>
		</buildCommand>
	</buildSpec>
	<natures>
		<nature>org.eclipse.jdt.core.javanature</nature>
	</natures>
</projectDescription>
"""
