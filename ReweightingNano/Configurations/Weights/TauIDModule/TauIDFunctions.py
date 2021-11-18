import ROOT

def CalculateTauIDWeight(self,theTree):
    self.value[0] = 1.0
    for tau in range(len(theTree.allTau_pt)):
        tauVector =  ROOT.TLorentzVector()
        tauVector.SetPtEtaPhiM(theTree.allTau_pt[tau],theTree.allTau_eta[tau],theTree.allTau_phi[tau],theTree.allTau_mass[tau])
        print ("pt value that is passed = ", tauVector.Pt())
        self.value[0] = self.value[0] * self.SFTool.getSFvsPT(tauVector.Pt(),genmatch=theTree.allTau_genPartFlav[tau])
        
