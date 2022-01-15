import ROOT
import glob
import argparse


#Now we need to take inputs
parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
parser.add_argument('--inputFile',help="Full path to the signal file including the name")
parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
parser.add_argument('--postfix',help="string at the end of output file names", default="")
args = parser.parse_args()

#open the file
theFile = ROOT.TFile("args.inputFile") #opening the root file
 

 #Grab the Event tree as this is a nanoAOD file

theTree = theFile.Get("Events")
nEntries = theTree.GetEntries()

#Now we Just directly plot the branches in the ttree

#First doing it for Higgs..................................

#Higgs mass
theTree.Draw("ResoGenHiggs_mass>>HiggsMassResoMTT(40,0,2)")
HiggsMassResoMTT = ROOT.gDirectory.Get("HiggsMassResoMTT").Clone()
HiggsMassResoMTT.SetLineColor(1)

theTree.Draw("ResoVisHiggs_mass>>HiggsMassResoVis(40,0,2)")
HiggsMassResoVis = ROOT.gDirectory.Get("HiggsMassResoVis").Clone()
HiggsMassResoVis.SetLineColor(4)

#Higgs pt
theTree.Draw("ResoGenHiggs_pt>>HiggsptResoMTT(40,0,2)")
HiggsptResoMTT = ROOT.gDirectory.Get("HiggsptResoMTT").Clone()
HiggsptResoMTT.SetLineColor(1)

theTree.Draw("ResoVisHiggs_pt>>HiggsptResoVis(40,0,2)")
HiggsptResoVis = ROOT.gDirectory.Get("HiggsptResoVis").Clone()
HiggsptResoVis.SetLineColor(4)

#Next we do it for Radion

#Radion Mass##
theTree.Draw("ResoGenRadion_mass>>RadionMassResoMTT(40,0,2)")
RadionMassResoMTT = ROOT.gDirectory.Get("RadionMassResoMTT").Clone()
RadionMassResoMTT.SetLineColor(1)

theTree.Draw("ResoGenRadionWithMet_mass>>RadionMassWithMetResoMTT(40,0,2)")
RadionMassWithMetResoMTT = ROOT.gDirectory.Get("RadionMassWithMetResoMTT").Clone()
RadionMassWithMetResoMTT.SetLineColor(2)

theTree.Draw("ResoVisRadion_mass>>RadionMassVisReso(40,0,2)")
RadionMassVisReso = ROOT.gDirectory.Get("RadionMassVisReso").Clone()
RadionMassVisReso.SetLineColor(4)


#Radion pt##
theTree.Draw("ResoGenRadion_pt>>RadionptResoMTT(40,0,2)")
RadionptResoMTT = ROOT.gDirectory.Get("RadionptResoMTT").Clone()
RadionptResoMTT.SetLineColor(1)

theTree.Draw("ResoGenRadionWithMet_pt>>RadionptWithMetResoMTT(40,0,2)")
RadionptWithMetResoMTT = ROOT.gDirectory.Get("RadionptWithMetResoMTT").Clone()
RadionptWithMetResoMTT.SetLineColor(2)

theTree.Draw("ResoVisRadion_pt>>RadionptVisReso(40,0,2)")
RadionptVisReso = ROOT.gDirectory.Get("RadionptVisReso").Clone()
RadionptVisReso.SetLineColor(4)













