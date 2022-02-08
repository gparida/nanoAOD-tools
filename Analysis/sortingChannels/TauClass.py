from branchesList import *
from particleClass import particle
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Tau(particle):
    def __init__(self, particleType):
        super(Tau,self).__init__(particleType)
