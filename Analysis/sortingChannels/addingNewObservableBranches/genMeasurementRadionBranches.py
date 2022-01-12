from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
import ROOT


import argparse
import glob
import multiprocessing as  np

class genMeasurementRadionBranches(Module):
    def __init__(self, filename):
        print("Storing the gen distributions for radion")
        print ("processing file ",filename)
        self.filename = filename
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        #creating separate branches just separating Radion from other gen particles
        self.out.branch("genRadion_pt","F")
        self.out.branch("genRadion_eta","F")
        self.out.branch("genRadion_phi","F")
        self.out.branch("genRadion_m", "F")

        #creating branches for radion reconstructed from gen Higgs
        self.out.branch("RecoGenRadion_pt","F")
        self.out.branch("RecoGenRadion_eta","F")
        self.out.branch("RecoGenRadion_phi","F")
        self.out.branch("RecoGenRadion_m", "F")

        def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
            pass
    

    def analyze(self, event):
        genParticles = Collection(event, 'GenPart', 'nGenPart')

        genParticleRadion = filter(lambda x: (x.mass==1000 or x.mass==1200 or x.mass==1400 or x.mass == 1600 or x.mass==1800 or x.mass==2000 or x.mass==2500 or x.mass==3000 or x.mass==3500 or x.mass==4000 or x.mass==4500) and x.pt>=1,genParticles)
        genParticlesHiggs = filter(lambda x: x.mass==125,genParticles)

        Higgs1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        Higgs2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)

        if len(genParticlesHiggs)==2:
            Higgs1.SetPtEtaPhiM(genParticlesHiggs[0].pt,genParticlesHiggs[0].eta,genParticlesHiggs[0].phi,genParticlesHiggs[0].mass)
            Higgs2.SetPtEtaPhiM(genParticlesHiggs[1].pt,genParticlesHiggs[1].eta,genParticlesHiggs[1].phi,genParticlesHiggs[1].mass)
            self.out.fillBranch("RecoGenRadion_m",abs((Higgs1+Higgs2).M()))
            self.out.fillBranch("RecoGenRadion_eta",abs((Higgs1+Higgs2).Eta()))
            self.out.fillBranch("RecoGenRadion_phi",abs((Higgs1+Higgs2).Phi()))
            self.out.fillBranch("RecoGenRadion_pt",abs((Higgs1+Higgs2).Pt()))
        else:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!More than two Higgs in Signal!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if len(genParticleRadion)>=1:
            self.out.fillBranch("genRadion_pt",genParticlesHiggs[0].pt)
            self.out.fillBranch("genRadion_eta",genParticlesHiggs[0].eta)
            self.out.fillBranch("genRadion_phi",genParticlesHiggs[0].phi)
            self.out.fillBranch("genRadion_m",genParticlesHiggs[0].mass)
        
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!More than one Radion in Signal!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print (genParticleRadion[0].pt,genParticleRadion[1].pt)


        return True
    

def call_postpoc(files):
	genMeasurementRadion = lambda:genMeasurementRadionBranches(filename)
	nameStrip=files.strip()
	filename = (nameStrip.split('/')[-1]).split('.')[-2]
	p = PostProcessor(outputDir,[files], cut=cuts,branchsel=outputbranches,modules=[genMeasurementRadion()], postfix=post,noOut=False,outputbranchsel=outputbranches)
	p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to add Radion Gen Measurement Branches')
	#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	parser.add_argument('--postfix',help="string at the end of output file names", default="")
	args = parser.parse_args()

	

	#Define Eevnt Selection - all those to be connected by or

	#fnames = ["/data/aloeliger/bbtautauAnalysis/2016/Data.root"]
	fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
	#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel".format(args.Channel)
	outputDir = args.outputLocation
	#outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cuts = None
	#post ="_{}Channel".format(str(args.Channel))
	post = args.postfix
	argList = list()
	filename =""
	for file in fnames:
		argList.append(file)
		#nameStrip = file.strip()
    	#filename = (nameStrip.split('/')[-1]).split('.')[-2]
	
	#print (argList)

	if int(args.ncores) == 1:
		for arr in argList:
			#print ("This is what is passed ",arr[1])
			call_postpoc(arr)
	
	else:
		pool = np.Pool(int(args.ncores))
		#with np.Pool(object,ncores) as pool:
		print ("list", argList)
		res=pool.map(call_postpoc, argList)
        





        






