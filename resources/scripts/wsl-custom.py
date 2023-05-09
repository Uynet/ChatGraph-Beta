
def onInput(self):
    import os
    import subprocess
    cmds = "wsl " + self.input
    # current dir
    origCd = os.getcwd()
    # parce cd
    cwd = self.get("cwd")
    if cwd is None: cwd="." 

    os.chdir(cwd)

    # move to relative path
    if self.input.startswith("cd "):
        target_dir = self.input[3:].strip()
        print("cd to ",target_dir)
        newDir = os.chdir(target_dir)
        self.set("cwd",newDir)

    commandList = cmds.split()
    result = subprocess.run(commandList, capture_output=True, cwd=cwd,text=True,shell=True)

    newDir = os.getcwd()
    self.set("label","wsl: "+newDir.split("/")[-1])
    self.set("cwd",newDir)
    os.chdir(origCd)

    print("[you >"+self.input)
    if result.returncode != 0: print("[wsl >"+result.stderr)
    else: print("[wsl >"+result.stdout)

onInput(node)