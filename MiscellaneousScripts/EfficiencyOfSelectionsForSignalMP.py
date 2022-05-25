# I will use this script to see if current selections or Isolations applied at a base level in 
# NanoAOD affect the efficiency of my signal when we move to higher and higher mass points


import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
parser.add_argument('--inputFile1',help="Path to the directory that contains the signal files for all the cuts applied")
parser.add_argument('--inputFile2',help="Path to the directory that contains the signal files without Lepton Isolation")
parser.add_argument('--inputFile3',help="Path to the directory that contains the signal files without Lepton and Tau Isolation")
args = parser.parse_args()


masspointEff = ROOT.TH1F("MassPoints","MassPoints",6,0,6)
masspointEff.GetXaxis().SetBinLabel(1,"1TeV")
masspointEff.GetXaxis().SetBinLabel(2,"2TeV")
masspointEff.GetXaxis().SetBinLabel(3,"2.5TeV")
masspointEff.GetXaxis().SetBinLabel(4,"3TeV")
masspointEff.GetXaxis().SetBinLabel(5,"3.5TeV")
masspointEff.GetXaxis().SetBinLabel(6,"4TeV")

masspointEff_without_Lep_Iso = ROOT.TH1F("MassPoints","MassPoints",6,0,6)
masspointEff_without_Lep_Iso.GetXaxis().SetBinLabel(1,"1TeV")
masspointEff_without_Lep_Iso.GetXaxis().SetBinLabel(2,"2TeV")
masspointEff_without_Lep_Iso.GetXaxis().SetBinLabel(3,"2.5TeV")
masspointEff_without_Lep_Iso.GetXaxis().SetBinLabel(4,"3TeV")
masspointEff_without_Lep_Iso.GetXaxis().SetBinLabel(5,"3.5TeV")
masspointEff_without_Lep_Iso.GetXaxis().SetBinLabel(6,"4TeV")

masspointEff_without_Lep_Tau_Iso = ROOT.TH1F("MassPoints","MassPoints",6,0,6)
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetBinLabel(1,"1TeV")
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetBinLabel(2,"2TeV")
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetBinLabel(3,"2.5TeV")
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetBinLabel(4,"3TeV")
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetBinLabel(5,"3.5TeV")
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetBinLabel(6,"4TeV")

#fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
listOfSignalFilesProcessing = ["RadionTohhtohtatahbb_M-1000","Radiontohhtohtatahbb_M-2000","Radiontohhtohtatahbb_M-2500","Radiontohhtohtatahbb_M-3000","Radiontohhtohtatahbb_M-3500","Radiontohhtohtatahbb_M-4000"]

for index, file in enumerate(listOfSignalFilesProcessing):
    #nameStrip = file.strip()
    #filename = (nameStrip.split('/')[-1]).split('.')[-2]
    rootfile = ROOT.TFile(args.inputFile1+"/"+file+".root")
    initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    finalEvents = tree_rootfile.GetEntries()
    masspointEff.SetBinContent(index+1,finalEvents/initialEvents)

for index, file in enumerate(listOfSignalFilesProcessing):
    #nameStrip = file.strip()
    #filename = (nameStrip.split('/')[-1]).split('.')[-2]
    rootfile = ROOT.TFile(args.inputFile2+"/"+file+".root")
    initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    finalEvents = tree_rootfile.GetEntries()
    masspointEff_without_Lep_Iso.SetBinContent(index+1,finalEvents/initialEvents)

for index, file in enumerate(listOfSignalFilesProcessing):
    #nameStrip = file.strip()
    #filename = (nameStrip.split('/')[-1]).split('.')[-2]
    rootfile = ROOT.TFile(args.inputFile3+"/"+file+".root")
    initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    finalEvents = tree_rootfile.GetEntries()
    masspointEff_without_Lep_Tau_Iso.SetBinContent(index+1,finalEvents/initialEvents)


masspointEff.SetMarkerColor(4)
masspointEff.SetMarkerStyle(34)
masspointEff.SetMarkerSize(1.5)
masspointEff.GetXaxis().SetTitle("Mass Point")
masspointEff.GetYaxis().SetTitle("Efficiency")
masspointEff.GetYaxis().SetRangeUser(0.0,0.15)

masspointEff_without_Lep_Iso.SetMarkerColor(2)
masspointEff_without_Lep_Iso.SetMarkerStyle(21)
masspointEff_without_Lep_Iso.SetMarkerSize(1.5)
masspointEff_without_Lep_Iso.GetXaxis().SetTitle("Mass Point")
masspointEff_without_Lep_Iso.GetYaxis().SetTitle("Efficiency")
masspointEff_without_Lep_Iso.GetYaxis().SetRangeUser(0.0,0.2)

masspointEff_without_Lep_Tau_Iso.SetMarkerColor(3)
masspointEff_without_Lep_Tau_Iso.SetMarkerStyle(22)
masspointEff_without_Lep_Tau_Iso.SetMarkerSize(1.5)
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetTitle("Mass Point")
masspointEff_without_Lep_Tau_Iso.GetYaxis().SetTitle("Efficiency")
masspointEff_without_Lep_Tau_Iso.GetYaxis().SetRangeUser(0.0,0.2)

legend = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(masspointEff,"All Cuts applied","ep")
legend.AddEntry(masspointEff_without_Lep_Iso,"All except Lep Isolation","ep")
legend.AddEntry(masspointEff_without_Lep_Tau_Iso,"All except Lep, Tau Isolation","ep")

can2 = ROOT.TCanvas("canvas2", "efficiency")
can2.SetGrid()
masspointEff.Draw("P")
masspointEff_without_Lep_Iso.Draw("same P")
masspointEff_without_Lep_Tau_Iso.Draw("same P")
legend.Draw("same")
can2.SaveAs("Signal_Efficiency.pdf")



    

    

