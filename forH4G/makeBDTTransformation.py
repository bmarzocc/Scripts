#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
from optparse import OptionParser
import operator
import math 

if __name__ == '__main__':


  #parser = OptionParser()
  #parser.add_option( "-v", "--Var",    dest="var",    default="bdt",  type="string", help="variable" )
  
  #(options, args) = parser.parse_args()  
  #var = options.var

  #print "Var    = ", var

  var = "bdt"
  
  fileName_sig = '/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_60/22April2020_withreweighting_phoMVA_diffParamTrain/signal_m_60.root'
  treeName_sig = 'SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons'  
  f_sig = TFile(fileName_sig)   
  #f_sig = TFile('/eos/user/t/twamorka/1April2020_CatTrainign/vLoose_KinPlusPhotonID/signal_m_60.root')  
  #f_sig = TFile('/eos/user/t/twamorka/1April2020_CatTrainign/vLoose_OnlyKin/signal_m_60.root')    
  t_sig = f_sig.Get(treeName_sig)
  #print "t_sig      =",t_sig.GetEntries()

  fileName_data = '/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_60/22April2020_withreweighting_phoMVA_diffParamTrain/data_all.root'
  treeName_data = 'Data_13TeV_4photons'   
  f_data = TFile(fileName_data) 
  #f_data = TFile('/eos/user/t/twamorka/1April2020_CatTrainign/vLoose_KinPlusPhotonID/data_all.root') 
  #f_data = TFile('/eos/user/t/twamorka/1April2020_CatTrainign/vLoose_OnlyKin/data_all.root')   
  t_data = f_data.Get(treeName_data) 
  #print "t_data     =",t_data.GetEntries()

  fileName_data_mix = '/eos/user/t/twamorka/16April2020_Ntuples_BDTPairing/m_60/22April2020_withreweighting_phoMVA_diffParamTrain/data_mix_all.root' 
  treeName_data_mix = 'Data_13TeV_4photons'
  f_data_mix = TFile(fileName_data_mix) 
  #f_data_mix = TFile('/eos/user/t/twamorka/1April2020_CatTrainign/vLoose_KinPlusPhotonID/data_mix.root')  
  #f_data_mix = TFile('/eos/user/t/twamorka/1April2020_CatTrainign/vLoose_OnlyKin/data_mix.root')  
  t_data_mix = f_data_mix.Get(treeName_data_mix) 
  #print "t_data_mix =",t_data_mix.GetEntries()   

  xmin = -1.
  xmax = 1.
  precision = 0.000001
  nBins = int(1./precision)
  
  print "nBins = ", nBins

  #selection = "(1.>0.)"
  selection = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && (tp_mass > 110 && tp_mass < 180) && pho1_MVA>-0.9 && pho2_MVA>-0.9 && pho3_MVA>-0.9 && pho4_MVA>-0.9)" 

  histoMVA_sig = TH1F("histoMVA_sig","histoMVA_sig",int((xmax-xmin)/precision),xmin,xmax)
  t_sig.Draw("bdt >> histoMVA_sig","weight*36*"+selection,"goff")
  cumulativeHisto_sig = histoMVA_sig.GetCumulative()
  cumulativeHisto_sig.Scale(1./histoMVA_sig.Integral())
  cumulativeGraph_sig = TGraph(cumulativeHisto_sig)
  cumulativeGraph_sig.SetTitle("cumulativeGraph_sig")
  cumulativeGraph_sig.SetName("cumulativeGraph_sig")
  print "Cumulative done!" 

  print "Transforming signal..."
  f_sigTransformed = TFile.Open("signal_m_60_transformedMVA.root","recreate")
  chain_sig = TChain(t_sig.GetName())
  chain_sig.Add(fileName_sig)
  copyTree = chain_sig.CopyTree("")
  copyTree.SetName(treeName_sig)
  copyTree.SetTitle(treeName_sig)

  transfMVA = array( 'f', [ 0. ] )
  transfBranch = copyTree.Branch("bdtTransformed",transfMVA,"bdtTransformed/F");
  for i,event in enumerate(copyTree):
     if i>copyTree.GetEntries():break
     mva = event.bdt
     transfMVA[0] = cumulativeGraph_sig.Eval(mva)
     #print i, mva, transfMVA[0] 
     transfBranch.Fill()
  f_sigTransformed.Write()
  f_sigTransformed.Close()
 
  print "Transforming datamix..."
  f_bkgTransformed = TFile.Open("data_mixing_transformedMVA.root","recreate")
  chain_bkg = TChain(t_data_mix.GetName())
  chain_bkg.Add(fileName_data_mix)
  copyTree = chain_bkg.CopyTree("")
  copyTree.SetName(treeName_data_mix)
  copyTree.SetTitle(treeName_data_mix)

  transfMVA = array( 'f', [ 0. ] )
  transfBranch = copyTree.Branch("bdtTransformed",transfMVA,"bdtTransformed/F");
  for i,event in enumerate(copyTree):
     if i>copyTree.GetEntries():break
     mva = event.bdt
     transfMVA[0] = cumulativeGraph_sig.Eval(mva)
     #print i, mva, transfMVA[0] 
     transfBranch.Fill()
  f_bkgTransformed.Write()
  f_bkgTransformed.Close()

  print "Transforming data..." 
  f_dataTransformed = TFile.Open("data_all_transformedMVA.root","recreate")
  chain_data = TChain(t_data.GetName())
  chain_data.Add(fileName_data)
  copyTree = chain_data.CopyTree("")
  copyTree.SetName(treeName_data)
  copyTree.SetTitle(treeName_data)

  transfMVA = array( 'f', [ 0. ] )
  transfBranch = copyTree.Branch("bdtTransformed",transfMVA,"bdtTransformed/F");
  for i,event in enumerate(copyTree):
     if i>copyTree.GetEntries():break
     mva = event.bdt
     transfMVA[0] = cumulativeGraph_sig.Eval(mva)
     #print i, mva, transfMVA[0] 
     transfBranch.Fill()
  f_dataTransformed.Write()
  f_dataTransformed.Close()

  f_sigTransformed = TFile('signal_m_60_transformedMVA.root') 
  t_sigTransformed = f_sigTransformed.Get(treeName_sig)
  histoMVAtrans_sig = TH1F("histoMVAtrans_sig","histoMVAtrans_sig",100,0.,xmax) 
  histoMVAtrans_sig.Sumw2()
  t_sigTransformed.Draw("bdtTransformed >> histoMVAtrans_sig","weight*36*"+selection,"goff")
  
  f_bkgTransformed = TFile('data_mixing_transformedMVA.root') 
  t_bkgTransformed = f_bkgTransformed.Get(treeName_data_mix)
  histoMVAtrans_bkg = TH1F("histoMVAtrans_bkg","histoMVAtrans_bkg",100,0.,xmax) 
  histoMVAtrans_bkg.Sumw2()
  t_bkgTransformed.Draw("bdtTransformed >> histoMVAtrans_bkg",selection,"goff")

  histoMVAtrans_sig.Scale(0.5*500*histoMVAtrans_bkg.GetEntries()/histoMVAtrans_sig.GetEntries())
  histoMVAtrans_bkg.GetYaxis().SetRangeUser(0.001,1.5*histoMVAtrans_bkg.GetMaximum())

  #cumulativeGraph_sig.SetMarkerStyle(20)
  cumulativeGraph_sig.SetMarkerColor(kBlack)
  cumulativeGraph_sig.SetLineColor(kBlack)
  cumulativeGraph_sig.SetLineWidth(2)
  cumulativeGraph_sig.GetXaxis().SetTitle(var)
  cumulativeGraph_sig.GetYaxis().SetTitle("Cumulative") 

  #histoMVAtrans_sig.SetMarkerStyle(20)
  histoMVAtrans_sig.SetMarkerColor(kRed)
  histoMVAtrans_sig.SetLineColor(kRedi)
  histoMVAtrans_sig.SetLineWidth(2)
  histoMVAtrans_sig.GetXaxis().SetTitle(var+"_transformed")
  
  #histoMVAtrans_bkg.SetMarkerStyle(20)
  histoMVAtrans_bkg.SetMarkerColor(kBlue)
  histoMVAtrans_bkg.SetLineColor(kBlue)
  histoMVAtrans_bkg.SetLineWidth(2)
  histoMVAtrans_bkg.GetXaxis().SetTitle(var+"_transformed")
  
  gStyle.SetOptStat(0)

  c = TCanvas("c")

  c.cd()
  cumulativeGraph_sig.Draw("APL")
  c.SaveAs("cumulativeGraph_sig.png","png")
  c.SaveAs("cumulativeGraph_sig.pdf","pdf")

  c.cd()
  c.SetLogy() 
  histoMVAtrans_bkg.Draw("hist")
  histoMVAtrans_sig.Draw("hist,same")
  c.SaveAs("BDT_transformed_"+str(nBins)+"Bins.png","png")
  c.SaveAs("BDT_transformed_"+str(nBins)+"Bins.pdf","pdf")

  
  
