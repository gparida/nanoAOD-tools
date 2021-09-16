import ROOT
import os
import json

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.b2gAnalysisWeights.pileupWeightingModule.pileupWeight import pileupWeight_2016


Radion_M3500Config = ReweightConfiguration()
Radion_M3500Config.name = 'Radion_M3500'
#Radion_M3500Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
Radion_M3500Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(Radion_M3500Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[Radion_M3500Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

Radion_M3500Config.inputFile = jsonInfo[Radion_M3500Config.name]['file']

crossSectionWeight.XS = jsonInfo[Radion_M3500Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[Radion_M3500Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


Radion_M3500Config.listOfWeights = [
    crossSectionWeight,
    pileupWeight_2016,
]