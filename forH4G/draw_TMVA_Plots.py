
#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
from optparse import OptionParser
import operator
import os
import glob

#def makeRejection(h1):
#   h1_clone = h1.Clone()
#   h1_clone.Reset()
#   for bin in range(1,h1.GetNbinsX()+1):
#      h1_clone.SetBinContent(bin,1.-h1.GetBinContent(bin))  
#    
#   return h1_clone  

def getall(d, basepath="/"):
   if d.ClassName() != "TTree":  
     for key in d.GetListOfKeys():
       kname = key.GetName()
       if key.IsFolder():
         # TODO: -> "yield from" in Py3
         for i in getall(d.Get(kname), basepath+kname+"/"):
           yield i
       else:
         yield basepath+kname, d.Get(kname)

def drawH2(h2,name):

   gStyle.SetOptStat(0000)

   c = TCanvas()
   h2.Draw("COLZ,TEXT")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 


def drawROC(h1,name):

   gStyle.SetOptStat(0000)

   h1.GetXaxis().SetTitle("signal efficiency")
   h1.GetYaxis().SetTitle("bkg rejection")
   h1.SetTitle("")
   h1.GetXaxis().SetRangeUser(0.,1.01)
   h1.GetYaxis().SetRangeUser(0.,1.01)

   h1.SetLineColor(kBlack)
   h1.SetLineWidth(2) 

   latex = TLatex(0.35,0.45,"ROC = "+str(h1.Integral()/100.))
   latex.SetNDC()
   latex.SetTextFont(42)
   latex.SetTextSize(0.04)
   latex.SetTextColor(kBlack)
   
   c = TCanvas()
   h1.Draw("L")
   latex.Draw("same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

def drawROCs(h1,h2,name):

   gStyle.SetOptStat(0000)

   h1.GetXaxis().SetTitle("signal efficiency")
   h1.GetYaxis().SetTitle("bkg rejection")
   h1.SetTitle("")
   h1.GetXaxis().SetRangeUser(0.,1.01)
   h1.GetYaxis().SetRangeUser(0.,1.01)

   h1.SetLineColor(kBlue+1)
   h1.SetLineWidth(2) 
   h2.SetLineColor(kRed+1)
   h2.SetLineWidth(2) 

   leg = TLegend(0.2,0.83,0.8,0.88)
   leg.SetFillColor(kWhite)
   leg.SetFillStyle(1000)
   leg.SetLineWidth(0)
   leg.SetLineColor(kWhite)
   leg.SetTextFont(42)
   leg.SetTextSize(0.04)
   leg.SetNColumns(2)
   leg.AddEntry(h1,"Training","PL")
   leg.AddEntry(h2,"Test","PL")
   
   c = TCanvas()
   h1.Draw("L")
   h2.Draw("L,same")
   leg.Draw("same") 
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

def drawHistos(h_sig,h_bkg,var,label):

   gStyle.SetOptStat(0000)

   h_sig.Scale(1./h_sig.Integral())
   h_bkg.Scale(1./h_bkg.Integral())

   h_sig.GetXaxis().SetTitle(label)
   h_sig.GetYaxis().SetTitle("")
   h_sig.SetTitle(var)
   h_sig.SetFillColor(kBlue)  
   h_sig.SetFillStyle(3017)  
     
   maxs = [h_sig.GetMaximum(), h_bkg.GetMaximum()] 
   h_sig.GetYaxis().SetRangeUser(0.,max(maxs)*1.2)
   
   h_bkg.SetFillColor(kRed)  
   h_bkg.SetFillStyle(3001) 

   leg = TLegend(0.2,0.83,0.8,0.88)
   leg.SetFillColor(kWhite)
   leg.SetFillStyle(1000)
   leg.SetLineWidth(0)
   leg.SetLineColor(kWhite)
   leg.SetTextFont(42)
   leg.SetTextSize(0.04)
   leg.SetNColumns(2)
   leg.AddEntry(h_sig,"Signal","f")
   leg.AddEntry(h_bkg,"Background","f")
   
   c = TCanvas()
   h_sig.Draw("Hist")
   h_bkg.Draw("Hist,same")
   leg.Draw("same") 
   c.SaveAs(var+".png","png") 
   c.SaveAs(var+".pdf","pdf") 

def drawScores(sig_training, bkg_training, sig_test, bkg_test, name):

   gStyle.SetOptStat(0000)

   sig_test.GetXaxis().SetTitle("BDT response")
   sig_test.GetYaxis().SetTitle("")
   sig_test.SetTitle("")

   maxs = [sig_test.GetMaximum(), sig_training.GetMaximum(), bkg_test.GetMaximum(), bkg_training.GetMaximum()] 
   sig_test.GetYaxis().SetRangeUser(0.,max(maxs)*1.3)

   sig_test.SetFillColor(kBlue)  
   sig_test.SetFillStyle(3017)  
   sig_training.SetMarkerColor(kBlue) 
   sig_training.SetLineColor(kBlue)  
   sig_training.SetMarkerStyle(20) 

   bkg_test.SetFillColor(kRed)  
   bkg_test.SetFillStyle(3354)  
   bkg_training.SetMarkerColor(kRed) 
   bkg_training.SetLineColor(kRed)  
   bkg_training.SetMarkerStyle(20) 

   leg = TLegend(0.2,0.78,0.8,0.88)
   leg.SetFillColor(kWhite)
   leg.SetFillStyle(1000)
   leg.SetLineWidth(0)
   leg.SetLineColor(kWhite)
   leg.SetTextFont(42)
   leg.SetTextSize(0.03)
   leg.SetNColumns(2);
   leg.AddEntry(sig_test,"signal (test sample)","f");
   leg.AddEntry(sig_training,"signal (training sample)","PL");
   leg.AddEntry(bkg_test,"bkg (test sample)","f");
   leg.AddEntry(bkg_training,"bkg (training sample)","PL");

   kst_sig = sig_test.KolmogorovTest(sig_training,"X") 
   kst_bkg = bkg_test.KolmogorovTest(bkg_training,"X") 
   latex = TLatex(0.21,0.73,"K-S test: signal (background) probability = "+str(round(kst_sig,3))+" ("+str(round(kst_bkg,3))+")")
   latex.SetNDC();
   latex.SetTextFont(42);
   latex.SetTextSize(0.03);
   latex.SetTextColor(kBlack);
 
   c = TCanvas()
   sig_test.Draw("Hist")
   sig_training.Draw("PL,same")
   bkg_test.Draw("Hist,same")
   bkg_training.Draw("PL,same")
   leg.Draw("same") 
   latex.Draw("same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

if __name__ == '__main__':
 
  gROOT.SetBatch(kTRUE)

  parser = OptionParser()
  parser.add_option( "-d", "--dir",    dest="dir",    default="",   type="string", help="dir" )
  parser.add_option( "-i", "--inDir",    dest="inDir",    default="Method_BDT",   type="string", help="inDir" )
  (options, args) = parser.parse_args()  

  inDir = options.dir
  addDir = options.inDir
  inputFile = inDir+"/categorization_training.root"

  print "inputFile = ", inputFile
  print "internalDir = ", addDir
  file = TFile(inputFile) 

  dataset=inDir.split('/')[-2]
  Label = "BDTG"
  Dir = dataset+"/"+addDir+"/"+Label  

  CorrelationMatrix_Sig = file.Get(dataset+"/CorrelationMatrixS")
  drawH2(CorrelationMatrix_Sig,"CorrelationMatrix_Signal")

  CorrelationMatrix_Bkg = file.Get(dataset+"/CorrelationMatrixB")
  drawH2(CorrelationMatrix_Bkg,"CorrelationMatrix_Background")

  ROC_test = file.Get(Dir+"/MVA_BDTG_rejBvsS") 
  drawROC(ROC_test,"ROC")
 
  ROC_training = file.Get(Dir+"/MVA_BDTG_trainingRejBvsS")
  drawROCs(ROC_training,ROC_test,"ROCs_Training_and_Test")

  score_Sig_Training = file.Get(Dir+"/MVA_"+Label+"_Train_S")  
  score_Sig_Test = file.Get(Dir+"/MVA_"+Label+"_S") 
  score_Bkg_Training = file.Get(Dir+"/MVA_"+Label+"_Train_B") 
  score_Bkg_Test = file.Get(Dir+"/MVA_"+Label+"_B") 
  drawScores(score_Sig_Training, score_Bkg_Training, score_Sig_Test, score_Bkg_Test, "BDT_Response")

  #vars = ['a1_mass_dM_M_a2_mass_dM', 'cosTheta_a1_dM', 'a1_pt_dM', 'a2_pt_dM', 'pho1_MVA__M_1.__M_1.1:pho1_MVA', 'pho2_MVA__M_1.__M_1.1:pho2_MVA', 'pho3_MVA__M_1.__M_1.1:pho3_MVA', 'pho4_MVA__M_1.__M_1.1:pho4_MVA', 'a1_a2_dR_dM', 'a1_pt_dM_D_tp_mass', 'a2_pt_dM_D_tp_mass']
  #var_labels = ['a1_mass-a2_mass', 'cos#theta', 'Pt (GeV)', 'Pt (GeV)', '#gamma1 MVA', '#gamma2 MVA', '#gamma3 MVA', '#gamma4 MVA', 'dR(a1,a2)', 'a1_pt_dM/tp_mass', 'a2_pt_dM/tp_mass']

  vars = ['a1_mass_dM_M_a2_mass_dM', 'cosTheta_a1_dM', 'a1_pt_dM', 'a2_pt_dM', 'pho1_MVA__M_1.__M_1.1:pho1_MVA', 'pho2_MVA__M_1.__M_1.1:pho2_MVA', 'pho3_MVA__M_1.__M_1.1:pho3_MVA', 'pho4_MVA__M_1.__M_1.1:pho4_MVA', 'a1_a2_dR_dM', 'a1_pt_dM_D_tp_mass', 'a2_pt_dM_D_tp_mass', 'a1_mass_dM', 'a2_mass_dM']
  var_labels = ['a1_mass-a2_mass', 'cos#theta', 'Pt (GeV)', 'Pt (GeV)', '#gamma1 MVA', '#gamma2 MVA', '#gamma3 MVA', '#gamma4 MVA', 'dR(a1,a2)', 'a1_pt_dM/tp_mass', 'a2_pt_dM/tp_mass', 'a1_mass (GeV)', 'a2_mass (GeV)']  
  
  for iVar in range(0,len(vars)):  
     h_sig = file.Get(Dir+"/"+vars[iVar]+"__Signal")
     h_bkg = file.Get(Dir+"/"+vars[iVar]+"__Background")
     drawHistos(h_sig,h_bkg,vars[iVar],var_labels[iVar]) 
   

