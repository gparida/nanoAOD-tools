from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class mySkimAdd(Module):
	 def __init__(self):
        # add any arguments needed after the self and set them here
        pass

    def beginJob(self):
		pass

	def endJob(self):
    	pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    	self.out = wrappedOutputTree #--->Is this the name of output file
    	self.out.branch("MET_Trigger_pt","F");
        self.out.branch("MET_HT_Trigger_pt","F");
        self.out.branch("MET_Lepton_Trigger_pt","F");
        self.out.branch("MET_HT_Lepton_Trigger_pt","F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):

		if((event.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight
			or event.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight 
			or event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_PFMET110_PFMHT110_IDTight 
			or event.HLT_PFMET120_PFMHT120_IDTight 
			or event.HLT_PFMET170_NoiseCleaned
			or event.HLT_PFMET170_HBHECleaned 
			or event.HLT_PFMET170_HBHE_BeamHaloCleaned) and event.MET_pt >= 205): 

			self.out.fillBranch("MET_Trigger_pt",event.MET_pt)


		if((event.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight 
			or event.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight 
			or event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_PFMET110_PFMHT110_IDTight
			or event.HLT_PFMET120_PFMHT120_IDTight 
			or event.HLT_PFMET170_NoiseCleaned
			or event.HLT_PFMET170_HBHECleaned 
			or event.HLT_PFMET170_HBHE_BeamHaloCleaned 
			or event.HLT_AK8PFJet360_TrimMass30 or event.HLT_PFHT300_PFMET110) and event.MET_pt >= 205) :

			self.out.fillBranch("MET_HT_Trigger_pt",event.MET_pt)

		if((event.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight 
			or event.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight 
			or event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_PFMET110_PFMHT110_IDTight
			or event.HLT_PFMET120_PFMHT120_IDTight 
			or event.HLT_PFMET170_NoiseCleaned
			or event.HLT_PFMET170_HBHECleaned 
			or event.HLT_PFMET170_HBHE_BeamHaloCleaned
			or event.HLT_IsoMu22 
			or event.HLT_IsoMu22_eta2p1 
			or event.HLT_IsoTkMu22  
			or event.HLT_IsoTkMu22_eta2p1 
			or event.HLT_IsoMu19_eta2p1_LooseIsoPFTau20 
			or event.HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1
			or event.HLT_Ele25_eta2p1_WPTight_Gsf 
			or event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg 
			or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg 
			or event.HLT_Mu50 
			or event.HLT_IsoMu24 
			or event.HLT_Ele32_eta2p1_WPTight_Gsf 
			or event.HLT_Ele115_CaloIdVT_GsfTrkIdT) and event.MET_pt >= 205) :
			
			self.out.fillBranch("MET_Lepton_Trigger_pt",event.MET_pt)

		if((event.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight 
			or event.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight 
			or event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight 
			or event.HLT_PFMET110_PFMHT110_IDTight 
			or event.HLT_PFMET120_PFMHT120_IDTight 
			or event.HLT_PFMET170_NoiseCleaned 
			or event.HLT_PFMET170_HBHECleaned 
			or event.HLT_PFMET170_HBHE_BeamHaloCleaned
			or event.HLT_AK8PFJet360_TrimMass30 
			or event.HLT_PFHT300_PFMET110  
			or event.HLT_IsoMu22  
			or event.HLT_IsoMu22_eta2p1 
			or event.HLT_IsoTkMu22 
			or event.HLT_IsoTkMu22_eta2p1 
			or event.HLT_IsoMu19_eta2p1_LooseIsoPFTau20 
			or event.HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1 
			or event.HLT_Ele25_eta2p1_WPTight_Gsf 
			or event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg 
			or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg  
			or event.HLT_Mu50 
			or event.HLT_IsoMu24 
			or event.HLT_Ele32_eta2p1_WPTight_Gsf  
			or event.HLT_Ele115_CaloIdVT_GsfTrkIdT) and event.MET_pt >= 205):

			self.out.fillBranch("MET_HT_Lepton_Trigger_pt",event.MET_pt)


		return True


mySkimAdd = lambda: mySkimAdd()








