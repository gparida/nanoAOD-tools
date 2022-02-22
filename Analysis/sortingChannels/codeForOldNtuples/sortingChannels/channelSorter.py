from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from addingNewObservableBranches.visibleMass import VisibleMass  #Importing modules works if the folders are in the place where the scripts are
from sortingTaus import mergeTau
import ROOT
import glob
from particleClass import particle
from FatJetClass import FatJet
from TauClass import Tau
from BoostedTauClass import BoostedTau
from ElectronClass import Electron
from MuonClass import Muon
import argparse
import traceback
import multiprocessing as  np
import os

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Channel(Module):
	def __init__(self, channel,filename):
		print ("Running the channel sorter Module")
		print ("processing file ",filename)
		self.channel = channel # Specify the channel
		self.filename = filename #filename passed cause we needed to count the events with zero divide errors
		#All these objects are common to all channels	
		self.boostedTau = BoostedTau("boostedTau")
		self.Tau = Tau("Tau")
		self.FatJet = FatJet("FatJet")
		self.Electron = Electron("Electron")
		self.Muon = Muon("Muon")
		self.Jet = particle("Jet")

		#this is for testing
		if self.channel == "test":
			self.boostedTau = particle("boostedTau")
			

	def beginJob(self):
		pass
	
	def endJob(self):
		pass

	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.countBadevents = 0 #This is to keep track of bad events per file
		self.out = wrappedOutputTree
		self.Tau.setUpBranches(self.out) #creating the new branches
		self.FatJet.setUpBranches(self.out)
		self.boostedTau.setUpBranches(self.out)
		self.Electron.setUpBranches(self.out)
		self.Muon.setUpBranches(self.out)
		
		if self.channel == "test":
			self.boostedTau.setUpBranches(self.out)
		


    		
    		
	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		print ("Number of Bad Events ", self.countBadevents)
		if self.countBadevents!=0:
			save_path = MYDIR=os.getcwd() + "/badEvents"
			file_name = "badEvents_"+str(self.filename)+"_"+str(self.channel)
			complete_Name =  os. path. join(save_path, file_name)
			file = open(complete_Name,"w")
			file.write("The Bad events for this file "+str(self.filename)+" is "+str(self.countBadevents))
			file.close()	
		#pass
	
	def HPStauVeto(self,tauCollectionObject):
		isTau =""
		tau1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau1.SetPtEtaPhiM(tauCollectionObject.pt,tauCollectionObject.eta,tauCollectionObject.phi,tauCollectionObject.mass)
		for boostedtau in self.boostedTau.collection:
			tau2.SetPtEtaPhiM(boostedtau.pt,boostedtau.eta,boostedtau.phi,boostedtau.mass)
			deltaR = tau1.DeltaR(tau2)
			if deltaR <= 0.02:
				isTau = "bad"
				break
		
		if isTau != "bad":
			return True
		else:
			return False
	
	def FatJetConeIsolation(self,CollectionObject):
		isObj =""
		obj1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		obj2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)	
		obj1.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)
		for fatjet in self.FatJet.collection:
			obj2.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
			deltaR = obj1.DeltaR(obj2)
			if deltaR <= 0.8:
				isObj = "bad"
				break
		
		if isObj != "bad":
			return True
		else:
			return False

	#event loop
	def analyze(self, event): 
		

		#Select the AK4 Jets and keep choose Jets with Tight DeepJet ID
		self.Jet.setupCollection(event)
		self.Jet.apply_cut(lambda x: (x.pt > 20) and (x.btagDeepB >= 0.8767))
		
		self.Tau.setupCollection(event)
		self.Tau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idDeepTau2017v2p1VSjet & 1 == 1))  #Deeptau ID for the standard Taus loosest WP
		


		self.boostedTau.setupCollection(event)
		self.boostedTau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 2 == 2)) # VLoose ID for newMVA for boosted Taus - but use oldMVA weighttn

		self.Tau.collection =  filter(self.HPStauVeto,self.Tau.collection)

		self.FatJet.setupCollection(event)
		try:
			#self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250) and ((x.tau2/x.tau1) < 0.75))
			self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250))	
		except ZeroDivisionError:
			self.countBadevents += 1
			print("Error:(")
			traceback.print_exc()
			return False

		self.Electron.setupCollection(event)
		self.Electron.apply_cut(lambda x: x.mvaFall17V2Iso_WPL and (x.pt > 10))
		self.Electron.collection = filter(self.Electron.relativeIso,self.Electron.collection)

		self.Muon.setupCollection(event)
		self.Muon.apply_cut(lambda x: x.pt > 10 and x.mvaId >= 1 and x.pfRelIso03_all < 0.25)

		#filter Objects to remove those within the fatjet cone

		self.Tau.collection = filter(self.FatJetConeIsolation,self.Tau.collection)
		self.boostedTau.collection = filter(self.FatJetConeIsolation,self.boostedTau.collection)
		self.Electron.collection = filter(self.FatJetConeIsolation,self.Electron.collection)
		self.Muon.collection = filter(self.FatJetConeIsolation,self.Muon.collection)
		self.Jet.collection = filter (self.FatJetConeIsolation,self.Jet.collection)

		############################################################################

		#Now Add all the channel based selection####################################
		# condition for hadronic channel
		if self.channel == "tt":
			#loose against both electron and Muon
			self.boostedTau.apply_cut(lambda x: (x.idAntiEle2018 & 2 ==2) and (x.idAntiMu & 1 == 1))
			self.Tau.apply_cut(lambda x: (x.idAntiEle2018 & 2 ==2) and (x.idAntiMu & 1 == 1))
			if(((len(self.Tau.collection) + len(self.boostedTau.collection))==2) 
				and len(self.FatJet.collection)==1 
				and len(self.Electron.collection)==0 
				and len(self.Muon.collection)==0
				and len(self.Jet.collection)==0):
				#print ("length of good elec ",len(self.Electron.collection),"length of good muons ",len(self.Muon.collection))
				self.Tau.fillBranches(self.out) #Fill the branches
				self.FatJet.fillBranches(self.out)
				self.boostedTau.fillBranches(self.out)
				self.Electron.fillBranches(self.out)
				self.Muon.fillBranches(self.out)
				return True # Store event
			else:
				return False # Reject event
		
		if self.channel == "et":
			#Electron is in the channel, so Tight discrimiantion against it and loose discrimination against Muon
			self.boostedTau.apply_cut(lambda x: (x.idAntiEle2018 & 8 ==8) and (x.idAntiMu & 1 == 1))
			self.Tau.apply_cut(lambda x: (x.idAntiEle2018 & 8 ==8) and (x.idAntiMu & 1 == 1))
			if(((len(self.Tau.collection) + len(self.boostedTau.collection))==1) 
				and len(self.FatJet.collection)==1 
				and len(self.Electron.collection)==1 
				and len(self.Muon.collection)==0
				and len(self.Jet.collection)==0):
				self.Tau.fillBranches(self.out) #Fill the branches
				self.FatJet.fillBranches(self.out)
				self.boostedTau.fillBranches(self.out)
				self.Electron.fillBranches(self.out)
				self.Muon.fillBranches(self.out)
				return True
			else:
				return False
		
		if self.channel == "mt":
			#Muon is in the channel so Tight diiscrimination against Muon and Loose against electron
			self.boostedTau.apply_cut(lambda x: (x.idAntiEle2018 & 2 ==2) and (x.idAntiMu & 2 == 2))
			self.Tau.apply_cut(lambda x: (x.idAntiEle2018 & 2 ==2) and (x.idAntiMu & 2 == 2))
			if(((len(self.Tau.collection) + len(self.boostedTau.collection))==1) 
				and len(self.FatJet.collection)==1 
				and len(self.Electron.collection)==0 
				and len(self.Muon.collection)==1
				and len(self.Jet.collection)==0):
				self.Tau.fillBranches(self.out) #Fill the branches
				self.FatJet.fillBranches(self.out)
				self.boostedTau.fillBranches(self.out)
				self.Muon.fillBranches(self.out)
				self.Electron.fillBranches(self.out)
				return True
			else:
				return False
		
		#####################################################################



			
	



