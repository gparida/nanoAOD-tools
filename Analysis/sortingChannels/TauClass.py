from branchesList import *
from particleClass import particle
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Tau(particle):
    def __init__(self, particleType):
        super(Tau,self).__init__(particleType)
    
    def setUpBranches(self, wrappedOutputTree):
        super(Tau,self).setUpBranches(wrappedOutputTree)
        for branch in TauBranches.values():
            wrappedOutputTree.branch("g{}_{}".format(self.particleType,branch[0]),"{}".format(branch[1]),lenVar="gn{}".format(self.particleType))
    
    def fillBranches(self,wrappedOutputTree):
        super(Tau,self).fillBranches(wrappedOutputTree)
        for branch in TauBranches.values():
            wrappedOutputTree.fillBranch("g{}_{}".format(self.particleType,branch[0]),self.get_attributes(branch[0]))


    
    
    
            

    
    
    
    
    
