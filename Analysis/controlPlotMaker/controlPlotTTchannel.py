from numbers import Integral
import ROOT
import argparse  ##Importing root and package to take arguments 
from controlPlotDictionaryCamilla import *
import os
from array import array

class MakeHistograms(object):
    #constructor to initialize the objects
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
        if standardCutString != None:
            cutString =weighting+'*('+'('+standardCutString+')'+' && '
            if otherCuts!=None:
                for cut in otherCuts:
                    cutString += '('+cut+')' + ' && '
        else:
            cutString=weighting +' && '
        cutString = cutString[:len(cutString)-3] # removing the && at the very end of the final cutstring
        cutString+=')'
        return cutString
        
    #Histogram Making member function and storing it in an attribute
    def StandardDraw(self,theFile,
                 variable,
                 standardCutString,
                 additionalSelections,
                 histogramName,
                 theWeight = 'FinalWeighting'):

        theTree = theFile.Get('Events')

        #print ('g'+variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
        #                 self.CreateCutString(standardCutString,
        #                                 additionalSelections,theWeight))
        ##
        #theTree.Draw('g'+variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
        #        self.CreateCutString(standardCutString,
        #                        additionalSelections,theWeight))
        ##print ("uhoh No g in it")
        print (variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
                         self.CreateCutString(standardCutString,
                                         additionalSelections,theWeight))
        
        theTree.Draw(variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
                self.CreateCutString(standardCutString,
                                additionalSelections,theWeight))
            



        
        #print ('g'+variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
        #                     self.CreateCutString(standardCutString,
        #                                     additionalSelections,theWeight))
        
        
        #3
    #so, if the tree has no entries, root doesn't even hand back an empty histogram
    #and therefore this ends up trying to get clone a none type
    #pass the None forward, and we can let the Add handle this
        try:
            theHisto = ROOT.gDirectory.Get(histogramName).Clone()
        except ReferenceError:
            theHisto = None
        #return theHisto
        self.HistogramName=theHisto

