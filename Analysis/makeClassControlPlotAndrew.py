import ROOT
import argparse  ##Importing root and package to take arguments 


class MakeHistograms(object):
    #constructor to initialize the objects
    #def __init__(self,RootFilePath,RootFileName,Weight):
    def __init__(self,RootFilePath,RootFileName, userWeight = "1.0"):
        self.RootFileName = ROOT.TFile(RootFilePath+RootFileName+'.root')
        self.HistogramName = None
        self.PassFailHistogramName = ROOT.TH1F("PassFailHist","PassFailHist",1,0,1)
        self.userWeight = userWeight

    #Cut creating member function
    def CreateCutString(self,standardCutString,
                    otherCuts,
                    weighting):
    #cutString = weighting+'*('+standardCutString+' && '
        cutString =weighting+'*('+'('+standardCutString+')'+' && '
        if otherCuts!=None:
            for cut in otherCuts:
                cutString += '('+cut+')' + ' && '

        cutString = cutString[:len(cutString)-3] # removing the && at the very end of the final cutstring
        #cutString+=')'
        return cutString
        
    #Histogram Making member function and storing it in an attribute
    def StandardDraw(self,theFile,
                 variable,
                 standardCutString,
                 additionalSelections,
                 histogramName,
                 theWeight = 'FinalWeighting'):
        trig_MET_MC =["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_PFMET110_PFMHT110_IDTight",
            "HLT_PFMET120_PFMHT120_IDTight",
            #"HLT_PFMET170_NoiseCleaned",
            "HLT_PFMET170_HBHECleaned",
            "HLT_PFMET170_HBHE_BeamHaloCleaned"]

        trig_MET_Data =["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
                "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
                "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
                "HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
                "HLT_PFMET110_PFMHT110_IDTight",
                "HLT_PFMET120_PFMHT120_IDTight",
                #"HLT_PFMET170_NoiseCleaned",
                "HLT_PFMET170_HBHECleaned",
                "HLT_PFMET170_HBHE_BeamHaloCleaned"]

        theTree = theFile.Get('Events')
        print (variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
                             self.CreateCutString(standardCutString,
                                             additionalSelections,theWeight)+' && '+'(' + '||'.join(trig_MET_MC) + ')'+')')
        theTree.Draw(variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
                             self.CreateCutString(standardCutString,
                                             additionalSelections,theWeight)+' && '+'(' + '||'.join(trig_MET_MC) + ')'+')')
    #so, if the tree has no entries, root doesn't even hand back an empty histogram
    # and therefore this ends up trying to get clone a none type
    #pass the None forward, and we can let the Add handle this
        try:
            theHisto = ROOT.gDirectory.Get(histogramName).Clone()
        except ReferenceError:
            theHisto = None
        #return theHisto
        self.HistogramName=theHisto


    def FillEvents(self, theFile, dataset):
        #PassFailHist = ROOT.TH1F("PassFailHist","PassFailHist",3,0,3)
        #self.PassFailHistogramName.GetXaxis().SetBinLabel(1,"All")
        #self.PassFailHistogramName.GetXaxis().SetBinLabel(2,"FailTrigger")
        self.PassFailHistogramName.GetXaxis().SetBinLabel(1,"PassTrigger")
        trig_MET_MC =["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_PFMET110_PFMHT110_IDTight",
            "HLT_PFMET120_PFMHT120_IDTight",
            #"HLT_PFMET170_NoiseCleaned",
            "HLT_PFMET170_HBHECleaned",
            "HLT_PFMET170_HBHE_BeamHaloCleaned"]

        trig_MET_Data =["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_PFMET110_PFMHT110_IDTight",
            "HLT_PFMET120_PFMHT120_IDTight",
            #"HLT_PFMET170_NoiseCleaned",
            "HLT_PFMET170_HBHECleaned",
            "HLT_PFMET170_HBHE_BeamHaloCleaned"]


        theTree=theFile.Get('Events')

        if dataset == "data":
            self.PassFailHistogramName.SetBinContent(1,theTree.GetEntries("MET_pt >= 200 && (" + "||".join(trig_MET_MC) + ")"))
        else:
            self.PassFailHistogramName.SetBinContent(1,theTree.GetEntries("MET_pt >= 200 && (" + "||".join(trig_MET_Data) + ")"))


        #self.PassFailHistogramName.SetBinContent(1,theTree.GetEntries())
        #self.PassFailHistogramName.SetBinContent(2,(theTree.GetEntries()-theTree.GetEntries("MET_pt >= 205 && (" + "||".join(trig_MET) + ")")))
        
        #self.PassFailHistogramName.SetBinContent(1,theTree.GetEntries("MET_pt >= 205 && (" + "||".join(trig_MET_MC) + ")"))

        #self.PassFailHistogramName = PassFailHist
        #del PassFailHist






    






