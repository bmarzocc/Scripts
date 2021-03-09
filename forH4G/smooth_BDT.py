import ROOT
import argparse
import os
import math
from array import array

def findMin(vec):
  min = 999.
  for i in vec:
    if i<min: min=i
  return min  

def findMax(vec):
  max = -999.
  for i in vec:
    if i>max: max=i
  return max    

def nonZeroMin(h):
   min = 999.
   for bin in range(1,h.GetNbinsX()+1):
      if h.GetBinContent(bin)>0. and h.GetBinContent(bin)<min: min = h.GetBinContent(bin)
   return min
    
def isPositive(h):
   isPos = True
   for bin in range(1,h.GetNbinsX()+1):
     if h.GetBinContent(bin)<=0.: 
       isPos = False 
       break
   return isPos

def reduceTree(inTree, cut):
  small = inTree.CopyTree(str(cut))
  return small

def makeRatio(h_num,h_denom):
  h_ratio = h_num.Clone()
  h_ratio.Divide(h_denom) 
  return h_ratio

def MakeTree(inputTree, h_ratio, scale, ouputFile):
 outFile = ROOT.TFile(ouputFile, "RECREATE")
 inputTree.SetBranchStatus('bdt_weight',0)
 outTree = inputTree.CloneTree(0)
 bdt_weight = array('f', [0])
 _bdt_weight = outTree.Branch('bdt_weight', bdt_weight, 'bdt_weight/F')     
 nentries = inputTree.GetEntries()
 for i in range(0, nentries):
    inputTree.GetEntry(i)
    if h_ratio.GetBinContent(h_ratio.FindBin(inputTree.bdt))!=0.: 
        bdt_weight[0] = scale*float(h_ratio.GetBinContent(h_ratio.FindBin(inputTree.bdt)))
    else: bdt_weight[0] = scale 
    outTree.Fill() 
 outFile.cd()
 outTree.Write()
 outFile.Close()

