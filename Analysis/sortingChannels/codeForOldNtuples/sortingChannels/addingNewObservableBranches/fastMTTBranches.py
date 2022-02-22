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

        #HTT created with FastMTT pt,m, and visible eta/phi
        self.out.branch("fastMTT_HTTleg_pt","F")
        self.out.branch("fastMTT_HTTleg_eta","F")
        self.out.branch("fastMTT_HTTleg_phi","F")
        self.out.branch("fastMTT_HTTleg_m", "F")

        #HTT created with FastMTT pt,m, and visible+MET eta/phi
        self.out.branch("fastMTT_HTTlegWithMet_pt","F")
        self.out.branch("fastMTT_HTTlegWithMet_eta","F")
        self.out.branch("fastMTT_HTTlegWithMet_phi","F")
        self.out.branch("fastMTT_HTTlegWithMet_m", "F")


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

        #Visible components branches
        self.out.branch("VisHiggs_m","F")
        self.out.branch("VisHiggs_pt","F")
        self.out.branch("VisHiggs_eta","F")
        self.out.branch("VisHiggs_phi","F")

        self.out.branch("VisRadion_pt","F")
        self.out.branch("VisRadion_eta","F")
        self.out.branch("VisRadion_phi","F")
        self.out.branch("VisRadion_m","F")
        

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

        collectionBasedFirstLepton = None
        collectionBasedSecondLepton = None
        fastMTTfirstLeptonMass = 0.0
        fastMTTsecondLeptonMass = 0.0
        firstLeptonType = ''
        secondLeptonType = ''
        firstLeptonTrueMass = 0.0
        secondLeptonTrueMass = 0.0

        if event.channel == 0:
            firstLeptonType = 'Tau'
            secondLeptonType = 'Tau'
            if len(gTau) == 2:
                collectionBasedFirstLepton = gTau[0]
                collectionBasedSecondLepton = gTau[1]
            elif len(gboostedTau)==2:
                collectionBasedFirstLepton = gboostedTau[0]
                collectionBasedSecondLepton = gboostedTau[1]
                
            elif (len(gTau)==1 and len(gboostedTau)==1):
                collectionBasedFirstLepton = gboostedTau[0]
                collectionBasedSecondLepton = gTau[0]
            fastMTTfirstLeptonMass = collectionBasedFirstLepton.mass
            fastMTTsecondLeptonMass = collectionBasedSecondLepton.mass

        elif event.channel == 1 or event.channel == 2:
            firstLeptonType = 'Tau'
            if(len(gTau) != 0):
                collectionBasedFirstLepton = gTau[0]
            if(len(gboostedTau) != 0):
                collectionBasedFirstLepton = gboostedTau[0]
            fastMTTfirstLeptonMass = collectionBasedFirstLepton.mass

            if event.channel == 1:
                secondLeptonType = 'Electron'
                collectionBasedSecondLepton = gElectron[0]
                fastMTTsecondLeptonMass = 0.000511 #This seems to be hard set in the tool
                #Ask Cecile...

            elif event.channel == 2:
                secondLeptonType = 'Muon'
                collectionBasedSecondLepton = gMuon[0]
                fastMTTsecondLeptonMass = collectionBasedSecondLepton.mass
    
    
        firstLeptonTrueMass = collectionBasedFirstLepton.mass
        secondLeptonTrueMass = collectionBasedSecondLepton.mass

        firstLepton = fastMTTlepton(
            pt = collectionBasedFirstLepton.pt,
            eta = collectionBasedFirstLepton.eta,
            phi = collectionBasedFirstLepton.phi,
            m = fastMTTfirstLeptonMass,
            leptonType = firstLeptonType
        )
        if firstLeptonType == 'Tau':
            firstLepton.setTauDecayMode(collectionBasedFirstLepton.decayMode)
            #if (firstLepton.getM() > 1.5 or firstLepton.getM() < 0.3):
                #print ("decay mode = ",firstLepton.getTauDecayMode()," Prepare for warning")
            if firstLepton.getTauDecayMode() == 1: #check if we went over any mass bounds
                #technically fast MTT does this for us, but this should disable warnings
                if firstLepton.getM() > 1.5:
                    firstLepton.setM(1.5) 
                if firstLepton.getM() < 0.3:
                    firstLepton.setM(0.3)
            
        secondLepton = fastMTTlepton(
            pt = collectionBasedSecondLepton.pt,
            eta = collectionBasedSecondLepton.eta,
            phi = collectionBasedSecondLepton.phi,
            m = fastMTTsecondLeptonMass,
            leptonType = secondLeptonType,
        )
        if secondLeptonType == 'Tau':
            secondLepton.setTauDecayMode(collectionBasedSecondLepton.decayMode)
            #if (secondLepton.getM() > 1.5 or secondLepton.getM() < 0.3):
                #print ("decay mode = ",secondLepton.getTauDecayMode()," Prepare for warning")
            if secondLepton.getTauDecayMode() == 1: #check if we went over any mass bounds
                #technically fast MTT does this for us, but this should disable warnings
                if secondLepton.getM() > 1.5:
                    secondLepton.setM(1.5) 
                if secondLepton.getM() < 0.3:
                    secondLepton.setM(0.3)

                
        theMET = fastMTTmet(
            measuredX = event.MET_pt * math.cos(event.MET_phi),
            measuredY = event.MET_pt * math.sin(event.MET_phi),
            xx = event.MET_covXX,
            xy = event.MET_covXY,
            yy = event.MET_covYY)


        #Now, we can try to reconstruct the radion in different ways
        #start with the simple ones
        #then we try to reconstruct the HTT vertex

        
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

        #okay, now we can compute the HTT vector
        self.theFastMTTtool.setFirstLepton(firstLepton)
        self.theFastMTTtool.setSecondLepton(secondLepton)
        self.theFastMTTtool.setTheMET(theMET)
        
        
        fastMTTHiggsPt = self.theFastMTTtool.getFastMTTpt()
        fastMTTHiggsMass = self.theFastMTTtool.getFastMTTmass()

        firstLeptonVector = ROOT.TLorentzVector()
        secondLeptonVector = ROOT.TLorentzVector()

        #we're going to use the true lepton mass for right now
        #This may need to be the mass given to FastMTT? It's unclear
        firstLeptonVector.SetPtEtaPhiM(
            self.theFastMTTtool.getFirstLepton().getPt(),
            self.theFastMTTtool.getFirstLepton().getEta(),
            self.theFastMTTtool.getFirstLepton().getPhi(),
            firstLeptonTrueMass)
        secondLeptonVector.SetPtEtaPhiM(
            self.theFastMTTtool.getSecondLepton().getPt(),
            self.theFastMTTtool.getSecondLepton().getEta(),
            self.theFastMTTtool.getSecondLepton().getPhi(),
            secondLeptonTrueMass)

        HTTvectorWithoutMET = ROOT.TLorentzVector()
        HTTvectorWithMET = ROOT.TLorentzVector()
        HTTvectorVisible = ROOT.TLorentzVector()

        HTTvectorWithoutMET.SetPtEtaPhiM(
            fastMTTHiggsPt,
            (firstLeptonVector + secondLeptonVector).Eta(),
            (firstLeptonVector + secondLeptonVector).Phi(),
            fastMTTHiggsMass)

        HTTvectorWithMET.SetPtEtaPhiM(
            fastMTTHiggsPt,
            (firstLeptonVector + secondLeptonVector + METvector).Eta(),
            (firstLeptonVector + secondLeptonVector + METvector).Phi(),
            fastMTTHiggsMass)
        
        HTTvectorVisible.SetPtEtaPhiM(
            (firstLeptonVector + secondLeptonVector).Pt(),
            (firstLeptonVector + secondLeptonVector).Eta(),
            (firstLeptonVector + secondLeptonVector).Phi(),
            event.gMVis_LL)




        self.out.fillBranch("fastMTT_HTTleg_pt", HTTvectorWithoutMET.Pt())
        self.out.fillBranch("fastMTT_HTTleg_eta", HTTvectorWithoutMET.Eta())
        self.out.fillBranch("fastMTT_HTTleg_phi", HTTvectorWithoutMET.Phi())
        self.out.fillBranch("fastMTT_HTTleg_m", HTTvectorWithoutMET.M())

        self.out.fillBranch("fastMTT_HTTlegWithMet_pt", HTTvectorWithMET.Pt())
        self.out.fillBranch("fastMTT_HTTlegWithMet_eta", HTTvectorWithMET.Eta())
        self.out.fillBranch("fastMTT_HTTlegWithMet_phi", HTTvectorWithMET.Phi())
        self.out.fillBranch("fastMTT_HTTlegWithMet_m", HTTvectorWithMET.M())

        self.out.fillBranch("VisHiggs_pt",HTTvectorVisible.Pt())
        self.out.fillBranch("VisHiggs_eta",HTTvectorVisible.Eta())
        self.out.fillBranch("VisHiggs_phi",HTTvectorVisible.Phi())
        self.out.fillBranch("VisHiggs_m",HTTvectorVisible.M())


        #Radion vector, without met included
        RadionVector = HTTvectorWithoutMET + HbbVector

        #Radion vector with met included
        RadionVectorPlusMET = HTTvectorWithMET + HbbVector

        #Radion vector with only visible components
        RadionVectorVisible = HTTvectorVisible + HbbVector

        #read these out to the branches
        self.out.fillBranch("fastMTT_RadionLeg_pt", RadionVector.Pt())
        self.out.fillBranch("fastMTT_RadionLeg_eta", RadionVector.Eta())
        self.out.fillBranch("fastMTT_RadionLeg_phi", RadionVector.Phi())
        self.out.fillBranch("fastMTT_RadionLeg_m", RadionVector.M())

        self.out.fillBranch("fastMTT_RadionLegWithMet_pt", RadionVectorPlusMET.Pt())
        self.out.fillBranch("fastMTT_RadionLegWithMet_eta", RadionVectorPlusMET.Eta())
        self.out.fillBranch("fastMTT_RadionLegWithMet_phi", RadionVectorPlusMET.Phi())
        self.out.fillBranch("fastMTT_RadionLegWithMet_m", RadionVectorPlusMET.M())

        self.out.fillBranch("VisRadion_pt",RadionVectorVisible.Pt())
        self.out.fillBranch("VisRadion_eta",RadionVectorVisible.Eta())
        self.out.fillBranch("VisRadion_phi",RadionVectorVisible.Phi())
        self.out.fillBranch("VisRadion_m",RadionVectorVisible.M())

        
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