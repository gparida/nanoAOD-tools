import ROOT
from Configurations.Weights.WeightDefinition import Weight as Weight
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
import TauIDFunctions

tauIDWeight_2016 = Weight()
tauIDWeight_2016.name = 'TauIDWeight'
tauIDWeight_2016.SFTool = TauIDSFTool("2016Legacy","MVAoldDM2017v2","VLoose")
tauIDWeight_2016.CalculateWeight = TauIDFunctions.CalculateTauIDWeight
tauIDWeight_2016.hasUpDownUncertainties = True