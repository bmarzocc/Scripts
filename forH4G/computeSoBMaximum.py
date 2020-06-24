#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
from optparse import OptionParser
import operator
import os
import glob


if __name__ == '__main__':


  parser = OptionParser()
  parser.add_option(   "-i", "--inputDir",  dest="inputDir",   default="",      type="string",  help="inputDir" )

  (options, args) = parser.parse_args()  
  inputDir = options.inputDir
  print "Options: inputDir = ", inputDir

  file_list = os.listdir(inputDir)
  #print file_list 
  
  scores_bkg = []
  scores_data_mix = []
  for iFile in range(len(file_list)):
     #print iFile,inputDir+file_list[iFile]
     with open(inputDir+file_list[iFile]) as f_dump:
        data_dump = f_dump.read()
        lines_dump = data_dump.splitlines() 
        for pos,x in enumerate(lines_dump): 
           #print x.split()
           if "score_data_mix =" in x:       
              if x.split()[2]>0.: 
                 scores_data_mix.append([float(x.split()[2]),lines_dump[pos-5],float(x.split()[7]),float(x.split()[13])])

  print "----> ALL scores_data_mix:"           
  for iSel in range(len(scores_data_mix)) :
     print "scores_data_mix: ",scores_data_mix[iSel] 
  
  print "Best scores_data_mix: "
  print sorted(scores_data_mix)[len(scores_data_mix)-1] 
  print sorted(scores_data_mix)[len(scores_data_mix)-2] 
  print sorted(scores_data_mix)[len(scores_data_mix)-3] 
  print sorted(scores_data_mix)[len(scores_data_mix)-4] 
  print sorted(scores_data_mix)[len(scores_data_mix)-5] 
  print sorted(scores_data_mix)[len(scores_data_mix)-6] 
  print sorted(scores_data_mix)[len(scores_data_mix)-7] 
  print sorted(scores_data_mix)[len(scores_data_mix)-8] 
  print sorted(scores_data_mix)[len(scores_data_mix)-9] 
  print sorted(scores_data_mix)[len(scores_data_mix)-10] 
  print sorted(scores_data_mix)[len(scores_data_mix)-11] 
  print sorted(scores_data_mix)[len(scores_data_mix)-12] 
  print sorted(scores_data_mix)[len(scores_data_mix)-13] 
  print sorted(scores_data_mix)[len(scores_data_mix)-14] 
  print sorted(scores_data_mix)[len(scores_data_mix)-15] 
  print sorted(scores_data_mix)[len(scores_data_mix)-16] 
  print sorted(scores_data_mix)[len(scores_data_mix)-17] 
  print sorted(scores_data_mix)[len(scores_data_mix)-18] 
  print sorted(scores_data_mix)[len(scores_data_mix)-19] 
  print sorted(scores_data_mix)[len(scores_data_mix)-20] 
   
  
