from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Utilities.RecursiveLoader import RecursiveLoader
from Configurations.ConfigDefinition import ReweightConfiguration
import argparse
import traceback
import sys
import glob
import ROOT
from array import array
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Handle script for performing final reweighting of events')
    parser.add_argument('--ConfigFiles',nargs = '+',help="Python based config files used to specify samples",required=True)

    args = parser.parse_args()
    theLoader= RecursiveLoader()    
    numErrors = 0

    for configFile in args.ConfigFiles:
    	try:
    		print("Loading from configFile: "+configFile)
            theConfigModule = theLoader.LoadFromDirectoryPath(configFile)
            for item in dir(theConfigModule):
                theConfig = getattr(theConfigModule,item)
                if isinstance(theConfig,ReweightConfiguration):
                    break

            listOfBranchesToAdd=[]
            listOfBranchesWithVariationToAdd=[]
            for weight in theConfig.listOfWeights:
            	
