#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
from optparse import OptionParser
import operator
import math  

def drawRatio(h_sig, h_bkg, label, name):

   gStyle.SetOptStat(0000)

   h_ratio = h_sig.Clone()
   h_ratio.Reset()

   for bin in range(1,h_sig.GetNbinsX()+1):
      if(h_bkg.GetBinContent(bin)>0.):
         h_ratio.SetBinContent(bin, h_sig.GetBinContent(bin)/math.sqrt(h_bkg.GetBinContent(bin)))         

   h_ratio.SetMarkerStyle(20)
   h_ratio.SetMarkerColor(kBlack)
   h_ratio.GetXaxis().SetTitle(label)
   h_ratio.GetYaxis().SetTitle("S/#sqrt{B}")  
   h_ratio.SetTitle(name)

   c = TCanvas()
   h_ratio.Draw("P")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

if __name__ == '__main__':
 
  ## Files used for Signal and Bkgs
  bkg_file = TChain()
  bkg_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only_noBlind/data_mix_transformedMVA.root/Data_13TeV_H4GTag_0')

  sig_file = TChain()
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_60_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_55_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_55_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_50_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_50_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_45_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_45_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_40_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_40_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_35_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_35_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_30_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_30_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_25_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_25_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_20_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_20_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_15_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_15_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_10_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_10_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
  sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/noSystematics/2016/hadd/CatMVA_PhoMVA_Only/signal_m_5_transformedMVA.root/SUSYGluGluToHToAA_AToGG_M_5_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0') 

  h_bdt_signal = TH1F('h_bdt_signal','h_bdt_signal',100,-1.,1.)
  h_bdt_bkg = TH1F('h_bdt_bkg','h_bdt_bkg',100,-1.,1.)

  h_bdtTransformed_signal = TH1F('h_bdtTransformed_signal','h_bdt_signal',100,0.,1.)
  h_bdtTransformed_bkg = TH1F('h_bdtTransformed_bkg','h_bdt_bkg',100,0.,1.)

  lumi = 36.773

  Cut_Signal = 'weight*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180 && pho1_MVA > -999. && pho2_MVA > -999. && pho3_MVA > -999. && pho4_MVA > -999)'

  Cut_Background = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180 && pho1_MVA > -999. && pho2_MVA > -999. && pho3_MVA > -999. && pho4_MVA > -999)' 

  sig_file.Draw("bdt>>h_bdt_signal",Cut_Signal)  
  sig_file.Draw("bdtTransformed>>h_bdtTransformed_signal",Cut_Signal)  

  bkg_file.Draw("bdt>>h_bdt_bkg",Cut_Background) 
  bkg_file.Draw("bdtTransformed>>h_bdtTransformed_bkg",Cut_Background) 

  h_bdt_signal.Scale(lumi)
  h_bdtTransformed_signal.Scale(lumi)

  h_bdt_bkg.Scale(1./10.)
  h_bdtTransformed_bkg.Scale(1./10.) 

  drawRatio(h_bdt_signal, h_bdt_bkg, 'bdt', 'bdt_significance')
  drawRatio(h_bdtTransformed_signal, h_bdtTransformed_bkg, 'bdtTransformed', 'bdtTransformed_significance')
  drawRatio(h_bdt_signal.GetCumulative(False), h_bdt_bkg.GetCumulative(False), 'bdt', 'bdt_significance_cumulative')
  drawRatio(h_bdtTransformed_signal.GetCumulative(False), h_bdtTransformed_bkg.GetCumulative(False), 'bdtTransformed', 'bdtTransformed_significance_cumulative')

  





  

