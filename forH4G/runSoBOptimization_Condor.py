#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
import itertools
from optparse import OptionParser
import operator
import os



if __name__ == '__main__':


  parser = OptionParser()
  parser.add_option(   "-v", "--vars",     dest="vars",     default="",   type="string", help="variables" )
  parser.add_option(   "-M", "--maxs",     dest="maxs",     default="",   type="string", help="max values" )
  parser.add_option(   "-m", "--mins",     dest="mins",     default="",   type="string", help="min values" )
  parser.add_option(   "-n", "--nSteps",   dest="nSteps",   default=1,    type="int",    help="nSteps" )
  parser.add_option(   "-b", "--nBunch",   dest="nBunch",   default=1,    type="int",    help="nBunch" ) 
  parser.add_option(   "-g", "--genMass",  dest="genMass",  default=60,   type="int",    help="genMass" )
  parser.add_option(   "",   "--maximize", dest="maximize", default="",   type="string", help="maximize" )
  (options, args) = parser.parse_args()  

  vars     = options.vars.split(',') 
  maxs     = options.maxs.split(',') 
  mins     = options.mins.split(',') 
  nSteps   = options.nSteps 
  nBunch   = options.nBunch 
  mass     = options.genMass
  maximize = options.maximize.split(',') 
  
  print "Mass     =",mass
  print "vars     =",vars
  print "maxs     =",maxs
  print "mins     =",mins
  print "Maximize =",maximize
  print "nSteps   =",nSteps
  print "nBunch   =",nBunch
  
  inputDir = os.getcwd()
  if not os.path.isdir('error_m'+str(mass)): os.mkdir('error_m'+str(mass)) 
  if not os.path.isdir('output_m'+str(mass)): os.mkdir('output_m'+str(mass)) 
  if not os.path.isdir('log_m'+str(mass)): os.mkdir('log_m'+str(mass)) 

  selections_perVar = [] 
  for i in range(len(maxs)):  
     step = (float(maxs[i])-float(mins[i]))/float(nSteps) 
     selections = [] 
     for s in range(nSteps):
        if maximize[i] == "1": selections.append(vars[i]+">"+str(float(mins[i])+s*float(step)))
        else: selections.append(vars[i]+"<"+str(float(maxs[i])-s*float(step)))
     selections_perVar.append(selections)
  
  subset_len = len(list(itertools.combinations(range(nSteps), len(maxs))))
  step = float(subset_len)/float(nBunch)
  subset_min = []
  subset_max = [] 
  for i in range(nBunch):
     subset_min.append(int(i*step))
     subset_max.append(int((i+1)*step))
     
  print "Number combinatorics: ", subset_len
  print "Step: ", step
   
  iSubset = 0
  final_selection = ['']*nBunch
  for subset in itertools.combinations(range(nSteps), len(maxs)):
     selection_tmp = "1>0"
     for ivar in range(len(subset)):
        selection_tmp = selection_tmp +" && "+selections_perVar[ivar][int(subset[ivar])]
     final_selection[int(iSubset/step)] = final_selection[int(iSubset/step)] + " / " + selection_tmp
     #print iSubset,int(iSubset/step),final_selection[int(iSubset/step)]
     iSubset=iSubset+1
     
  # Prepare condor jobs
  condor = '''executable              = run_script.sh
output                  = output/strips.$(ClusterId).$(ProcId).out
error                   = error/strips.$(ClusterId).$(ProcId).err
log                     = log/strips.$(ClusterId).log
transfer_input_files    = run_script.sh
on_exit_remove          = (ExitBySignal == False) && (ExitCode == 0)
periodic_release        = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > (60*60))
    
+JobFlavour             = "workday"
+AccountingGroup        = "group_u_CMS.CAF.ALCA"
queue arguments from arguments.txt
'''
  condor = condor.replace('output/strips','output_m'+str(mass)+'/strips')
  condor = condor.replace('error/strips','error_m'+str(mass)+'/strips')
  condor = condor.replace('log/strips','log_m'+str(mass)+'/strips') 

  with open("condor_job.txt", "w") as cnd_out:
     cnd_out.write(condor)

  outputDir = os.getcwd()

  script = '''#!/bin/sh -e

JOBID=$1; 
MASS=$2; 
INPUTDIR=$3;
INPUTSTRING=$4;
OUTPUTDIR=$5;

cd $INPUTDIR/

echo -e "evaluate"
eval `scramv1 ru -sh`

echo -e "Compute SoB";
python runSoBOptimization.py -g ${MASS}  -s \"${INPUTSTRING}\"

echo -e "DONE";
'''
  arguments=[]
  for iBunch in range(len(final_selection)):
     arguments.append("\""+"{} {} {} {} {}".format(iBunch,mass,inputDir,"\'"+final_selection[iBunch]+"\'",outputDir)+"\"")     
  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments)) 
  with open("run_script.sh", "w") as rs:
     rs.write(script) 

