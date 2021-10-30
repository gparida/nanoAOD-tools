from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
import argparse
import multiprocessing as  np


ROOT.PyConfig.IgnoreCommandLineOptions = True

class VisibleMass(Module):
    def __init__(self, channel):
       self.channel = channel # Specify the channel


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MVis", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self,event):
       gTau = Collection(event, "gTau","gnTau")
       gboostedTau = Collection(event,"gboostedTau","gnboostedTau")
       gElectron = Collection(event,"gElectron","gnElectron")
       gMuon = Collection(event,"gMuon","gnMuon")

       lepton1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
       lepton2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)

       if self.channel == "tt":
            if (len(gTau)==2):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gTau[1].pt,gTau[1].eta,gTau[1].phi,gTau[1].mass)
            if (len(gboostedTau)==2):
                lepton1.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
                lepton2.SetPtEtaPhiM(gboostedTau[1].pt,gboostedTau[1].eta,gboostedTau[1].phi,gboostedTau[1].mass)
            if (len(gTau)==1 and len(gboostedTau)==1):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
            self.out.fillBranch("MVis",abs((lepton1 + lepton2).M()))
    
       if self.channel == "et":
            if (len(gTau)!=0):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gElectron[0].pt,gElectron[0].eta,gElectron[0].phi,gElectron[0].mass)
            
            if (len(gboostedTau)!=0):
                 lepton1.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
                 lepton2.SetPtEtaPhiM(gElectron[0].pt,gElectron[0].eta,gElectron[0].phi,gElectron[0].mass)
            self.out.fillBranch("MVis",abs((lepton1 + lepton2).M()))

       if self.channel == "mt":
            if (len(gTau)!=0):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gMuon[0].pt,gMuon[0].eta,gMuon[0].phi,gMuon[0].mass)
            if (len(gboostedTau)!=0):
                lepton1.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
                lepton2.SetPtEtaPhiM(gMuon[0].pt,gMuon[0].eta,gMuon[0].phi,gMuon[0].mass)
            self.out.fillBranch("MVis",abs((lepton1 + lepton2).M())) 
       
       return True     

def call_postpoc(files):
		addBranches = lambda: VisibleMass(args.Channel)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=None,branchsel=None,modules=[addBranches()], postfix=post,noOut=False,outputbranchsel=outputbranches)
		p.run()
          
              
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True)
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	args = parser.parse_args()


	#Define Eevnt Selection - all those to be connected by or

	#fnames = ["/data/aloeliger/bbtautauAnalysis/2016/Data.root"]
	fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
	outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel".format(args.Channel)
	#outputDir = "."
	outputbranches = "keep_and_drop.txt"
	#cuts = "&&".join(eventSelectionAND)
	post ="MVis"
	argList = list()
	filename =""
	for file in fnames:
		argList.append(file)
		#nameStrip = file.strip()
    	#filename = (nameStrip.split('/')[-1]).split('.')[-2]
	
	#print (argList)

	if int(args.ncores) == 1:
		for arr in argList:
			#print ("This is what is passed ",arr[1])
			call_postpoc(arr)
	
	else:
		pool = np.Pool(int(args.ncores))
		#with np.Pool(object,ncores) as pool:
		res=pool.map(call_postpoc, argList)           
          
               
          
        
