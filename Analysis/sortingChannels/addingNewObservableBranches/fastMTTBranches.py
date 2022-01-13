#Andrew Loeliger
#Module for creating our analysis's FastMTT based branches
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
import ROOT
from bbtautauAnalysisScripts.fastMTTPython.fastMTTtool import *
import math
import argparse
import glob
import multiprocessing as  np

class fastMTTBranches(Module):
    def __init__(self, filename):
        print("Creating fast MTT based branches")
        self.theFastMTTtool = fastMTTtool()
        print ("processing file ",filename)
        self.filename = filename

        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch("fastMTT_HTTleg_pt","F")
        self.out.branch("fastMTT_HTTleg_eta","F")
        self.out.branch("fastMTT_HTTleg_phi","F")
        self.out.branch("fastMTT_HTTleg_m", "F")

        #Radion created from visible HTT components
        self.out.branch("fastMTT_RadionLeg_pt","F")
        self.out.branch("fastMTT_RadionLeg_eta", "F")
        self.out.branch("fastMTT_RadionLeg_phi","F")
        self.out.branch("fastMTT_RadionLeg_m","F")

        #Radion created from visible HTT + MET components
        self.out.branch("fastMTT_RadionLegWithMet_pt", "F")
        self.out.branch("fastMTT_RadionLegWithMet_eta", "F")
        self.out.branch("fastMTT_RadionLegWithMet_phi", "F")
        self.out.branch("fastMTT_RadionLegWithMet_m","F")
        

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        gTau = Collection(event, 'gTau', 'gnTau')
        gboostedTau = Collection(event, 'gboostedTau', 'gnboostedTau')
        gElectron = Collection(event, 'gElectron', 'gnElectron')
        gMuon = Collection(event, 'gMuon', 'gnMuon')
        gFatJet = Collection(event, 'gFatJet', 'gnFatJet')

        firstLepton = fastMTTlepton()
        secondLepton = fastMTTlepton()
        theMET = fastMTTmet()

        if event.channel == 0:
            if len(gTau) == 2:
                firstLepton = fastMTTlepton(
                    pt = gTau[0].pt,
                    eta = gTau[0].eta,
                    phi = gTau[0].phi,
                    m = 0.13957,
                    tauDecayMode = gTau[0].decayMode,
                    leptonType = 'Tau')
                secondLepton = fastMTTlepton(
                    pt = gTau[1].pt,
                    eta = gTau[1].eta,
                    phi = gTau[1].phi,
                    m = 0.13957,
                    tauDecayMode = gTau[1].decayMode,
                    leptonType = 'Tau')

            elif len(gboostedTau)==2:
                firstLepton = fastMTTlepton(
                    pt = gboostedTau[0].pt,
                    eta = gboostedTau[0].eta,
                    phi = gboostedTau[0].phi,
                    m = 0.13957,
                    tauDecayMode = gboostedTau[0].decayMode,
                    leptonType = 'Tau')
                secondLepton = fastMTTlepton(
                    pt = gboostedTau[1].pt,
                    eta = gboostedTau[1].eta,
                    phi = gboostedTau[1].phi,
                    m = 0.13957,
                    tauDecayMode = gboostedTau[1].decayMode,
                    leptonType='Tau')

            elif (len(gTau)==1 and len(gboostedTau)==1):
                firstLepton = fastMTTlepton(
                    pt = gboostedTau[0].pt,
                    eta = gboostedTau[0].eta,
                    phi = gboostedTau[0].phi,
                    m = 0.13957,
                    tauDecayMode = gboostedTau[0].decayMode,
                    leptonType='Tau')
                secondLepton = fastMTTlepton(
                    pt = gTau[0].pt,
                    eta = gTau[0].eta,
                    phi = gTau[0].phi,
                    m = 0.13957,
                    tauDecayMode = gTau[0].decayMode,
                    leptonType = 'Tau')

        elif event.channel == 1 or event.channel == 2:
            if(len(gTau) != 0):
                firstLepton = fastMTTlepton(
                    pt = gTau[0].pt,
                    eta = gTau[0].pt,
                    phi = gTau[0].pt,
                    m = 0.13957,
                    tauDecayMode = gTau[0].decayMode,
                    leptonType = 'Tau')
            if(len(gboostedTau) != 0):
                firstLepton = fastMTTlepton(
                    pt = gboostedTau[0].pt,
                    eta = gboostedTau[0].eta,
                    phi = gboostedTau[0].phi,
                    m = 0.13957,
                    tauDecayMode = gboostedTau[0].decayMode,
                    leptonType = 'Tau')

            if event.channel == 1:
                secondLepton = fastMTTlepton(
                    pt = gElectron[0].pt,
                    eta = gElectron[0].eta,
                    phi = gElectron[0].phi,
                    #m = gElectron[0].mass,
                    #This seems to be another hard set in the tool.
                    m = 0.000511,
                    leptonType = 'Electron')

            elif event.channel == 2:
                secondLepton = fastMTTlepton(
                    pt = gMuon[0].pt,
                    eta = gMuon[0].eta,
                    phi = gMuon[0].phi,
                    m = gMuon[0].mass,
                    leptonType = 'Muon')
    
        theMET = fastMTTmet(
            measuredX = event.MET_pt * math.cos(event.MET_phi),
            measuredY = event.MET_pt * math.sin(event.MET_phi),
            xx = event.MET_covXX,
            xy = event.MET_covXY,
            yy = event.MET_covYY)

        #okay, now we can compute the HTT vector
        self.theFastMTTtool.setFirstLepton(firstLepton)
        self.theFastMTTtool.setSecondLepton(secondLepton)
        self.theFastMTTtool.setTheMET(theMET)

        print ("mass= ",self.theFastMTTtool.getFastMTTmass(),"phi= ",self.theFastMTTtool.getFastMTTphi(),"eta= ",self.theFastMTTtool.getFastMTTeta(),"pt= ", self.theFastMTTtool.getFastMTTpt())
        
        HTTvector = ROOT.TLorentzVector()
        HTTvector.SetPtEtaPhiM(
            self.theFastMTTtool.getFastMTTpt(),
            self.theFastMTTtool.getFastMTTeta(),
            self.theFastMTTtool.getFastMTTphi(),
            self.theFastMTTtool.getFastMTTmass())
        
        print ("VecorMass= ",HTTvector.M(),"VecotrPhi= ",HTTvector.Phi(),"VectorEta= ", HTTvector.Eta(),"VectorPt= ",HTTvector.Pt())

        #self.out.fillBranch("fastMTT_HTTleg_pt", HTTvector.Pt())
        #self.out.fillBranch("fastMTT_HTTleg_eta", HTTvector.Eta())
        #self.out.fillBranch("fastMTT_HTTleg_phi", HTTvector.Phi())
        #self.out.fillBranch("fastMTT_HTTleg_m", HTTvector.M())

        self.out.fillBranch("fastMTT_HTTleg_pt",self.theFastMTTtool.getFastMTTpt())
        self.out.fillBranch("fastMTT_HTTleg_eta", self.theFastMTTtool.getFastMTTeta())
        self.out.fillBranch("fastMTT_HTTleg_phi", self.theFastMTTtool.getFastMTTphi())
        self.out.fillBranch("fastMTT_HTTleg_m", self.theFastMTTtool.getFastMTTmass())

        #Now, we can try to reconstruct the radion in different ways as well.
        
        #Hbb vector
        HbbVector = ROOT.TLorentzVector()
        HbbVector.SetPtEtaPhiM(
            gFatJet[0].pt,
            gFatJet[0].eta,
            gFatJet[0].phi,
            gFatJet[0].msoftdrop)

        #MET vector
        METvector = ROOT.TLorentzVector()
        METvector.SetPtEtaPhiM(
            event.MET_pt,
            0.0,
            event.MET_phi,
            0.0)

        #Radion vector, without met included
        RadionVector = HTTvector + HbbVector

        #Radion vector with met included
        RadionVectorPlusMET = HTTvector + METvector + HbbVector

        #read these out to the branches
        self.out.fillBranch("fastMTT_RadionLeg_pt", RadionVector.Pt())
        self.out.fillBranch("fastMTT_RadionLeg_eta", RadionVector.Eta())
        self.out.fillBranch("fastMTT_RadionLeg_phi", RadionVector.Phi())
        self.out.fillBranch("fastMTT_RadionLeg_m", RadionVector.M())

        self.out.fillBranch("fastMTT_RadionLegWithMet_pt", RadionVectorPlusMET.Pt())
        self.out.fillBranch("fastMTT_RadionLegWithMet_eta", RadionVectorPlusMET.Eta())
        self.out.fillBranch("fastMTT_RadionLegWithMet_phi", RadionVectorPlusMET.Phi())
        self.out.fillBranch("fastMTT_RadionLegWithMet_m", RadionVectorPlusMET.M())
        
        return True

def call_postpoc(files):
		MTTBranches = lambda: fastMTTBranches(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=outputbranches,modules=[MTTBranches()], postfix=post,noOut=False,outputbranchsel=outputbranches)

		p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	parser.add_argument('--postfix',help="string at the end of output file names", default="")
	args = parser.parse_args()

	

	#Define Eevnt Selection - all those to be connected by or

	#fnames = ["/data/aloeliger/bbtautauAnalysis/2016/Data.root"]
	fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
	#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel".format(args.Channel)
	outputDir = args.outputLocation
	#outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cuts = None
	#post ="_{}Channel".format(str(args.Channel))
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
		print ("list", argList)
		res=pool.map(call_postpoc, argList)