#This dictionary lists observable to be plotted in control plots and their corresponding histogram binning and range
variableSettingDictionary = {
    'Tau_pt':'16,0.0,400.0',
    'Tau_phi':'30,-3.14,3.14',
    'Tau_eta':'20, -2.0, 2.0',
    'nboostedTau':'6,0,6',
    'nTau':'6,0,6',
    'FatJet_pt':'60,0.0,1500.0',
    'FatJet_phi':'30,-3.14,3.14',
    'FatJet_eta':'20, -2.0, 2.0',
    'nFatJet':'5,0,5',
    'Electron_pt':'40,0.0,1000.0',
    'Electron_phi':'30,-3.14,3.14',
    'Electron_eta':'20, -2.0, 2.0',
    'nElectron':'6,0,6',
    'MET_pt':'60,0.0,1500.0',
    'MET_phi':'30,-3.14,3.14',
    'MET_sumEt':'40,0.00,1000.00',
    'Muon_pt':'16,0.0,400.0',
    'Muon_eta':'20, -2.0, 2.0',
    'Muon_phi':'30,-3.14,3.14',
    'nMuon':'6,0,6',
    #'Electron_eta':'48,-2.4,2.4',
    #'Electron_pt':'20,20.0,400.0',
    #'pt_2':'25,30.0,80.0',
    #'eta_2':'50,-2.5,2.5',
    #'pt_1':'30,20.0,80.0',
    #'eta_1':'48,-2.4,2.4',
    #'m_vis':'30,50.0,200.0',
    #'m_sv':'25,50.0,300.0',
    #'njets':'6,0.0,6.0',
    #'HiggsPt':'40,0.0,400.0',
    #'HiggsPt_Differential':'40,0.0,400.0',
    #'met':'40,0.0,400.0',
    #'DeltaR':'40,0.0,6.0',
    #'mjj':'20,0.0,500.0',
    #'abs(eta_1-eta_2)':'45,0.0,2.5',
    #'jpt_1':'50,0.0,200.0',
    #'jeta_1':'50,-5.0,5.0',
    #'jpt_2':'50,0.0,200.0',
    #'jeta_2':'50,-5.0,5.0',
    #'MT':'20,0.0,200.0',
}


#This dictionary lists observable and its corresponding X-Axis name
variableAxisTitleDictionary = {
    #'Electron_eta':'Electron #eta',
    #'Electron_pt':'Electron p_{t}','Tau_pt':'#tau_{p_{T}}',
    'Tau_pt':'p_{T}(#tau)',
    'Tau_phi':'#phi(#tau)',
    'Tau_eta':'#eta(#tau)',
    'nboostedTau':'Number of Boosted #tau',
    'nTau':'Number of #tau',
    'FatJet_pt':'ak8 jet p_{T}[GeV]',
    'FatJet_phi':'#phi(ak8 jet)',
    'FatJet_eta':'#eta(ak8 jet)',
    'nFatJet':'Number of ak8 Jets',
    'Electron_pt':'p_{T} (e)[GeV]',
    'Electron_phi':'#phi (e)',
    'Electron_eta':'#eta(e)',
    'nElectron':'Number of e',
    'MET_pt':'MET_{p_{T}}',
    'MET_phi':'#phi(MET)',
    'MET_sumEt':'Scalar Sum of E_{T}',
    'Muon_pt':'#phi(#mu)',
    'Muon_eta':'#eta(#mu)',
    'Muon_phi':'#phi(#mu)',
    'nMuon':'Number of #mu',
    
    #'pt_2':'#tau p_{t}',
    #'eta_2':'#tau #eta',
    #'pt_1':'#mu p_{t}',
    #'eta_1':'#mu #eta',
    #'m_vis':'m_{vis}',
    #'m_sv':'m_{#tau#tau}',
    #'njets':'N_{jets}',
    #'HiggsPt':'Higgs p_{t}',
    #'HiggsPt_Differential':'Higgs p_{t}',
    #'met':'MET',
    #'DeltaR':'#Delta r_{#mu,#tau}',
    #'mjj':'m_{jj}',
    #'abs(eta_1-eta_2)':'#Delta#eta_{jj}',
    #'jpt_1':'p_{t} j_{1}',
    #'jeta_1':'#eta j_{1}',
    #'jpt_2':'p_{t} j_{2}',
    #'jeta_2':'#eta j_{2}',    
    #'MT':'Transverse Mass',
    }

