from branchesList import *
from particleClass import particle


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class BoostedTau(particle):
    def __init__(self, particleType):
        super(BoostedTau,self).__init__(particleType)