# I will use this script to see if current selections or Isolations applied at a base level in 
# NanoAOD affect significance - Because the efficiency of Signal may be increasing but then we select more background


import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
parser.add_argument('--inputFile1',help="Path to the directory that contains the signal files for all the cuts applied - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
parser.add_argument('--inputFile2',help="Path to the directory that contains the signal files without Lepton Isolation - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
parser.add_argument('--inputFile3',help="Path to the directory that contains the signal files without Lepton and Tau Isolation - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
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

totalbackground = 0
for file in  glob.glob(args.inputFile1+ "/Background/*.root"):
    rootfile = ROOT.TFile(file)
    #initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    totalbackground = totalbackground + tree_rootfile.GetEntries()

for index, file in enumerate(listOfSignalFilesProcessing):
    #nameStrip = file.strip()
    #filename = (nameStrip.split('/')[-1]).split('.')[-2]
    rootfile = ROOT.TFile(args.inputFile1+"/Signal/"+file+".root")
    #initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    finalEvents = tree_rootfile.GetEntries()
    #print (float(float(finalEvents)/float(totalbackground)), finalEvents)
    masspointEff.SetBinContent(index+1,float(float(finalEvents)/float(totalbackground)))


totalbackground = 0
for file in glob.glob(args.inputFile2+ "/Background/*.root"):
    rootfile = ROOT.TFile(file)
    #initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    totalbackground = totalbackground + tree_rootfile.GetEntries()

#print (totalbackground)


for index, file in enumerate(listOfSignalFilesProcessing):
    #nameStrip = file.strip()
    #filename = (nameStrip.split('/')[-1]).split('.')[-2]
    rootfile = ROOT.TFile(args.inputFile2+"/Signal/"+file+".root")
    #initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    finalEvents = tree_rootfile.GetEntries()
    masspointEff_without_Lep_Iso.SetBinContent(index+1,float(float(finalEvents)/float(totalbackground)))

totalbackground = 0
for file in glob.glob(args.inputFile3+ "/Background/*.root"):
    rootfile = ROOT.TFile(file)
    initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    totalbackground = totalbackground + tree_rootfile.GetEntries()

for index, file in enumerate(listOfSignalFilesProcessing):
    #nameStrip = file.strip()
    #filename = (nameStrip.split('/')[-1]).split('.')[-2]
    rootfile = ROOT.TFile(args.inputFile3+"/Signal/"+file+".root")
    #initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    finalEvents = tree_rootfile.GetEntries()
    masspointEff_without_Lep_Tau_Iso.SetBinContent(index+1,float(float(finalEvents)/float(totalbackground)))


masspointEff.SetMarkerColor(4)
masspointEff.SetMarkerStyle(34)
masspointEff.SetMarkerSize(1.5)
masspointEff.GetXaxis().SetTitle("Mass Point")
masspointEff.GetYaxis().SetTitle("S/B")
#masspointEff.GetYaxis().SetRangeUser(0.0,0.04)

masspointEff_without_Lep_Iso.SetMarkerColor(2)
masspointEff_without_Lep_Iso.SetMarkerStyle(21)
masspointEff_without_Lep_Iso.SetMarkerSize(1.5)
masspointEff_without_Lep_Iso.GetXaxis().SetTitle("Mass Point")
masspointEff_without_Lep_Iso.GetYaxis().SetTitle("S/B")
#masspointEff_without_Lep_Iso.GetYaxis().SetRangeUser(0.0,0.2)

masspointEff_without_Lep_Tau_Iso.SetMarkerColor(3)
masspointEff_without_Lep_Tau_Iso.SetMarkerStyle(22)
masspointEff_without_Lep_Tau_Iso.SetMarkerSize(1.5)
masspointEff_without_Lep_Tau_Iso.GetXaxis().SetTitle("Mass Point")
masspointEff_without_Lep_Tau_Iso.GetYaxis().SetTitle("S/B")
#masspointEff_without_Lep_Tau_Iso.GetYaxis().SetRangeUser(0.0,0.2)

legend = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(masspointEff,"All Cuts applied","ep")
legend.AddEntry(masspointEff_without_Lep_Iso,"All except Lep Isolation","ep")
legend.AddEntry(masspointEff_without_Lep_Tau_Iso,"All except Lep, Tau Isolation","ep")

can2 = ROOT.TCanvas("canvas2", "efficiency")
can2.SetGrid()
can2.SetLogy()
masspointEff.Draw("P")
masspointEff_without_Lep_Iso.Draw("same P")
masspointEff_without_Lep_Tau_Iso.Draw("same P")
legend.Draw("same")
can2.SaveAs("SignalOverBackground.pdf")



    

    

