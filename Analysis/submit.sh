
outDir="Out_$(date +"%d-%m-%Y_%H-%M")" 
mkdir $outDir 

###########################   MC  #########################

# run locally
#echo "run locally ........."
#python main.py

# run script on condor , with n arguments, n+1 th arg is for condor
echo "submit on condor ........."
./MakeCondorFiles.csh runFile_skim_test_gp.py  sample_python_script  $outDir
