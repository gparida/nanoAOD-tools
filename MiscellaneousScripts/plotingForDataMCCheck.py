import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from plotSettings import *


fnamesWJetsNew = glob.glob("/data/gparida/Background_Samples/bbtautauAnalysis/2016/ChannelFiles_Camilla_28Jan_2022/WJets*.root")

WNewHist = None

for file in fnamesWJetsNew:
    theFile = ROOT.TFile(file) #opening the root file
    theTree = theFile.Get("Events")
    nEntries = theTree.GetEntries()

    Wtemp = setUpHistrogram(Name="Wtemp",LineColor=1,LineWidth=2,XTitle="LHE_HT",YTitle="Events",ttree=theTree,branch="LHE_HT",Nbins=300,min=0,max=3000,cond="FinalWeighting")
    
    if WNewHist == None:
        WNewHist = Wtemp
    else:
        WNewHist.Add(Wtemp)



fnamesWJetsOld = glob.glob("/data/gparida/Background_Samples/bbtautauAnalysis/2016/ChannelFiles_Camilla/W.root")

WOldHist = None

for file in fnamesWJetsOld:
    theFile = ROOT.TFile(file) #opening the root file
    theTree = theFile.Get("Events")
    nEntries = theTree.GetEntries()

    Wtemp = setUpHistrogram(Name="Wtemp",LineColor=1,LineWidth=2,XTitle="LHE_HT",YTitle="Events",ttree=theTree,branch="LHE_HT",Nbins=300,min=0,max=3000,cond="FinalWeighting")
    
    if WOldHist == None:
        WOldHist = Wtemp
    else:
        WOldHist.Add(Wtemp)



HT_Check = setUpCanvas("HT_Check")
WNewHist.SetMaximum(max(WNewHist.GetMaximum(),WOldHist.GetMaximum())+50)
WNewHist.Draw("Hist")
WOldHist.Draw("Hist same")




legend = setUpLegend()
legend.AddEntry(WOldHist,"Old Files","ep")
legend.AddEntry(WNewHist,"New Files","ep")

legend.Draw("same")


cmsLatex = setUpCmsLatex(2016)
HT_Check.SaveAs("HT_Check.pdf")