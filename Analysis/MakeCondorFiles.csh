#!/bin/sh

currentDir=${PWD}
outDir=${3}
#export CMSSW_RELEASE_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc630/cms/cmssw/CMSSW_9_4_1/
export CMSSW_RELEASE_BASE=/cvmfs/cms.cern.ch/slc7_amd64_gcc630/cms/cmssw/CMSSW_9_4_13/
cat> $outDir/Job_${2}.sh<<EOF
#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh 
cd $CMSSW_RELEASE_BASE
eval `scramv1 runtime -sh`
cd \${_CONDOR_SCRATCH_DIR}
python ${1} ${2}

EOF

chmod 775 $outDir/Job_${2}.sh
cat > $outDir/condor_${2}<<EOF
x509userproxy = /tmp/x509up_u10104
universe = vanilla
Executable = $outDir/Job_${2}.sh
Notification         = never
WhenToTransferOutput = On_Exit
ShouldTransferFiles  = yes
Requirements = (TARGET.UidDomain == "hep.wisc.edu" && TARGET.HAS_CMS_HDFS && OpSysAndVer == "CENTOS7" && TARGET.Arch == "X86_64" && (MY.RequiresSharedFS=!=true || TARGET.HasAFS_OSG) && (TARGET.OSG_major =!= undefined || TARGET.IS_GLIDEIN=?=true) && IsSlowSlot=!=true)
on_exit_remove       = (ExitBySignal == FALSE && (ExitCode == 0 || ExitCode == 42 || NumJobStarts>3))
+IsFastQueueJob      = True
getenv               = True
request_memory       = 1992
request_disk         = 2048000

#OutputDestination = ${outdir}
#Initialdir = Out_${2}         
Transfer_Input_Files = ${currentDir}/${1} , ${currentDir}/skim_test_gp.py , /afs/hep.wisc.edu/home/parida/Physics_Tools_NanoAOD_Tools_HHbbtt/CMSSW_10_6_25/src/PhysicsTools

output               = $outDir/\$(Cluster)_\$(Process)_${2}.out
error                = $outDir/\$(Cluster)_\$(Process)_${2}.err
Log                  = $outDir/\$(Cluster)_\$(Process)_${2}.log
Queue
EOF

condor_submit $outDir/condor_${2}
