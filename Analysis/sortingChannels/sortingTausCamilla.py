from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from visibleMass import VisibleMass
import ROOT
import glob
#from particleClass import particle
from branchesList import *
import multiprocessing as  np
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class mergeTauCamilla(Module):
    def __init__(self,filename):
        print ("Running the sorting Taus Module")
        #self.channel = channel # Specify the channel
        self.filename = filename
        self.event =None
        self.branch_names_tau = dict()
        self.branch_names_btau = dict()
        self.tauCollection =  None
        self.boostedtauCollection = None
        self.event = None
    
    #lets define the branches that need to be filled
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
#        self.out.branch("nallTau","I")
#        type_dict = {"Float_t" : "F", "Int_t": "I", "Bool_t" : "O", "UChar_t": "I"}
#        for leaf in inputTree.GetListOfLeaves():
#            print (leaf)
#            lName = leaf.GetName()
#            if "_" not in lName:
#                continue
#            partName = lName[:lName.index("_")]
#            varName = lName[lName.index("_")+1:]
#            if partName == "gboostedTau":
#                self.branch_names_btau[varName] = type_dict[leaf.GetTypeName()]
#            if partName == "gTau":
#                self.branch_names_tau[varName] = type_dict[leaf.GetTypeName()]
#        
#        print (self.branch_names_btau,self.branch_names_tau)
#
#        for branch,branchType in self.branch_names_btau.iteritems(): 
#            for branch2, branchType2 in self.branch_names_tau.iteritems():
#                if branch==branch2:
#                    if (self.filename == "Data" and (branch == "genPartFlav" or branch =="genPartIdx")):
#                        break
#                    self.out.branch("{}_{}".format("allTau",branch),"{}".format(branchType),lenVar="n{}".format("allTau"))
#                    break

    def createBranches(self):
        self.out.branch("nallTau","I")
        type_dict = {"Float_t" : "F", "Int_t": "I", "Bool_t" : "O", "UChar_t": "I"}
        for leaf in self.tauCollection._event._tree.GetListOfLeaves():
            print (leaf)
            lName = leaf.GetName()
            if "_" not in lName:
                continue
            partName = lName[:lName.index("_")]
            varName = lName[lName.index("_")+1:]
            if partName == "boostedTau":
                self.branch_names_btau[varName] = type_dict[leaf.GetTypeName()]
            if partName == "Tau":
                self.branch_names_tau[varName] = type_dict[leaf.GetTypeName()]
        
        print (self.branch_names_btau,self.branch_names_tau)

        for branch,branchType in self.branch_names_btau.iteritems(): 
            for branch2, branchType2 in self.branch_names_tau.iteritems():
                if branch==branch2:
                    if (self.filename == "Data" and (branch == "genPartFlav" or branch =="genPartIdx")):
                        break
                    self.out.branch("{}_{}".format("allTau",branch),"{}".format(branchType),lenVar="n{}".format("allTau"))
                    break

            #self.out.branch("{}_{}".format("allTau",branch[0]),"{}".format(branch[1]),lenVar="n{}".format("allTau"))
    
    def fillBranches(self,colllist):
        if self.event.channel == 0:
            length = 2
        else:
            length =1
        self.out.fillBranch("nallTau",length)
        for branch in self.branch_names_tau.keys():           
            for branch2 in self.branch_names_btau.keys():
                if branch==branch2:
                    if (self.filename == "Data" and (branch == "genPartFlav" or branch=="genPartIdx")):
                        break
                    self.out.fillBranch("{}_{}".format("allTau",branch),self.get_attributes(branch,colllist))
                    break    
            #if (self.filename == "Data" and (branch[0] == "genPartFlav" or branch[0] =="genPartIdx")):
            #    continue
            #self.out.fillBranch("{}_{}".format("allTau",branch[0]),self.get_attributes(branch[0],colllist))

    def get_attributes(self,variable,collList):
        list = []
        for coll in collList:
            for obj in coll:
                list.append(obj[variable])
        #if variable == "pt":
            #print (list)
        return list

        #return [obj[variable] for obj in self.allTauCollection]
            

    def analyze(self,event):
        self.event = event
        self.tauCollection = Collection(event, "gTau","gnTau")
        print ("type of the collection = ",type(self.tauCollection),)
        self.boostedtauCollection = Collection(event, "gboostedTau","gnboostedTau")
        self.createBranches()

        #channelCollection = Collection(event,"channel")
        #print ("channel",channelCollection[0].channel)
        colllist =[]
        #print ("Type of the collection", type(tauCollection))
        #print ("MET",event.MET_pt)
        if event.channel == 0:
            if (len(self.tauCollection)==2):
                #self.allTauCollection = tauCollection
                colllist.append(self.tauCollection)
            if (len(self.boostedtauCollection)==2):
                #self.allTauCollection = boostedtauCollection
                colllist.append(self.boostedtauCollection)
            if (len(self.tauCollection)==1 or len(self.boostedtauCollection)==1):
                if self.tauCollection[0].pt >= self.boostedtauCollection[0].pt:
                    colllist.append(self.tauCollection)
                    colllist.append(self.boostedtauCollection)
                    #self.allTauCollection = tauCollection
                    #self.allTauCollection.extend(boostedtauCollection)

                else:
                    colllist.append(self.boostedtauCollection)
                    colllist.append(self.tauCollection)
                    #allTauCollection = boostedtauCollection
                    #allTauCollection.extend(tauCollection)
            self.fillBranches(colllist)
            return True    
        
        if (event.channel == 1  or event.channel == 2):
            if (len(self.tauCollection)==1):
                colllist.append(self.tauCollection)
            if (len(self.boostedtauCollection)==1):
                colllist.append(self.boostedtauCollection)
            self.fillBranches(colllist)
            return True
        



	
    
    
	
	
	













        
        

    
		


