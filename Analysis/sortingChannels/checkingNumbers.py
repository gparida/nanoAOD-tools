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

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Channel(Module):
	def __init__(self, channel,filename):
		self.writeHistFile=True
		self.channel = channel # Specify the channel
		self.filename = filename #filename passed cause we needed to count the events with zero divide errors
		#All these objects are common to all channels	
		self.boostedTau = particle("boostedTau")
		self.Tau = particle("Tau")
		self.FatJet = FatJet("FatJet")
		self.Electron = particle("Electron")
		self.Muon = particle("Muon")

		#this is for testing
		if self.channel == "test":
			self.boostedTau = particle("boostedTau")
			

	def beginJob(self, histFile=None,histDirName=None):
		Module.beginJob(self,histFile,histDirName)
		self.cutflow_tau =  ROOT.TH1F('cutflow_tau', 'cutflow_tau', 3, 0, 3)
		self.cutflow_tau.GetXaxis().SetBinLabel(1,"Events_preselected")
		self.cutflow_tau.GetXaxis().SetBinLabel(2,"2 or more taus")
		self.cutflow_tau.GetXaxis().SetBinLabel(3,"Object selection applied")
		self.cutflow_tau.SetFillColor(38)
		self.cutflow_mu =  ROOT.TH1F('cutflow_mu', 'cutflow_mu', 3, 0, 3)
		self.addObject(self.cutflow_tau)
		self.addObject(self.cutflow_mu)
		#pass

	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass
		 		
	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):	
		pass
    	
	#event loop
	def analyze(self, event): 
		
		self.cutflow_tau.AddBinContent(1)

		#This is for testing the sccript on boosted tau branches
		if self.channel == "test":
			self.boostedTau.setupCollection(event)
			self.boostedTau.apply_cut(lambda x: x.pt > 20 and (abs(x.eta) < 2.3) and (x.idMVAoldDM2017v2 & 1 == 1) )
			self.boostedTau.fillBranches(self.out)
			return True

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

		############################################################################

		#Now Add all the channel based selection####################################
		# condition for hadronic channel
		if self.channel == "tt":
			if((len(self.Tau.collection)>=2 or len(self.boostedTau.collection)>=2) and (len(self.Electron.collection)==0 and len(self.Muon.collection)==0) and (len(self.FatJet.collection)==1)):
				self.cutflow_tau.AddBinContent(2)
				#print ("length of good elec ",len(self.Electron.collection),"length of good muons ",len(self.Muon.collection))
				#self.Tau.fillBranches(self.out) #Fill the branches
				#self.FatJet.fillBranches(self.out)
				#self.boostedTau.fillBranches(self.out)
				return True # Store event
			else:
				return False # Reject event
		
		if self.channel == "et":
			if((len(self.Tau.collection)==1 or len(self.boostedTau.collection)==1) 
				and len(self.FatJet.collection)==1 
				and len(self.Electron.collection)==1 
				and len(self.Muon.collection)==0):
				self.Tau.fillBranches(self.out) #Fill the branches
				self.FatJet.fillBranches(self.out)
				self.boostedTau.fillBranches(self.out)
				self.Electron.fillBranches(self.out)
				return True
			else:
				return False
		
		if self.channel == "mut":
			if((len(self.Tau.collection)==1 or len(self.boostedTau.collection)==1) 
				and len(self.FatJet.collection)==1 
				and len(self.Electron.collection)==0 
				and len(self.Muon.collection)==1):
				self.Tau.fillBranches(self.out) #Fill the branches
				self.FatJet.fillBranches(self.out)
				self.boostedTau.fillBranches(self.out)
				self.Muon.fillBranches(self.out)
				return True
			else:
				return False
		
		#####################################################################



			
	



def call_postpoc(files):
		letsSortChannels = lambda: Channel(args.Channel,filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix=post,noOut=True,outputbranchsel=outputbranches,histFileName="histOut.root",histDirName="Cutfdlow/plots")
		p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	parser.add_argument('--Channel',help="enter either tt or et or mut. For boostedTau test enter test",required=True)
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
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

	#Define Eevnt Selection - all those to be connected by or

	#fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
	fnames =["/data/aloeliger/bbtautauAnalysis/2016/Data.root"]
	#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel".format(args.Channel)
	outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cuts = "&&".join(eventSelectionAND)
	post ="_{}Channel".format(str(args.Channel))
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
