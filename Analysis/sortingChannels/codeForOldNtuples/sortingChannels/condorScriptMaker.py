#!/usr/bin/env python
#Essentially used when I want to parallelize jobs per file, that is, run one root file per job.
#List of full paths of the files per background and output directory taken as input
import os, sys,  imp, re, pprint, string
import argparse

# cms specific
import FWCore.ParameterSet.Config as cms

import time
import datetime
import os
import sys
import glob


parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
parser.add_argument('--Channel',help="enter either tt or et or mut",required=True)
parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
parser.add_argument('--outputLocation',help="storing location of the output files",default="")
args = parser.parse_args()


MYDIR=os.getcwd()
#print MYDIR

os.system("rm -rf Jobs_%s"%str(args.Channel))
os.system("mkdir Jobs_%s"%str(args.Channel))

for name in glob.glob(args.inputLocation + "/*.root"):
    print (name)
    nameStrip = name.strip()
    filename = (nameStrip.split('/')[-1]).split('.')[-2]
    print (filename)
    jobDir = MYDIR+'/Jobs_%s/%s/'%(str(args.Channel),str(filename))
    os.system('mkdir %s'%jobDir)

    tmp_jobname="sub_%s.sh"%(str(filename))
    tmp_job =open(jobDir+tmp_jobname,'w')
    tmp_job.write("#!/bin/sh\n")
    tmp_job.write("ulimit -S\n")
    tmp_job.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
    tmp_job.write("scramv1 project CMSSW CMSSW_10_6_25\n")
    tmp_job.write("cp -R PhysicsTools  CMSSW_10_6_25/src\n")
    tmp_job.write("cd CMSSW_10_6_25/src/PhysicsTools/NanoAODTools\n")
    tmp_job.write("eval `scramv1 runtime -sh`\n")
    tmp_job.write("scram b\n")
    tmp_job.write("cd Analysis/sortingChannels\n")
    tmp_job.write("python channelSorter.py --inputLocation %s --Channel %s\n"%(str(name),str(args.Channel)))
    tmp_job.write("xrdcp %s root://cmsxrootd.hep.wisc.edu//%s/.\n"%("*.root",str(args.outputLocation)))
    tmp_job.write("echo 'Job Completed Succesfully'\n")
    tmp_job.close()
    os.system('chmod +x %s'%(jobDir+tmp_jobname))

sub_total = open("condor_%s.jobb"%str(args.Channel),'w')
sub_total.write("x509userproxy = /tmp/x509up_u10104\n")
sub_total.write("universe = vanilla\n")
sub_total.write("executable = $(filename)\n")
sub_total.write("ShouldTransferFiles  = Yes\n")
sub_total.write("requirements = HAS_CMS_HDFS\n")
sub_total.write("+IsFastQueueJob      = True\n")
sub_total.write("getenv               = True\n")
sub_total.write("request_memory       = 2G\n")
sub_total.write("request_disk         = 3G\n")
sub_total.write("Transfer_Input_Files =/nfs_scratch/parida/channelSorting/CMSSW_10_6_25/src/PhysicsTools\n")
sub_total.write("output               = $Fp(filename)sorter.out\n")
sub_total.write("error                = $Fp(filename)sorter.err\n")
sub_total.write("Log                  = $Fp(filename)sorter.log\n")
sub_total.write("queue filename matching ("+MYDIR+"/Jobs_%s/*/*.sh)\n"%str(args.Channel))
	
	
	
	
	
	
	
	
	
	




