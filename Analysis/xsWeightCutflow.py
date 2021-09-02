#This script is designed to look at the cutflow diagram of the events in the background, since there are a huge discrepancy between MC and Data at the time.
#This scripts creates a root file as output that had the cutflow histograms for all the backgrounds mentioned in the list, there is a separate plotting here that will help plot a stacked background and data cutflow
from ROOT import *
import math 
import time



#Creating a list of triggers
trig_MET =["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_PFMET110_PFMHT110_IDTight",
            "HLT_PFMET120_PFMHT120_IDTight",
            #"HLT_PFMET170_NoiseCleaned",
            "HLT_PFMET170_HBHECleaned",
            "HLT_PFMET170_HBHE_BeamHaloCleaned"]

#Creating a dictionary for all the samples and the corresponding weights
DatasetNameXSWeightDictionary={
    "QCD_1000to1400":0.006405107,
    "QCD_120to170":230.3234918,
    "QCD_1400to1800":0.000997817,
    "QCD_15to30":1058937.981,
    "QCD_170to300":59.15251935,
    "QCD_1800to2400":0.00026933,
    "QCD_2400to3200":0.0000296633850303439,
    "QCD_300to470":2.00778766,
    "QCD_30to50":90647.48201,
    "QCD_3200toInf":0.00000227136,
    "QCD_470to600":0.178230811,
    "QCD_800to1000":0.011793967,
    "QCD_80to120":1323.643203,
    "QCD_50to80":13473.64119,
    "QCD_600to800":0.040118257,
    "ST_s-channel_4f":0.009501705,
    "TTTo2L2Nu":0.255495352,
    "TTToHadronic":0.102523092,
    "TTToSemiLeptonic":0.07267512,
    "W":10.63712415,
    "WW":0.088197968,
    "WZ":0.060063755,
    "ZZ":0.197924492,
    "DYlow":9.15316241,
    "DY":0.901934791,
    "Data":1,
    }

#Creating a list of datasets to be used in the code later
dataset = ["QCD_1000to1400",
		   "QCD_120to170",
		   "QCD_1400to1800",
		   "QCD_15to30",
		   "QCD_170to300",
		   "QCD_1800to2400",
		   "QCD_2400to3200",
		   "QCD_300to470",
		   "QCD_30to50",
		   "QCD_3200toInf",
		   "QCD_470to600",
		   "QCD_800to1000",
		   "QCD_80to120",
		   "QCD_50to80",
		   "QCD_600to800",
		   "ST_s-channel_4f",
		   "TTTo2L2Nu",
		   "TTToHadronic",
		   "TTToSemiLeptonic",
		   "W",
		   "WW",
		   "WZ",
		   "ZZ",
		   "DYlow",
		   "DY",
		   "Data"]



rootfile = TFile("xsWeightCutHist.root", "RECREATE")  # Opening the root file to write to it
workdir = rootfile.mkdir("September1check") #Creating a directory inside it 

for data in range(len(dataset)):  #loop through the names in the dataset
	file_bbtt = TFile("/data/aloeliger/bbtautauAnalysis/2016/"+dataset[data]+".root") #open those root files
	total_events = 0
    	total_events_Weighted = 0
    	total_events_METpt_Selection = 0
    	total_events_Trigger = 0

	print ("hello")
	tree_bbtt = file_bbtt.Get('Events') #In case of NanoAOD get hold of the event tree
	currentdir = file_bbtt.GetDirectory("") #poitns to current direcotry you are in

	#Defining the cutflow histogram
	cutflow1 = currentdir.Get("cutflow")
	cutflow2 = TH1F("cutflow_" + dataset[data],"cutflow_" + dataset[data],5,0,5);
	cutflow2.GetXaxis().SetBinLabel(1,"Before_Skim_Total")
	cutflow2.GetXaxis().SetBinLabel(2,"After_Skim_Total")
	cutflow2.GetXaxis().SetBinLabel(3,"Weight_Applied")
	cutflow2.GetXaxis().SetBinLabel(4,"METpt")
	cutflow2.GetXaxis().SetBinLabel(5,"MET_Triggers")
	#cutflow.GetXaxis().SetBinLabel(5,"DecayMode_ID")
	#cutflow.GetXaxis().SetBinLabel(6,"MVA_Tau_ID")
	#cutflow2.SetFillColor(38)
	cutflow2.SetStats(0)
	cutflow2.GetXaxis().SetTitle("Weights_and_Selections")
	cutflow2.GetYaxis().SetTitle("Events")
	total_events = tree_bbtt.GetEntries()

	#Using the condition itself in the GetEntries to get it more efficiently
	
	total_events_Weighted = DatasetNameXSWeightDictionary[dataset[data]]*total_events
	total_events_METpt_Selection = DatasetNameXSWeightDictionary[dataset[data]]*(tree_bbtt.GetEntries("MET_pt>200"))
	total_events_Trigger = DatasetNameXSWeightDictionary[dataset[data]]*(tree_bbtt.GetEntries("MET_pt >= 205 && (" + "||".join(trig_MET) + ")"))
	cutflow2.SetBinContent(1,0)
	cutflow2.SetBinContent(2,total_events)
	cutflow2.SetBinContent(3,total_events_Weighted)
	cutflow2.SetBinContent(4,total_events_METpt_Selection)
	cutflow2.SetBinContent(5,total_events_Trigger)

	workdir.WriteObject(cutflow2,dataset[data]) #Write the Histogram into the root file


#rootfile.close()









