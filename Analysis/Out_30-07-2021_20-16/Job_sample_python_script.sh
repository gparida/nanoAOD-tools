#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh 
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc630/cms/cmssw/CMSSW_9_4_13/
eval unset  SRT_CMSSW_RELEASE_BASE_SCRAMRTDEL;
export SRT_CMSSW_RELEASE_BASE_SCRAMRT="/cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_10_6_25";
export CMSSW_RELEASE_BASE="/cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_10_6_25";
export PATH="/cvmfs/cms.cern.ch/share/overrides/bin:/afs/hep.wisc.edu/user/parida/Physics_Tools_NanoAOD_Tools_HHbbtt/CMSSW_10_6_25/bin/slc7_amd64_gcc820:/afs/hep.wisc.edu/user/parida/Physics_Tools_NanoAOD_Tools_HHbbtt/CMSSW_10_6_25/external/slc7_amd64_gcc820/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_10_6_25/bin/slc7_amd64_gcc820:/cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_10_6_25/external/slc7_amd64_gcc820/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/llvm/7.1.0-pafccj/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/gcc/8.2.0-pafccj/bin:/afs/hep.wisc.edu/home/parida/.config/bin:/cvmfs/cms.cern.ch/common:/cvmfs/cms.cern.ch/common:/usr/local/bin/smb:/usr/local/bin/raid:/usr/lib64/qt-3.3/bin:/usr/local/etc:/usr/local/bin/hadoop:/usr/local/bin/firstboot:/usr/local/bin/cephdir:/usr/local/bin/afs:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin:/afs/hep.wisc.edu/home/parida/.fzf/bin:/afs/hep.wisc.edu/home/parida/bin";
cd ${_CONDOR_SCRATCH_DIR}
python runFile_skim_test_gp.py sample_python_script

