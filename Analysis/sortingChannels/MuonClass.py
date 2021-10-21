from branchesList import *
from particleClass import particle

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Muon(particle):
    def __init__(self, particleType):
        super(Muon,self).__init__(particleType)
    
    def setUpBranches(self, wrappedOutputTree):
        super(Muon,self).setUpBranches(wrappedOutputTree)
        for branch in MuonBranches.values():
            wrappedOutputTree.branch("g{}_{}".format(self.particleType,branch[0]),"{}".format(branch[1]),lenVar="gn{}".format(self.particleType))
    
    def fillBranches(self,wrappedOutputTree):
        super(Muon,self).fillBranches(wrappedOutputTree)
        for branch in MuonBranches.values():
            wrappedOutputTree.fillBranch("g{}_{}".format(self.particleType,branch[0]),self.get_attributes(branch[0]))

    def apply_cut(self,l_func):
        if self.collection is None:
	        return

        #self.collection = filter(self.passingMVAID,self.collection)
        self.collection = filter(l_func,self.collection)

    
    def passingMVAID(self,muonCollectionObject):
        print ("Testing Muon MVA ID= ",type(muonCollectionObject.mvaId),muonCollectionObject.mvaId)
        theMuonIDBits = ''.join(format(ord(i), '016b')for i in muonCollectionObject.mvaId)
        theMuonID = int(theMuonIDBits, 2)    
        if theMuonID >= 1:
            return True
        else:
            return False

            
                
            
                

        

    
    
    
    
    
