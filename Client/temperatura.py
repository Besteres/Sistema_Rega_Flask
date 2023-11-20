import os

class Temperatura:
    def __init__(self,path):
        self.timescalledtoday = 0
        self.loadFile(path)
        
    def loadFile(self,path):
        if(os.path.exists(path)):
            with open(path,"r") as numfile:
                value = numfile.read().strip()

            if value.isdigit():
                self.timescalledtoday = int(value)
                return
        else:
            self.createFile(path)

            
    def createFile(self,path):
        with open(path,"w") as numfile:
            numfile.write(0)