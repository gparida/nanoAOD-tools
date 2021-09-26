FatJetBranches=["area":["area","F"],
                "btagCSVV2":["btagCSVV2"],
                "btagDDBvLV2",
                "btagDDCvBV2",
                "btagDDCvLV2",
                "btagDeepB",
                "btagHbb",
                "deepTagMD_H4qvsQCD",
                "deepTagMD_HbbvsQCD",
                "deepTagMD_TvsQCD",
                "deepTagMD_WvsQCD",
                "deepTagMD_ZHbbvsQCD",
                "deepTagMD_ZHccvsQCD",
                "deepTagMD_ZbbvsQCD",
                "deepTagMD_ccvsLight",
                "deepTag_H",
                "deepTag_QCD",
                "deepTag_QCDothers",
                "deepTag_TvsQCD",
                "deepTag_WvsQCD",
                "deepTag_ZvsQCD",
                "msoftdrop",
                "n2b1",
                "n3b1",
                "particleNetMD_QCD",
                "particleNetMD_Xbb",
                "particleNetMD_Xcc",
                "particleNetMD_Xqq",
                "particleNet_H4qvsQCD",
                "particleNet_HbbvsQCD",
                "particleNet_HccvsQCD",
                "particleNet_QCD",
                "particleNet_TvsQCD",
                "particleNet_WvsQCD",
                "particleNet_ZvsQCD",
                "particleNet_mass",
                "rawFactor",
                "tau1",
                "tau2",
                "tau3",
                "tau4",
                "lsf3",
                "jetId",
                "subJetIdx1",
                "subJetIdx2",
                "electronIdx3SJ",
                "muonIdx3SJ"]

FatJetBranchesType=[]


MuonBranches={
"1":["Muon_charge","Int_t"],
"2":["Muon_cleanmask","UChar_t"],
"3":["Muon_dxy","F"],
"4":["Muon_dxyErr","F"],
"5":["Muon_dxybs","F"],
"6":["Muon_dz","F"],
"7":["Muon_dzErr","F"],
"8":["Muon_eta","F"],
"9":["Muon_fsrPhotonIdx","Int_t(index to Fsrphoton)"],
"10":["Muon_genPartFlav","UChar_t"],
"11":["Muon_genPartIdx","Int_t(index to Genpart)"],
"12":["Muon_highPtId","UChar_t"],
"13":["Muon_highPurity","Bool_t"],
"14":["Muon_inTimeMuon","Bool_t"],
"15":["Muon_ip3d","F"],
"16":["Muon_isGlobal","Bool_t"],
"17":["Muon_isPFcand","Bool_t"],
"18":["Muon_isTracker","Bool_t"],
"19":["Muon_jetIdx","Int_t(index to Jet)"],
"20":["Muon_jetPtRelv2","F"],
"21":["Muon_jetRelIso","F"],
"22":["Muon_looseId","Bool_t"],
"23":["Muon_mass","F"],
"24":["Muon_mediumId","Bool_t"],
"25":["Muon_mediumPromptId","Bool_t"],
"26":["Muon_miniIsoId","UChar_t"],
"27":["Muon_miniPFRelIso_all","F"],
"28":["Muon_miniPFRelIso_chg","F"],
"29":["Muon_multiIsoId","UChar_t"],
"30":["Muon_mvaId","UChar_t"],
"31":["Muon_mvaLowPt","F"],
"32":["Muon_mvaLowPtId","UChar_t"],
"33":["Muon_mvaTTH","F"],
"34":["Muon_nStations","Int_t"],
"35":["Muon_nTrackerLayers","Int_t"],
"36":["Muon_pdgId","Int_t"],
"37":["Muon_pfIsoId","UChar_t"],
"38":["Muon_pfRelIso03_all","F"],
"39":["Muon_pfRelIso03_chg","F"],
"40":["Muon_pfRelIso04_all","F"],
"41":["Muon_phi","F"],
"42":["Muon_pt","F"],
"43":["Muon_ptErr","F"],
"44":["Muon_segmentComp","F"],
"45":["Muon_sip3d","F"],
"46":["Muon_softId","Bool_t"],
"47":["Muon_softMva","F"],
"48":["Muon_softMvaId","Bool_t"],
"49":["Muon_tightCharge","Int_t"],
"50":["Muon_tightId","Bool_t"],
"51":["Muon_tkIsoId","UChar_t"],
"52":["Muon_tkRelIso","F"],
"53":["Muon_triggerIdLoose","Bool_t"],
"54":["Muon_tunepRelPt","F"]
}

