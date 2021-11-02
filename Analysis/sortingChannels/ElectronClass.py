from branchesList import *
from particleClass import particle

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Electron(particle):
    def __init__(self, particleType):
        super(Electron,self).__init__(particleType)
    
    def setUpBranches(self, wrappedOutputTree):
        super(Electron,self).setUpBranches(wrappedOutputTree)
        for branch in ElectronBranches.values():
            wrappedOutputTree.branch("g{}_{}".format(self.particleType,branch[0]),"{}".format(branch[1]),lenVar="gn{}".format(self.particleType))
    
    def fillBranches(self,wrappedOutputTree):
        super(Electron,self).fillBranches(wrappedOutputTree)
        for branch in ElectronBranches.values():
            wrappedOutputTree.fillBranch("g{}_{}".format(self.particleType,branch[0]),self.get_attributes(branch[0]))

    def relativeIso(self,electronCollectionObject):
        if abs(electronCollectionObject.eta) <= 1.479:
            if (electronCollectionObject.pfRelIso03_all < 0.175):
                return True
            else:
                return False
        elif ((abs(electronCollectionObject.eta) > 1.479) and (abs(electronCollectionObject.eta) <= 2.5)):
            if (electronCollectionObject.pfRelIso03_all < 0.159):
                return True
            else:
                return False
        else:
            return False






    
    
        

    
    
    
    
    