def call_postpoc(files):
		letsSortChannels = lambda: Channel(args.Channel,filename)
		tauOdering = lambda: mergeTau(args.Channel,filename)
		visibleM = lambda:VisibleMass(args.Channel)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=outputbranches,modules=[letsSortChannels(),tauOdering(),visibleM()], postfix=post,noOut=False,outputbranchsel=outputbranches)

		p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	parser.add_argument('--postfix',help="string at the end of output file names", default="")
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

	#Define Eevnt Selection - all those to be connected by or

	#fnames = ["/data/aloeliger/bbtautauAnalysis/2016/Data.root"]
	fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
	#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel".format(args.Channel)
	outputDir = args.outputLocation
	#outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cuts = "&&".join(eventSelectionAND)
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

	
	



    ##Start the post processor
	#try:
	#	if args.Channel == "tt":
	#		fnames = glob.glob(args.inputLocation + "/*.root")
	#		#fnames = [str(args.inputLocation)] #for condor - Singular files too need to be in a list
 	#		outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/tt_Channel"
	#		#outputDir = "." #for condor
 	#		outputbranches = "keep_and_drop.txt"
 	#		#cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseIsoFilter && Flag_HBHENoiseFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter" # Event Based selection
 	#		cuts = "&&".join(eventSelectionAND)
	#		p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix="_ttChannel",noOut=False,outputbranchsel=outputbranches) # running the post processor - output files will have the _ttChannels appended to their name 
	#		p.run()
