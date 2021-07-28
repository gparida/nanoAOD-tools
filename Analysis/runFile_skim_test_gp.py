from skim_test_gp
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import glob
import ROOT

fnames = glob.glob("/hdfs/store/user/parida/Skim_test/*.root")

outputDir = "/afs/hep.wisc.edu/home/parida/Skim_Test/"

outputbranches = "keep_and_drop.txt"

cuts = "(nTau > 0 || nboostedTau > 0) && nFatJet > 0"

p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[mySkimAdd()], postfix="_Skim_Done",noOut=False,outputbranchsel=outputbranches)
p.run()