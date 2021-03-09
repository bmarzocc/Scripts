#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
import itertools
import argparse
import operator
import os



if __name__ == '__main__':

  parser =  argparse.ArgumentParser(description='cat MVA')
  parser.add_argument('-d', '--inDir', dest='inDir', required=True, type=str)
  parser.add_argument('-m', '--min', dest='min', required=False, type=float)
  parser.add_argument('-M', '--max', dest='max', required=False, type=float)
  parser.add_argument('-r', '--massMin', dest='massMin', required=False, type=float)
  parser.add_argument('-R', '--massMax', dest='massMax', required=False, type=float)
   
  args = parser.parse_args()
  inDir = args.inDir

  min = -0.9
  if args.min: min = args.min
  max = 1.
  if args.max: max = args.max
  
  massMin = 115.
  if args.massMin: massMin = args.massMin
  massMax = 135.
  if args.massMax: massMax = args.massMax

  print "inDir:",inDir
  print "bdtMin:",min
  print "bdtMax:",max
  print "massMin:",massMin
  print "massMin:",massMax
  
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
GENMASS=$4
NBINS=$5;
MIN=$6
MAX=$7
MASSMIN=$8
MASSMAX=$9

echo -e "evaluate"
eval `scramv1 ru -sh`

echo -e "smoothing...";
python ${LOCAL}/smooth_BDT.py -d ${INPUTDIR} -g ${GENMASS} -n ${NBINS} --min ${MIN} --max ${MAX} --massMin ${MASSMIN} --massMax ${MASSMAX}

echo -e "DONE";
'''

  arguments=[]
  nBins = [30,60,120,190,380,760,1520]
  masses = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
  for mass  in masses:
     for iBin in nBins:
        for i  in range(0,4): 
           arguments.append("{} {} {} {} {} {} {} {} {}".format(1,local,inDir+"/"+str(mass)+"/",str(mass),iBin,min,max,massMin+i,massMax-i))     
  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments)) 
  with open("run_script.sh", "w") as rs:
     rs.write(script) 