def clubHistograms(list,histObjects):
        clubHist = None
        for name in list:
            if histObjects[name].HistogramName != None:
                if clubHist == None:
                    clubHist = histObjects[name].HistogramName.Clone()
                clubHist.Add(histObjects[name].HistogramName)
        return clubHist

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
    #finalRatioHist.GetYaxis().SetTitleSize(0.1)
    finalRatioHist.GetYaxis().SetTitleSize(0.1)
    finalRatioHist.GetYaxis().SetTitleOffset(0.32)
    finalRatioHist.GetYaxis().CenterTitle()
    finalRatioHist.GetYaxis().SetLabelSize(0.1)
    finalRatioHist.GetYaxis().SetNdivisions(6,0,0)
    #finalRatioHist.GetYaxis().SetRangeUser(1.3*1.05,0.7*0.95) #this doesn't seem to take effect here?    
    finalRatioHist.GetXaxis().SetTitleOffset(0.83)
    finalRatioHist.SetMaximum(1.3)
    finalRatioHist.SetMinimum(0.7)
    finalRatioHist.GetYaxis().SetRangeUser(0.0,2.0)

    finalRatioHist.GetXaxis().SetLabelSize(0.15)

    finalRatioHist.GetXaxis().SetTitle(variableAxisTitleDictionary[variable])
    #finalRatioHist.GetXaxis().SetTitleSize(0.14)
    finalRatioHist.GetXaxis().SetTitleSize(0.17)

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

    parser.add_argument('--variables',
                    nargs='+',
                    help='Variables to draw the control plots for',
                    default=["gFatJet_pt",
                            "gFatJet_eta",
                            "gFatJet_msoftdrop",
                            "MET_pt",
                            "allTau_pt",
                            "allTau_eta",
                            #"gMuon_pt",
                            #"gMuon_eta",
                            #"gElectron_pt",
                            #"gElectron_eta",
                            "gDeltaR_LL"])
                            #"boostedTau_pt",
                            #"boostedTau_pt[0]",
                            #"boostedTau_pt[1]",
                            #"boostedTau_eta",
                            #"boostedTau_eta[0]",
                            #"boostedTau_phi",
                            #"boostedTau_phi[0]",
                            #"nTau",
                            #"Tau_pt",
                            #"Tau_pt[0]",
                            #"Tau_pt[1]",
                            #"Tau_eta",
                            #"Tau_eta[0]",
                            #"Tau_phi",
                            #"Tau_phi[0]",
                            #"nElectron",
                            #"nMuon",
                            #"boostedTau_idMVAnewDM2017v2",
                            #"Electron_mvaFall17V2Iso_WPL",
                            #"Electron_mvaFall17V2Iso_WP90",
                            #"Electron_pt",
                            #"Electron_pt[0]",
                            #"Electron_pt[1]",
                            #"Muon_mvaId",
                            #"Muon_pt",
                            #"Muon_eta",
                            #"Muon_phi",
                            #"boostedTau_decayMode",
                            #"boostedTau_idAntiEle2018",
                            #"Muon_pt[0]",
                            #"Muon_pt[1]",
                            #"nFatJet",
                            #"FatJet_pt",
                            #"FatJet_pt[0]",
                            #"FatJet_pt[1]",
                            #"FatJet_eta",
                            #"FatJet_eta[0]",
                            #"FatJet_phi",
                            #"FatJet_eta[1]",
                            #"FatJet_msoftdrop",
                            #"DeltaR_LL",
                            #"MVis_LL",
                            #"FatJet_msoftdrop[0]"]
                            #"FatJet_msoftdrop[1]",
                            #"FatJet_particleNet_HbbvsQCD",
                            #"FatJet_particleNet_HbbvsQCD[0]",
                            #"FatJet_particleNet_HbbvsQCD[1]",
                            #"FatJet_particleNetMD_Xbb",
                            #"FatJet_particleNetMD_Xbb[0]",
                            #"FatJet_particleNetMD_Xbb[1]",
                            #"FatJet_tau2/FatJet_tau1",
                            #"FatJet_tau2[0]/FatJet_tau1[0]",
                            #"FatJet_tau2[1]/FatJet_tau1[1]"]
                            #)
                    #default=['Tau_pt',
                    #       'Tau_phi',
                    #       'Tau_eta',
                    #       'nboostedTau',
                    #       'nTau',
                    #       'FatJet_pt',
                    #       'FatJet_phi',
                    #       'FatJet_eta',
                    #       'nFatJet',
                    #       'Electron_pt',
                    #       'Electron_phi',
                    #       'Electron_eta',
                    #       'nElectron',
                    #       'MET_pt',
                    #       'MET_phi',
                    #       'MET_sumEt',
                    #       'Muon_pt',
                    #       'Muon_eta',
                    #       'Muon_phi',
                    #       'nMuon'])


    parser.add_argument('--additionalSelections',
                        nargs='+',
                        help='additional region selections',
                        #default=['Tau_idMVAoldDM2017v2 & 4 == 4','nTau==2 || nboostedTau==2','FatJet_btagDeepB > 0.45','nFatJet == 1'])
                        #default=["PV_ndof > 4", "abs(PV_z) < 24","sqrt(PV_x*PV_x+PV_y*PV_y) < 2",
                        #"Flag_goodVertices",
                        #"Flag_globalSuperTightHalo2016Filter",
                        #"Flag_HBHENoiseIsoFilter",
                        #"Flag_HBHENoiseFilter",
                        #"Flag_EcalDeadCellTriggerPrimitiveFilter",
                        #"Flag_BadPFMuonFilter",
                        #"Flag_eeBadScFilter"])
                        default=["gDeltaR_LL<1.5","fastMTT_RadionLegWithMet_m>750","fastMTT_RadionLegWithMet_m<4250","gMVis_LL>0","(gFatJet_particleNetMD_Xbb / (gFatJet_particleNetMD_Xbb + gFatJet_particleNetMD_QCD))>=0.87"])
    parser.add_argument('--pause',
                        help='pause after drawing each plot to make it easier to view',
                        action='store_true')
    parser.add_argument('--standardCutString',
                        nargs='?',
                        help='Change the standard cutting definition',
                        default="channel==0")
    parser.add_argument('--changeHistogramBounds',
                        nargs = '?',
                        help = 'Change the standard histogram bounding (affects all histograms)')
    
    parser.add_argument('--logScale', help='make log plots', action='store_true')

    parser.add_argument('--Path',help='path to the files',required=True)
    parser.add_argument('--Weight',help='weight to be added to MC', default='FinalWeighting')

    args = parser.parse_args()

    ROOT.gStyle.SetOptStat(0)
    if args.batchMode:
        ROOT.gROOT.SetBatch(ROOT.kTRUE)
    #change the standard cut definition if that's available

    

    if args.year == '2016':
        #dataPath = '/data/gparida/Background_Samples/bbtautauAnalysis/2016/ChannelFiles_Camilla/'
        #dataPath = '/data/gparida/Background_Samples/bbtautauAnalysis/2016/ChannelFiles_Camilla_28Jan_2022/'
        dataPath = args.Path
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

        save_path = MYDIR=os.getcwd() + "/countingData"
        file_name = "Entries_MTChannel.txt"
        complete_Name =  os. path. join(save_path, file_name)
        file = open(complete_Name,"a")
        file.write("variable "+'\t'+ "Data Counts"+'\n')
		
        ####Drawing the Histograms#######  
        DatasetObjects={}
        for index in range(len(DatasetNameList)) :
            #DatasetObjects[DatasetNameList[index]]=MakeHistograms(dataPath,DatasetNameList[index],str(DatasetNameXSWeightDictionary[DatasetNameList[index]]))
            DatasetObjects[DatasetNameList[index]]=MakeHistograms(dataPath,DatasetNameList[index])

        for index in range(len(DatasetNameList)):
            print DatasetNameList[index]
            if DatasetNameList[index] == "Data":
                DatasetObjects[DatasetNameList[index]].StandardDraw(DatasetObjects[DatasetNameList[index]].RootFileName,
                variable,
                args.standardCutString,
                args.additionalSelections,
                DatasetNameList[index],theWeight='1')
            else:
                DatasetObjects[DatasetNameList[index]].StandardDraw(DatasetObjects[DatasetNameList[index]].RootFileName,
                    variable,
                    args.standardCutString,
                    args.additionalSelections,
                    DatasetNameList[index],theWeight=args.Weight)
                   # DatasetObjects[DatasetNameList[index]].userWeight)  
                #DatasetObjects[DatasetNameList[index]].FillEvents((DatasetObjects[DatasetNameList[index]].RootFileName),DatasetNameList[index])

        SignalObjects={}
        for index in range(len(SignalNameList)):
            SignalObjects[SignalNameList[index]]=MakeHistograms(dataPath,SignalNameList[index])
        
        for index in range(len(SignalNameList)):
            print SignalNameList[index]
            SignalObjects[SignalNameList[index]].StandardDraw(SignalObjects[SignalNameList[index]].RootFileName,
                variable,
                args.standardCutString,
                args.additionalSelections,
                SignalNameList[index])
            break
        
        ########################Signal-Histogram#############################
        Signal_Histo = SignalObjects["RadionTohhtohtatahbb_M-1000"].HistogramName.Clone()
        #####################################################################


        #######################DY-Histograms####################################

        DY_Histo = clubHistograms(["DYJetsToLL_M-10to50",
                                   "DYJets_HT-100to200",
                                   "DYJets_HT-200to400",
                                   "DYJets_HT-1200to2500",
                                   "DYJets_HT-2500toinf",
                                   "DYJets_HT-400to600",
                                   "DYJets_HT-600to800",
                                   "DYJets_HT-800to1200"],DatasetObjects)
        
	    

        ########################################################################