DatasetNameXSWeightDictionary={
    "QCD_1000to1400":0.006405107,
    "QCD_120to170":230.3234918,
    "QCD_1400to1800":0.000997817,
    "QCD_15to30":1058937.981,
    "QCD_170to300":59.15251935,
    "QCD_1800to2400":0.00026933,
    "QCD_2400to3200":0.0000296633850303439,
    "QCD_300to470":2.00778766,
    "QCD_30to50":90647.48201,
    "QCD_3200toInf":0.00000227136,
    "QCD_470to600":0.178230811,
    "QCD_800to1000":0.011793967,
    "QCD_80to120":1323.643203,
    "QCD_50to80":13473.64119,
    "QCD_600to800":0.040118257,
    "ST_s-channel_4f":0.009501705,
    #"TTTo2L2Nu":0.255495352,
    #"TTToHadronic":0.102523092,
    #"TTToSemiLeptonic":0.07267512,
    "TTTo2L2Nu":0.036459448,
    "TTToHadronic":0.036459448,
    "TTToSemiLeptonic":0.036459448,
    "W":10.63712415,
    "WW":0.088197968,
    "WZ":0.060063755,
    "ZZ":0.197924492,
    "DYlow":9.15316241,
    "DY":0.901934791,
    "Data":1,
    }

DatasetNameList=["QCD_1000to1400",
"QCD_120to170",
"QCD_1400to1800",
"QCD_15to30",
"QCD_170to300",
"QCD_1800to2400",
"QCD_2400to3200",
"QCD_300to470",
"QCD_30to50",
"QCD_3200toInf",
"QCD_470to600",
"QCD_800to1000",
"QCD_80to120",
"QCD_50to80",
"QCD_600to800",
"ST_s-channel_4f",
"TTTo2L2Nu",
"TTToHadronic",
"TTToSemiLeptonic",
"W",
"WW",
"WZ",
"ZZ",
"DYlow",
"DY",
"Data"]

#DatasetObjects={}

def MakeStackErrors(theStack):
    denominatorHistos = theStack.GetHists().At(0).Clone()
    denominatorHistos.Reset()

    for i in range(0,theStack.GetNhists()):
        denominatorHistos.Add(theStack.GetHists().At(i))
    
    theErrorHisto = denominatorHistos.Clone()
    theErrorHisto.Reset()
    
    for i in range(0,denominatorHistos.GetNbinsX()+1):
        theErrorHisto.SetBinContent(i,denominatorHistos.GetBinContent(i))
        theErrorHisto.SetBinError(i,denominatorHistos.GetBinError(i))
    theErrorHisto.SetLineColor(0)
    theErrorHisto.SetLineWidth(0)
    theErrorHisto.SetMarkerStyle(0)
    theErrorHisto.SetFillStyle(3001)
    theErrorHisto.SetFillColor(15)
    return theErrorHisto


    #make the statistical errors on the prediction stack
def MakeStackErrors(theStack):
    denominatorHistos = theStack.GetHists().At(0).Clone()
    denominatorHistos.Reset()

    for i in range(0,theStack.GetNhists()):
        denominatorHistos.Add(theStack.GetHists().At(i))
    
    theErrorHisto = denominatorHistos.Clone()
    theErrorHisto.Reset()
    
    for i in range(0,denominatorHistos.GetNbinsX()+1):
        theErrorHisto.SetBinContent(i,denominatorHistos.GetBinContent(i))
        theErrorHisto.SetBinError(i,denominatorHistos.GetBinError(i))
    theErrorHisto.SetLineColor(0)
    theErrorHisto.SetLineWidth(0)
    theErrorHisto.SetMarkerStyle(0)
    theErrorHisto.SetFillStyle(3001)
    theErrorHisto.SetFillColor(15)
    return theErrorHisto


#make the ratio histograms and associated errors
def MakeRatioHistograms(dataHisto,backgroundStack,variable):
    ratioHist = dataHisto.Clone()

    denominatorHistos = dataHisto.Clone()
    denominatorHistos.Reset()
    for i in range(0,backgroundStack.GetNhists()):
        denominatorHistos.Add(backgroundStack.GetHists().At(i))
    ratioHist.Divide(denominatorHistos)
    finalRatioHist = ratioHist.Clone()
    for i in range(1,finalRatioHist.GetNbinsX()+1):
        try:
            finalRatioHist.SetBinError(i,dataHisto.GetBinError(i)/dataHisto.GetBinContent(i)*ratioHist.GetBinContent(i))
        except ZeroDivisionError:
            finalRatioHist.SetBinError(i,0)

    finalRatioHist.SetMarkerStyle(20)
    finalRatioHist.SetTitle("")
    finalRatioHist.GetYaxis().SetTitle("Data/Predicted")
    finalRatioHist.GetYaxis().SetTitleSize(0.1)
    finalRatioHist.GetYaxis().SetTitleOffset(0.32)
    finalRatioHist.GetYaxis().CenterTitle()
    finalRatioHist.GetYaxis().SetLabelSize(0.1)
    finalRatioHist.GetYaxis().SetNdivisions(6,0,0)
    #finalRatioHist.GetYaxis().SetRangeUser(1.3*1.05,0.7*0.95) #this doesn't seem to take effect here?    
    finalRatioHist.GetXaxis().SetTitleOffset(0.75)
    finalRatioHist.SetMaximum(1.3)
    finalRatioHist.SetMinimum(0.7)

    finalRatioHist.GetXaxis().SetLabelSize(0.1)

    finalRatioHist.GetXaxis().SetTitle(variableAxisTitleDictionary[variable])
    finalRatioHist.GetXaxis().SetTitleSize(0.14)

    MCErrors = ratioHist.Clone()
    MCErrors.Reset()
    for i in range(1,MCErrors.GetNbinsX()+1):
        MCErrors.SetBinContent(i,1.0)
        try:
            MCErrors.SetBinError(i,denominatorHistos.GetBinError(i)/denominatorHistos.GetBinContent(i))
        except ZeroDivisionError:
            MCErrors.SetBinError(i,0)
    MCErrors.SetFillStyle(3001)
    MCErrors.SetFillColor(15)
    MCErrors.SetMarkerStyle(0)

    return finalRatioHist,MCErrors



