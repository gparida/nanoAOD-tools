from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?


class particle(Module):
	def __init__(self, particleType):
		self.particleType = particleType # What type of particle it is Tau, Jet etc


	def beginJob(self):
		pass
    	


	def endJob(self):
		pass
	
	#Create the new branches to be added for the selected objects
	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		#self.out = wrappedOutputTree
		if self.particleType == "Tau": 
			wrappedOutputTree.branch("ngTau","I")
			wrappedOutputTree.branch("gTau_mass","F",lenVar="ngTau")
			wrappedOutputTree.branch("gTau_pt","F",lenVar="ngTau")
			wrappedOutputTree.branch("gTau_phi","F",lenVar="ngTau")
			wrappedOutputTree.branch("gTau_eta","F",lenVar="ngTau")
		
		if self.particleType == "FatJet":
			wrappedOutputTree.branch("ngFatJet","I")
			wrappedOutputTree.branch("gFatJet_mass","F",lenVar="ngFatJet")
			wrappedOutputTree.branch("gFatJet_pt","F",lenVar="ngFatJet")
			wrappedOutputTree.branch("gFatJet_phi","F",lenVar="ngFatJet")
			wrappedOutputTree.branch("gFatJet_eta","F",lenVar="ngFatJet")
		#return self.out

	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass


	###########################Branch Filling methods of different good Objects- Need to add more a#########################################################
	#Fill the new "good" Tau branches
	def fillBranchTau(self,wrappedOutputTree,particleObject):
		particleArray=self.makeParticleArray(particleObject)
		wrappedOutputTree.fillBranch("ngTau",len(particleObject))
		wrappedOutputTree.fillBranch("gTau_mass",particleArray["mass"])
		wrappedOutputTree.fillBranch("gTau_pt",particleArray["pt"])
		wrappedOutputTree.fillBranch("gTau_phi",particleArray["phi"])

	#Fill the new "good" FatJet branches
	def fillBranchFatJet(self,wrappedOutputTree,particleObject):
		particleArray=self.makeParticleArray(particleObject)
		wrappedOutputTree.fillBranch("ngFatJet",len(particleObject))
		wrappedOutputTree.fillBranch("gFatJet_mass",particleArray["mass"]) 
		wrappedOutputTree.fillBranch("gFatJet_pt",particleArray["pt"])
		wrappedOutputTree.fillBranch("gFatJet_phi",particleArray["phi"])

	########################################################################################################################################################


	#Making arrays for different variables for a object so that they can be filled in their respective branches. 
	def makeParticleArray(self,particleObject):
		particleAttributes={}
		#Adding attribiutes that will be be common to almost all objetcs but if there are special ones (like softdrop mass etc) could use the self.particle and if statements for them
		particleAttributes["mass"] = [particleObject[k].mass for k in range(len(particleObject))] # interating through the "good" objects collection in an event and storing their masses in a iterable
		particleAttributes["eta"] = [particleObject[k].eta for k in range(len(particleObject))]
		particleAttributes["phi"] = [particleObject[k].phi for k in range(len(particleObject))]
		particleAttributes["pt"] = [particleObject[k].pt for k in range(len(particleObject))]
		return particleAttributes

    






