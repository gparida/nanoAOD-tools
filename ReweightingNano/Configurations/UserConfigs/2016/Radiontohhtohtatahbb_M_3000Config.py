
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


Radiontohhtohtatahbb_M_3000Config = ReweightConfiguration()
Radiontohhtohtatahbb_M_3000Config.name = 'Radiontohhtohtatahbb_M-3000'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
Radiontohhtohtatahbb_M_3000Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(Radiontohhtohtatahbb_M_3000Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[Radiontohhtohtatahbb_M_3000Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

Radiontohhtohtatahbb_M_3000Config.inputFile = jsonInfo[Radiontohhtohtatahbb_M_3000Config.name]['file']
Radiontohhtohtatahbb_M_3000Config.inputFile_tt = jsonInfo[Radiontohhtohtatahbb_M_3000Config.name]['file_tt']
Radiontohhtohtatahbb_M_3000Config.inputFile_et = jsonInfo[Radiontohhtohtatahbb_M_3000Config.name]['file_et']
Radiontohhtohtatahbb_M_3000Config.inputFile_mt = jsonInfo[Radiontohhtohtatahbb_M_3000Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[Radiontohhtohtatahbb_M_3000Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[Radiontohhtohtatahbb_M_3000Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


Radiontohhtohtatahbb_M_3000Config.listOfWeights = list