def main():
    parser = argparse.ArgumentParser(description='Generate control plots quick.')    
    parser.add_argument('--year',
                        nargs='?',
                        choices=['2016','2017','2018','test'],
                        help='Use the file\'s fake factor weightings when making plots for these files.',
                        required=True)
    parser.add_argument('--batchMode',
                        help='run in batch mode',
                        action='store_true')
    #parser.add_argument('--variables',
    #                    nargs='+',
    #                    help='Variables to draw the control plots for',
    #                    default=['pt_2',
    #                             'eta_2',
    #                             'pt_1',
    #                             'eta_1',
    #                             'm_vis',
    #                             'm_sv',
    #                             'njets',
    #                             'HiggsPt',
    #                             'met',
    #                             'DeltaR',
    #                             'mjj',
    #                             'abs(eta_1-eta_2)',
    #                             'jpt_1',
    #                             'jeta_1',
    #                             'jpt_2',
    #                             'jeta_2',])

    parser.add_argument('--variables',
                    nargs='+',
                    help='Variables to draw the control plots for',
                    #default=['nTau','nboostedTau'])
                    default=['Tau_pt',
                            'Tau_phi',
                            'Tau_eta',
                            'nboostedTau',
                            'nTau',
                            'FatJet_pt',
                            'FatJet_phi',
                            'FatJet_eta',
                            'nFatJet',
                            'Electron_pt',
                            'Electron_phi',
                            'Electron_eta',
                            'nElectron',
                            'MET_pt',
                            'MET_phi',
                            'MET_sumEt',
                            'Muon_pt',
                            'Muon_eta',
                            'Muon_phi',
                            'nMuon'])


    parser.add_argument('--additionalSelections',
                        nargs='+',
                        help='additional region selections',
                        #default=['Tau_idMVAoldDM2017v2 & 4 == 4','nTau==2 || nboostedTau==2','FatJet_btagDeepB > 0.45','nFatJet == 1'])
                        default=["PV_ndof > 4", "abs(PV_z) < 24","sqrt(PV_x*PV_x+PV_y*PV_y) < 2"])
    parser.add_argument('--pause',
                        help='pause after drawing each plot to make it easier to view',
                        action='store_true')
    parser.add_argument('--standardCutString',
                        nargs='?',
                        help='Change the standard cutting definition',
                        default='MET_pt>200')
    parser.add_argument('--changeHistogramBounds',
                        nargs = '?',
                        help = 'Change the standard histogram bounding (affects all histograms)')

    args = parser.parse_args()

    ROOT.gStyle.SetOptStat(0)
    if args.batchMode:
        ROOT.gROOT.SetBatch(ROOT.kTRUE)
    #change the standard cut definition if that's available

    

    if args.year == '2016':
        dataPath = '/data/aloeliger/bbtautauAnalysis/2016/'
    elif args.year == '2017':
        dataPath = '/data/aloeliger/SMHTT_Selected_2017_Deep/'
    elif args.year == '2018':
        dataPath = '/data/aloeliger/SMHTT_Selected_2018_Deep/'
    elif args.year == 'test':
        #dataPath = '/afs/hep.wisc.edu/home/parida/HHbbtt_Analysis_Scripts/Plotting_Scripts/'
        dataPath = "/hdfs/store/user/parida/HHbbtt_Background_Files/Andrew_Script_Skim/"

    #Open all the files that are necessary for plotting .......................#############################
    #for index in range(len(DatasetNameList)) 

    print DatasetNameList
    

    ########################################################################################################

    #For loop to draw histograms
    for variable in args.variables:
        try:
            variableSettingDictionary[variable] != None
        except KeyError:
            print("No defined histogram settings for variable: "+variable)
            continue
        try:
            variableAxisTitleDictionary[variable]
        except KeyError:
            print("No defined title information for variable: "+variable)
            continue

        if args.changeHistogramBounds != None:
            variableSettingDictionary[variable] = args.changeHistogramBounds


        ####Drawing the Histograms#######  
        DatasetObjects={}
        for index in range(len(DatasetNameList)) :
            DatasetObjects[DatasetNameList[index]]=MakeHistograms(dataPath,DatasetNameList[index],str(DatasetNameXSWeightDictionary[DatasetNameList[index]]))
            #DatasetObjects[DatasetNameList[index]]=MakeHistograms(dataPath,DatasetNameList[index])

        for index in range(len(DatasetNameList)):
            print DatasetNameList[index]
            DatasetObjects[DatasetNameList[index]].StandardDraw(DatasetObjects[DatasetNameList[index]].RootFileName,
                variable,
                args.standardCutString,
                args.additionalSelections,
                DatasetNameList[index],
                DatasetObjects[DatasetNameList[index]].userWeight)  
            #DatasetObjects[DatasetNameList[index]].FillEvents((DatasetObjects[DatasetNameList[index]].RootFileName),DatasetNameList[index])

        
        #######################DY-Histograms####################################
        DY_Histo = DatasetObjects["DYlow"].HistogramName.Clone()
        DY_Histo.Add(DatasetObjects["DY"].HistogramName)

        #PF_DY_Histo = DatasetObjects["DYJetsToLL_M-10to50"].PassFailHistogramName.Clone()
        #PF_DY_Histo.Add(DatasetObjects["DYJetsToLL_M-50"].PassFailHistogramName)
        ########################################################################
