from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
from particleClass import particle
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Channel(particle):
	def __init__(self, channel):
		self.channel = channel # Here we determine what kind of a particle it is
		if self.channel == "tt":
    		self.Tau = particle("Tau")
    		self.FatJet = particle("FatJet")

	def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    	self.Tau.beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    	self.FatJet.beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


   	def analyze(self, event):
   		tau = Collection(event, "Tau")
   		gtau = filter(lambda x: x.pt > 20 and abs(x.eta < 2.3), tau)
		fatjet = Collection(event,"FatJet")
		gfatjet = filter(lambda x: x.pt > 200 and abs(x.eta < 2.4), fatjet)
		if (len(gtau)==2 and len(gfatjet)==1):
			self.Tau.fillingStuff(event,gtau)
			self.FatJet.fillingStuff(event,gfatjet)
			return True
		else:
			return False		

letsSortChannels = lambda: Channel(channelName)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	parser.add_argument('--Channel',help="enter either tt or et or mut",required=True)
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")

try:

 	if args.Channel == "tt":
 		fnames = glob.glob(args.inputLocation)
 		outputDir = "."
 		outputbranches = "keep_and_drop.txt"
 		cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2"
 		p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels(args.Channel)], postfix="_ttChannel",noOut=False,outputbranchsel=outputbranches)
		p.run()

except Exception as error:
	print("Error!")