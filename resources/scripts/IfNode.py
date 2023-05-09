def onInput(self ):

    flag = int(self.input) < 50
    if type(flag) == bool:
        self.set("flag",self.input )
        print(self.input)
    else :
        self.set("flag","Other")
        print(self.input)
        raise Exception("Error:input is not bool")
onInput(node)