#
        ############################ST-Histograms############################################
        ST_Histo = DatasetObjects["ST_s-channel_4f"].HistogramName.Clone()

        #PF_ST_Histo = DatasetObjects["ST_s-channel_4f"].PassFailHistogramName.Clone()
        #####################################################################################
#
        ##############################QCD-Histograms##########################################
        QCD_Histo = DatasetObjects["QCD_120to170"].HistogramName.Clone()
        QCD_Histo.Add(DatasetObjects["QCD_1400to1800"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_15to30"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_170to300"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_1800to2400"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_2400to3200"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_300to470"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_30to50"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_3200toInf"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_470to600"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_800to1000"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_80to120"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_50to80"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_600to800"].HistogramName)
        QCD_Histo.Add(DatasetObjects["QCD_1000to1400"].HistogramName)

        #PF_QCD_Histo = DatasetObjects["QCD_Pt_120to170"].PassFailHistogramName.Clone()
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_1400to1800"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_15to30"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_170to300"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_1800to2400"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_2400to3200"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_300to470"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_30to50"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_3200toInf"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_470to600"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_800to1000"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_80to120"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_50to80"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_600to800"].PassFailHistogramName)
        #PF_QCD_Histo.Add(DatasetObjects["QCD_Pt_1000to1400"].PassFailHistogramName)


        #####################################################################################

        ##################################WJets##############################################
        WJets_Histo = DatasetObjects["W"].HistogramName.Clone()

        #PF_WJets_Histo = DatasetObjects["WJetsToLNu"].PassFailHistogramName.Clone()
        ######################################################################################
#
        ####################################TT-Histograms######################################
        TT_Histo = DatasetObjects["TTTo2L2Nu"].HistogramName.Clone()
        TT_Histo.Add(DatasetObjects["TTToHadronic"].HistogramName)
        TT_Histo.Add(DatasetObjects["TTToSemiLeptonic"].HistogramName)

        #PF_TT_Histo = DatasetObjects["TTTo2L2Nu"].PassFailHistogramName.Clone()
        #PF_TT_Histo.Add(DatasetObjects["TTToHadronic"].PassFailHistogramName)
        ########################################################################################