def smoothing(h_bdt,method="SmoothSuper"):
 
 bin_min = h_bdt.GetBinCenter(1)-h_bdt.GetBinWidth(1)/2.
 bin_max = h_bdt.GetBinCenter(h_bdt.GetNbinsX())+h_bdt.GetBinWidth(h_bdt.GetNbinsX())/2.
 h_bdt_smooth = ROOT.TH1F(h_bdt.GetName()+"_smooth",h_bdt.GetName()+"_smooth",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_bdt_smooth_rnd = ROOT.TH1F(h_bdt.GetName()+"_smooth_rnd",h_bdt.GetName()+"_smooth_rnd",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_bdt_smooth_up = ROOT.TH1F(h_bdt.GetName()+"_smooth_up",h_bdt.GetName()+"_smooth_up",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_bdt_smooth_down = ROOT.TH1F(h_bdt.GetName()+"_smooth_down",h_bdt.GetName()+"_smooth_down",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_diff = ROOT.TH1F(h_bdt.GetName()+"_smoothing_Diff",h_bdt.GetName()+"_smoothing_Diff",200,-20.,20.)

 g_bdt = ROOT.TGraph()
 g_bdt_smooth = ROOT.TGraph() 
 smoother = ROOT.TGraphSmooth()

 for bin in range(0,h_bdt.GetNbinsX()): 
  g_bdt.SetPoint(bin,h_bdt.GetBinCenter(bin+1),h_bdt.GetBinContent(bin+1))
 if method=="SmoothLowess": g_bdt_smooth = smoother.SmoothLowess(g_bdt)
 elif method=="SmoothKern": g_bdt_smooth = smoother.SmoothKern(g_bdt)
 elif method=="SmoothSuper": g_bdt_smooth = smoother.SmoothSuper(g_bdt,"",0)
 else: 
    print "WARNING: unknown smoothing method!"
    return -1

 rnd = ROOT.TRandom()
 x = array('d', [0])
 y = array('d', [0])
 for bin in range(0,h_bdt_smooth.GetNbinsX()): 
  g_bdt_smooth.GetPoint(bin+1,x,y)
  h_bdt_smooth.SetBinContent(bin+1,y[0])
  h_bdt_smooth_rnd.SetBinContent(bin+1,rnd.Poisson(float(y[0])))
  
 h_bdt_smooth.Scale(h_bdt.Integral()/h_bdt_smooth.Integral())
 h_bdt_smooth_rnd.Scale(h_bdt.Integral()/h_bdt_smooth_rnd.Integral())

 for bin in range(0,h_bdt_smooth.GetNbinsX()): 
  y = h_bdt_smooth.GetBinContent(bin+1) 
  if y>=0.: 
     h_bdt_smooth_up.SetBinContent(bin+1,y+math.sqrt(y))
     if (y-math.sqrt(y))>0.: h_bdt_smooth_down.SetBinContent(bin+1,y-math.sqrt(y))
     else: h_bdt_smooth_down.SetBinContent(bin+1,0.)
  else:
     h_bdt_smooth_up.SetBinContent(bin+1,0.)
     h_bdt_smooth_down.SetBinContent(bin+1,0.)
  h_diff.Fill(y-h_bdt.GetBinContent(bin+1)) 

 return [h_bdt_smooth,h_bdt_smooth_up,h_bdt_smooth_down,h_bdt_smooth_rnd,h_diff] 

def compareHistos(hist_data_tmp,hist_datamix_tmp,name,rebin):

   ROOT.gStyle.SetOptStat(0000)
 
   hist_data = hist_data_tmp.Clone()
   hist_data.SetName(hist_data_tmp.GetName()+'_Rebin') 
   hist_data.Rebin(rebin)

   hist_datamix = hist_datamix_tmp.Clone()
   hist_datamix.SetName(hist_datamix_tmp.GetName()+'_Rebin') 
   hist_datamix.Rebin(rebin)
  
   hist_data.SetLineColor(ROOT.kBlack)
   hist_data.SetMarkerColor(ROOT.kBlack)
   hist_data.SetMarkerStyle(20)
   hist_datamix.SetLineColor(ROOT.kBlack)

   #hist_datamix.Scale(hist_data.Integral()/hist_datamix.Integral())

   min = nonZeroMin(hist_datamix)
   if min>nonZeroMin(hist_data): min = nonZeroMin(hist_data)
   max = hist_datamix.GetMaximum()
   if max<hist_data.GetMaximum(): max = hist_data.GetMaximum()
   hist_datamix.GetYaxis().SetRangeUser(min*0.5,max*2.)

   c = ROOT.TCanvas()
   #if isPositive(hist_datamix) and isPositive(hist_data): c.SetLogy()
   c.SetLogy()
   hist_datamix.Draw("HIST") 
   hist_data.Draw("P,same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

   ROOT.gStyle.SetOptStat(1111)

def drawHistos(hist,hist_smooth,hist_smooth_up,hist_smooth_down,name):

   ROOT.gStyle.SetOptStat(0000)

   mins = [float(nonZeroMin(hist)),float(nonZeroMin(hist_smooth)),float(nonZeroMin(hist_smooth_up)),float(nonZeroMin(hist_smooth_down))]
   maxs = [float(hist.GetMaximum()),float(hist_smooth.GetMaximum()),float(hist_smooth_up.GetMaximum()),float(hist_smooth_down.GetMaximum())]
   
   minimum = findMin(mins)
   maximum = findMax(maxs)
   hist.SetLineColor(ROOT.kBlack)
   hist_smooth.SetLineColor(ROOT.kRed)
   hist_smooth_up.SetLineColor(ROOT.kGreen)
   hist_smooth_down.SetLineColor(ROOT.kBlue)
   hist.GetYaxis().SetRangeUser(minimum*0.5,2.*maximum)
   hist.GetXaxis().SetTitle('bdt')
   
   title = name
   hist.SetTitle(title.replace('h_',''))

   leg = ROOT.TLegend(0.70,0.7,0.85,0.88)
   leg.SetFillColor(ROOT.kWhite)
   leg.SetFillStyle(1000)
   leg.SetLineWidth(0)
   leg.SetLineColor(ROOT.kWhite)
   leg.SetTextFont(42)
   leg.SetTextSize(0.035)
   leg.AddEntry(hist_smooth_up,"Smoothing + #sigma","L")
   leg.AddEntry(hist_smooth,"Smoothing ","L")
   leg.AddEntry(hist_smooth_down,"Smoothing - #sigma","L")
   
   c = ROOT.TCanvas()
   #if isPositive(hist) and isPositive(hist_smooth) and isPositive(hist_smooth_up) and isPositive(hist_smooth_down): c.SetLogy()
   c.SetLogy()
   hist.Draw("HIST") 
   hist_smooth.Draw("HIST,same")
   hist_smooth_up.Draw("HIST,same")
   hist_smooth_down.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

   ROOT.gStyle.SetOptStat(1111)

def drawHisto(hist,name):

   ROOT.gStyle.SetOptStat(1111)

   hist.SetLineColor(ROOT.kBlack)
   
   c = ROOT.TCanvas()
   hist.Draw("HIST") 
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

if __name__ == '__main__': 

 ROOT.gROOT.SetBatch(ROOT.kTRUE)

 parser =  argparse.ArgumentParser(description='cat MVA')
 parser.add_argument('-d', '--inDir', dest='inDir', required=True, type=str)
 parser.add_argument('-g', '--genMass', dest='genMass', required=True, type=str)
 parser.add_argument('-n', '--nBins', dest='nBins', required=False, type=int)
 parser.add_argument('-m', '--min', dest='min', required=False, type=float)
 parser.add_argument('-M', '--max', dest='max', required=False, type=float)
 parser.add_argument('-r', '--massMin', dest='massMin', required=False, type=float)
 parser.add_argument('-R', '--massMax', dest='massMax', required=False, type=float)
 
 args = parser.parse_args()
 inDir = args.inDir
 #inDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/'
 #inDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2/'

 nBins = 190
 if args.nBins: nBins = args.nBins
 min = -0.9
 if args.min: min = args.min
 max = 1.
 if args.max: max = args.max
 
 massMin = 115.
 if args.massMin: massMin = args.massMin
 massMax = 135.
 if args.massMax: massMax = args.massMax

 mass = args.genMass
 #mass = 60

 print "inDir:",inDir
 print "nBins:",nBins
 print "bdtMin:",min
 print "bdtMax:",max
 print "massMin:",massMin
 print "massMax:",massMax
 print "Mass:",mass

 histo_scale = ROOT.TH1F("histo_scale","",100000,-1.1,1.)
 Cut_noMass = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && bdt>-0.9)'
 Cut_SR = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 100 && tp_mass < 180 && (tp_mass > '+str(massMin)+' && tp_mass < '+str(massMax)+') && bdt>-0.9 )'
 Cut_SB = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 100 && tp_mass < 180 && !(tp_mass > 115 && tp_mass < 135) && bdt>-0.9 )'
 
 h_bdt_signal_SB_2016 = ROOT.TH1F("h_bdt_signal_SB_2016","h_bdt_signal_SB_2016",int(nBins),float(min),float(max)) 
 h_bdt_signal_SB_2017 = ROOT.TH1F("h_bdt_signal_SB_2017","h_bdt_signal_SB_2017",int(nBins),float(min),float(max))
 h_bdt_signal_SB_2018 = ROOT.TH1F("h_bdt_signal_SB_2018","h_bdt_signal_SB_2018",int(nBins),float(min),float(max)) 
 h_bdt_signal_SR_2016 = ROOT.TH1F("h_bdt_signal_SR_2016","h_bdt_signal_SR_2016",int(nBins),float(min),float(max)) 
 h_bdt_signal_SR_2017 = ROOT.TH1F("h_bdt_signal_SR_2017","h_bdt_signal_SR_2017",int(nBins),float(min),float(max)) 
 h_bdt_signal_SR_2018 = ROOT.TH1F("h_bdt_signal_SR_2018","h_bdt_signal_SR_2018",int(nBins),float(min),float(max)) 
 h_bdt_data_SB_2016 = ROOT.TH1F("h_bdt_data_SB_2016","h_bdt_data_SB_2016",int(nBins),float(min),float(max)) 
 h_bdt_data_SB_2017 = ROOT.TH1F("h_bdt_data_SB_2017","h_bdt_data_SB_2017",int(nBins),float(min),float(max))  
 h_bdt_data_SB_2018 = ROOT.TH1F("h_bdt_data_SB_2018","h_bdt_data_SB_2018",int(nBins),float(min),float(max))  
 h_bdt_datamix_SR_2016 = ROOT.TH1F("h_bdt_datamix_SR_2016","h_bdt_datamix_SR_2016",int(nBins),float(min),float(max)) 
 h_bdt_datamix_SR_2017 = ROOT.TH1F("h_bdt_datamix_SR_2017","h_bdt_datamix_SR_2017",int(nBins),float(min),float(max))  
 h_bdt_datamix_SR_2018 = ROOT.TH1F("h_bdt_datamix_SR_2018","h_bdt_datamix_SR_2018",int(nBins),float(min),float(max))   
 
 h_bdt_data_SB_2016_diffBins = ROOT.TH1F("h_bdt_data_SB_2016_diffBins","h_bdt_data_SB_2016_diffBins",50,float(min),float(max)) 
 h_bdt_data_SB_2017_diffBins = ROOT.TH1F("h_bdt_data_SB_2017_diffBins","h_bdt_data_SB_2017_diffBins",50,float(min),float(max))  
 h_bdt_data_SB_2018_diffBins = ROOT.TH1F("h_bdt_data_SB_2018_diffBins","h_bdt_data_SB_2018_diffBins",50,float(min),float(max))  
 h_bdt_datamix_SB_2016_diffBins = ROOT.TH1F("h_bdt_datamix_SB_2016_diffBins","h_bdt_datamix_SB_2016_diffBins",50,float(min),float(max)) 
 h_bdt_datamix_SB_2017_diffBins = ROOT.TH1F("h_bdt_datamix_SB_2017_diffBins","h_bdt_datamix_SB_2017_diffBins",50,float(min),float(max)) 
 h_bdt_datamix_SB_2018_diffBins = ROOT.TH1F("h_bdt_datamix_SB_2018_diffBins","h_bdt_datamix_SB_2018_diffBins",50,float(min),float(max)) 
  
 ### 2016 ###
 lumi_2016 = 35.9

 histo_scale.Reset() 
 data_tree_2016 = ROOT.TChain()
 #data_tree_2016.AddFile(inDir+'/data_'+str(mass)+'_2016.root/Data_13TeV_H4GTag_0')
 data_tree_2016.AddFile(inDir+'/data_2016.root/Data_13TeV_H4GTag_0') 
 data_tree_2016 = reduceTree(data_tree_2016,Cut_noMass)
 data_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale",Cut_SB)
 data_scale_2016 = float(histo_scale.Integral())
 data_tree_2016.Draw("bdt>>h_bdt_data_SB_2016",Cut_SB)
 data_tree_2016.Draw("bdt>>h_bdt_data_SB_2016_diffBins",Cut_SB)
 
 histo_scale.Reset() 
 datamix_tree_2016 = ROOT.TChain()
 #datamix_tree_2016.AddFile(inDir+'/data_mix_'+str(mass)+'_2016.root/Data_13TeV_H4GTag_0')
 datamix_tree_2016.AddFile(inDir+'/data_mix_2016_even.root/Data_13TeV_H4GTag_0')
 datamix_tree_2016 = reduceTree(datamix_tree_2016,Cut_noMass)
 datamix_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SB)
 datamix_scale_2016 = float(histo_scale.Integral())
 datamix_tree_2016.Draw("bdt>>h_bdt_datamix_SB_2016_diffBins",str(data_scale_2016/datamix_scale_2016)+"*weight*"+Cut_SB)
 datamix_tree_2016.Draw("bdt>>h_bdt_datamix_SR_2016",str(data_scale_2016/datamix_scale_2016)+"*weight*"+Cut_SR)

 histo_scale.Reset() 
 sig_tree_2016 = ROOT.TChain()
 sig_tree_2016.AddFile(inDir+'/signal_m_'+str(mass)+'_2016_even.root/HAHMHToAA_AToGG_MA_'+str(mass)+'GeV_TuneCUETP8M1_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0')
 sig_tree_2016.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SR)
 sig_scale_2016 = float(histo_scale.Integral())
 sig_tree_2016.Draw("bdt>>h_bdt_signal_SB_2016",str(lumi_2016)+"*weight*"+Cut_SB) 
 sig_tree_2016.Draw("bdt>>h_bdt_signal_SR_2016",str(lumi_2016)+"*weight*"+Cut_SR) 

 print "2016 Data/DataMix SB scale:",data_scale_2016/datamix_scale_2016
 

 ### 2017 ###
 lumi_2017 = 41.5

 histo_scale.Reset() 
 data_tree_2017 = ROOT.TChain()
 #data_tree_2017.AddFile(inDir+'/data_'+str(mass)+'_2017.root/Data_13TeV_H4GTag_0')
 data_tree_2017.AddFile(inDir+'/data_2017.root/Data_13TeV_H4GTag_0') 
 data_tree_2017 = reduceTree(data_tree_2017,Cut_noMass)
 data_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale",Cut_SB)
 data_scale_2017 = float(histo_scale.Integral())
 data_tree_2017.Draw("bdt>>h_bdt_data_SB_2017",Cut_SB)
 data_tree_2017.Draw("bdt>>h_bdt_data_SB_2017_diffBins",Cut_SB)
 
 histo_scale.Reset() 
 datamix_tree_2017 = ROOT.TChain()
 #datamix_tree_2017.AddFile(inDir+'/data_mix_'+str(mass)+'_2017.root/Data_13TeV_H4GTag_0')
 datamix_tree_2017.AddFile(inDir+'/data_mix_2017_even.root/Data_13TeV_H4GTag_0')
 datamix_tree_2017 = reduceTree(datamix_tree_2017,Cut_noMass)
 datamix_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SB)
 datamix_scale_2017 = float(histo_scale.Integral())
 datamix_tree_2017.Draw("bdt>>h_bdt_datamix_SB_2017_diffBins",str(data_scale_2017/datamix_scale_2017)+"*weight*"+Cut_SB)
 datamix_tree_2017.Draw("bdt>>h_bdt_datamix_SR_2017",str(data_scale_2017/datamix_scale_2017)+"*weight*"+Cut_SR)

 histo_scale.Reset() 
 sig_tree_2017 = ROOT.TChain()
 sig_tree_2017.AddFile(inDir+'/signal_m_'+str(mass)+'_2017_even.root/HAHMHToAA_AToGG_MA_'+str(mass)+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0')
 sig_tree_2017.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SR)
 sig_scale_2017 = float(histo_scale.Integral())
 sig_tree_2017.Draw("bdt>>h_bdt_signal_SB_2017",str(lumi_2017)+"*weight*"+Cut_SB)  
 sig_tree_2017.Draw("bdt>>h_bdt_signal_SR_2017",str(lumi_2017)+"*weight*"+Cut_SR) 

 print "2017 Data/DataMix SB scale:",data_scale_2017/datamix_scale_2017

 ### 2018 ###
 lumi_2018 = 54.38

 histo_scale.Reset() 
 data_tree_2018 = ROOT.TChain()
 #data_tree_2018.AddFile(inDir+'/data_'+str(mass)+'_2018.root/Data_13TeV_H4GTag_0')
 data_tree_2018.AddFile(inDir+'/data_2018.root/Data_13TeV_H4GTag_0')  
 data_tree_2018 = reduceTree(data_tree_2018,Cut_noMass)
 data_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale",Cut_SB)
 data_scale_2018 = float(histo_scale.Integral())
 data_tree_2018.Draw("bdt>>h_bdt_data_SB_2018",Cut_SB)
 data_tree_2018.Draw("bdt>>h_bdt_data_SB_2018_diffBins",Cut_SB)
 
 histo_scale.Reset() 
 datamix_tree_2018 = ROOT.TChain()
 #datamix_tree_2018.AddFile(inDir+'/data_mix_'+str(mass)+'_2018.root/Data_13TeV_H4GTag_0')
 datamix_tree_2018.AddFile(inDir+'/data_mix_2018_even.root/Data_13TeV_H4GTag_0')
 datamix_tree_2018 = reduceTree(datamix_tree_2018,Cut_noMass)
 datamix_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SB)
 datamix_scale_2018 = float(histo_scale.Integral())
 datamix_tree_2018.Draw("bdt>>h_bdt_datamix_SB_2018_diffBins",str(data_scale_2018/datamix_scale_2018)+"*weight*"+Cut_SB)
 datamix_tree_2018.Draw("bdt>>h_bdt_datamix_SR_2018",str(data_scale_2018/datamix_scale_2018)+"*weight*"+Cut_SR)

 histo_scale.Reset() 
 sig_tree_2018 = ROOT.TChain()
 sig_tree_2018.AddFile(inDir+'/signal_m_'+str(mass)+'_2018_even.root/HAHMHToAA_AToGG_MA_'+str(mass)+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0')
 sig_tree_2018.Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>histo_scale","weight*"+Cut_SR)
 sig_scale_2018 = float(histo_scale.Integral())
 sig_tree_2018.Draw("bdt>>h_bdt_signal_SB_2018",str(lumi_2018)+"*weight*"+Cut_SB) 
 sig_tree_2018.Draw("bdt>>h_bdt_signal_SR_2018",str(lumi_2018)+"*weight*"+Cut_SR) 

 print "2018 Data/DataMix SB scale:",data_scale_2018/datamix_scale_2018

 h_bdt_signal_SB = h_bdt_signal_SB_2016.Clone()
 h_bdt_signal_SB.Add(h_bdt_signal_SB_2017)
 h_bdt_signal_SB.Add(h_bdt_signal_SB_2018)
 h_bdt_signal_SB.SetName('h_bdt_signal_SB')
 h_bdt_signal_SB.SetTitle('h_bdt_signal_SB')

 h_bdt_signal_SR = h_bdt_signal_SR_2016.Clone()
 h_bdt_signal_SR.Add(h_bdt_signal_SR_2017)
 h_bdt_signal_SR.Add(h_bdt_signal_SR_2018)
 h_bdt_signal_SR.SetName('h_bdt_signal_SR')
 h_bdt_signal_SR.SetTitle('h_bdt_signal_SR')

 h_bdt_data_SB = h_bdt_data_SB_2016.Clone()
 h_bdt_data_SB.Add(h_bdt_data_SB_2017)
 h_bdt_data_SB.Add(h_bdt_data_SB_2018)
 h_bdt_data_SB.SetName('h_bdt_data_SB')
 h_bdt_data_SB.SetTitle('h_bdt_data_SB')
 
 h_bdt_data_SB_diffBins = h_bdt_data_SB_2016_diffBins.Clone()
 h_bdt_data_SB_diffBins.Add(h_bdt_data_SB_2017_diffBins)
 h_bdt_data_SB_diffBins.Add(h_bdt_data_SB_2018_diffBins)
 h_bdt_data_SB_diffBins.SetName('h_bdt_data_SB_diffBins')
 h_bdt_data_SB_diffBins.SetTitle('h_bdt_data_SB_diffBins')

 h_bdt_datamix_SB_diffBins = h_bdt_datamix_SB_2016_diffBins.Clone()
 h_bdt_datamix_SB_diffBins.Add(h_bdt_datamix_SB_2017_diffBins)
 h_bdt_datamix_SB_diffBins.Add(h_bdt_datamix_SB_2018_diffBins)
 h_bdt_datamix_SB_diffBins.SetName('h_bdt_datamix_SB_diffBins')
 h_bdt_datamix_SB_diffBins.SetTitle('h_bdt_datamix_SB_diffBins')

 h_bdt_datamix_SR = h_bdt_datamix_SR_2016.Clone()
 h_bdt_datamix_SR.Add(h_bdt_datamix_SR_2017)
 h_bdt_datamix_SR.Add(h_bdt_datamix_SR_2018)
 h_bdt_datamix_SR.SetName('h_bdt_datamix_SR')
 h_bdt_datamix_SR.SetTitle('h_bdt_datamix_SR')

 
 h_bdt_ratio_SB = makeRatio(h_bdt_data_SB_diffBins,h_bdt_datamix_SB_diffBins)

 compareHistos(h_bdt_data_SB_diffBins,h_bdt_datamix_SB_diffBins,"h_bdt_SB_m"+str(mass),1)

 h_bdt_datamix_SB_weighted_2016 = ROOT.TH1F("h_bdt_datamix_SB_weighted_2016","h_bdt_datamix_SB_weighted_2016",int(nBins),float(min),float(max))
 h_bdt_datamix_SB_weighted_2017 = ROOT.TH1F("h_bdt_datamix_SB_weighted_2017","h_bdt_datamix_SB_weighted_2017",int(nBins),float(min),float(max))
 h_bdt_datamix_SB_weighted_2018 = ROOT.TH1F("h_bdt_datamix_SB_weighted_2018","h_bdt_datamix_SB_weighted_2018",int(nBins),float(min),float(max)) 
 h_bdt_datamix_SB_weighted_2016_diffBins = ROOT.TH1F("h_bdt_datamix_SB_weighted_2016_diffBins","h_bdt_datamix_SB_weighted_2016_diffBins",50,float(min),float(max))
 h_bdt_datamix_SB_weighted_2017_diffBins = ROOT.TH1F("h_bdt_datamix_SB_weighted_2017_diffBins","h_bdt_datamix_SB_weighted_2017_diffBins",50,float(min),float(max))
 h_bdt_datamix_SB_weighted_2018_diffBins = ROOT.TH1F("h_bdt_datamix_SB_weighted_2018_diffBins","h_bdt_datamix_SB_weighted_2018_diffBins",50,float(min),float(max)) 

 h_bdt_datamix_SR_weighted_2016 = ROOT.TH1F("h_bdt_datamix_SR_weighted_2016","h_bdt_datamix_SR_weighted_2016",int(nBins),float(min),float(max))
 h_bdt_datamix_SR_weighted_2017 = ROOT.TH1F("h_bdt_datamix_SR_weighted_2017","h_bdt_datamix_SR_weighted_2017",int(nBins),float(min),float(max))
 h_bdt_datamix_SR_weighted_2018 = ROOT.TH1F("h_bdt_datamix_SR_weighted_2018","h_bdt_datamix_SR_weighted_2018",int(nBins),float(min),float(max)) 

 print "Fill 2016 datamix reweighting..."
 datamix_tree_2016_bdtWeight = ROOT.TChain()
 MakeTree(datamix_tree_2016, h_bdt_ratio_SB, data_scale_2016/datamix_scale_2016, 'file.root')
 datamix_tree_2016_bdtWeight.AddFile('file.root/Data_13TeV_H4GTag_0')
 datamix_tree_2016_bdtWeight.Draw("bdt>>h_bdt_datamix_SB_weighted_2016","bdt_weight*weight*"+Cut_SB)
 datamix_tree_2016_bdtWeight.Draw("bdt>>h_bdt_datamix_SB_weighted_2016_diffBins","bdt_weight*weight*"+Cut_SB)
 datamix_tree_2016_bdtWeight.Draw("bdt>>h_bdt_datamix_SR_weighted_2016","bdt_weight*weight*"+Cut_SR)
 
 print "Fill 2017 datamix reweighting..."
 datamix_tree_2017_bdtWeight = ROOT.TChain()
 MakeTree(datamix_tree_2017, h_bdt_ratio_SB, data_scale_2017/datamix_scale_2017, 'file.root')
 datamix_tree_2017_bdtWeight.AddFile('file.root/Data_13TeV_H4GTag_0')
 datamix_tree_2017_bdtWeight.Draw("bdt>>h_bdt_datamix_SB_weighted_2017","bdt_weight*weight*"+Cut_SB)
 datamix_tree_2017_bdtWeight.Draw("bdt>>h_bdt_datamix_SB_weighted_2017_diffBins","bdt_weight*weight*"+Cut_SB)
 datamix_tree_2017_bdtWeight.Draw("bdt>>h_bdt_datamix_SR_weighted_2017","bdt_weight*weight*"+Cut_SR)

 print "Fill 2018 datamix reweighting..."
 datamix_tree_2018_bdtWeight = ROOT.TChain()
 MakeTree(datamix_tree_2018, h_bdt_ratio_SB, data_scale_2018/datamix_scale_2018, 'file.root')
 datamix_tree_2018_bdtWeight.AddFile('file.root/Data_13TeV_H4GTag_0')
 datamix_tree_2018_bdtWeight.Draw("bdt>>h_bdt_datamix_SB_weighted_2018","bdt_weight*weight*"+Cut_SB)
 datamix_tree_2018_bdtWeight.Draw("bdt>>h_bdt_datamix_SB_weighted_2018_diffBins","bdt_weight*weight*"+Cut_SB)
 datamix_tree_2018_bdtWeight.Draw("bdt>>h_bdt_datamix_SR_weighted_2018","bdt_weight*weight*"+Cut_SR)
 
 h_bdt_datamix_SB_weighted = h_bdt_datamix_SB_weighted_2016.Clone()
 h_bdt_datamix_SB_weighted.Add(h_bdt_datamix_SB_weighted_2017)
 h_bdt_datamix_SB_weighted.Add(h_bdt_datamix_SB_weighted_2018)
 h_bdt_datamix_SB_weighted.SetName('h_bdt_datamix_SB_weighted')
 h_bdt_datamix_SB_weighted.SetTitle('h_bdt_datamix_SB_weighted')

 h_bdt_datamix_SB_weighted_diffBins = h_bdt_datamix_SB_weighted_2016_diffBins.Clone()
 h_bdt_datamix_SB_weighted_diffBins.Add(h_bdt_datamix_SB_weighted_2017_diffBins)
 h_bdt_datamix_SB_weighted_diffBins.Add(h_bdt_datamix_SB_weighted_2018_diffBins)
 h_bdt_datamix_SB_weighted_diffBins.SetName('h_bdt_datamix_SB_weighted_diffBins')
 h_bdt_datamix_SB_weighted_diffBins.SetTitle('h_bdt_datamix_SB_weighted_diffBins')

 h_bdt_datamix_SR_weighted = h_bdt_datamix_SR_weighted_2016.Clone()
 h_bdt_datamix_SR_weighted.Add(h_bdt_datamix_SR_weighted_2017)
 h_bdt_datamix_SR_weighted.Add(h_bdt_datamix_SR_weighted_2018)
 h_bdt_datamix_SR_weighted.SetName('h_bdt_datamix_SR_weighted')
 h_bdt_datamix_SR_weighted.SetTitle('h_bdt_datamix_SR_weighted')

 compareHistos(h_bdt_data_SB_diffBins,h_bdt_datamix_SB_weighted_diffBins,"h_bdt_SB_weighted_m"+str(mass),1)

 print "Smooth distributions..."
 algos = ['SmoothSuper']

 for algo in algos:
   outFile = ROOT.TFile(inDir+'/BDT_Histos_smoothing_'+algo+'_bins'+str(nBins)+'_massMin'+str(massMin)+'_massMax'+str(massMax)+'.root',"RECREATE")
   outFile.cd()
   hist_smooth = smoothing(h_bdt_datamix_SR_weighted,algo)
   if hist_smooth!=-1: 
     drawHistos(h_bdt_datamix_SR_weighted,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_bdt_datamix_SR_weighted.GetName()+"_smoothing_"+algo+"_m"+str(mass))
     drawHisto(hist_smooth[4],h_bdt_datamix_SR_weighted.GetName()+"_smoothing_"+algo+"_Diff_m"+str(mass)) 
     h_bdt_datamix_SR_weighted.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write() 
   hist_smooth = smoothing(h_bdt_datamix_SR,algo)
   if hist_smooth!=-1: 
     drawHistos(h_bdt_datamix_SR,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_bdt_datamix_SR.GetName()+"_smoothing_"+algo+"_m"+str(mass))
     drawHisto(hist_smooth[4],h_bdt_datamix_SR.GetName()+"_smoothing_"+algo+"_Diff_m"+str(mass)) 
     h_bdt_datamix_SR.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write() 
   hist_smooth = smoothing(h_bdt_datamix_SB_weighted,algo)
   if hist_smooth!=-1: 
     drawHistos(h_bdt_datamix_SB_weighted,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_bdt_datamix_SB_weighted.GetName()+"_smoothing_"+algo+"_m"+str(mass))
     drawHisto(hist_smooth[4],h_bdt_datamix_SB_weighted.GetName()+"_smoothing_"+algo+"_Diff_m"+str(mass)) 
     h_bdt_datamix_SB_weighted.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write()  
   hist_smooth = smoothing(h_bdt_data_SB,algo)
   if hist_smooth!=-1: 
     drawHistos(h_bdt_data_SB,hist_smooth[0],hist_smooth[1],hist_smooth[2],h_bdt_data_SB.GetName()+"_smoothing_"+algo+"_m"+str(mass))
     drawHisto(hist_smooth[4],h_bdt_data_SB.GetName()+"_smoothing_"+algo+"_Diff_m"+str(mass)) 
     h_bdt_data_SB.Write()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write() 
   h_bdt_signal_SR.Write()
   h_bdt_signal_SB.Write()
   h_bdt_data_SB_diffBins.Write()
   h_bdt_datamix_SB_diffBins.Write()
   h_bdt_datamix_SB_weighted_diffBins.Write()
   outFile.Close()

