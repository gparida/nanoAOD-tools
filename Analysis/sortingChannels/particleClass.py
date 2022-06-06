from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?
import traceback
import numpy as np

class particle(object):
	def __init__(self, particleType):
		self.particleType = particleType # What type of particle it is Tau, Jet etc
		self.collection = None
		self.branch_names = dict() #The keys of this dictionary will store name of the branches like the pt, eta, mass etc - the entries corresponding to the key will store the data type of the branch
		self.branches_setup = False

	#Create the new branches to be added for the selected objects. Specific bracnches for objects such as FatJets (softdropmass) can be added by writing a separate class that inherits base particle class
	def setUpBranches(self, wrappedOutputTree):
		if self.branches_setup:
			return
		
		length_name = "gn{}".format(self.particleType)
		wrappedOutputTree.branch(length_name,"I")
		for bName, bType in self.branch_names.iteritems():
			wrappedOutputTree.branch("g{}_{}".format(self.particleType, bName), bType, lenVar=length_name)
		
		self.branches_setup = True

	def setupCollectionforInitialization(self, event):
		self.collection = Collection(event,self.particleType)
		if self.branch_names:
			return
		
		print("here", self.particleType)
		type_dict = {"Float_t" : "F", "Int_t": "I", "Bool_t" : "O", "UChar_t": "I"}
		for leaf in self.collection._event._tree.GetListOfLeaves():
			lName = leaf.GetName()
			if "_" not in lName:
				continue
			partName = lName[:lName.index("_")]
			varName = lName[lName.index("_")+1:]
			if partName == self.particleType:
				self.branch_names[varName] = type_dict[leaf.GetTypeName()]


	def setupCollection(self, event):
		self.collection = Collection(event,self.particleType)
		if self.branch_names:
			return
		
		print("here", self.particleType)

	
	#Cuts more complicated for some objects could be added in a separate class that inherits particle class
	def apply_cut(self,l_func):
		if self.collection is None:
			return
		self.collection = filter(l_func,self.collection)
	

	def fillBranches(self,wrappedOutputTree):
		wrappedOutputTree.fillBranch("gn{}".format(self.particleType),len(self.collection))
		for bName in self.branch_names.keys():
			wrappedOutputTree.fillBranch("g{}_{}".format(self.particleType, bName), self.get_attributes(bName))
			

	def get_attributes(self,variable):
		try:
			dtype_dict = {"I": "int", "O": "bool", "F": "float"}
			dtype = dtype_dict[self.branch_names[variable]]
			return np.array([obj[variable] for obj in self.collection], dtype=dtype)

		except RuntimeError:
			print("here: ", self.particleType, variable)
			return []
	
