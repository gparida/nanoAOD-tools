#a quick class used for lloading other modules in the package in a convenient way

class RecursiveLoader():
    def __init__(self):
        pass
    def LoadPath(self,PathToLoad):
        Module = __import__(PathToLoad)
        ToLoad = PathToLoad.split('.')
        if len(ToLoad) == 1:
            return Module
        else:            
            for i in range(1,len(ToLoad)):
                try:
                    Module = getattr(Module,ToLoad[i])
                except AttributeError:
                    continue                
            return Module
    def LoadFromDirectoryPath(self,PathToLoad):
        #trim the .py file extension off
        PathToLoad=PathToLoad[:len(PathToLoad)-3]
        PathToLoad=PathToLoad.replace("/",".")        
        return self.LoadPath(PathToLoad)