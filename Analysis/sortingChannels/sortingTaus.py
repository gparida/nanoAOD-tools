from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from visibleMass import VisibleMass
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
    
    def fillBranches(self,colllist):
        if self.channel == "tt":
            length = 2
        else:
            length =1
        self.out.fillBranch("nallTau",length)
        self.out.fillBranch("{}_pt".format("allTau"),self.get_attributes("pt",colllist))
        self.out.fillBranch("{}_mass".format("allTau"),self.get_attributes("mass",colllist))
        self.out.fillBranch("{}_phi".format("allTau"),self.get_attributes("phi",colllist))
        self.out.fillBranch("{}_eta".format("allTau"),self.get_attributes("eta",colllist))
        for branch in boostedTauBranches.values():
            self.out.fillBranch("{}_{}".format("allTau",branch[0]),self.get_attributes(branch[0],colllist))

    def get_attributes(self,variable,collList):
        list = []
        for coll in collList:
            for obj in coll:
                list.append(obj[variable])
        if variable == "pt":
            print (list)
        return list

        #return [obj[variable] for obj in self.allTauCollection]
            

    def analyze(self,event):
        tauCollection = Collection(event, "gTau","gnTau")
        boostedtauCollection = Collection(event, "gboostedTau","gnboostedTau")
        colllist =[]
        print ("Type of the collection", type(tauCollection))

        if self.channel == "tt":
            if (len(tauCollection)==2):
                #self.allTauCollection = tauCollection
                colllist.append(tauCollection)
            if (len(boostedtauCollection)==2):
                #self.allTauCollection = boostedtauCollection
                colllist.append(boostedtauCollection)
            if (len(tauCollection)==1 or len(boostedtauCollection)==1):
                if tauCollection[0].pt >= boostedtauCollection[0].pt:
                    colllist.append(tauCollection)
                    colllist.append(boostedtauCollection)
                    #self.allTauCollection = tauCollection
                    #self.allTauCollection.extend(boostedtauCollection)

                else:
                    colllist.append(boostedtauCollection)
                    colllist.append(tauCollection)
                    #allTauCollection = boostedtauCollection
                    #allTauCollection.extend(tauCollection)
            #print ("Type of the new collection", type(allTauCollection))
            self.fillBranches(colllist)
            return True    
        
        if (self.channel == "mt"  or self.channel == "et"):
            if (len(tauCollection)==1):
                colllist= tauCollection
            if (len(boostedtauCollection)==1):
                colllist = boostedtauCollection
            self.fillBranches(colllist)
            return True
        

def call_postpoc(files):
        visibleM = lambda:VisibleMass(args.Channel)
        addBranches = lambda: mergeTau(args.Channel)
        nameStrip=files.strip()
        filename = (nameStrip.split('/')[-1]).split('.')[-2]
        p = PostProcessor(outputDir,[files], cut=None,branchsel=None,modules=[addBranches(),visibleM()], postfix=post,noOut=False,outputbranchsel=outputbranches)
        p.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to create a total reconstructed Tau collection')
    parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True)
    parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
    parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
    parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
    parser.add_argument('--postfix',help="string at the end of output file names", default="")
    args = parser.parse_args()

    #Define Eevnt Selection - all those to be connected by or

    fnames = [args.inputLocation+"/W.root"]
    #fnames = glob.glob(args.inputLocation + "/DY.root")  #making a list of input files
    #outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel/Test".format(args.Channel)
    outputDir = args.outputLocation
	#outputDir = "."
    outputbranches = "keep_and_drop.txt"
	#cuts = "&&".join(eventSelectionAND)
    post = args.postfix
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


	
    
    
	
	
	













        
        

    
		


