
import ROOT

files = [
         "TTToSemiLeptonic.root",
         #"Run2016F.root",
         "QCD_HT100to200.root",
         "QCD_HT2000toinf.root",
         "ST_tW_antitop_5f.root",
         "ST_tW_top_5f.root",
         "WJets_HT-600to800.root",
         "WZTo2Q2Nu.root",
         "ST_s-channel_4f.root",
         "WJets_HT-400to600.root",
         "DYJets_HT-1200to2500.root",
         "DYJetsToLL_M-10to50.root",
         "WJets_HT-100To200.root",
         "ZZTo2Q2Nu.root",
         "DYJets_HT-100to200.root",
         "RadionTohhTohtatahbb_M-1400.root",
         #"Run2016H.root",
         "Radiontohhtohtatahbb_M-3500.root",
         "Radiontohhtohtatahbb_M-2500.root",
         "WJets_HT-800to1200.root",
         "WJets_HT-200to400.root",
         "RadionTohhtohtatahbb_M-1000.root",
         "QCD_HT500to700.root",
         "WZTo1L1nu2q.root",
         "WWTo1L1Nu2Q.root",
         "DYJets_HT-400to600.root",
         "WJets_HT-1200to2500.root",
         "Radiontohhtohtatahbb_M-3000.root",
         "QCD_HT200to300.root",
         "ST_t-channel_antitop_4f.root",
         "TTToHadronic.root",
         "QCD_HT1500to2000.root",
         "DYJets_HT-800to1200.root",
         "QCD+JT50to100.root",
         #"Run2016G.root",
         "DYJets_HT-600to800.root",
         "WJets_HT-2500toInf.root",
         "TTTo2L2Nu.root",
         "QCD_HT700to1000.root",
         "Radiontohhtohtatahbb_M-4500.root",
         "ST_t-channel_top_4f.root",
         "QCD_HT1000to1500.root",
         "RadionTohhtohtatahbb_M-1200.root",
         "RadionTohhtohtatahbb_M-1600.root",
         "QCD_HT300to500.root",
         "Radiontohhtohtatahbb_M-4000.root",
         "DYJets_HT-200to400.root",
         "RadionTohhtohtatahbb_M-1800.root",
         "DYJets_HT-2500toinf.root",
         "Radiontohhtohtatahbb_M-2000.root" 
]
f = open("genWeightList.txt", "w")
for file in files:
    file_bbtt = ROOT.TFile("/data/gparida/bbtautauAnalysis/2016/SignalBackgroundData_28Jan2022/"+str(file))
    tree_bbtt = file_bbtt.Get('Events')
    nEntries = tree_bbtt.GetEntries()
    f.write(file+"\t"+str(nEntries)+"\n")
    for x in range(nEntries):
        if x==10:
            break
        
        tree_bbtt.GetEntry(x)
        f.write(str(tree_bbtt.genWeight)+"\n")
    

f.close()

    
            