ElectronBranches={

    
}


TauBranches ={
1:["charge","Int_t"],
2:["chargedIso","F"],
3:["cleanmask","UChar_t"],
4:["decayMode","Int_t"],
5:["dxy","F"],
6:["dz","F"],
7:["eta","F"],
8:["genPartFlav","UChar_t"],
9:["genPartIdx","Int_t"],
10:["Tau_idAntiEle","UChar_t"],
11:["idAntiEle2018","UChar_t"],
12:["idAntiEleDeadECal","Bool_t"],
13:["idAntiMu","UChar_t"],
14:["idDecayMode","Bool_t"],
15:["idDecayModeNewDMs","Bool_t"],
16:["idDeepTau2017v2p1VSe","UChar_t"],
17:["idDeepTau2017v2p1VSjet","UChar_t"],
18:["idDeepTau2017v2p1VSmu","UChar_t"],
19:["idMVAnewDM2017v2","UChar_t"],
20:["idMVAoldDM","UChar_t"],
21:["idMVAoldDM2017v1","UChar_t"],
22:["idMVAoldDM2017v2","UChar_t"],
23:["idMVAoldDMdR032017v2","UChar_t"],
24:["jetIdx","Int_t(index to Jet)"],
25:["leadTkDeltaEta","F"],
26:["leadTkDeltaPhi","F"],
27:["leadTkPtOverTauPt","F"],
28:["mass","F"],
29:["neutralIso","F"],
30:["phi","F"],
31:["photonsOutsideSignalCone","F"],
32:["pt","F"],
33:["puCorr","F"],
34:["rawAntiEle","F"],
35:["rawAntiEle2018","F"],
36:["rawAntiEleCat","Int_t"],
37:["rawAntiEleCat2018","Int_t"],
38:["rawDeepTau2017v2p1VSe","F"],
39:["rawDeepTau2017v2p1VSjet","F"],
40:["rawDeepTau2017v2p1VSmu","F"],
41:["rawIso","F"],
42:["rawIsodR03","F"],
43:["rawMVAnewDM2017v2","F"],
44:["rawMVAoldDM","F"],
45:["rawMVAoldDM2017v1","F"],
46:["rawMVAoldDM2017v2","F"],
47:["rawMVAoldDMdR032017v2","F"]
}


boostedTauBranches ={
1:["charge","Int_t"],
2:["chargedIso","F"],
3:["cleanmask","UChar_t"],
4:["decayMode","Int_t"],
5:["dxy","F"],
6:["dz","F"],
7:["eta","F"],
8:["genPartFlav","UChar_t"],
9:["genPartIdx","Int_t"],
10:["Tau_idAntiEle","UChar_t"],
11:["idAntiEle2018","UChar_t"],
12:["idAntiEleDeadECal","Bool_t"],
13:["idAntiMu","UChar_t"],
14:["idDecayMode","Bool_t"],
15:["idDecayModeNewDMs","Bool_t"],
16:["idDeepTau2017v2p1VSe","UChar_t"],
17:["idDeepTau2017v2p1VSjet","UChar_t"],
18:["idDeepTau2017v2p1VSmu","UChar_t"],
19:["idMVAnewDM2017v2","UChar_t"],
20:["idMVAoldDM","UChar_t"],
21:["idMVAoldDM2017v1","UChar_t"],
22:["idMVAoldDM2017v2","UChar_t"],
23:["idMVAoldDMdR032017v2","UChar_t"],
24:["jetIdx","Int_t"],
25:["leadTkDeltaEta","F"],
26:["leadTkDeltaPhi","F"],
27:["leadTkPtOverTauPt","F"],
28:["mass","F"],
29:["neutralIso","F"],
30:["phi","F"],
31:["photonsOutsideSignalCone","F"],
32:["pt","F"],
33:["puCorr","F"],
34:["rawAntiEle","F"],
35:["rawAntiEle2018","F"],
36:["rawAntiEleCat","Int_t"],
37:["rawAntiEleCat2018","Int_t"],
38:["rawDeepTau2017v2p1VSe","F"],
39:["rawDeepTau2017v2p1VSjet","F"],
40:["rawDeepTau2017v2p1VSmu","F"],
41:["rawIso","F"],
42:["rawIsodR03","F"],
43:["rawMVAnewDM2017v2","F"],
44:["rawMVAoldDM","F"],
45:["rawMVAoldDM2017v1","F"],
46:["rawMVAoldDM2017v2","F"],
47:["rawMVAoldDMdR032017v2","F"]
}