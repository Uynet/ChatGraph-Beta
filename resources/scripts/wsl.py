import os
import subprocess
import sys

cmds = "wsl " + node.input

origCd = os.getcwd()
# parce cd
cwd = node.getProperty("cwd")
if cwd is None: cwd="." 

if node.input.startswith("cd "):
    target_dir = node.input[3:].strip()
    print("cd to ",target_dir)
    os.chdir(target_dir)
    node.set("cwd",newDir)


result = subprocess.run(cmds.split(), capture_output=True, cwd=cwd,text=True,shell=True)



newDir = os.getcwd()
node.set("label","wsl: "+newDir.split("/")[-1])

os.chdir(origCd)

if result.returncode != 0:
	print(result.stderr)
else :
	print(result.stdout)