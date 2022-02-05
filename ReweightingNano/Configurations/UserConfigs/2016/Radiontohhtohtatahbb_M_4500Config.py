
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


Radiontohhtohtatahbb_M_4500Config = ReweightConfiguration()
Radiontohhtohtatahbb_M_4500Config.name = 'Radiontohhtohtatahbb_M-4500'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
Radiontohhtohtatahbb_M_4500Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(Radiontohhtohtatahbb_M_4500Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[Radiontohhtohtatahbb_M_4500Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

Radiontohhtohtatahbb_M_4500Config.inputFile = jsonInfo[Radiontohhtohtatahbb_M_4500Config.name]['file']
Radiontohhtohtatahbb_M_4500Config.inputFile_tt = jsonInfo[Radiontohhtohtatahbb_M_4500Config.name]['file_tt']
Radiontohhtohtatahbb_M_4500Config.inputFile_et = jsonInfo[Radiontohhtohtatahbb_M_4500Config.name]['file_et']
Radiontohhtohtatahbb_M_4500Config.inputFile_mt = jsonInfo[Radiontohhtohtatahbb_M_4500Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[Radiontohhtohtatahbb_M_4500Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[Radiontohhtohtatahbb_M_4500Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


Radiontohhtohtatahbb_M_4500Config.listOfWeights = list