#
	#	if args.Channel == "et":
	#		fnames = glob.glob(args.inputLocation + "/*.root")
	#		#fnames = [str(args.inputLocation)] #for condor
 	#		outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/et_Channel"
	#		#outputDir = "." #for condor
 	#		outputbranches = "keep_and_drop.txt"
 	#		#cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseIsoFilter && Flag_HBHENoiseFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter" # Event Based selection
 	#		cuts = "&&".join(eventSelectionAND)
	#		p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix="_etChannel",noOut=False,outputbranchsel=outputbranches) # running the post processor - output files will have the _ttChannels appended to their name 
	#		p.run()
	#	
	#	if args.Channel == "mut":
	#		#fnames = glob.glob(args.inputLocation + "/*.root")
	#		fnames = ["/data/aloeliger/bbtautauAnalysis/2016/QCD_1000to1400.root"] #for condor
 	#		#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/mut_Channel"
	#		outputDir = "." #for condor
 	#		outputbranches = "keep_and_drop.txt"
	#		cuts = "&&".join(eventSelectionAND)
 	#		#cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseIsoFilter && Flag_HBHENoiseFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter" # Event Based selection
 	#		p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix="_mutChannel",noOut=False,outputbranchsel=outputbranches) # running the post processor - output files will have the _ttChannels appended to their name 
	#		p.run()
	#	
	#	if args.Channel == "test":
	#		#fnames = glob.glob(args.inputLocation + "/*.root")
	#		fnames = [str(args.inputLocation)] #for condor
 	#		#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/TestOutput"
	#		outputDir = "." #for condor
 	#		outputbranches = "keep_and_drop.txt"
	#		cuts = "&&".join(eventSelectionAND) 
 	#		#cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseIsoFilter && Flag_HBHENoiseFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter" # These wholesale cuts applied even before entering event loop
 	#		p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix="_boostedTest",noOut=False,outputbranchsel=outputbranches) # running the post processor - output files will have the _ttChannels appended to their name 
	#		p.run()
#
	#	
	#except Exception as error:
	#	print("Error:(")
	#	traceback.print_exc()
