from branchesList import *
from particleClass import particle


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class BoostedTau(particle):
    def __init__(self, particleType):
        super(BoostedTau,self).__init__(particleType)
    
    def setUpBranches(self, wrappedOutputTree):
        super(BoostedTau,self).setUpBranches(wrappedOutputTree)
        for branch in boostedTauBranches.values():
            wrappedOutputTree.branch("g{}_{}".format(self.particleType,branch[0]),"{}".format(branch[1]),lenVar="gn{}".format(self.particleType))
    
    def fillBranches(self,wrappedOutputTree):
        super(BoostedTau,self).fillBranches(wrappedOutputTree)
        for branch in boostedTauBranches.values():
            wrappedOutputTree.fillBranch("g{}_{}".format(self.particleType,branch[0]),self.get_attributes(branch[0]))


    
    
        

    
    
    
    
    
