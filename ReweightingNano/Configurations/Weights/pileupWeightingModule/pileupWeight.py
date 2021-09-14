import ROOT
from Configurations.Weights.WeightDefinition import Weight as Weight
from Configurations.Weights import b2gWeightPath

def calculatePileupWeight(self, theTree):
    pileupWeighting = 1.0

    pileupWeighting = self.dataHisto.GetBinContent(self.dataHisto.GetXaxis().FindBin(theTree.PV_npvs)) / self.mcHisto.GetBinContent(self.mcHisto.GetXaxis().FindBin(theTree.PV_npvs))

    self.value[0] = pileupWeighting

pileupWeight_2016 = Weight()
pileupWeight_2016.name = 'pileupWeighting'
pileupWeight_2016.mcHistoFilePath = b2gWeightPath+'mcPileupUL2016.root'
pileupWeight_2016.mcHistoFile = ROOT.TFile(pileupWeight_2016.mcHistoFilePath)
pileupWeight_2016.mcHisto = pileupWeight_2016.mcHistoFile.Get('pu_mc')
pileupWeight_2016.dataHistoFilePath = b2gWeightPath+'PileupHistogram-UL2016-100bins_withVar.root'
pileupWeight_2016.dataHistoFile = ROOT.TFile(pileupWeight_2016.dataHistoFilePath)
pileupWeight_2016.dataHisto = pileupWeight_2016.dataHistoFile.Get('pileup')
pileupWeight_2016.dataHistoUp = pileupWeight_2016.dataHistoFile.Get('pileup_plus')
pileupWeight_2016.dataHistoDown = pileupWeight_2016.dataHistoFile.Get('pileup_minus')
pileupWeight_2016.mcHisto.Scale(1.0/pileupWeight_2016.mcHisto.Integral())
pileupWeight_2016.dataHisto.Scale(1.0/pileupWeight_2016.dataHisto.Integral())
pileupWeight_2016.dataHistoUp.Scale(1.0/pileupWeight_2016.dataHistoUp.Integral())
pileupWeight_2016.dataHistoDown.Scale(1.0/pileupWeight_2016.dataHistoDown.Integral())
pileupWeight_2016.CalculateWeight = calculatePileupWeight

pileupWeight_2017 = Weight()
pileupWeight_2017.name = 'pileupWeighting'
pileupWeight_2017.mcHistoFilePath = b2gWeightPath+'mcPileupUL2017.root'
pileupWeight_2017.mcHistoFile = ROOT.TFile(pileupWeight_2017.mcHistoFilePath)
pileupWeight_2017.mcHisto = pileupWeight_2017.mcHistoFile.Get('pu_mc')
pileupWeight_2017.dataHistoFilePath = b2gWeightPath+'PileupHistogram-UL2017-100bins_withVar.root'
pileupWeight_2017.dataHistoFile = ROOT.TFile(pileupWeight_2017.dataHistoFilePath)
pileupWeight_2017.dataHisto = pileupWeight_2017.dataHistoFile.Get('pileup')
pileupWeight_2017.dataHistoUp = pileupWeight_2017.dataHistoFile.Get('pileup_plus')
pileupWeight_2017.dataHistoDown = pileupWeight_2017.dataHistoFile.Get('pileup_minus')
pileupWeight_2017.mcHisto.Scale(1.0/pileupWeight_2017.mcHisto.Integral())
pileupWeight_2017.dataHisto.Scale(1.0/pileupWeight_2017.dataHisto.Integral())
pileupWeight_2017.dataHistoUp.Scale(1.0/pileupWeight_2017.dataHistoUp.Integral())
pileupWeight_2017.dataHistoDown.Scale(1.0/pileupWeight_2017.dataHistoDown.Integral())
pileupWeight_2017.CalculateWeight = calculatePileupWeight

pileupWeight_2018 = Weight()
pileupWeight_2018.name = 'pileupWeighting'
pileupWeight_2018.mcHistoFilePath = b2gWeightPath+'mcPileupUL2018.root'
pileupWeight_2018.mcHistoFile = ROOT.TFile(pileupWeight_2018.mcHistoFilePath)
pileupWeight_2018.mcHisto = pileupWeight_2018.mcHistoFile.Get('pu_mc')
pileupWeight_2018.dataHistoFilePath = b2gWeightPath+'PileupHistogram-UL2018-100bins_withVar.root'
pileupWeight_2018.dataHistoFile = ROOT.TFile(pileupWeight_2018.dataHistoFilePath)
pileupWeight_2018.dataHisto = pileupWeight_2018.dataHistoFile.Get('pileup')
pileupWeight_2018.dataHistoUp = pileupWeight_2018.dataHistoFile.Get('pileup_plus')
pileupWeight_2018.dataHistoDown = pileupWeight_2018.dataHistoFile.Get('pileup_minus')
pileupWeight_2018.mcHisto.Scale(1.0/pileupWeight_2018.mcHisto.Integral())
pileupWeight_2018.dataHisto.Scale(1.0/pileupWeight_2018.dataHisto.Integral())
pileupWeight_2018.dataHistoUp.Scale(1.0/pileupWeight_2018.dataHistoUp.Integral())
pileupWeight_2018.dataHistoDown.Scale(1.0/pileupWeight_2018.dataHistoDown.Integral())
pileupWeight_2018.CalculateWeight = calculatePileupWeight