#
        ############################ST-Histograms############################################
        ST_Histo = clubHistograms(["ST_s-channel_4f",
                                "ST_t-channel_antitop_4f",
                                "ST_t-channel_top_4f",
                                "ST_tW_antitop_5f",
                                "ST_tW_top_5f"],DatasetObjects)

        #PF_ST_Histo = DatasetObjects["ST_s-channel_4f"].PassFailHistogramName.Clone()
        #####################################################################################
#
        ##############################QCD-Histograms##########################################
        QCD_Histo = clubHistograms(["QCD_HT1000to1500",
                                    "QCD_HT100to200",
                                    "QCD_HT1500to2000",
                                    "QCD_HT2000toinf",
                                    "QCD_HT200to300",
                                    "QCD_HT300to500",
                                    "QCD_HT500to700",
                                    "QCD_HT700to1000"],DatasetObjects)

        #####################################################################################

        ##################################WJets##############################################
        WJets_Histo = clubHistograms(["WJets_HT-100To200", 
                                      "WJets_HT-1200to2500",
                                      "WJets_HT-200to400", 
                                      "WJets_HT-2500toInf",
                                      "WJets_HT-400to600",
                                      "WJets_HT-600to800",
                                      "WJets_HT-800to1200"],DatasetObjects)

        ######################################################################################
