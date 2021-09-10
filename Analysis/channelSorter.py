from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
from particleClass import particle
import argparse
import traceback

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Channel(Module):
	def __init__(self, channel):
		self.channel = channel # Specify the channel
		#Need to add conditons for other channels
		if self.channel == "tt":
    			self.Tau = particle("Tau")
    			self.FatJet = particle("FatJet")

	def beginJob(self):
        	pass
	
	def endJob(self):
		pass

	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.out = wrappedOutputTree
		self.Tau.beginFile(inputFile, outputFile, inputTree, self.out) #creating thre new branches
		self.FatJet.beginFile(inputFile, outputFile, inputTree, self.out)
    		
    		
	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass
    	
	#event loop
	def analyze(self, event): 
		#Basic filtering procedure with the pt and eta contions for the time being
		tau = Collection(event, "Tau") #creating Tau collection
		gtau = filter(lambda x: x.pt > 20 and (abs(x.eta) < 2.4), tau) #Filtering "good" taus in a event
		fatjet = Collection(event,"FatJet")
		gfatjet = filter(lambda x: x.pt > 200 and (abs(x.eta) < 2.4), fatjet)

		#Need to add more cchannels to this
		if self.channel == "tt":
			if (len(gtau)==2 and len(gfatjet)==1): # condition for hadronic channel
				self.Tau.fillBranchTau(self.out,gtau) #Fill the branches
				self.FatJet.fillBranchFatJet(self.out,gfatjet)
				return True # Store event
			else:
				return False # Reject event

			
	

letsSortChannels = lambda: Channel(args.Channel)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	parser.add_argument('--Channel',help="enter either tt or et or mut",required=True)
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	args = parser.parse_args()
	try:
		if args.Channel == "tt":
			fnames = glob.glob(args.inputLocation + "/*.root")
 			outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/TestOutput"
 			outputbranches = "keep_and_drop.txt"
 			cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2" # These wholesale cuts applied even before entering event loop
 			p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix="_ttChannel",noOut=False,outputbranchsel=outputbranches) # running the post processor - output files will have the _ttChannels appended to their name 
			p.run()
		
	except Exception as error:
		print("Error:(")
		traceback.print_exc()



