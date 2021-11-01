from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
#from particleClass import particle
from branchesList import *
import multiprocessing as  np
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class mergeTau(Module):
    def __init__(self, channel):
        self.channel = channel # Specify the channel
        self.allTauCollection = []
    
    #lets define the branches that need to be filled
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nallTau","I")
        self.out.branch("{}_pt".format("allTau"),"F",lenVar="n{}".format("allTau"))
        self.out.branch("{}_mass".format("allTau"),"F",lenVar="n{}".format("allTau"))
        self.out.branch("{}_phi".format("allTau"),"F",lenVar="n{}".format("allTau"))
        self.out.branch("{}_eta".format("allTau"),"F",lenVar="n{}".format("allTau"))
        #The boosted Tau branches listed in the dictionary are the ones that are common for both Taus and boosted Taus
        for branch in boostedTauBranches.values():
            self.out.branch("{}_{}".format("allTau",branch[0]),"{}".format(branch[1]),lenVar="n{}".format("allTau"))
    
    def fillBranches(self):
        self.out.fillBranch("nallTau",len(self.allTauCollection))
        self.out.fillBranch("{}_pt".format("allTau"),self.get_attributes("pt"))
        self.out.fillBranch("{}_mass".format("allTau"),self.get_attributes("mass"))
        self.out.fillBranch("{}_phi".format("allTau"),self.get_attributes("phi"))
        self.out.fillBranch("{}_eta".format("allTau"),self.get_attributes("eta"))
        for branch in boostedTauBranches.values():
            self.out.fillBranch("g{}_{}".format("allTau",branch[0]),self.get_attributes(branch[0]))

    def get_attributes(self,variable):
        return [obj[variable] for obj in self.allTauCollection]
            

    def analyze(self,event):
        tauCollection = Collection(event, "gTau","gnTau")
        boostedtauCollection = Collection(event, "gboostedTau","gnboostedTau")

        if self.channel == "tt":
            if (len(tauCollection)==2):
                self.allTauCollection = tauCollection
            if (len(boostedtauCollection)==2):
                self.allTauCollection = boostedtauCollection
            if (len(tauCollection)==1 or len(boostedtauCollection)==1):
                if tauCollection[0].pt > boostedtauCollection[0].pt:
                    self.allTauCollection = tauCollection
                    self.allTauCollection.extend(boostedtauCollection)

                else:
                    allTauCollection = boostedtauCollection
                    allTauCollection.extend(tauCollection)
            self.fillBranches(self.out)
            return True    
        
        if self.channel == "mt"  or self.channel == "et":
            if (len(tauCollection)==1):
                self.allTauCollection = tauCollection
            if (len(boostedtauCollection)==1):
                self.allTauCollection = boostedtauCollection
            self.fillBranches(self.out)
            return True
        

def call_postpoc(files):
		addBranches = lambda: mergeTau(args.Channel)
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
    outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel/VisibleMassAdded".format(args.Channel)
	#outputDir = "."
    outputbranches = "keep_and_drop.txt"
	#cuts = "&&".join(eventSelectionAND)
    post ="_MVis"
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


	
    
    
	
	
	













        
        

    
		