#
        ################################DiBoson-Histograms##########################################
        DiBoson_Histo = DatasetObjects["WW"].HistogramName.Clone()
        DiBoson_Histo.Add(DatasetObjects["WZ"].HistogramName)
        DiBoson_Histo.Add(DatasetObjects["ZZ"].HistogramName)

        #PF_DiBoson_Histo = DatasetObjects["WW"].PassFailHistogramName.Clone()
        #PF_DiBoson_Histo.Add(DatasetObjects["WZ"].PassFailHistogramName)
        #PF_DiBoson_Histo.Add(DatasetObjects["ZZ"].PassFailHistogramName)
        ################################################################################################

        ################################Data is represented as points########################################################################

        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.SetMarkerStyle(20)
        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.SetMarkerSize(1.5)
        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.Sumw2()

        #DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].PassFailHistogramName.SetMarkerStyle(20)
        #DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].PassFailHistogramName.SetMarkerSize(1.5)
        #DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].PassFailHistogramName.Sumw2()

        ################################Color_Definitions -- Background Fill##############################################
        color_DiBoson="#ff66c4"
        color_TT="#ff9e66"
        color_WJets="#ffe866"
        color_QCD="#d4ff66"
        color_ST="#66ffe8"
        color_DY="#bf66ff" 
        #color_jetfake="#f1cde1"

        #################################Filling Color for Backgrounds###############################################################################

        #ST_s_channel_4f.SetFillColor(ROOT.TColor.GetColor("#ffcc66"))

        DiBoson_Histo.SetFillColor(ROOT.TColor.GetColor(color_DiBoson))
        TT_Histo.SetFillColor(ROOT.TColor.GetColor(color_TT))
        WJets_Histo.SetFillColor(ROOT.TColor.GetColor(color_WJets))
        QCD_Histo.SetFillColor(ROOT.TColor.GetColor(color_QCD))
        ST_Histo.SetFillColor(ROOT.TColor.GetColor(color_ST))
        DY_Histo.SetFillColor(ROOT.TColor.GetColor(color_DY))

        #PF_DiBoson_Histo.SetFillColor(ROOT.TColor.GetColor(color_DiBoson))
        #PF_TT_Histo.SetFillColor(ROOT.TColor.GetColor(color_TT))
        #PF_WJets_Histo.SetFillColor(ROOT.TColor.GetColor(color_WJets))
        #PF_QCD_Histo.SetFillColor(ROOT.TColor.GetColor(color_QCD))
        #PF_ST_Histo.SetFillColor(ROOT.TColor.GetColor(color_ST))
        #PF_DY_Histo.SetFillColor(ROOT.TColor.GetColor(color_DY))

        #####################################Setting the line width to zero for all expect Data###########################################################################################################

        #for index in range(len(DatasetNameList)-1) :
         #   DatasetObjects[DatasetNameList[index]].HistogramName.SetLineWidth(0)

        for index in range(len(DatasetNameList)-1) :
            DatasetObjects[DatasetNameList[index]].HistogramName.SetLineWidth(0)
            #DatasetObjects[DatasetNameList[index]].PassFailHistogramName.SetLineWidth(0)


        

        ########################################Histograms For Shape Check###############################
        BackgroundShape = DY_Histo.Clone()
        BackgroundShape.Add(ST_Histo)
        BackgroundShape.Add(QCD_Histo)
        BackgroundShape.Add(WJets_Histo)
        BackgroundShape.Add(TT_Histo)
        BackgroundShape.Add(DiBoson_Histo)

        ScaleBackground = 1/BackgroundShape.Integral()

        DataShape = DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.Clone()
        
        ScaleData = 1/DataShape.Integral()

        DataShape.Scale(ScaleData)

        

        
        ###########################################Making the Stack of Histograms#####################################################################
        
        backgroundStack = ROOT.THStack('backgroundStack','backgroundstack')
        backgroundStack.Add(DY_Histo,'HIST')
        backgroundStack.Add(ST_Histo,'HIST')
        backgroundStack.Add(QCD_Histo,'HIST')
        backgroundStack.Add(WJets_Histo,'HIST')
        backgroundStack.Add(TT_Histo,'HIST')
        backgroundStack.Add(DiBoson_Histo,'HIST')
#
        backgroundStack_Errors = MakeStackErrors(backgroundStack)


        #PassFailStack = ROOT.THStack('PassFailStack','PassFailStack')
        #PassFailStack.Add(PF_DY_Histo,'HIST')
        #PassFailStack.Add(PF_ST_Histo,'HIST')
        #PassFailStack.Add(PF_QCD_Histo,'HIST')
        #PassFailStack.Add(PF_WJets_Histo,'HIST')
        #PassFailStack.Add(PF_TT_Histo,'HIST')
        #PassFailStack.Add(PF_DiBoson_Histo,'HIST')
#
        #PassFailStack_Errors = MakeStackErrors(PassFailStack)
        N_DY_Histo = (DY_Histo.Clone())
        N_ST_Histo = (ST_Histo.Clone())
        N_QCD_Histo = (QCD_Histo.Clone())
        N_WJets_Histo = (WJets_Histo.Clone())
        N_TT_Histo = (TT_Histo.Clone())
        N_DiBoson_Histo = (DiBoson_Histo.Clone())

        N_DY_Histo.Scale(ScaleBackground)
        N_ST_Histo.Scale(ScaleBackground) 
        N_QCD_Histo.Scale(ScaleBackground)
        N_WJets_Histo.Scale(ScaleBackground)
        N_TT_Histo.Scale(ScaleBackground)
        N_DiBoson_Histo.Scale(ScaleBackground)

        ShapeStack = ROOT.THStack('ShapeStack','ShapeStack')
        ShapeStack.Add(N_DY_Histo,'HIST')
        ShapeStack.Add(N_ST_Histo,'HIST')
        ShapeStack.Add(N_QCD_Histo,'HIST')
        ShapeStack.Add(N_WJets_Histo,'HIST')
        ShapeStack.Add(N_TT_Histo,'HIST')
        ShapeStack.Add(N_DiBoson_Histo,'HIST')

        ShapeStack_Errors = MakeStackErrors(ShapeStack)







        ##########################################Preparing the Canvas##################################################

        theCanvas = ROOT.TCanvas("theCanvas","theCanvas")
        theCanvas.Divide(1,2)
        
        plotPad = ROOT.gPad.GetPrimitive('theCanvas_1')
        ratioPad = ROOT.gPad.GetPrimitive('theCanvas_2')
        
        plotPad.SetPad("pad1","plot",0.0,0.20,1.0,1.0,0)
        ratioPad.SetPad("pad2","ratio",0.0,0.0,1.0,0.25,0)
