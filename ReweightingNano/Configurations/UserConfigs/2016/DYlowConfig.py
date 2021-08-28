import ROOT
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight


from Configurations.ConfigDefinition import ReweightConfiguration

DYConfiguration = ReweightConfiguration()
DYConfiguration.name = 'DYlow'
DYConfiguration.inputFile = "/data/aloeliger/bbtautauAnalysis/2016/DYlow.root"
crossSectionWeight.sample = 'DY'
crossSectionWeight.year = '2016'
totalEventsFile = ROOT.TFile.Open(DYConfiguration.inputFile)
crossSectionWeight.totalEvents=totalEventsFile.cutflow.GetBinContent(1)
totalEventsFile.Close()
DYConfiguration.listOfWeights = [
    crossSectionWeight,
    ]