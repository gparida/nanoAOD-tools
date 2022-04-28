from tokenize import Name
import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from plotSettings import *


#Now we need to take inputs
parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
parser.add_argument('--inputFile',help="Full path to the signal file including the name")
#parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
#parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
#parser.add_argument('--postfix',help="string at the end of output file names", default="")
args = parser.parse_args()

#open the file
theFile = ROOT.TFile(args.inputFile) #opening the root file
 

 #Grab the Event tree as this is a nanoAOD file

theTree = theFile.Get("Events")
nEntries = theTree.GetEntries()

#Now we Just directly plot the branches in the ttree
#First doing it for Higgs..................................

#Higgs mass

HiggsMassResoMTT= setUpHistrogram(Name="HiggsMassResoMTT",LineColor=1,LineWidth=2,XTitle="Higgs Mass^{Reco}/Higgs Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenHiggs_mass",Nbins=40,min=0,max=2)
HiggsMassResoVis= setUpHistrogram(Name="HiggsMassResoVis",LineColor=4,LineWidth=2,XTitle="Higgs Mass^{Reco}/Higgs Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoVisHiggs_mass",Nbins=40,min=0,max=2)

HiggsMass = setUpCanvas("HiggsMass")
HiggsMassResoMTT.SetMaximum(max(HiggsMassResoMTT.GetMaximum(),HiggsMassResoVis.GetMaximum())+50)
#HiggsMassResoMTT.Draw("C")
#HiggsMassResoVis.Draw("C same")
HiggsMassResoMTT.Draw("Hist E1")
HiggsMassResoVis.Draw("same Hist E1")


legend = setUpLegend()
legend.AddEntry(HiggsMassResoMTT,"FastMTT","ep")
legend.AddEntry(HiggsMassResoVis,"Visible","ep")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)

HiggsMass.SaveAs("HiggsM_Reso.pdf")



#Higgs pt
HiggsptResoMTT= setUpHistrogram(Name="HiggsptResoMTT",LineColor=1,LineWidth=2,XTitle="Higgs Pt^{Reco}/Higgs Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoGenHiggs_pt",Nbins=40,min=0,max=2)
HiggsptResoVis= setUpHistrogram(Name="HiggsptResoVis",LineColor=4,LineWidth=2,XTitle="Higgs Pt^{Reco}/Higgs Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoVisHiggs_pt",Nbins=40,min=0,max=2)


HiggsPt = setUpCanvas("HiggsPt")
HiggsptResoMTT.SetMaximum(max(HiggsMassResoMTT.GetMaximum(),HiggsMassResoVis.GetMaximum())+50)
#HiggsptResoMTT.Draw("C")
#HiggsptResoVis.Draw("C same")
HiggsptResoMTT.Draw("Hist E1")
HiggsptResoVis.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(HiggsptResoMTT,"FastMTT","ep")
legend.AddEntry(HiggsptResoVis,"Visible","ep")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
HiggsPt.SaveAs("HiggsPt_Reso.pdf")

#Next we do it for Radion

#Radion Mass##
RadionMassResoMTT= setUpHistrogram(Name="RadionMassResoMTT",LineColor=1,LineWidth=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadion_mass",Nbins=40,min=0,max=2)
RadionMassWithMetResoMTT= setUpHistrogram(Name="RadionMassWithMetResoMTT",LineColor=2,LineWidth=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadionWithMet_mass",Nbins=40,min=0,max=2)
RadionMassVisReso = setUpHistrogram(Name="RadionMassVisReso",LineColor=4,LineWidth=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoVisRadion_mass",Nbins=40,min=0,max=2)

RadionMass = setUpCanvas("RadionMass")
HiggsMassResoMTT.SetMaximum(max(RadionMassResoMTT.GetMaximum(),RadionMassWithMetResoMTT.GetMaximum(),RadionMassVisReso.GetMaximum())+50)
#RadionMassResoMTT.Draw("C")
#RadionMassWithMetResoMTT.Draw("C same")
#RadionMassVisReso.Draw("C same")
#RadionMassResoMTT.Draw("Hist E1")
RadionMassWithMetResoMTT.Draw("same Hist E1")
RadionMassVisReso.Draw("same Hist E1")


legend = setUpLegend()
legend.AddEntry(RadionMassResoMTT,"FastMTT","ep")
legend.AddEntry(RadionMassWithMetResoMTT,"FastMTT + MET","ep")
legend.AddEntry(RadionMassVisReso,"Visible","ep")
legend.Draw("same")


cmsLatex = setUpCmsLatex(2016)
RadionMass.SaveAs("RadionM_Reso.pdf")

#Radion Momemtum##
RadionptResoMTT= setUpHistrogram(Name="RadionptResoMTT",LineColor=1,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadion_pt",Nbins=30,min=0,max=2)
RadionptWithMetResoMTT= setUpHistrogram(Name="RadionptWithMetResoMTT",LineColor=2,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadionWithMet_pt",Nbins=30,min=0,max=2)
RadionptVisReso = setUpHistrogram(Name="RadionptVisReso",LineColor=4,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoVisRadion_pt",Nbins=30,min=0,max=2)

Radionpt = setUpCanvas("Radionpt")
RadionptResoMTT.SetMaximum(max(RadionptResoMTT.GetMaximum(),RadionptWithMetResoMTT.GetMaximum(),RadionptVisReso.GetMaximum())+50)
#RadionptResoMTT.Draw("Hist E1")
RadionptWithMetResoMTT.Draw("same Hist E1")
RadionptVisReso.Draw("same Hist E1")



legend = setUpLegend()
#legend.AddEntry(RadionptResoMTT,"FastMTT","ep")
legend.AddEntry(RadionptWithMetResoMTT,"FastMTT + MET","ep")
legend.AddEntry(RadionptVisReso,"Visible","ep")
legend.Draw("same")


cmsLatex = setUpCmsLatex(2016)
Radionpt.SaveAs("RadionPt_Reso.pdf")


#Plotting Higgs Mass
HiggsMassbb = setUpHistrogram(Name="HiggsMassbb",LineColor=1,LineWidth=2,XTitle="Softdrop Mass^{Reco}/Higgs Mass^{True}",YTitle="Events",ttree=theTree,branch="(gFatJet_msoftdrop/125)",Nbins=40,min=0,max=2,cond="(FatJet_particleNetMD_Xbb/(FatJet_particleNetMD_Xbb+FatJet_particleNetMD_QCD))>0.87")

HiggsbbMass = setUpCanvas("Soft Drop Mass")
HiggsMassbb.SetMaximum(HiggsMassbb.GetMaximum()+50)
HiggsMassbb.Draw("Hist E1")

legend = setUpLegend()
legend.AddEntry(HiggsMassbb,"SoftDrop Mass","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
HiggsbbMass.SaveAs("HMass_bb.pdf")