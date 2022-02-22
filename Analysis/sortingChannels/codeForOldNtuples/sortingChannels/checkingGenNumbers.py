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

class Channel(Module):
    def __init__(self,filename):
        self.writeHistFile=True
        self.filename = filename #filename passed cause we needed to count the events with zero divide errors	
        self.GenPart = particle("GenPart")
    
    def beginJob(self, histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
		#Now lets define the cutflow histograms
		#Starting to Di Tau channel selections
        self.cutflow_diTau =  ROOT.TH1F('cutflow_diTau', 'cutflow_diTau', 4, 0, 4)
        self.cutflow_diTau.GetXaxis().SetBinLabel(1,"Events_Preselected")
        self.cutflow_diTau.GetXaxis().SetBinLabel(2,"Two Higgs")
        self.cutflow_diTau.GetXaxis().SetBinLabel(3,"2b2t")
        self.cutflow_diTau.GetXaxis().SetBinLabel(4,"diTau")
        self.cutflow_diTau.GetXaxis().SetTitle("Selections")
        self.cutflow_diTau.GetYaxis().SetTitle("Events")
        self.cutflow_diTau.SetFillColor(38)

        self.cutflow_et =  ROOT.TH1F('cutflow_et', 'cutflow_et', 4, 0, 4)
        self.cutflow_et.GetXaxis().SetBinLabel(1,"Events_Preselected")
        self.cutflow_et.GetXaxis().SetBinLabel(2,"Two Higgs")
        self.cutflow_et.GetXaxis().SetBinLabel(3,"2b2t")
        self.cutflow_et.GetXaxis().SetBinLabel(4,"et")
        self.cutflow_et.GetXaxis().SetTitle("Selections")
        self.cutflow_et.GetYaxis().SetTitle("Events")
        self.cutflow_et.SetFillColor(38)


        self.cutflow_mt =  ROOT.TH1F('cutflow_mt', 'cutflow_mt', 4, 0, 4)
        self.cutflow_mt.GetXaxis().SetBinLabel(1,"Events_Preselected")
        self.cutflow_mt.GetXaxis().SetBinLabel(2,"Twi Higgs")
        self.cutflow_mt.GetXaxis().SetBinLabel(3,"2b2t")
        self.cutflow_mt.GetXaxis().SetBinLabel(4,"mt")
        self.cutflow_mt.GetXaxis().SetTitle("Selections")
        self.cutflow_mt.GetYaxis().SetTitle("Events")
        self.cutflow_mt.SetFillColor(38)
    
        self.cutflow_em =  ROOT.TH1F('cutflow_em', 'cutflow_em', 4, 0, 4)
        self.cutflow_em.GetXaxis().SetBinLabel(1,"Events_Preselected")
        self.cutflow_em.GetXaxis().SetBinLabel(2,"Twi Higgs")
        self.cutflow_em.GetXaxis().SetBinLabel(3,"2b2t")
        self.cutflow_em.GetXaxis().SetBinLabel(4,"em")
        self.cutflow_em.GetXaxis().SetTitle("Selections")
        self.cutflow_em.GetYaxis().SetTitle("Events")
        self.cutflow_em.SetFillColor(38)

        self.addObject(self.cutflow_diTau)
        self.addObject(self.cutflow_mt)
        self.addObject(self.cutflow_et)
        self.addObject(self.cutflow_em)


    def analyze(self, event): 
        #Filling pre selected events
        self.cutflow_diTau.AddBinContent(1)
        self.cutflow_et.AddBinContent(1)
        self.cutflow_mt.AddBinContent(1)
        self.cutflow_em.AddBinContent(1)

        hCount = 0
        tCount = 0
        haCount = 0
        #bCount=0
        eCount = 0
        muCount = 0
        tau_index =[]
        tau_charge =[]
        tau1_particlesID =[]
        tau2_particlesID =[]
        tau1=""
        tau2=""  
        


        self.GenPart.setupCollection(event)

        for obj in self.GenPart.collection:
            if obj.pdgId == 25:
                hCount += 1
        
        if hCount == 2:
            #Counting events with just 2 higgs. Should be equal to preselected events
            self.cutflow_diTau.AddBinContent(2)
            self.cutflow_et.AddBinContent(2)
            self.cutflow_mt.AddBinContent(2)
            self.cutflow_em.AddBinContent(2)
            for i in range(len(self.GenPart.collection)):
                if abs(self.GenPart.collection[i].pdgId) == 15 and self.GenPart.collection[i].statusFlags & 2 ==2 and self.GenPart.collection[i].genPartIdxMother >=0 :
                #if abs(self.GenPart.collection[i].pdgId) == 15 and self.GenPart.collection[i].genPartIdxMother >=0 :
                    if self.GenPart.collection[self.GenPart.collection[i].genPartIdxMother].pdgId == 25:
                        tCount += 1
                        tau_index.append(i) 
                        tau_charge.append(self.GenPart.collection[i].pdgId)        

                #if abs(self.GenPart.collection[i].pdgId) == 5 and self.GenPart.collection[i].genPartIdxMother >=0:
                    #if self.GenPart.collection[self.GenPart.collection[i].genPartIdxMother].pdgId == 25:
                        #bCount += 1

        if tCount == 2 and (tau_charge[0]*tau_charge[1])<0:
            self.cutflow_diTau.AddBinContent(3)
            self.cutflow_et.AddBinContent(3)
            self.cutflow_mt.AddBinContent(3)
            self.cutflow_em.AddBinContent(3)
            for i in range(len(self.GenPart.collection)):
                if self.GenPart.collection[i].genPartIdxMother == tau_index[0]:
                    tau1_particlesID.append(self.GenPart.collection[i].pdgId)
                
                elif self.GenPart.collection[i].genPartIdxMother == tau_index[1]:
                    tau2_particlesID.append(self.GenPart.collection[i].pdgId)


            for entry in tau1_particlesID:
                if abs(entry)>100:
                    haCount+=1
                if abs(entry)==11:
                    eCount+=1
                if abs(entry)==13:
                    muCount+=1

            if haCount!=0:
                tau1="t"
            elif eCount==1 and haCount == 0 and muCount==0:
                tau1="e"
            elif muCount==1 and eCount==0 and haCount==0:
                tau1="m" 
            else:
                print ("tau1 unassigned")
                print ("tau1 ","hadron Count = ",haCount," eCount = ",eCount," muCount = ",muCount,"pdg= ",tau1_particlesID)

            haCount=0
            eCount=0
            muCount=0

            for entry in tau2_particlesID:
                if abs(entry)>100:
                    haCount+=1
                if abs(entry)==11:
                    eCount+=1
                if abs(entry)==13:
                    muCount+=1
        
            if haCount!=0:
                tau2="t"
            elif eCount==1 and haCount == 0 and muCount==0:
                tau2="e"
            elif muCount==1 and eCount==0 and haCount==0:
                tau2="m" 
            else:
                print ("tau2 unassigned")
                print ("tau2","hadron Count = ",haCount," eCount = ",eCount," muCount = ",muCount,"pdg= ",tau2_particlesID)       
                    

            if ((tau1+tau2) =="tt"):
                self.cutflow_diTau.AddBinContent(4) 
            elif ((tau1+tau2) =="mt" or (tau1+tau2) =="tm"):
                self.cutflow_mt.AddBinContent(4)
            elif ((tau1+tau2) =="et" or (tau1+tau2) =="te"):
                self.cutflow_et.AddBinContent(4)
            elif ((tau1+tau2) =="ee" or (tau1+tau2) =="mm" or (tau1+tau2) =="em" or (tau1+tau2) =="me"):
                self.cutflow_em.AddBinContent(4)
            else:
                print ("gadbad")
    
        return True        


def call_postpoc(files):
		letsSortChannels = lambda: Channel(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=None,modules=[letsSortChannels()],noOut=True,outputbranchsel=outputbranches,histFileName="Gen_"+filename+".root",histDirName="Plots")
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

                













    

