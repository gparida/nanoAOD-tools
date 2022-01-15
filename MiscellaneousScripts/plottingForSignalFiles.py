import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


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
theTree.Draw("ResoGenHiggs_mass>>HiggsMassResoMTT(40,0,2)")
HiggsMassResoMTT = ROOT.gDirectory.Get("HiggsMassResoMTT").Clone()
HiggsMassResoMTT.SetLineColor(1)
HiggsMassResoMTT.SetLineWidth(4)
HiggsMassResoMTT.SetTitle("Higgs Mass Resolution")
HiggsMassResoMTT.GetXaxis().SetTitle("Higgs Mass^{Reco}/Higgs Mass^{True}")
HiggsMassResoMTT.GetYaxis().SetTitle("Events")

theTree.Draw("ResoVisHiggs_mass>>HiggsMassResoVis(60,0,2)")
HiggsMassResoVis = ROOT.gDirectory.Get("HiggsMassResoVis").Clone()
HiggsMassResoVis.SetLineColor(4)
HiggsMassResoVis.SetLineWidth(4)

legend = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(HiggsMassResoMTT,"FastMTT","ep")
legend.AddEntry(HiggsMassResoVis,"Visible","ep")

HiggsMass = ROOT.TCanvas("HiggsMass", "HiggsMass")
#HiggsMass.SetGrid()
HiggsMassResoMTT.SetMaximum(max(HiggsMassResoMTT.GetMaximum(),HiggsMassResoVis.GetMaximum()))
HiggsMassResoMTT.Draw("HIST")
HiggsMassResoVis.Draw("same")
legend.Draw("same")
HiggsMass.SaveAs("HiggsM_Reso.pdf")



#Higgs pt
theTree.Draw("ResoGenHiggs_pt>>HiggsptResoMTT(60,0,2)")
HiggsptResoMTT = ROOT.gDirectory.Get("HiggsptResoMTT").Clone()
HiggsptResoMTT.SetLineColor(1)
HiggsptResoMTT.SetLineWidth(4)
HiggsptResoMTT.SetTitle("Higgs Pt Resolution")
HiggsptResoMTT.GetXaxis().SetTitle("Higgs Pt^{Reco}/Higgs Pt^{True}")
HiggsptResoMTT.GetYaxis().SetTitle("Events")

theTree.Draw("ResoVisHiggs_pt>>HiggsptResoVis(40,0,2)")
HiggsptResoVis = ROOT.gDirectory.Get("HiggsptResoVis").Clone()
HiggsptResoVis.SetLineColor(4)
HiggsptResoVis.SetLineWidth(4)


legend = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(HiggsptResoMTT,"FastMTT","ep")
legend.AddEntry(HiggsptResoVis,"Visible","ep")

HiggsPt = ROOT.TCanvas("HiggsPt", "HiggsPt")
#HiggsMass.SetGrid()
HiggsptResoMTT.SetMaximum(max(HiggsptResoMTT.GetMaximum(),HiggsptResoVis.GetMaximum()))
HiggsptResoMTT.Draw("HIST")
HiggsptResoVis.Draw("same")
legend.Draw("same")
HiggsPt.SaveAs("HiggsPt_Reso.pdf")

#Next we do it for Radion

#Radion Mass##
theTree.Draw("ResoGenRadion_mass>>RadionMassResoMTT(40,0,2)")
RadionMassResoMTT = ROOT.gDirectory.Get("RadionMassResoMTT").Clone()
RadionMassResoMTT.SetLineColor(1)
RadionMassResoMTT.SetLineWidth(4)
RadionMassResoMTT.SetTitle("Radion Mass Resolution")
RadionMassResoMTT.GetXaxis().SetTitle("#Radion Mass^{Reco}/#Radion Mass^{True}")
RadionMassResoMTT.GetYaxis().SetTitle("Events")


theTree.Draw("ResoGenRadionWithMet_mass>>RadionMassWithMetResoMTT(40,0,2)")
RadionMassWithMetResoMTT = ROOT.gDirectory.Get("RadionMassWithMetResoMTT").Clone()
RadionMassWithMetResoMTT.SetLineColor(2)
RadionMassWithMetResoMTT.SetLineWidth(4)

theTree.Draw("ResoVisRadion_mass>>RadionMassVisReso(40,0,2)")
RadionMassVisReso = ROOT.gDirectory.Get("RadionMassVisReso").Clone()
RadionMassVisReso.SetLineColor(4)
RadionMassVisReso.SetLineWidth(4)

legend = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(RadionMassResoMTT,"Radion FastMTT ","ep")
legend.AddEntry(RadionMassWithMetResoMTT,"Radion FastMTT and With MET ","ep")
legend.AddEntry(RadionMassVisReso,"Radion with Visible Mass","ep")

RadionMass = ROOT.TCanvas("RadionMass", "RadionMass")
#HiggsMass.SetGrid()
RadionMassResoMTT.SetMaximum(max(RadionMassResoMTT.GetMaximum(),RadionMassResoMTT.GetMaximum(),RadionMassVisReso.GetMaximum()))
RadionMassResoMTT.Draw("ap")
RadionMassWithMetResoMTT.Draw("same p")
RadionMassVisReso.Draw("same p")
legend.Draw("same")
RadionMass.SaveAs("RadionMass_Reso.pdf")



#Radion pt##
theTree.Draw("ResoGenRadion_pt>>RadionptResoMTT(40,0,2)")
RadionptResoMTT = ROOT.gDirectory.Get("RadionptResoMTT").Clone()
RadionptResoMTT.SetLineColor(1)
RadionptResoMTT.SetLineWidth(4)
RadionptResoMTT.SetTitle("Radion Pt Resolution")
RadionptResoMTT.GetXaxis().SetTitle("#Radion Pt^{Reco}/#Radion Pt^{True}")
RadionptResoMTT.GetYaxis().SetTitle("Events")

theTree.Draw("ResoGenRadionWithMet_pt>>RadionptWithMetResoMTT(40,0,2)")
RadionptWithMetResoMTT = ROOT.gDirectory.Get("RadionptWithMetResoMTT").Clone()
RadionptWithMetResoMTT.SetLineColor(2)
RadionptWithMetResoMTT.SetLineWidth(4)

theTree.Draw("ResoVisRadion_pt>>RadionptVisReso(40,0,2)")
RadionptVisReso = ROOT.gDirectory.Get("RadionptVisReso").Clone()
RadionptVisReso.SetLineColor(4)
RadionptVisReso.SetLineWidth(4)

legend = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(RadionptResoMTT,"Radion with FastMTT ","ep")
legend.AddEntry(RadionptWithMetResoMTT,"Radion with FastMTT and MET ","ep")
legend.AddEntry(RadionptVisReso,"Radion with Visible Mass","ep")

RadionPt = ROOT.TCanvas("RadionPt", "RadionPt")
#HiggsMass.SetGrid()
RadionptResoMTT.SetMaximum(max(RadionptResoMTT.GetMaximum(),RadionptWithMetResoMTT.GetMaximum(),RadionptVisReso.GetMaximum()))
RadionptResoMTT.Draw("ap")
RadionptWithMetResoMTT.Draw("same p")
RadionptVisReso.Draw("same p")
legend.Draw("same")
RadionPt.SaveAs("RadionPt_Reso.pdf")