#
        ####################################TT-Histograms######################################
        TT_Histo = clubHistograms(["TTTo2L2Nu",          
                                   "TTToHadronic",      
                                   "TTToSemiLeptonic"],DatasetObjects)
        ########################################################################################
#
        ################################DiBoson-Histograms##########################################
        DiBoson_Histo = clubHistograms(["WWTo1L1Nu2Q",
                                        "WZTo1L1nu2q",
                                        "WZTo2Q2Nu",
                                        "ZZTo2Q2Nu"],DatasetObjects)
        
        ################################################################################################

         ####################################Combine=ing Backgrounds########################################
        Other_Histo = clubHistograms(["WWTo1L1Nu2Q",
                        "WZTo1L1nu2q",
                        "WZTo2Q2Nu",
                        "ZZTo2Q2Nu",
                        "ST_s-channel_4f",    
                        "ST_t-channel_antitop_4f",
                        "ST_t-channel_top_4f",    
                        "ST_tW_antitop_5f",
                        "ST_tW_top_5f",
                        "QCD_HT1000to1500",
                        "QCD_HT100to200",
                        "QCD_HT1500to2000",
                        "QCD_HT2000toinf",
                        "QCD_HT200to300",
                        "QCD_HT300to500",
                        "QCD_HT500to700",
                        "QCD_HT700to1000"],DatasetObjects)
        #new_binning = array('d', [0,(100*6/3),(100*18/3), 1500])
        #Other_Histo = Other_Histo.Rebin(3, '', new_binning ) # for custom binning

        #print ("Number of bins in new histogram = ",Other_Histo.GetNbinsX())
        ################################Data is represented as points########################################################################


        ################################Data is represented as points########################################################################

        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.SetMarkerStyle(20)
        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.SetMarkerSize(0.7)
        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.Sumw2()
        #########################################Counting the events contributing##########################################################

        print ("Number of events in TTBar = ",TT_Histo.Integral())
        print ("Number of events in WJets = ",WJets_Histo.Integral())
        print ("Number of events in DY = ",DY_Histo.Integral())
        print ("Number of events in Others = ",Other_Histo.Integral())
        print ("Number of events of Data = ",DatasetObjects["Data"].HistogramName.Integral())
        ################################Color_Definitions -- Background Fill##############################################
        color_DiBoson="#ff66c4"
        color_TT="#6d9416"
        color_WJets="#76dfee"
        color_QCD="#d4ff66"
        color_ST="#66ffe8"
        color_DY="#e1b93e"
        color_other = "#ca35ff" 
        #color_jetfake="#f1cde1"

        #################################Filling Color for Backgrounds###############################################################################

        #ST_s_channel_4f.SetFillColor(ROOT.TColor.GetColor("#ffcc66"))
        Signal_Histo.SetLineColor(ROOT.kRed)
        Signal_Histo.Scale(0)
        Signal_Histo.SetLineWidth(1)

        DiBoson_Histo.SetFillColor(ROOT.TColor.GetColor(color_DiBoson))
        TT_Histo.SetFillColor(ROOT.TColor.GetColor(color_TT))
        WJets_Histo.SetFillColor(ROOT.TColor.GetColor(color_WJets))
        QCD_Histo.SetFillColor(ROOT.TColor.GetColor(color_QCD))
        ST_Histo.SetFillColor(ROOT.TColor.GetColor(color_ST))
        DY_Histo.SetFillColor(ROOT.TColor.GetColor(color_DY))
        Other_Histo.SetFillColor(ROOT.TColor.GetColor(color_other))

        DiBoson_Histo.SetLineWidth(0)
        TT_Histo.SetLineWidth(0)
        WJets_Histo.SetLineWidth(0)
        QCD_Histo.SetLineWidth(0)
        ST_Histo.SetLineWidth(0)
        DY_Histo.SetLineWidth(0)
        Other_Histo.SetLineWidth(0)
        
        ########################################Histograms For Shape Check###############################
        BackgroundShape = Other_Histo.Clone()
        #BackgroundShape.Add(ST_Histo)
        #BackgroundShape.Add(QCD_Histo)
        BackgroundShape.Add(DY_Histo)
        BackgroundShape.Add(WJets_Histo)
        BackgroundShape.Add(TT_Histo)
        
        #BackgroundShape.Add(DiBoson_Histo)
        #BackgroundShape.SetOptTitle(0)

        ScaleBackground = 1/BackgroundShape.Integral()

        DataShape = DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.Clone()

        file.write(variable + '\t' + str(DataShape.Integral())+'\n')
        
        ScaleData = 1/DataShape.Integral()

        DataShape.Scale(ScaleData)

        

        
        ###########################################Making the Stack of Histograms#####################################################################
        
        backgroundStack = ROOT.THStack('backgroundStack','backgroundstack')
        backgroundStack.Add(Other_Histo,'HIST')
        backgroundStack.Add(DY_Histo,'HIST')
        #backgroundStack.Add(ST_Histo,'HIST')
        #backgroundStack.Add(QCD_Histo,'HIST')
        backgroundStack.Add(WJets_Histo,'HIST')
        backgroundStack.Add(TT_Histo,'HIST')
        #backgroundStack.Add(DiBoson_Histo,'HIST')
        #backgroundStack.Add(Other_Histo,'HIST')

        #new_binning = array('d', [0,(100*6/3),(100*18/3), 1500])
        #backgroundStack = backgroundStack.Rebin(3,'',new_binning)
