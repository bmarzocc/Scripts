#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
from optparse import OptionParser
import operator
import math  



if __name__ == '__main__':


  parser = OptionParser()
  parser.add_option( "-v", "--var",    dest="var",    default="",   type="string", help="var" )
  parser.add_option( "-s", "--sel",    dest="sel",    default="",   type="string", help="sel" )
  parser.add_option( "-m", "--min",    dest="min",    default="0.", type="float", help="min" )
  parser.add_option( "-M", "--max",    dest="max",    default="1.", type="float", help="max" )
  parser.add_option( "-n", "--nsteps", dest="nsteps", default=1,    type="int",    help="nsteps" )
  (options, args) = parser.parse_args()  

  var    = options.var
  sel    = options.sel
  min    = options.min 
  max    = options.max 
  nsteps = options.nsteps 
  
  if sel=="":
     print "Var    =",var
     print "Min    =",min
     print "Max    =",max
     print "nSteps =",nsteps
  else:
     print "Selection =",sel

  #f_sig = TFile('/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_60/21April2020_withreweighting_phoMVA_BDTPair_diffParamTrain/signal_m_60_transformedMVA.root')
  #f_sig = TFile('/eos/user/t/twamorka/1May2020_BDTPairing_withoutdeltaMVar_m60/1May2020_BDTPairing_withoutdeltaMVar_m60_phoMVA_BDTPair/signal_m_60_transformedMVA.root') 
  #t_sig = f_sig.Get('SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons')
  #f_sig = TFile('/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_15/24April2020_withreweighting_phoMVA_BDTPair/signal_m_15_transformedMVA.root')
  #t_sig = f_sig.Get('SUSYGluGluToHToAA_AToGG_M_15_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons')
  #print "t_sig      =",t_sig.GetEntries()
  chain_sig = TChain()
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_60/27April2020_withreweighting_phoMVA_BDTPair/signal_m_60_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_55/27April2020_withreweighting_phoMVA_BDTPair/signal_m_55_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_55_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_50/27April2020_withreweighting_phoMVA_BDTPair/signal_m_50_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_50_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_45/27April2020_withreweighting_phoMVA_BDTPair/signal_m_45_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_45_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_40/27April2020_withreweighting_phoMVA_BDTPair/signal_m_40_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_40_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_35/27April2020_withreweighting_phoMVA_BDTPair/signal_m_35_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_35_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_30/27April2020_withreweighting_phoMVA_BDTPair/signal_m_30_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_30_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_25/27April2020_withreweighting_phoMVA_BDTPair/signal_m_25_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_25_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons') 
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_20/27April2020_withreweighting_phoMVA_BDTPair/signal_m_20_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_20_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons')  
  chain_sig.AddFile('/eos/user/t/twamorka/26April2020_Ntuples_CommonBDTPairing/m_15/27April2020_withreweighting_phoMVA_BDTPair/signal_m_15_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_15_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons')    

  #f_data = TFile('/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_60/21April2020_withreweighting_phoMVA_BDTPair_diffParamTrain/data_all_transformedMVA.root')
  #f_data = TFile('/eos/user/t/twamorka/1May2020_BDTPairing_withoutdeltaMVar_m60/1May2020_BDTPairing_withoutdeltaMVar_m60_phoMVA_BDTPair/data_all_transformedMVA.root')
  f_data = TFile('/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_15/24April2020_withreweighting_phoMVA_BDTPair/data_all_transformedMVA.root')
  t_data = f_data.Get('Data_13TeV_4photons') 
  #print "t_data     =",t_data.GetEntries()

  #f_data_mix = TFile('/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_60/21April2020_withreweighting_phoMVA_BDTPair_diffParamTrain/data_mix_transformedMVA.root') 
  #f_data_mix = TFile('/eos/user/t/twamorka/1May2020_BDTPairing_withoutdeltaMVar_m60/1May2020_BDTPairing_withoutdeltaMVar_m60_phoMVA_BDTPair/data_mix_transformedMVA.root') 
  f_data_mix = TFile('/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_15/24April2020_withreweighting_phoMVA_BDTPair/data_mix_transformedMVA.root')  
  t_data_mix = f_data_mix.Get('Data_13TeV_4photons') 
  #print "t_data_mix =",t_data_mix.GetEntries()  

  xmin = -1.
  xmax = 1.
  precision = 0.0001

  hist_window_sig = TH1F("hist_window_sig","hist_window_sig",int((xmax-xmin)/precision),xmin,xmax); 
  hist_sideband_sig = TH1F("hist_sideband_sig","hist_sideband_sig",int((xmax-xmin)/precision),xmin,xmax);  
  hist_window_data_mix = TH1F("hist_window_data_mix","hist_window_data_mix",int((xmax-xmin)/precision),xmin,xmax); 
  hist_sideband_data_mix = TH1F("hist_sideband_data_mix","hist_sideband_data_mix",int((xmax-xmin)/precision),xmin,xmax);  
  hist_sideband_data_mix_noSel = TH1F("hist_sideband_data_mix_noSel","hist_sideband_data_mix_noSel",int((xmax-xmin)/precision),xmin,xmax);  
  hist_sideband_data = TH1F("hist_sideband_data","hist_sideband_data",int((xmax-xmin)/precision),xmin,xmax);

  #selection_photonID = " 1.>0. && "
  selection_photonID = " pho1_MVA>-0.9 && pho2_MVA>-0.9 && pho3_MVA>-0.9 && pho4_MVA>-0.9 && "

  selection_window_data = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && (tp_mass > 110 && tp_mass < 180) && ((tp_mass>115)&&(tp_mass<135)) && "+selection_photonID+" 1.>0.) "
  selection_sideband_data = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && (tp_mass > 110 && tp_mass < 180) && ((tp_mass<115)||(tp_mass>135)) && "+selection_photonID+" 1.>0.) "
  #t_data.Draw("pho1_MVA >> hist_window_data",selection_window_data) 
  t_data.Draw("pho1_MVA >> hist_sideband_data",selection_sideband_data)
  #t_data_mix.Draw("pho1_MVA >> hist_window_data_mix_noSel",selection_window_data) 
  t_data_mix.Draw("pho1_MVA >> hist_sideband_data_mix_noSel",selection_sideband_data)
 
  scale = -1.
  if hist_sideband_data_mix_noSel.Integral()>0.:
     scale = hist_sideband_data.Integral()/hist_sideband_data_mix_noSel.Integral()
  else: 
     print "WARNING: selections too tight, no events in datamix sideband!!"  
     sys.exit() 
      
  print "Datamix to data scaling: ",scale

  selections = ""
  step = abs(min-max)/float(nsteps)
  for i in range(nsteps):
     selections += " / "+str(var)+">"+str(min+i*step)

  if sel!="":
     selections = sel

  selection_vec = selections.split('/')
  for iSel in range(len(selection_vec)):
 
     if selection_vec[iSel].isspace():
        continue
     #if selection_vec[iSel].strip():
     #   continue
     if not selection_vec[iSel]:
        continue

     print "selection: ",selection_vec[iSel] 
     
     hist_window_sig.Reset()
     hist_sideband_sig.Reset()
     hist_window_data_mix.Reset()
     hist_sideband_data_mix.Reset()

     selection_window_sig = "weight*36.*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && (tp_mass > 110 && tp_mass < 180) && ((tp_mass>115)&&(tp_mass<135)) && "+selection_photonID+selection_vec[iSel]+") "
     selection_sideband_sig = "weight*36.*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && (tp_mass > 110 && tp_mass < 180) && ((tp_mass<115)||(tp_mass>135)) && "+selection_photonID+selection_vec[iSel]+") "
     #t_sig.Draw("pho1_MVA >> hist_window_sig",selection_window_sig)
     chain_sig.Draw("pho1_MVA >> hist_window_sig",selection_window_sig)
     #t_sig.Draw("pho1_MVA >> hist_sideband_sig",selection_sideband_sig)

     selection_window_data_mix = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && (tp_mass > 110 && tp_mass < 180) && ((tp_mass>115)&&(tp_mass<135)) && "+selection_photonID+selection_vec[iSel]+") "
     selection_sideband_data_mix = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && (tp_mass > 110 && tp_mass < 180) && ((tp_mass<115)||(tp_mass>135)) && "+selection_photonID+selection_vec[iSel]+") "
     t_data_mix.Draw("pho1_MVA >> hist_window_data_mix",selection_window_data_mix) 
     t_data_mix.Draw("pho1_MVA >> hist_sideband_data_mix",selection_sideband_data_mix)

     hist_window_data_mix.Scale(scale)
     hist_sideband_data_mix.Scale(scale)
     
     print "hist_window_sig        = ",hist_window_sig.Integral()
     print "hist_window_data_mix   = ",hist_window_data_mix.Integral()
     print "hist_sideband_data_mix = ",hist_sideband_data_mix.Integral()
 
     score_data_mix = -999. 
     if((hist_sideband_data_mix.Integral()+hist_window_data_mix.Integral())>=6. and hist_window_data_mix.Integral()>0. and hist_sideband_data_mix_noSel.Integral()>0.):
        score_data_mix = pow(hist_window_sig.Integral(),2.)/hist_window_data_mix.Integral()
        
     print "score_data_mix =",score_data_mix," - nEvents in datamix:",hist_sideband_data_mix.Integral()+hist_window_data_mix.Integral()

     
