#!/usr/bin/python
import numpy as n
import ROOT 
import sys, getopt
from array import array
from optparse import OptionParser
import operator
import math  

def reduceTree(inTree, cut):
  small = inTree.CopyTree(str(cut))
  return small

if __name__ == '__main__':

  ROOT.gROOT.SetBatch(ROOT.kTRUE)

  parser = OptionParser()
  parser.add_option( "-v", "--var",      dest="var",      default="",    type="string", help="var" )
  parser.add_option( "-s", "--sel",      dest="sel",      default="",    type="string", help="sel" )
  parser.add_option( "-m", "--min",      dest="min",      default="-1.", type="float",  help="min" )
  parser.add_option( "-M", "--max",      dest="max",      default="1.",  type="float",  help="max" )
  parser.add_option( "-n", "--nsteps",   dest="nsteps",   default=1,     type="int",    help="nsteps" )
  parser.add_option( "-g", "--genMass",  dest="genMass",  default=60,    type="int",    help="genMass" )
  parser.add_option( "",   "--maximize", dest="maximize", default=1,     type="int",   help="maximize" )
  (options, args) = parser.parse_args()  

  var      = options.var
  sel      = options.sel
  min      = options.min 
  max      = options.max 
  nsteps   = options.nsteps 
  mass     = options.genMass 
  maximize = options.maximize
  
  print "Mass     =",mass
  if sel=="":
     print "Var      =",var
     print "Min      =",min
     print "Max      =",max
     print "nSteps   =",nsteps
     print "Maximize =",maximize
  else:
     print "Selection =",sel

  histo_scale = ROOT.TH1F("histo_scale","",100000,-1.1,1.)

  #Cut_noMass = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && pho1_MVA>=-1. && pho2_MVA>=-1. && pho3_MVA>=-1. && pho4_MVA>=-1. '
  Cut_noMass = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && pho1_MVA>-1. && pho2_MVA>0.75 && pho3_MVA>=-1. && pho4_MVA>=-1. '
  #Cut_SR = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1  && pho1_MVA>=-1. && pho2_MVA>=-1. && pho3_MVA>=-1. && pho4_MVA>=-1. && tp_mass > 100 && tp_mass < 180 && (tp_mass > 115 && tp_mass < 135) '
  Cut_SR = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1  && pho1_MVA>-1. && pho2_MVA>0.75 && pho3_MVA>=-1. && pho4_MVA>=-1. && tp_mass > 100 && tp_mass < 180 && (tp_mass > 115 && tp_mass < 135) '
  #Cut_SB = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1  && pho1_MVA>=-1. && pho2_MVA>=-1. && pho3_MVA>=-1. && pho4_MVA>=-1. && tp_mass > 100 && tp_mass < 180 && !(tp_mass > 115 && tp_mass < 135) '
  Cut_SB = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1  && pho1_MVA>-1. && pho2_MVA>0.75 && pho3_MVA>=-1. && pho4_MVA>=-1. && tp_mass > 100 && tp_mass < 180 && !(tp_mass > 115 && tp_mass < 135) '

  ### 2016 ###
  lumi_2016 = 35.9

  histo_scale.Reset() 
  data_tree_2016 = ROOT.TChain()
  data_tree_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_2016.root/tagsDumper/trees/Data_13TeV_H4GTag_0')
  data_tree_2016 = reduceTree(data_tree_2016,Cut_noMass+')')
  data_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale",Cut_SB+')')
  data_scale_2016 = float(histo_scale.Integral())
  
  histo_scale.Reset() 
  datamix_tree_2016 = ROOT.TChain()
  #datamix_tree_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_mix_2016_mvaWeight.root/Data_13TeV_H4GTag_0')
  datamix_tree_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_mix_2016_kinWeight.root/Data_13TeV_H4GTag_0')
  datamix_tree_2016 = reduceTree(datamix_tree_2016,Cut_noMass+')')
  datamix_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SB+')')
  datamix_scale_2016 = float(histo_scale.Integral())
  
  histo_scale.Reset() 
  sig_tree_2016 = ROOT.TChain()
  sig_tree_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+str(mass)+'_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SR+')')
  sig_scale_2016 = float(histo_scale.Integral())
  
  print "2016 Data/DataMix SB scale:",data_scale_2016/datamix_scale_2016
  
  ### 2017 ###
  lumi_2017 = 41.5

  histo_scale.Reset() 
  data_tree_2017 = ROOT.TChain()
  data_tree_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_2017.root/tagsDumper/trees/Data_13TeV_H4GTag_0')
  data_tree_2017 = reduceTree(data_tree_2017,Cut_noMass+')')
  data_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale",Cut_SB+')')
  data_scale_2017 = float(histo_scale.Integral())
  
  histo_scale.Reset() 
  datamix_tree_2017 = ROOT.TChain()
  #datamix_tree_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_mix_2017_mvaWeight.root/Data_13TeV_H4GTag_0')
  datamix_tree_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_mix_2017_kinWeight.root/Data_13TeV_H4GTag_0')
  datamix_tree_2017 = reduceTree(datamix_tree_2017,Cut_noMass+')')
  datamix_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SB+')')
  datamix_scale_2017 = float(histo_scale.Integral())
  
  histo_scale.Reset() 
  sig_tree_2017 = ROOT.TChain()
  sig_tree_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+str(mass)+'_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0')
  sig_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SR+')')
  sig_scale_2017 = float(histo_scale.Integral())

  print "2017 Data/DataMix SB scale:",data_scale_2017/datamix_scale_2017
  
  ### 2018 ###
  lumi_2018 = 54.38

  histo_scale.Reset() 
  data_tree_2018 = ROOT.TChain()
  data_tree_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_2018.root/tagsDumper/trees/Data_13TeV_H4GTag_0')
  data_tree_2018 = reduceTree(data_tree_2018,Cut_noMass+')')
  data_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale",Cut_SB+')')
  data_scale_2018 = float(histo_scale.Integral())
  
  histo_scale.Reset() 
  datamix_tree_2018 = ROOT.TChain()
  #datamix_tree_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_mix_2018_mvaWeight.root/Data_13TeV_H4GTag_0')
  datamix_tree_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_mix_2018_kinWeight.root/Data_13TeV_H4GTag_0') 
  datamix_tree_2018 = reduceTree(datamix_tree_2018,Cut_noMass+')')
  datamix_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SB+')')
  datamix_scale_2018 = float(histo_scale.Integral())
  
  histo_scale.Reset() 
  sig_tree_2018 = ROOT.TChain()
  sig_tree_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/HAHMHToAA_AToGG_MA_'+str(mass)+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0')
  sig_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SR+')')
  sig_scale_2018 = float(histo_scale.Integral())

  print "2018 Data/DataMix SB scale:",data_scale_2018/datamix_scale_2018
  
  histo_SR_sig_2016 = ROOT.TH1F("histo_SR_sig_2016","histo_SR_sig_2016",100000,-1,1) 
  histo_SR_datamix_2016 = ROOT.TH1F("histo_SR_datamix_2016","histo_SR_datamix_2016",100000,-1,1) 
  histo_SB_datamix_2016 = ROOT.TH1F("histo_SB_datamix_2016","histo_SB_datamix_2016",100000,-1,1)  
  histo_SB_data_2016 = ROOT.TH1F("histo_SB_data_2016","histo_SB_data_2016",100000,-1,1)
  
  histo_SR_sig_2017 = ROOT.TH1F("histo_SR_sig_2017","histo_SR_sig_2017",100000,-1,1) 
  histo_SR_datamix_2017 = ROOT.TH1F("histo_SR_datamix_2017","histo_SR_datamix_2017",100000,-1,1)
  histo_SB_datamix_2017 = ROOT.TH1F("histo_SB_datamix_2017","histo_SB_datamix_2017",100000,-1,1)  
  histo_SB_data_2017 = ROOT.TH1F("histo_SB_data_2017","histo_SB_data_2017",100000,-1,1)

  histo_SR_sig_2018 = ROOT.TH1F("histo_SR_sig_2018","histo_SR_sig_2018",100000,-1,1) 
  histo_SR_datamix_2018 = ROOT.TH1F("histo_SR_datamix_2018","histo_SR_datamix_2018",100000,-1,1) 
  histo_SB_datamix_2018 = ROOT.TH1F("histo_SB_datamix_2018","histo_SB_datamix_2018",100000,-1,1)  
  histo_SB_data_2018 = ROOT.TH1F("histo_SB_data_2018","histo_SB_data_2018",100000,-1,1)
 
  selection_photonID = " 1.>0. && "
  
  selections = ""
  step = abs(min-max)/float(nsteps)
  for i in range(nsteps):
     if maximize==1: selections += " / "+str(var)+">"+str(min+i*step)
     else: selections += " / "+str(var)+"<"+str(max-i*step)

  if sel!="":
     selections = sel

  selection_vec = selections.split('/')
  for iSel in range(len(selection_vec)):
 
     if selection_vec[iSel].isspace():
        continue
     if not selection_vec[iSel]:
        continue

     print "selection: ",selection_vec[iSel] 
     
     histo_SR_sig_2016.Reset()
     sig_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SR_sig_2016",str(lumi_2016)+'*weight*'+Cut_SR+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SB_data_2016.Reset()
     data_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SB_data_2016",Cut_SB+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SR_datamix_2016.Reset()
     datamix_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SR_datamix_2016",str(data_scale_2016/datamix_scale_2016)+'*weight*'+Cut_SR+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SB_datamix_2016.Reset()  
     datamix_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SB_datamix_2016",str(data_scale_2016/datamix_scale_2016)+'*weight*'+Cut_SB+'&& '+selection_photonID+selection_vec[iSel]+' )')
     
     histo_SR_sig_2017.Reset()
     sig_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SR_sig_2017",str(lumi_2017)+'*weight*'+Cut_SR+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SB_data_2017.Reset()
     data_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SB_data_2017",Cut_SB+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SR_datamix_2017.Reset()
     datamix_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SR_datamix_2017",str(data_scale_2017/datamix_scale_2017)+'*weight*'+Cut_SR+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SB_datamix_2017.Reset()  
     datamix_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SB_datamix_2017",str(data_scale_2017/datamix_scale_2017)+'*weight*'+Cut_SB+'&& '+selection_photonID+selection_vec[iSel]+' )')

     histo_SR_sig_2018.Reset()
     sig_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SR_sig_2018",str(lumi_2018)+'*weight*'+Cut_SR+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SB_data_2018.Reset()
     data_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SB_data_2018",Cut_SB+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SR_datamix_2018.Reset()
     datamix_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SR_datamix_2018",str(data_scale_2018/datamix_scale_2018)+'*weight*'+Cut_SR+'&& '+selection_photonID+selection_vec[iSel]+' )') 
     histo_SB_datamix_2018.Reset()  
     datamix_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_SB_datamix_2018",str(data_scale_2018/datamix_scale_2018)+'*weight*'+Cut_SB+'&& '+selection_photonID+selection_vec[iSel]+' )') 

     histo_SR_sig = histo_SR_sig_2016.Clone()
     histo_SR_sig.Add(histo_SR_sig_2017)
     histo_SR_sig.Add(histo_SR_sig_2018)
     histo_SR_sig.SetName('histo_SR_sig')
     histo_SR_sig.SetTitle('histo_SR_sig')

     histo_SB_data = histo_SB_data_2016.Clone()
     histo_SB_data.Add(histo_SB_data_2017)
     histo_SB_data.Add(histo_SB_data_2018)
     histo_SB_data.SetName('histo_SB_data')
     histo_SB_data.SetTitle('histo_SB_data') 

     histo_SB_datamix = histo_SB_datamix_2016.Clone()
     histo_SB_datamix.Add(histo_SB_datamix_2017)
     histo_SB_datamix.Add(histo_SB_datamix_2018)
     histo_SB_datamix.SetName('histo_SB_datamix')
     histo_SB_datamix.SetTitle('histo_SB_datamix') 

     histo_SR_datamix = histo_SR_datamix_2016.Clone()
     histo_SR_datamix.Add(histo_SR_datamix_2017)
     histo_SR_datamix.Add(histo_SR_datamix_2018)
     histo_SR_datamix.SetName('histo_SR_datamix')
     histo_SR_datamix.SetTitle('histo_SR_datamix') 

     print "histo_SR_sig     = ",histo_SR_sig.Integral()
     print "histo_SB_data    = ",histo_SB_data.Integral()
     print "histo_SB_datamix = ",histo_SB_datamix.Integral()
     print "histo_SR_datamix = ",histo_SR_datamix.Integral()
 
     s1 = histo_SR_sig.Integral()
     b1 = histo_SR_datamix.Integral() 
     b2 = histo_SB_datamix.Integral()
     b3 = histo_SB_data.Integral()
 
     score_data_mix = -999. 
     if b2>=8. and b1>0. and b3>=8.:
        #score_data_mix = pow(hist_window_sig.Integral(),2.)/hist_window_data_mix.Integral()
        score_data_mix = ((2*(s1+b1)*math.log(1+(s1/b1))) - 2*s1)  
        if score_data_mix>=0.: score_data_mix = math.sqrt((2*(s1+b1)*math.log(1+(s1/b1))) - 2*s1) 
        else: score_data_mix = -999.      
        
     print "score_data_mix =",score_data_mix," - nEvents in datamix:",b2," - nEvents in data sidebands:", b3

     
