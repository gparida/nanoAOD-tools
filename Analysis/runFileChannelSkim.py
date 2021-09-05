from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import glob
import ROOT
from optparse import OptionParser
parser=OptionParser()

parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
parser.add_argument('--Channel',help="enter either tt or et or mut",required=True)
parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")


try:

 	if Channel == "tt":
 		fnames = glob.glob(args.inputLocation)
 		outputDir = "."
 		cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2"
 		p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[lets()], postfix="_Skim_Done",noOut=False,outputbranchsel=outputbranches)
		p.run()

except Exception as error:
	print("Error!")