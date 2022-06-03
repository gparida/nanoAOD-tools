from branchesList import *
from particleClass import particle

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Electron(particle):
    def __init__(self, particleType):
        super(Electron,self).__init__(particleType)

    def relativeIso(self,electronCollectionObject):
        if abs(electronCollectionObject.eta) <= 1.479:
            #if ((electronCollectionObject.TauCorrPfIso/electronCollectionObject.pt) < 0.175):
            if ((electronCollectionObject.pfRelIso03_all//electronCollectionObject.pt) < 0.175):
                return True
            else:
                return False
        elif ((abs(electronCollectionObject.eta) > 1.479) and (abs(electronCollectionObject.eta) <= 2.5)):
            if ((electronCollectionObject.pfRelIso03_all//electronCollectionObject.pt) < 0.159):
                return True
            else:
                return False
        else:
            return False






    
    
        

    
    
    
    
    
