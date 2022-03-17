from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from addingNewObservableBranches.visibleMassCamilla import VisibleMassCamilla  #Importing modules works if the folders are in the place where the scripts are
from addingNewObservableBranches.fastMTTBranches import fastMTTBranches
#from addingNewObservableBranches.genMeasurementRadionBranches import genMeasurementRadionBranches
from sortingTausCamilla import mergeTauCamilla
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

class ChannelCamilla(Module):
	def __init__(self,filename):
		print ("Running the channel sorter Module")
		print ("processing file ",filename)
		#self.channel = channel # Specify the channel
		self.filename = filename #filename passed cause we needed to count the events with zero divide errors
		#All these objects are common to all channels	
		self.boostedTau = BoostedTau("boostedTau")
		self.Tau = Tau("Tau")
		self.FatJet = FatJet("FatJet")
		self.Electron = Electron("Electron")    
		self.Muon = Muon("Muon")
		self.Jet = particle("Jet")
	
	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.countBadevents = 0 #This is to keep track of bad events per file
		self.out = wrappedOutputTree
		#self.input = inputTree
		self.Tau.setUpBranches(self.out) #creating the new branches     
		self.FatJet.setUpBranches(self.out)
		self.boostedTau.setUpBranches(self.out)
		self.Electron.setUpBranches(self.out)
		self.Muon.setUpBranches(self.out)
		self.out.branch("channel","I") # adding a new branch for channel 0-Di tau, 1- E-tau, 2- M-Tau
	
	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		print ("Number of Bad Events ", self.countBadevents)
		if self.countBadevents!=0:
			save_path = MYDIR=os.getcwd() + "/badEvents"
			file_name = "badEvents_"+str(self.filename)+"_"+str(self.channel)
			complete_Name =  os. path. join(save_path, file_name)
			file = open(complete_Name,"w")
			file.write("The Bad events for this file "+str(self.filename)+" is "+str(self.countBadevents))
			file.close()	
	

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
	
	def JetFatJetIsolation(self,CollectionObject):
		isObj =""
		Jet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		bigJet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		Jet.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)
		for fatjet in self.FatJet.collection:
			bigJet.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
			deltaR = Jet.DeltaR(bigJet)
			if deltaR <= 1.2:
				isObj = "bad"
				break
		
		if isObj != "bad":
			return True
		else:
			return False

	def FatJetTauOverlap(self,CollectionObject):
		isObj =""
		bigJet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)
		for fatjet in self.FatJet.collection:
			bigJet.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
			deltaR = tau.DeltaR(bigJet)
			if deltaR <= 1.5:
				isObj = "bad"
			break
		
		if isObj != "bad":
			return True
		else:
			return False

		
	
	def ElectronTauOverlap(self,CollectionObject):
		isObj =""
		tau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		lepton = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)
		for electron in self.Electron.collection:
			lepton.SetPtEtaPhiM(electron.pt,electron.eta,electron.phi,electron.mass)
			deltaR = tau.DeltaR(lepton)
			if deltaR <= 0.05:
				isObj = "bad"
				break
		
		if isObj != "bad":
			return True
		else:
			return False
	
	def MuonTauOverlap(self,CollectionObject):
		isObj =""
		tau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		lepton = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)
		for muon in self.Muon.collection:
			lepton.SetPtEtaPhiM(muon.pt,muon.eta,muon.phi,muon.mass)
			deltaR = tau.DeltaR(lepton)
			if deltaR <= 0.05:
				isObj = "bad"
				break
		
		if isObj != "bad":
			return True
		else:
			return False
		

	def selfPairing(self,col1):
		combinedPt = -10
		index1 =-1
		index2 = -1
		if len(col1)<=1:
			return (combinedPt,index1,index2)
		for i in range(len(col1)):
			for j in range(i+1,len(col1)):
				sumFourVector = col1[i].p4() + col1[j].p4()
				pt = sumFourVector.Pt()
				if pt >= combinedPt:
					combinedPt = pt
					index1 = i
					index2 = j
		
		return (combinedPt,index1,index2)
	
	def crossPairing(self,col1,col2):
		combinedPt = -10
		index1 =-1
		index2 = -1
		if (len(col1)==0 or len(col2)==0):
			return (combinedPt,index1,index2)
		for i in range(len(col1)):
			for j in range(len(col2)):
				sumFourVector = col1[i].p4() + col2[j].p4()
				pt = sumFourVector.Pt()
				if pt >= combinedPt:
					combinedPt = pt
					index1 = i
					index2 = j
		
		return (combinedPt,index1,index2)

	def applyElectronIsolation (self,electronCollectionObject): #passing the inidivial eletrons from the collection to apply the correction
		#print ("Electron Isoaltion computation")
		isTau = ""
		#Define the Four vectors for Delta R calculation
		Ele = ROOT.TLorentzVector(0.0,0.0,0.0,0.0) 
		boostedtau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		Ele.SetPtEtaPhiM(electronCollectionObject.pt,electronCollectionObject.eta,electronCollectionObject.phi,electronCollectionObject.mass)
		for btau in self.boostedTau.collection:
			boostedtau.SetPtEtaPhiM(btau.pt,btau.eta,btau.phi,btau.mass)
			deltaR = boostedtau.DeltaR(Ele)
			if deltaR <= 0.4:
				isTau = "close"
				break
		
		if isTau == "close":
			if abs(electronCollectionObject.eta) <= 1.479:
				if ((electronCollectionObject.TauCorrPfIso/electronCollectionObject.pt) < 0.175):
					return True
				else:
					return False
			elif ((abs(electronCollectionObject.eta) > 1.479) and (abs(electronCollectionObject.eta) <= 2.5)):
				if ((electronCollectionObject.TauCorrPfIso/electronCollectionObject.pt) < 0.159):
					return True
				else:
					return False
			else:
				return False
		
		if isTau =="":
			if (abs(electronCollectionObject.eta) <= 1.479):
				if ((electronCollectionObject.pfRelIso03_all) < 0.175):
					return True
				else:
					return False
			elif ((abs(electronCollectionObject.eta) > 1.479) and (abs(electronCollectionObject.eta) <= 2.5)):
				if ((electronCollectionObject.pfRelIso03_all) < 0.159):
					return True
				else:
					return False
			else:
				return False


	def applyMuonIsolation (self,MuonCollectionObject):
		#print ("Muon Isoaltion computation")
		isTau = ""
		Muo = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		boostedtau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		Muo.SetPtEtaPhiM(MuonCollectionObject.pt,MuonCollectionObject.eta,MuonCollectionObject.phi,MuonCollectionObject.mass)
		for btau in self.boostedTau.collection:
			boostedtau.SetPtEtaPhiM(btau.pt,btau.eta,btau.phi,btau.mass)
			deltaR = boostedtau.DeltaR(Muo)
			if deltaR <= 0.4:
				isTau = "close"
				break
		
		if isTau == "close":
			if ((MuonCollectionObject.TauCorrPfIso/MuonCollectionObject.pt) < 0.25):
				return True
			else:
				return False
		
		if isTau =="":
			if ((MuonCollectionObject.pfRelIso03_all) < 0.25):
				return True
			else:
				return False


	def analyze(self, event): 
		list = {} # to store the combined pt and the indices of the pairs


		#Select the AK4 Jets and keep choose Jets with Tight DeepJet ID
		self.Jet.setupCollection(event)
		self.Jet.apply_cut(lambda x: (x.pt > 20) and (x.btagDeepB >= 0.8767))
		
		self.Tau.setupCollection(event)
		self.Tau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idDeepTau2017v2p1VSjet & 1 == 1))  #Deeptau ID for the standard Taus loosest WP
		


		self.boostedTau.setupCollection(event)
		self.boostedTau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 2 == 2)) # VLoose ID for newMVA for boosted Taus - but use oldMVA weight

		self.Tau.collection =  filter(self.HPStauVeto,self.Tau.collection) #HPS veto applied

		self.FatJet.setupCollection(event)
		try:
			#self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250) and ((x.tau2/x.tau1) < 0.75))
			self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250) and x.jetId>=2 and ((x.tau2/x.tau1) < 0.75))	
		except ZeroDivisionError:
			self.countBadevents += 1
			print("Error:(")
			traceback.print_exc()
			return False

		self.Electron.setupCollection(event)
		self.Electron.apply_cut(lambda x: x.mvaFall17V2Iso_WPL and (x.pt > 10))
		#self.Electron.collection = filter(self.Electron.relativeIso,self.Electron.collection)

		self.Muon.setupCollection(event)
		#self.Muon.apply_cut(lambda x: x.pt > 10 and x.mvaId >= 1 and ((x.TauCorrPfIso/x.pt) < 0.25))
		self.Muon.apply_cut(lambda x: x.pt > 10 and x.mvaId >= 1)
		#self.Muon.apply_cut(lambda x: x.pt > 10 and x.mvaId >= 1 and ((x.pfRelIso03_all/x.pt) < 0.25))

		#filter Objects to remove those within the fatjet cone
		self.Electron.collection = filter(self.FatJetConeIsolation,self.Electron.collection)
		self.Muon.collection = filter(self.FatJetConeIsolation,self.Muon.collection)

		#Tau and FatJet should be more than 1.5 distance apart
		self.Tau.collection = filter(self.FatJetTauOverlap,self.Tau.collection)
		self.boostedTau.collection = filter(self.FatJetTauOverlap,self.boostedTau.collection)
	
		#filter the AK4 Jet collection for FatJet and Ak4 Jet overlap, 1.2 distance apart
		self.Jet.collection = filter(self.JetFatJetIsolation,self.Jet.collection)

		#remove light lepton and tau overlap dist 0.05
		self.Tau.collection = filter(self.ElectronTauOverlap,self.Tau.collection)
		self.Tau.collection = filter(self.MuonTauOverlap,self.Tau.collection)

		self.boostedTau.collection = filter(self.ElectronTauOverlap,self.boostedTau.collection)
		self.boostedTau.collection = filter(self.MuonTauOverlap,self.boostedTau.collection)

		# With the collection veto applied, now apply the lepton isolation

		self.Electron.collection = filter(self.applyElectronIsolation, self.Electron.collection)
		self.Muon.collection = filter(self.applyMuonIsolation,self.Muon.collection)



		#print ("before channel","boostedTauLength = ",len(self.boostedTau.collection),"Tau length = ",len(self.Tau.collection))

		#if (len(self.FatJet.collection)==1 and len(self.Jet.collection)==0):
		if (len(self.FatJet.collection)==1):
			list["bb"]=self.selfPairing(self.boostedTau.collection)
			list["tt"]=self.selfPairing(self.Tau.collection)
			list["bt"]=self.crossPairing(self.boostedTau.collection,self.Tau.collection)
			list["be"]=self.crossPairing(self.boostedTau.collection,self.Electron.collection)
			list["bm"]=self.crossPairing(self.boostedTau.collection,self.Muon.collection)
			list["te"]=self.crossPairing(self.Tau.collection,self.Electron.collection)
			list["tm"]=self.crossPairing(self.Tau.collection,self.Muon.collection)

			#print (list)

			Keymax = max(list, key = lambda x: list[x][0])
			

			if (list[Keymax][0]>0):
				#print(Keymax)
				if Keymax == "bb":
					self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1] or self.boostedTau.collection.index(obj)==list[Keymax][2]]
					#self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==-1 or self.Tau.collection.index(obj)==-1]
					self.Tau.collection=[]
					self.Muon.collection=[]
					self.Electron.collection=[]
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1 or self.Electron.collection.index(obj)==-1]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1 or self.Muon.collection.index(obj)==-1]
					self.out.fillBranch("channel",0)
				elif Keymax == "bt":
					self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1]]
					self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][2]]
					self.Muon.collection = []
					self.Electron.collection = []
					#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
					self.out.fillBranch("channel",0)					

				elif Keymax == "tt":
					#self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==-1]
					self.boostedTau.collection = []
					self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][1] or self.Tau.collection.index(obj)==list[Keymax][2]]
					self.Electron.collection = []
					self.Muon.collection = []
					#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
					self.out.fillBranch("channel",0)

				elif Keymax == "te":
					#self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==-1]
					self.boostedTau.collection = []
					self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][1]]
					self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==list[Keymax][2]]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
					#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
					self.Muon.collection = []
					self.out.fillBranch("channel",1)
				
				elif Keymax == "be":
					self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1]]
					#self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==-1]
					self.Tau.collection = []
					self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==list[Keymax][2]]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
					self.Muon.collection = []
					self.out.fillBranch("channel",1)

				elif Keymax == "tm":
					#self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==-1]
					self.boostedTau.collection = []
					self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][1]]
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
					self.Electron.collection = []
					#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
					self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==list[Keymax][2]]
					self.out.fillBranch("channel",2)

				elif Keymax == "bm":
					self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1]]
					#self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==-1]
					self.Tau.collection = []
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
					self.Electron.collection = []
					self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==list[Keymax][2]]
					self.out.fillBranch("channel",2)
				else:
					print ("This also happens")
				
				self.Tau.fillBranches(self.out)
				self.FatJet.fillBranches(self.out)
				self.boostedTau.fillBranches(self.out)
				self.Muon.fillBranches(self.out)
				self.Electron.fillBranches(self.out)
				
				
				return True

			else:
				return False	
				
		else:
			return False	
			


