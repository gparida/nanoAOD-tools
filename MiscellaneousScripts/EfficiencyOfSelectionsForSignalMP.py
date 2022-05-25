# I will use this script to see if current selections or Isolations applied at a base level in 
# NanoAOD affect the efficiency of my signal when we move to higher and higher mass points


import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
parser.add_argument('--inputFile',help="Path to the directory that contains the signal files")
args = parser.parse_args()


masspointEff = ROOT.TH1F("MassPoints","MassPoints",6,0,6)
masspointEff.GetXaxis().SetBinLabel(1,"1TeV")
masspointEff.GetXaxis().SetBinLabel(2,"2TeV")
masspointEff.GetXaxis().SetBinLabel(3,"2.5TeV")
masspointEff.GetXaxis().SetBinLabel(4,"3TeV")
masspointEff.GetXaxis().SetBinLabel(5,"3.5TeV")
masspointEff.GetXaxis().SetBinLabel(6,"4TeV")

#fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
listOfSignalFilesProcessing = ["RadionTohhtohtatahbb_M-1000","Radiontohhtohtatahbb_M-2000","Radiontohhtohtatahbb_M-2500","Radiontohhtohtatahbb_M-3000","Radiontohhtohtatahbb_M-3500","Radiontohhtohtatahbb_M-4000"]

for index, file in enumerate(listOfSignalFilesProcessing):
    #nameStrip = file.strip()
    #filename = (nameStrip.split('/')[-1]).split('.')[-2]
    rootfile = ROOT.TFile(args.inputFile+"/"+file+".root")
    initialEvents = rootfile.cutflow.GetBinContent(1)
    tree_rootfile = rootfile.Get('Events')
    finalEvents = tree_rootfile.GetEntries()
    masspointEff.SetBinContent(index+1,finalEvents/initialEvents)


masspointEff.SetMarkerColor(4)
masspointEff.SetMarkerStyle(34)
masspointEff.SetMarkerSize(1.5)
masspointEff.GetXaxis().SetTitle("Mass Point")
masspointEff.GetYaxis().SetTitle("Efficiency")
masspointEff.GetYaxis().SetRangeUser(0.0,1.5)



can2 = ROOT.TCanvas("canvas2", "efficiency")
can2.SetGrid()
masspointEff.Draw("ap")
can2.SaveAs("Signal_Efficiency.pdf")



    

    

