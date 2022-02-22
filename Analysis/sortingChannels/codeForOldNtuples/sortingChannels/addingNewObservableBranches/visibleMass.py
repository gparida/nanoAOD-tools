from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
import argparse
import multiprocessing as  np


ROOT.PyConfig.IgnoreCommandLineOptions = True

class VisibleMass(Module):
    def __init__(self, channel):
       print ("Running the Visible Mass and Delta R branches")
       self.channel = channel # Specify the channel


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("gMVis_LL", "F")
        self.out.branch("gDeltaR_LL","F")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self,event):
       gTau = Collection(event, "gTau","gnTau")
       gboostedTau = Collection(event,"gboostedTau","gnboostedTau")
       gElectron = Collection(event,"gElectron","gnElectron")
       gMuon = Collection(event,"gMuon","gnMuon")

       lepton1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
       lepton2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)

       if self.channel == "tt":
            if (len(gTau)==2):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gTau[1].pt,gTau[1].eta,gTau[1].phi,gTau[1].mass)
            if (len(gboostedTau)==2):
                lepton1.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
                lepton2.SetPtEtaPhiM(gboostedTau[1].pt,gboostedTau[1].eta,gboostedTau[1].phi,gboostedTau[1].mass)
            if (len(gTau)==1 and len(gboostedTau)==1):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
            self.out.fillBranch("gMVis_LL",abs((lepton1 + lepton2).M()))
            self.out.fillBranch("gDeltaR_LL",lepton1.DeltaR(lepton2))
    
       if self.channel == "et":
            if (len(gTau)!=0):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gElectron[0].pt,gElectron[0].eta,gElectron[0].phi,gElectron[0].mass)
            
            if (len(gboostedTau)!=0):
                 lepton1.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
                 lepton2.SetPtEtaPhiM(gElectron[0].pt,gElectron[0].eta,gElectron[0].phi,gElectron[0].mass)
            self.out.fillBranch("gMVis_LL",abs((lepton1 + lepton2).M()))
            self.out.fillBranch("gDeltaR_LL",lepton1.DeltaR(lepton2))

       if self.channel == "mt":
            if (len(gTau)!=0):
                lepton1.SetPtEtaPhiM(gTau[0].pt,gTau[0].eta,gTau[0].phi,gTau[0].mass)
                lepton2.SetPtEtaPhiM(gMuon[0].pt,gMuon[0].eta,gMuon[0].phi,gMuon[0].mass)
            if (len(gboostedTau)!=0):
                lepton1.SetPtEtaPhiM(gboostedTau[0].pt,gboostedTau[0].eta,gboostedTau[0].phi,gboostedTau[0].mass)
                lepton2.SetPtEtaPhiM(gMuon[0].pt,gMuon[0].eta,gMuon[0].phi,gMuon[0].mass)
            self.out.fillBranch("gMVis_LL",abs((lepton1 + lepton2).M()))
            self.out.fillBranch("gDeltaR_LL",lepton1.DeltaR(lepton2)) 
       
       return True     


          
               
          
        
