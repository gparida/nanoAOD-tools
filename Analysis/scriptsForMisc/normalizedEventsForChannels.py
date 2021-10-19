import ROOT
import math 
import time

samplesFiles = ['RadionHH_M4500_GenTT','RadionHH_M4500_GenMT','RadionHH_M4500_GenET','RadionHH_M4500_GenEM']

NormalizedEvents =  ROOT.TH1F('NormalizedEvents', 'NormalizedEvents', 4, 0, 4)
NormalizedEvents.GetXaxis().SetBinLabel(1,"DiTau")
NormalizedEvents.GetXaxis().SetBinLabel(2,"mt")
NormalizedEvents.GetXaxis().SetBinLabel(3,"et")
NormalizedEvents.GetXaxis().SetBinLabel(4,"em")

rootfile = ROOT.TFile("NormlaizedEvents.root", "RECREATE")
workdir = rootfile.mkdir("Plots")

for samples in range(len(samplesFiles)):
    file_bbtt = ROOT.TFile("/data/gparida/bbtautauAnalysis/2016/"+samplesFiles[samples]+".root")
    tree_bbtt = file_bbtt.Get('Events')
    nEntries = tree_bbtt.GetEntries()

    for x in range(nEntries):
        if (x%1000 == 0):
            print("events_processed=",x)
        
        tree_bbtt.GetEntry(x)
        NormalizedEvents.AddBinContent((samples+1),tree_bbtt.FinalWeighting)

workdir.WriteObject(NormalizedEvents,"Normalized Events")
