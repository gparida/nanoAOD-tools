from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?


class particle(Module):
	def __init__(self, particleType):
		self.particleType = particleType # Here we determine what kind of a particle it is


	def beginJob(self):
        	pass

    	def endJob(self):
        	pass


    	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.out = wrappedOutputTree
		print ("The output tree while branch creation ",self.out)
    		if self.particleType == "Tau":
    			self.out.branch("ngTau","I")
    			self.out.branch("gTau_mass","F")
    			self.out.branch("gTau_pt","F")
    			self.out.branch("gTau_phi","F")

    		if self.particleType == "FatJet":
    			self.out.branch("ngFatJet","I")
			self.out.branch("gFatJet_mass","F")
			self.out.branch("gFatJet_pt","F")
			self.out.branch("gFatJet_phi","F")


	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        	pass

    	def fillingStuff(self,event,particleObject):
    		if self.particleType == "Tau":
    			self.out.fillBranch("ngTau",len(particleObject))
			print ("ngTau",len(particleObject))
			print ("the output tree while branch filling", self.out)
    			for i in range(len(particleObject)):
				print ("gTau_pt",particleObject[i].pt)
    				self.out.fillBranch("gTau_mass",particleObject[i].mass)
    				self.out.fillBranch("gTau_pt",particleObject[i].pt)
    				self.out.fillBranch("gTau_phi",particleObject[i].phi)

    		if self.particleType == "FatJet":
    			self.out.fillBranch("ngFatJet",len(particleObject))
    			for i in range(len(particleObject)):
    				self.out.fillBranch("gFatJet_mass",particleObject[i].mass)
    				self.out.fillBranch("gFatJet_pt",particleObject[i].pt)
    				self.out.fillBranch("gFatJet_phi",particleObject[i].phi)