def call_postpoc(files):
		letsSortChannels = lambda: ChannelCamilla(filename)
		tauOdering = lambda: mergeTauCamilla(filename)
		visibleM = lambda:VisibleMassCamilla()
		mttBranches = lambda:fastMTTBranches(filename)
		#radBranches = lambda:genMeasurementRadionBranches(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		if filename == "Data":
			p = PostProcessor(outputDir,[files], cut=cutsData,branchsel=outputbranches,modules=[letsSortChannels(),tauOdering(),visibleM(),mttBranches()], postfix=post,noOut=False,outputbranchsel=outputbranches)
		else:
			p = PostProcessor(outputDir,[files], cut=cuts,branchsel=outputbranches,modules=[letsSortChannels(),tauOdering(),visibleM(),mttBranches()], postfix=post,noOut=False,outputbranchsel=outputbranches)


		p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	parser.add_argument('--postfix',help="string at the end of output file names", default="")
	args = parser.parse_args()

	#Define Event Selection - all those to be connected by and
	eventSelectionAND = ["MET_pt>200",
						"genWeight>0",
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
	
	eventSelectionANDData = ["MET_pt>200",
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

	eventSelectionOR = [#"HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            			"HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            			"HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            			"HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
            			"HLT_PFMET110_PFMHT110_IDTight",
            			"HLT_PFMET120_PFMHT120_IDTight",
            			#"HLT_PFMET170_NoiseCleaned",
            			"HLT_PFMET170_HBHECleaned",
            			"HLT_PFMET170_HBHE_BeamHaloCleaned"]
	


	#fnames = ["/data/aloeliger/bbtautauAnalysis/2016/Data.root"]
	fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
	#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel".format(args.Channel)
	outputDir = args.outputLocation
	#outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cut1 = "&&".join(eventSelectionAND)
	cut2 = "||".join(eventSelectionOR)
	cut3 = "&&".join(eventSelectionANDData)
	cuts = "("+cut1+")"+"&&"+"("+cut2+")"
	cutsData = "("+cut3+")"+"&&"+"("+cut2+")"
	print ("cuts = ",cuts)
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
