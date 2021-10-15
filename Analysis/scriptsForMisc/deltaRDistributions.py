from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
from particleClass import particle
import argparse
import traceback
import multiprocessing as  np
import os

ROOT.PyConfig.IgnoreCommandLineOptions = True

class dRDistributions(Module):
    def __init__(self, filename):
        self.writeHistFile=True
        self.filename = filename #filename passed cause we needed to count the events with zero divide errors
	    #All these objects are common to all channels
        self.boostedTauLoose = particle("boostedTau")
        self.boostedTauVLoose = particle("boostedTau")
        self.boostedTaunoID = particle("boostedTau")
        self.Electron = particle("Electron")
        self.Muon = particle("Muon")		
		
    def beginJob(self, histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
		#Now lets define the cutflow histograms
		#Starting to Di Tau channel selections
        self.looseTau =  ROOT.TH1F('looseTau', 'looseTau', 20, 0, 1)
        self.vlooseTau =  ROOT.TH1F('vlooseTau', 'vlooseTau', 20, 0, 1)
        self.noIDTau =  ROOT.TH1F('noIDTau', 'noIDTau', 20, 0, 1)
        self.electron =  ROOT.TH1F('electron', 'electron', 20, 0, 1)
        self.muon =  ROOT.TH1F('muon', 'muon', 20, 0, 1)
        
        self.addObject(self.looseTau)
        self.addObject(self.vlooseTau)
        self.addObject(self.noIDTau)
        self.addObject(self.electron)
        self.addObject(self.muon)


    def analyze(self, event):
        deltaR = 0
        least_deltaR_LooseTau = 0 
        least_deltaR_VLooseTau = 0 
        least_deltaR_noIDTau = 0
        least_deltaR_electron = 0
        least_deltaR_muon = 0
        counter = 0

        self.boostedTauLoose.setupCollection(event)
        self.boostedTauLoose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 4 == 4))

        self.boostedTauVLoose.setupCollection(event)
        self.boostedTauVLoose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 2 == 2))

        self.boostedTaunoID.setupCollection(event)
        self.boostedTaunoID.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3))

        self.Electron.setupCollection(event)
        self.Electron.apply_cut(lambda x: x.mvaFall17V2Iso_WPL and (x.pt > 10))

        self.Muon.setupCollection(event) 
        self.Muon.apply_cut(lambda x: (x.pt > 10))

        leadingBoostedTau_V = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        secondLepton_V=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        if (len(self.boostedTauLoose.collection)!=0):
            leadingBoostedTau_V.SetPtEtaPhiM(self.boostedTauLoose.collection[0].pt,self.boostedTauLoose.collection[0].eta,self.boostedTauLoose.collection[0].phi,self.boostedTauLoose.collection[0].mass)
        else:
            return False
        for tau in  self.boostedTauLoose.collection:
            if (tau.pt == self.boostedTauLoose.collection[0].pt 
            and tau.eta == self.boostedTauLoose.collection[0].eta 
            and tau.phi == self.boostedTauLoose.collection[0].phi):
                continue
            secondLepton_V.SetPtEtaPhiM(tau.pt,tau.eta,tau.phi,tau.mass)
            deltaR = leadingBoostedTau_V.DeltaR(secondLepton_V)
            #print (deltaR)
            if (deltaR < least_deltaR_LooseTau or counter==0):
                least_deltaR_LooseTau = deltaR
                counter+=1
            
        
        self.looseTau.Fill(least_deltaR_LooseTau)
        self.looseTau.GetXaxis().SetTitle("Delta R")
        self.looseTau.GetYaxis().SetTitle("Events")
        self.looseTau.SetLineColor(1)
        self.looseTau.SetLineWidth(2)
        counter = 0 
        
        for tau in  self.boostedTauVLoose.collection:
            if (tau.pt == self.boostedTauLoose.collection[0].pt 
            and tau.eta == self.boostedTauLoose.collection[0].eta 
            and tau.phi == self.boostedTauLoose.collection[0].phi):
                continue
            secondLepton_V.SetPtEtaPhiM(tau.pt,tau.eta,tau.phi,tau.mass)
            deltaR = leadingBoostedTau_V.DeltaR(secondLepton_V)
            if (deltaR < least_deltaR_VLooseTau or counter==0):
                least_deltaR_VLooseTau = deltaR
                counter+=1
            

        self.vlooseTau.Fill(least_deltaR_VLooseTau)
        self.vlooseTau.GetXaxis().SetTitle("Delta R")
        self.vlooseTau.GetYaxis().SetTitle("Events")
        self.vlooseTau.SetLineColor(2)
        self.vlooseTau.SetLineWidth(2)
        counter=0
        
        for tau in  self.boostedTaunoID.collection:
            if (tau.pt == self.boostedTauLoose.collection[0].pt 
            and tau.eta == self.boostedTauLoose.collection[0].eta 
            and tau.phi == self.boostedTauLoose.collection[0].phi):
                continue
            secondLepton_V.SetPtEtaPhiM(tau.pt,tau.eta,tau.phi,tau.mass)
            deltaR = leadingBoostedTau_V.DeltaR(secondLepton_V)
            if (deltaR < least_deltaR_noIDTau or counter==0):
                least_deltaR_noIDTau= deltaR
                counter +=1
            
        
        self.noIDTau.Fill(least_deltaR_noIDTau)
        self.noIDTau.GetXaxis().SetTitle("Delta R")
        self.noIDTau.GetYaxis().SetTitle("Events")
        self.noIDTau.SetLineColor(42)
        self.noIDTau.SetLineWidth(2)
        counter = 0 



        for electron in  self.Electron.collection:
            secondLepton_V.SetPtEtaPhiM(electron.pt,electron.eta,electron.phi,electron.mass)
            deltaR = leadingBoostedTau_V.DeltaR(secondLepton_V)
            if (deltaR < least_deltaR_electron or counter == 0):
                least_deltaR_electron = deltaR
                counter+=1
            

        self.electron.Fill(least_deltaR_electron)
        self.electron.GetXaxis().SetTitle("Delta R")
        self.electron.GetYaxis().SetTitle("Events")
        self.electron.SetLineColor(4)
        self.electron.SetLineWidth(2)
        counter=0

        for muon in  self.Muon.collection:
            secondLepton_V.SetPtEtaPhiM(muon.pt,muon.eta,muon.phi,muon.mass)
            deltaR = leadingBoostedTau_V.DeltaR(secondLepton_V)
            if (deltaR < least_deltaR_muon or counter==0):
                least_deltaR_muon = deltaR
                counter+=1
            
        
        self.muon.Fill(least_deltaR_muon)
        self.muon.GetXaxis().SetTitle("Delta R")
        self.muon.GetYaxis().SetTitle("Events")
        self.muon.SetLineColor(28)
        self.muon.SetLineWidth(2)
        counter=0
        print (len(self.boostedTauLoose.collection),len(self.boostedTauVLoose.collection),len(self.boostedTaunoID.collection),len(self.Muon.collection),len(self.Electron.collection))
        print (least_deltaR_LooseTau,least_deltaR_VLooseTau, least_deltaR_noIDTau, least_deltaR_muon, least_deltaR_electron)
	
        return True        


