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

#The objective of the code is to get the multiplicity of taus - applying a base selection of VLoose for all taus
#The double counting of the taus needs to be avoided by applying the veto < 0.02\
#Then make two addtional histogram with the leading tau with a tigher wp

ROOT.PyConfig.IgnoreCommandLineOptions = True

class HPSVetoandMultiplicty(Module):
    def __init__(self, filename):
        self.writeHistFile=True
        self.filename = filename #filename passed cause we needed to count the events with zero divide errors
	    #All these objects are common to all channels
        self.boostedTauVVLoose = particle("boostedTau")
        self.HPSTauVVloose = particle ("Tau")		
		
    def beginJob(self, histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
		#Now lets define the cutflow histograms
		#Starting to Di Tau channel selections
        self.totalMultiplicity =  ROOT.TH1F('totalMultiplicity', 'totalMultiplicity', 5, 0, 5)
        self.leadingVLooseMultiplicity = ROOT.TH1F('leadingVLooseMultiplcity', 'leadingVLooseMultiplcity', 5, 0, 5)
        self.leadingLooseMultiplcity =  ROOT.TH1F('leadingLooseMultiplcity', 'leadingLooseMultiplcity', 5, 0, 5)
        self.leadingMediumMultiplicity = ROOT.TH1F('leadingMediumMultiplicity', 'leadingMediumMultiplicity', 5, 0, 5)
        self.leadingTightMultiplicity = ROOT.TH1F('leadingTightMultiplicity', 'leadingTightMultiplicity', 5, 0, 5)
        
        self.addObject(self.totalMultiplicity)
        self.addObject(self.leadingVLooseMultiplicity)
        self.addObject(self.leadingLooseMultiplcity)
        self.addObject(self.leadingMediumMultiplicity)
        self.addObject(self.leadingTightMultiplicity)

    def HPStauVeto(self,tauCollectionObject):
        isTau =""
        tau1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        tau2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        tau1.SetPtEtaPhiM(tauCollectionObject.pt,tauCollectionObject.eta,tauCollectionObject.phi,tauCollectionObject.mass)
        for loosetau in self.boostedTauVVLoose.collection:
            tau2.SetPtEtaPhiM(loosetau.pt,loosetau.eta,loosetau.phi,loosetau.mass)
            deltaR = tau1.DeltaR(tau2)
            if deltaR <= 0.02:
                isTau = "bad"
                break
        if isTau != "bad":
            return True
        else:
            return False
        



    def analyze(self, event):
        #self.boostedTauLoose.setupCollection(event)
        #self.boostedTauLoose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 4 == 4))

        self.boostedTauVVLoose.setupCollection(event)
        self.boostedTauVVLoose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 1 == 1))
        

        self.HPSTauVVloose.setupCollection(event)
        self.HPSTauVVloose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 1 == 1))

        HPSVetoCollection = filter(self.HPStauVeto,self.HPSTauVVloose.collection)

        #print ("original HPS Taus = ",len(self.HPSTauVVloose.collection),"Vetoed Taus = ",len(HPSVetoCollection))
        print ("Event Weight = ",event.FinalWeighting)

        self.totalMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

        if (len(self.boostedTauVVLoose.collection)!=0 and len(HPSVetoCollection)!=0):
            if ((self.boostedTauVVLoose.collection[0].pt > HPSVetoCollection[0].pt) and (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 2 == 2)):
                self.leadingVLooseMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

            if ((self.boostedTauVVLoose.collection[0].pt < HPSVetoCollection[0].pt) and (HPSVetoCollection[0].idMVAnewDM2017v2 & 2 == 2)):
                self.leadingVLooseMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
            

            if ((self.boostedTauVVLoose.collection[0].pt > HPSVetoCollection[0].pt) and (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 4 == 4)):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

            if ((self.boostedTauVVLoose.collection[0].pt < HPSVetoCollection[0].pt) and (HPSVetoCollection[0].idMVAnewDM2017v2 & 4 == 4)):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

            if ((self.boostedTauVVLoose.collection[0].pt > HPSVetoCollection[0].pt) and (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 8 == 8)):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

            if ((self.boostedTauVVLoose.collection[0].pt < HPSVetoCollection[0].pt) and (HPSVetoCollection[0].idMVAnewDM2017v2 & 8 == 8)):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
            
            if ((self.boostedTauVVLoose.collection[0].pt > HPSVetoCollection[0].pt) and (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 16 == 16)):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

            if ((self.boostedTauVVLoose.collection[0].pt < HPSVetoCollection[0].pt) and (HPSVetoCollection[0].idMVAnewDM2017v2 & 16 == 16)):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)


        if (len(self.boostedTauVVLoose.collection)!=0 and len(HPSVetoCollection)==0):
            if (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 2 == 2):
                self.leadingVLooseMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
            if (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 4 == 4):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
            if (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 8 == 8):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
            if (self.boostedTauVVLoose.collection[0].idMVAnewDM2017v2 & 16 == 16):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
        
        if (len(self.boostedTauVVLoose.collection)==0 and len(HPSVetoCollection)!=0):
            if (HPSVetoCollection[0].idMVAnewDM2017v2 & 2 == 2):
                self.leadingVLooseMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

            if (HPSVetoCollection[0].idMVAnewDM2017v2 & 4 == 4):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
            
            if (HPSVetoCollection[0].idMVAnewDM2017v2 & 8 == 8):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)
            
            if (HPSVetoCollection[0].idMVAnewDM2017v2 & 16 == 16):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVVLoose.collection)+len(HPSVetoCollection),event.FinalWeighting)

        self.totalMultiplicity.GetXaxis().SetTitle("Total Taus")
        self.totalMultiplicity.GetYaxis().SetTitle("Events")
        self.totalMultiplicity.SetLineColor(1)
        self.totalMultiplicity.SetLineWidth(3)

        self.leadingLooseMultiplcity.GetXaxis().SetTitle("Total Taus")
        self.leadingLooseMultiplcity.GetYaxis().SetTitle("Events")
        self.leadingLooseMultiplcity.SetLineColor(2)
        self.leadingLooseMultiplcity.SetLineWidth(3)

        self.leadingMediumMultiplicity.GetXaxis().SetTitle("Total Taus")
        self.leadingMediumMultiplicity.GetYaxis().SetTitle("Events")
        self.leadingMediumMultiplicity.SetLineColor(3)
        self.leadingMediumMultiplicity.SetLineWidth(3)

        self.leadingTightMultiplicity.GetXaxis().SetTitle("Total Taus")
        self.leadingTightMultiplicity.GetYaxis().SetTitle("Events")
        self.leadingTightMultiplicity.SetLineColor(4)
        self.leadingTightMultiplicity.SetLineWidth(3)

        self.leadingVLooseMultiplicity.GetXaxis().SetTitle("Total Taus")
        self.leadingVLooseMultiplicity.GetYaxis().SetTitle("Events")
        self.leadingVLooseMultiplicity.SetLineColor(5)
        self.leadingVLooseMultiplicity.SetLineWidth(3)
        




	
        return True        


def call_postpoc(files):
		letsSortChannels = lambda: HPSVetoandMultiplicty(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=None,modules=[letsSortChannels()],noOut=True,outputbranchsel=outputbranches,histFileName="HPSVeto_"+filename+".root",histDirName="Plots")
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

                













    

