from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
from particleClass import particle
from FatJetClass import FatJet
import argparse
import traceback
import multiprocessing as  np
import os

#This script is used to prepare cutflows to determine and optimize the selections for the objects

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Channel(Module):
	#Defining the particle objects for applying selections later
	def __init__(self,filename):
		self.writeHistFile=True
		self.filename = filename #filename passed cause we needed to count the events with zero divide errors	
		self.boostedTau = particle("boostedTau")
		self.Tau = particle("Tau")
		self.FatJet = FatJet("FatJet")
		self.Electron = particle("Electron")
		self.Muon = particle("Muon")
			

	def beginJob(self, histFile=None,histDirName=None):
		Module.beginJob(self,histFile,histDirName)

		#Now lets define the cutflow histograms
		#Starting to Di Tau channel selections
		self.cutflow_diTau =  ROOT.TH1F('cutflow_diTau', 'cutflow_diTau', 6, 0, 6)
		self.cutflow_diTau.GetXaxis().SetBinLabel(1,"Events_Preselected")
		#self.cutflow_diTau.GetXaxis().SetBinLabel(2,">1 gTau_gJet")
		self.cutflow_diTau.GetXaxis().SetBinLabel(2,"gTau condition")
		self.cutflow_diTau.GetXaxis().SetBinLabel(3,"gJet condition")
		self.cutflow_diTau.GetXaxis().SetBinLabel(4,"gElectron condition")
		self.cutflow_diTau.GetXaxis().SetBinLabel(5,"gMuon condition")
		self.cutflow_diTau.GetXaxis().SetTitle("Selections")
		self.cutflow_diTau.GetYaxis().SetTitle("Events")
		self.cutflow_diTau.SetFillColor(38)


		self.cutflow_et =  ROOT.TH1F('cutflow_et', 'cutflow_et', 6, 0, 6)
		self.cutflow_et.GetXaxis().SetBinLabel(1,"Events_Preselected")
		#self.cutflow_et.GetXaxis().SetBinLabel(2,">1 gTau_gJet")
		self.cutflow_et.GetXaxis().SetBinLabel(2,"gTau condition")
		self.cutflow_et.GetXaxis().SetBinLabel(3,"gJet condition")
		self.cutflow_et.GetXaxis().SetBinLabel(5,"gMuon condition")
		self.cutflow_et.GetXaxis().SetBinLabel(4,"gElectron condition")
		self.cutflow_et.GetXaxis().SetTitle("Selections")
		self.cutflow_et.GetYaxis().SetTitle("Events")
		self.cutflow_et.SetFillColor(38)

		self.cutflow_mt =  ROOT.TH1F('cutflow_mt', 'cutflow_mt', 6, 0, 6)
		self.cutflow_mt.GetXaxis().SetBinLabel(1,"Events_Preselected")
		#self.cutflow_mt.GetXaxis().SetBinLabel(2,">1 gTau_gJet")
		self.cutflow_mt.GetXaxis().SetBinLabel(2,"gTau condition")
		self.cutflow_mt.GetXaxis().SetBinLabel(3,"gJet condition")
		self.cutflow_mt.GetXaxis().SetBinLabel(4,"gMuon condition")
		self.cutflow_mt.GetXaxis().SetBinLabel(5,"gElectron condition")
		self.cutflow_mt.GetXaxis().SetTitle("Selections")
		self.cutflow_mt.GetYaxis().SetTitle("Events")
		self.cutflow_mt.SetFillColor(38)

		self.addObject(self.cutflow_diTau)
		self.addObject(self.cutflow_mt)
		self.addObject(self.cutflow_et)
		#pass

	#event loop
	def analyze(self, event): 
		#Fill all the preselcted events
		self.cutflow_diTau.AddBinContent(1)
		self.cutflow_et.AddBinContent(1)
		self.cutflow_mt.AddBinContent(1)

		#Add all the Object Based Selection########################################
		
		self.Tau.setupCollection(event)
		self.Tau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 4 == 4))

		self.boostedTau.setupCollection(event)
		self.boostedTau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 4 == 4))

		self.FatJet.setupCollection(event)
		try:
			self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250) and ((x.tau2/x.tau1) < 0.75))
		except ZeroDivisionError:
			self.countBadevents += 1
			print("Error:(")
			traceback.print_exc()
			return False

		self.Electron.setupCollection(event)
		self.Electron.apply_cut(lambda x: x.mvaFall17V2Iso_WPL and (x.pt > 10))

		self.Muon.setupCollection(event)
		#self.Muon.apply_cut(lambda x: x.isGlobal and (x.pt > 10) and x.mvaId & 1 ==1)
		self.Muon.apply_cut(lambda x:(x.pt > 10) and x.mvaId & 1 == 1)

		if((len(self.Tau.collection)==2 or len(self.boostedTau.collection)==2)):
			self.cutflow_diTau.AddBinContent(2)
			if (len(self.FatJet.collection)==1):
				self.cutflow_diTau.AddBinContent(3)
				if (len(self.Muon.collection)==0):
					self.cutflow_diTau.AddBinContent(4)
					if (len(self.Electron.collection)==0):
						self.cutflow_diTau.AddBinContent(5)

		if((len(self.Tau.collection)==1 or len(self.boostedTau.collection)==1)):
			self.cutflow_mt.AddBinContent(2)
			if (len(self.FatJet.collection)==1):
				self.cutflow_mt.AddBinContent(3)
				if (len(self.Muon.collection)==1):
					self.cutflow_mt.AddBinContent(4)
					if (len(self.Electron.collection)==0):
						self.cutflow_mt.AddBinContent(5)


		if((len(self.Tau.collection)==1 or len(self.boostedTau.collection)==1)):
			self.cutflow_et.AddBinContent(2)
			if (len(self.FatJet.collection)==1):
				self.cutflow_et.AddBinContent(3)
				if (len(self.Electron.collection)==1):
					self.cutflow_et.AddBinContent(4)
					if (len(self.Muon.collection)==0):
						self.cutflow_et.AddBinContent(5)



		return False


				
				 
				 
					 
					 

		
		#####################################################################


def call_postpoc(files):
		letsSortChannels = lambda: Channel(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=None,modules=[letsSortChannels()],noOut=True,outputbranchsel=outputbranches,histFileName="Cutflow_LooseTau"+filename+".root",histDirName="Plots")
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