def call_postpoc(files):
		letsSortChannels = lambda: dRDistributions(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=None,modules=[letsSortChannels()],noOut=True,outputbranchsel=outputbranches,histFileName="DR"+filename+".root",histDirName="Plots")
		p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	#parser.add_argument('--Channel',help="enter either tt or et or mut. For boostedTau test enter test",required=True)
	parser.add_argument('--inputFile',help="enter the path to the location of input file set",default="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	args = parser.parse_args()

	#Define Event Selection - all those to be connected by and
	eventSelectionAND = ["MET_pt>200",
						"PV_ndof > 4",
						"abs(PV_z) < 24",
						"sqrt(PV_x*PV_x+PV_y*PV_y) < 2",
						"Flag_goodVertices",
						"Flag_globalSuperTightHalo2016Filter", 
						"Flag_HBHENoiseIsoFilter",
						"Flag_HBHENoiseFilter",
						"Flag_EcalDeadCellTriggerPrimitiveFilter",
						"Flag_BadPFMuonFilter",
						"Flag_eeBadScFilter"]

	fnames =[args.inputFile]
	outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cuts = "&&".join(eventSelectionAND)
	argList = list()
	filename =""
	for file in fnames:
		argList.append(file)

	if int(args.ncores) == 1:
		for arr in argList:
			call_postpoc(arr)
	
	else:
		pool = np.Pool(int(args.ncores))
		res=pool.map(call_postpoc, argList)

                













    

