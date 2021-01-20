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
  parser.add_option( "-d", "--inDir",    dest="inDir",    default="",   type="string", help="inDir" )
  (options, args) = parser.parse_args()  

  inDir = options.inDir
 
  print "inDir:",inDir
  
  local = os.getcwd()
  if not os.path.isdir('error'): os.mkdir('error') 
  if not os.path.isdir('output'): os.mkdir('output') 
  if not os.path.isdir('log'): os.mkdir('log') 
   
  # Prepare condor jobs
  condor = '''executable              = run_script.sh
output                  = output/strips.$(ClusterId).$(ProcId).out
error                   = error/strips.$(ClusterId).$(ProcId).err
log                     = log/strips.$(ClusterId).log
transfer_input_files    = run_script.sh
on_exit_remove          = (ExitBySignal == False) && (ExitCode == 0)
periodic_release        = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > (60*60))
    
+JobFlavour             = "longlunch"
+AccountingGroup        = "group_u_CMS.CAF.ALCA"
queue arguments from arguments.txt
'''
  with open("condor_job.txt", "w") as cnd_out:
     cnd_out.write(condor)

  outputDir = os.getcwd()

  script = '''#!/bin/sh -e

JOBID=$1; 
LOCAL=$2; 
INPUTDIR=$3;
MASS=$4;

echo -e "evaluate"
eval `scramv1 ru -sh`

echo -e "Split trees";
python ${LOCAL}/split_Tree.py -i ${INPUTDIR}/signal_m_${MASS}.root

echo -e "DONE";
'''
  genMass = [15,20,25,30,35,40,45,50,55,60]
  arguments=[]
  for iBunch,mass in enumerate(genMass):
     arguments.append("{} {} {} {}".format(iBunch,local,inDir,mass))     
  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments)) 
  with open("run_script.sh", "w") as rs:
     rs.write(script) 

