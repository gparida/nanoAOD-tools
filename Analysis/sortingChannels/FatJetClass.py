from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from particleClass import particle
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class FatJet(particle, object):
    def __init__(self, particleType):
        super(FatJet,self).__init__(particleType)
    
    def setUpBranches(self, wrappedOutputTree):
        super(FatJet,self).setUpBranches(wrappedOutputTree)
        wrappedOutputTree.branch("g{}_msoftdrop".format(self.particleType),"F",lenVar="ng{}".format(self.particleType))
    
    def fillBranches(self,wrappedOutputTree):
        super(FatJet,self).fillBranches(wrappedOutputTree)
        wrappedOutputTree.fillBranch("g{}_msoftdrop".format(self.particleType),self.get_attributes("msoftdrop"))

    


        