#
        ratioPad.SetTopMargin(0.05)
        ratioPad.SetBottomMargin(0.27)
        plotPad.SetBottomMargin(0.08)
        plotPad.SetFrameLineWidth(1)
        ratioPad.SetGridy()
#
        ratioHist, ratioError = MakeRatioHistograms(DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName,backgroundStack,variable)
        ratioPad.cd()
        ratioHist.Draw('ex0')
        ratioError.Draw('SAME e2')
        ratioHist.Draw('SAME ex0')
#
        plotPad.cd()
        plotPad.SetFrameLineWidth(1)
        plotPad.SetTickx()
        plotPad.SetTicky()
#
        backgroundStack.SetMaximum(max(backgroundStack.GetMaximum(),DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.GetMaximum()))
        
        backgroundStack.Draw()
        backgroundStack_Errors.Draw('SAME e2')
        backgroundStack.SetTitle(variableAxisTitleDictionary[variable])
        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.Draw('SAME e1')
        #signalHisto.Draw('SAME HIST')
        backgroundStack.GetYaxis().SetTitle("Events")
        backgroundStack.GetYaxis().SetTitleOffset(1.58)
        backgroundStack.GetXaxis().SetLabelSize(0.0)

    ##############################Legend############################    

        theLegend = ROOT.TLegend(0.85, 0.45, 1.0, 0.75, "", "brNDC")
        theLegend.SetLineWidth(1)
        theLegend.SetLineStyle(1)
        theLegend.SetFillStyle(1001) #0
        theLegend.SetFillColor(0)
        theLegend.SetBorderSize(1)
        theLegend.SetTextFont(42)
        theLegend.AddEntry(DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName,'Observed','pe')
        theLegend.AddEntry(DiBoson_Histo,'DiBoson','f')
        theLegend.AddEntry(TT_Histo,'TTbar','f')
        theLegend.AddEntry(WJets_Histo,'WJets','f')
        theLegend.AddEntry(QCD_Histo,'QCD','f')
        theLegend.AddEntry(ST_Histo,'ST_s_Channel','f')
        theLegend.AddEntry(DY_Histo,'Drell-Yan','f')

        theLegend.Draw('SAME')
    ##############################################################################


    ##############################################################################
        #also draw the preliminary warnings
        cmsLatex = ROOT.TLatex()
        cmsLatex.SetTextSize(0.06)
        cmsLatex.SetNDC(True)
        cmsLatex.SetTextFont(61)
        cmsLatex.SetTextAlign(11)
        cmsLatex.DrawLatex(0.1,0.92,"CMS")
        cmsLatex.SetTextFont(52)
        cmsLatex.DrawLatex(0.1+0.08,0.92,"Preliminary")
    #################################################################################

    #######################################PASS FAIL CANVAS###########################################
        #PassFailCanvas = ROOT.TCanvas("PassFailCanvas","PassFailCanvas")
        #PassFailStack.SetMaximum(max(PassFailStack.GetMaximum(),DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].PassFailHistogramName.GetMaximum()))
        #PassFailStack.Draw()
        #PassFailStack_Errors.Draw('SAME e2')
        #PassFailStack.SetTitle("Trigger Pass Fail")
        #DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].PassFailHistogramName.Draw('SAME e1')
        #PassFailStack.GetYaxis().SetTitle("Events")
        #PassFailStack.GetYaxis().SetTitleOffset(1.58)
        #PassFailStack.GetXaxis().SetLabelSize(0.0)
        #theLegend.Draw()
        #cmsLatex = ROOT.TLatex()
        #cmsLatex.SetTextSize(0.06)
        #cmsLatex.SetNDC(True)
        #cmsLatex.SetTextFont(61)
        #cmsLatex.SetTextAlign(11)
        #cmsLatex.DrawLatex(0.1,0.92,"CMS")
        #cmsLatex.SetTextFont(52)
        #cmsLatex.DrawLatex(0.1+0.08,0.92,"Preliminary")

    #################################Shape Check Canvas########################################################
        ShapeCanvas = ROOT.TCanvas("ShapeCanvas","ShapeCanvas")
        ShapeCanvas.Divide(1,2)
        
        Shape_plotPad = ROOT.gPad.GetPrimitive('ShapeCanvas_1')
        Shape_ratioPad = ROOT.gPad.GetPrimitive('ShapeCanvas_2')
        
        Shape_plotPad.SetPad("Shape_pad1","Shape_plot",0.0,0.20,1.0,1.0,0)
        Shape_ratioPad.SetPad("Shape_pad2","Shape_ratio",0.0,0.0,1.0,0.25,0)
