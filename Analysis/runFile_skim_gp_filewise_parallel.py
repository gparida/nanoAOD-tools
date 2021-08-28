#from skim_test_gp import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import glob
import ROOT
from optparse import OptionParser
parser=OptionParser()

opts, args = parser.parse_args()

inputfile = str(args[0])
#haddname = str(args[1])

fnames = glob.glob(str(inputfile))

outputDir = "."

outputbranches = "keep_and_drop.txt"

cuts = "(nTau > 0 || nboostedTau > 0) && nFatJet > 0"

#p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[mySkimAdd()], postfix="Aug_3_condor_skim",noOut=False,haddFileName="Aug_3_hadd_test.root",fwkJobReport=True,outputbranchsel=outputbranches)
p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,postfix="_condor_skim",noOut=False,outputbranchsel=outputbranches)

#p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[mySkimAdd()],noOut=False, haddFileName=Output_post_processor_hadd.root,outputbranchsel=outputbranches)
p.run()
