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
  # parser.add_option(   "-i", "--input",     dest="input",     default="",   type="string", help="input root file" )
  parser.add_option(   "-m", "--max",     dest="max",     default="",   type="string", help="max" )
  # parser.add_option(   "-y", "--year",     dest="year",     default="",   type="string", help="year" )
  # parser.add_option(   "-o", "--output",     dest="output",     default="",   type="string", help="output" )


  (options, args) = parser.parse_args()

  # input     = options.input
  max     = options.max
  # year      = options.year
  # output    = options.output

  # print "input    =",input
  print "max      =",max
  # print "year     =",year
  # print "output    =",output


  inputDir = os.getcwd()
  if not os.path.isdir('error'): os.mkdir('error')
  if not os.path.isdir('output'): os.mkdir('output')
  if not os.path.isdir('log'): os.mkdir('log')

  # print max
  # for i in range(1,int(max)+1):
  #     print i

#   subset_len = len(list(itertools.combinations(range(nSteps), len(maxs))))
#   step = float(subset_len)/float(nBunch)
#   subset_min = []
#   subset_max = []
#   for i in range(nBunch):
#      subset_min.append(int(i*step))
#      subset_max.append(int((i+1)*step))
#
#   print "Number combinatorics: ", subset_len
#   print "Step: ", step
#
#   iSubset = 0
#   final_selection = ['']*nBunch
#   for subset in itertools.combinations(range(nSteps), len(maxs)):
#      selection_tmp = "1>0"
#      for ivar in range(len(subset)):
#         selection_tmp = selection_tmp +" && "+selections_perVar[ivar][int(subset[ivar])]
#      final_selection[int(iSubset/step)] = final_selection[int(iSubset/step)] + " / " + selection_tmp
#      #print iSubset,int(iSubset/step),final_selection[int(iSubset/step)]
#      iSubset=iSubset+1
#
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

  with open("condor_job.txt", "w") as cnd_out:
     cnd_out.write(condor)

  outputDir = os.getcwd()

  script = '''#!/bin/sh -e
INPUTEVENT=$1;
INPUTYEAR=$2;
INPUTERA=$3
INDIR=$4

python ${INDIR}/H4GTreeMixing.py  ${INPUTEVENT} ${INPUTYEAR} ${INPUTERA}
echo -e "DONE";
'''
  arguments=[]
  pwd = os.getcwd()
  #year = [2016]
  #eras = ['B','C','D','E','F','G','H']
  #year = [2017]
  #eras = ['B','C','D','E','F'] 
  year = [2018]
  eras = ['A','B','C','D']  
  #year = [2016, 2017, 2018]
  # max = 30
  for i in range(1,int(max)+1):
      for y in year:
          for era in eras:
              arguments.append("{} {} {} {}".format(i,y,era,pwd))
      # arguments.append("{} {}".format(input,i))
      # arguments.append("\""+"{} {} {}".format(input,i,"\'"+output)+"\"")
      # arguments.append("\""+"{} {} {} {}".format(input,"\'"+i+"\"",year+"\"",output)+"\"")

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)