#
        Shape_ratioPad.SetTopMargin(0.05)
        Shape_ratioPad.SetFrameLineWidth(1)
        Shape_ratioPad.SetBottomMargin(0.27)
        Shape_plotPad.SetBottomMargin(0.08)
        Shape_ratioPad.SetGridy()
#
        Shape_ratioHist, Shape_ratioError = MakeRatioHistograms(DataShape,ShapeStack,variable)
        Shape_ratioPad.cd()
        Shape_ratioHist.Draw('ex0')
        Shape_ratioError.Draw('SAME e2')
        Shape_ratioHist.Draw('SAME ex0')
#
        Shape_plotPad.cd()
        Shape_plotPad.SetFrameLineWidth(1)
        Shape_plotPad.SetTickx()
        Shape_plotPad.SetTicky()
#
        ShapeStack.SetMaximum(max(ShapeStack.GetMaximum(),DataShape.GetMaximum()))
        
        ShapeStack.Draw()
        ShapeStack_Errors.Draw('SAME e2')
        ShapeStack.SetTitle(variableAxisTitleDictionary[variable])
        DataShape.Draw('SAME e1')
        #signalHisto.Draw('SAME HIST')
        ShapeStack.GetYaxis().SetTitle("Events Normalized")
        ShapeStack.GetYaxis().SetTitleOffset(1.58)
        ShapeStack.GetXaxis().SetLabelSize(0.0)

        theLegend2 = ROOT.TLegend(0.85, 0.45, 1.0, 0.75, "", "brNDC")
        theLegend2.SetLineWidth(1)
        theLegend2.SetLineStyle(1)
        theLegend2.SetFillStyle(1001) #0
        theLegend2.SetFillColor(0)
        theLegend2.SetBorderSize(1)
        theLegend2.SetTextFont(42)
        theLegend2.AddEntry(DataShape,'Observed','pe')
        theLegend2.AddEntry(N_DiBoson_Histo,'DiBoson','f')
        theLegend2.AddEntry(N_TT_Histo,'TTbar','f')
        theLegend2.AddEntry(N_WJets_Histo,'WJets','f')
        theLegend2.AddEntry(N_QCD_Histo,'QCD','f')
        theLegend2.AddEntry(N_ST_Histo,'ST_s_Channel','f')
        theLegend2.AddEntry(N_DY_Histo,'Drell-Yan','f')

        theLegend2.Draw('SAME')
        cmsLatex = ROOT.TLatex()
        cmsLatex.SetTextSize(0.06)
        cmsLatex.SetNDC(True)
        cmsLatex.SetTextFont(61)
        cmsLatex.SetTextAlign(11)
        cmsLatex.DrawLatex(0.1,0.92,"CMS")
        cmsLatex.SetTextFont(52)
        cmsLatex.DrawLatex(0.1+0.08,0.92,"Preliminary")



    #############################Saving The Plots####################################
        #theCanvas.SaveAs('QuickControlPlots/'+variable+'_'+args.year+'.png')
        theCanvas.SaveAs('QuickControlPlots/'+variable+'_'+args.year+'.pdf')
        #theCanvas.SaveAs('QuickControlPlots/'+variable+'_'+args.year+'.root')
        #ShapeCanvas.SaveAs('QuickControlPlots/'+ "Normalized" +variable+'_'+args.year+'.png')
        ShapeCanvas.SaveAs('QuickControlPlots/'+ "Normalized" +variable+'_'+args.year+'.pdf')
        #ShapeCanvas.SaveAs('QuickControlPlots/'+ "Normalized" +variable+'_'+args.year+'.root')
        #PassFailCanvas.SaveAs('QuickControlPlots/'+"Trigg_PF"+'_'+args.year+'.png')
        #PassFailCanvas.SaveAs('QuickControlPlots/'+"Trigg_PF"+'_'+args.year+'.pdf')
        #PassFailCanvas.SaveAs('QuickControlPlots/'+"Trigg_PF"+'_'+args.year+'.root')
    ##################################################################################    

        if args.pause:
            raw_input("Press Enter to Continue...")
        #this causes issues if you don't get rid of the canvas
        #I suspect it to be something to do with modifiying histograms that 
        # are alreayd referenced by the canvas in preparing the next one
        del theCanvas
        #del PassFailCanvas
        del ShapeCanvas

        #Delete the Objects created to avoid memory leaks
        del DatasetObjects


        #for index in range(len(DatasetNameList)) :
            #del DatasetObjects[DatasetNameList[index]]

    
    #ST_s_channel_4f_File.close()
    #TTTo2L2Nu_File.close()
    #Data_File.close()




if __name__ == '__main__':
    main()