#
        backgroundStack_Errors = MakeStackErrors(backgroundStack)
#
        #PassFailStack_Errors = MakeStackErrors(PassFailStack)
        N_DY_Histo = (DY_Histo.Clone())
        N_ST_Histo = (ST_Histo.Clone())
        N_QCD_Histo = (QCD_Histo.Clone())
        N_WJets_Histo = (WJets_Histo.Clone())
        N_TT_Histo = (TT_Histo.Clone())
        N_DiBoson_Histo = (DiBoson_Histo.Clone())
        N_Other_Histo = (Other_Histo.Clone())

        N_DY_Histo.Scale(ScaleBackground)
        #N_ST_Histo.Scale(ScaleBackground) 
        #N_QCD_Histo.Scale(ScaleBackground)
        N_WJets_Histo.Scale(ScaleBackground)
        N_TT_Histo.Scale(ScaleBackground)
        #N_DiBoson_Histo.Scale(ScaleBackground)
        N_Other_Histo.Scale(ScaleBackground)

        ShapeStack = ROOT.THStack('ShapeStack','ShapeStack')
        ShapeStack.Add(N_DY_Histo,'HIST')
        #ShapeStack.Add(N_ST_Histo,'HIST')
        #ShapeStack.Add(N_QCD_Histo,'HIST')
        ShapeStack.Add(N_WJets_Histo,'HIST')
        ShapeStack.Add(N_TT_Histo,'HIST')
        ShapeStack.Add(N_Other_Histo,'HIST')
        #ShapeStack.Add(N_DiBoson_Histo,'HIST')

        ShapeStack_Errors = MakeStackErrors(ShapeStack)


        ##########################################Preparing the Canvas##################################################

        theCanvas = ROOT.TCanvas("theCanvas","theCanvas")
        theCanvas.Divide(1,2)
        
        plotPad = ROOT.gPad.GetPrimitive('theCanvas_1')
        ratioPad = ROOT.gPad.GetPrimitive('theCanvas_2')

        plotPad.SetPad("pad1","plot",0,0.25,1,1)
        plotPad.SetFillColor(0)
        plotPad.SetBorderMode(0)
        plotPad.SetBorderSize(1)
        plotPad.SetTickx(1)
        plotPad.SetTicky(1)
        #plotPad.SetGridx()
        plotPad.SetLeftMargin(0.15) #0.15
        plotPad.SetRightMargin(0.15) #0.1
        plotPad.SetTopMargin(0.14) #0.122 if the exponent is not present
        plotPad.SetBottomMargin(0.025)
        plotPad.SetFrameFillStyle(0)
        plotPad.SetFrameLineStyle(0)
        plotPad.SetFrameLineWidth(1) #1
        plotPad.SetFrameBorderMode(0)
        plotPad.SetFrameBorderSize(1)
        if args.logScale:
            plotPad.SetLogy(1)
        #plotPad.SetLogy(1)
        #plotPad.SetOptTitle(0)
        #
        ratioPad.SetPad("pad2","ratio",0,0,1,0.25)
        ratioPad.SetFillColor(0)
        ratioPad.SetTopMargin(0.02)
        ratioPad.SetBottomMargin(0.35)
        ratioPad.SetLeftMargin(0.15)
        ratioPad.SetRightMargin(0.15)
        ratioPad.SetTickx(1)
        ratioPad.SetTicky(1)
        ratioPad.SetFrameLineWidth(1)
        ratioPad.SetGridy()
        #pad2.SetGridx()
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
        maxi =max(backgroundStack.GetMaximum(),DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.GetMaximum(),Signal_Histo.GetMaximum())
        backgroundStack.SetMaximum(maxi + 0.5*maxi)
        
        backgroundStack.Draw()
        backgroundStack_Errors.Draw('SAME e2')
        #backgroundStack.SetTitle(variableAxisTitleDictionary[variable])
        backgroundStack.SetTitle("")
        DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName.Draw('SAME e1')
        Signal_Histo.Draw('SAME HIST')
        backgroundStack.GetYaxis().SetTitle("Events")
        backgroundStack.GetYaxis().SetTitleSize(0.065)
        backgroundStack.GetYaxis().SetLabelSize(0.05)
       #backgroundStack.GetYaxis().SetTitleOffset(1.58)
        backgroundStack.GetYaxis().SetTitleOffset(0.87)
        #backgroundStack.GetYaxis().SetTitleSize(1)
        backgroundStack.GetXaxis().SetLabelSize(0.0)

    ##############################Legend############################    

        theLegend = ROOT.TLegend(0.85, 0.45, 1.0, 0.75, "", "brNDC")
        theLegend.SetTextSize(0.03)
        theLegend.SetHeader("#tau-#tau Channel")
        theLegend.SetTextSize(0.03)
        theLegend.SetLineWidth(0)
        theLegend.SetLineStyle(1)
        theLegend.SetFillStyle(1001)#0
        theLegend.SetFillColor(0)
        theLegend.SetBorderSize(0)
        theLegend.SetTextFont(42)
        theLegend.AddEntry(DatasetObjects[DatasetNameList[len(DatasetNameList)-1]].HistogramName,'Observed','pe')
        #theLegend.AddEntry(DiBoson_Histo,'DiBoson','f')
        theLegend.AddEntry(TT_Histo,'TTbar','f')
        theLegend.AddEntry(WJets_Histo,'WJets','f')
        #theLegend.AddEntry(QCD_Histo,'QCD','f')
        #theLegend.AddEntry(ST_Histo,'ST_s_Channel','f')
        theLegend.AddEntry(DY_Histo,'Drell-Yan','f')
        theLegend.AddEntry(Other_Histo,'Others','f')
        theLegend.AddEntry(Signal_Histo,'Radion (#times 1)','l')

        theLegend.Draw('SAME')


        
    ##############################################################################


    ##############################################################################
        #also draw the preliminary warnings
        cmsLatex = ROOT.TLatex()
        cmsLatex.SetTextSize(0.06)
        cmsLatex.SetNDC(True)
        cmsLatex.SetTextFont(61)
        cmsLatex.SetTextAlign(11)
        #cmsLatex.DrawLatex(0.1,0.92,"CMS")
        cmsLatex.DrawLatex(0.15,0.92,"CMS")
        cmsLatex.SetTextFont(52)
        #cmsLatex.DrawLatex(0.1+0.08,0.92,"Preliminary")
        cmsLatex.DrawLatex(0.15+0.08,0.92,"Preliminary")

        cmsLatex.SetTextAlign(31)
        cmsLatex.SetTextFont(42)
        if args.year == '2016':
            lumiText = '16.81 fb^{-1}, 13 TeV'
        elif args.year == '2016APV':
            lumiText = '19.52 fb^{-1}, 13 TeV'
        elif args.year == '2017':
            lumiText = '41.48 fb^{-1}, 13 TeV'
        elif args.year == '2018':
            lumiText = '59.83 fb^{-1}, 13 TeV'
        #cmsLatex.DrawLatex(0.9,0.92,lumiText)
        cmsLatex.DrawLatex(0.85,0.87,lumiText)



    #############################################################################################

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
        theLegend2.SetHeader("#mu-#tau_{h} Channel","C")
        theLegend2.SetLineWidth(0)
        theLegend2.SetLineStyle(1)
        theLegend2.SetFillStyle(1001) #0
        theLegend2.SetFillColor(0)
        theLegend2.SetBorderSize(0)
        theLegend2.SetTextFont(42)
        theLegend2.AddEntry(DataShape,'Observed','pe')
         #theLegend2.AddEntry(N_DiBoson_Histo,'DiBoson','f')
        theLegend2.AddEntry(N_TT_Histo,'TTbar','f')
        theLegend2.AddEntry(N_WJets_Histo,'WJets','f')
        #theLegend2.AddEntry(N_QCD_Histo,'QCD','f')
        #theLegend2.AddEntry(N_ST_Histo,'ST_s_Channel','f')
        theLegend2.AddEntry(N_DY_Histo,'Drell-Yan','f')
        theLegend2.AddEntry(N_Other_Histo,'Others','f')
        #theLegend2.AddEntry(Signal_Histo,'Radion (#times 50)','l')

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
        theCanvas.SaveAs('TTPlots/'+variableAxisTitleDictionary[variable]+'_'+args.year+'.pdf')
        #theCanvas.SaveAs('QuickControlPlots/'+variable+'_'+args.year+'.root')
        #ShapeCanvas.SaveAs('QuickControlPlots/'+ "Normalized" +variable+'_'+args.year+'.png')
        ShapeCanvas.SaveAs('TTPlots/'+ "Normalized" +variableAxisTitleDictionary[variable]+'_'+args.year+'.pdf')
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
    file.close()

    
if __name__ == '__main__':
    main()


