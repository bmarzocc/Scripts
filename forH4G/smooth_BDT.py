import ROOT
import argparse
import os
import math
from array import array


def rebinHist(hist,nbins,min,max):
 name = hist.GetName()
 hist.SetName(name+'_oldBin')
 h_rebin = ROOT.TH1F(name,hist.GetTitle(),nbins,float(min),float(max)) 
 for bin in range(0,hist.GetNbinsX()+2): 
  h_rebin.SetBinContent(h_rebin.FindBin(hist.GetBinCenter(bin)),hist.GetBinContent(bin))
 return h_rebin

def smoothing(h_bdt,method="SmoothSuper"):
 
 bin_min = h_bdt.GetBinCenter(1)-h_bdt.GetBinWidth(1)/2.
 bin_max = h_bdt.GetBinCenter(h_bdt.GetNbinsX())+h_bdt.GetBinWidth(h_bdt.GetNbinsX())/2.
 h_bdt_smooth = ROOT.TH1F(h_bdt.GetName()+"_smooth",h_input.GetName()+"_smooth",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_bdt_smooth_rnd = ROOT.TH1F(h_bdt.GetName()+"_smooth_rnd",h_input.GetName()+"_smooth_rnd",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_bdt_smooth_up = ROOT.TH1F(h_bdt.GetName()+"_smooth_up",h_input.GetName()+"_smooth_up",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_bdt_smooth_down = ROOT.TH1F(h_bdt.GetName()+"_smooth_down",h_input.GetName()+"_smooth_down",h_bdt.GetNbinsX(),float(bin_min),float(bin_max))
 h_diff = ROOT.TH1F("h_bdt_diff_smoothing","h_bdt_diff_smoothing",100,-50.,50.)

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
  h_bdt_smooth_up.SetBinContent(bin+1,y+math.sqrt(y))
  h_bdt_smooth_down.SetBinContent(bin+1,y-math.sqrt(y))
  h_diff.Fill(y-h_bdt.GetBinContent(bin+1)) 

 return [h_bdt_smooth,h_bdt_smooth_up,h_bdt_smooth_down,h_bdt_smooth_rnd,h_diff] 

def drawHistos(hist,hist_smooth,hist_smooth_up,hist_smooth_down,name):

   ROOT.gStyle.SetOptStat(0000)

   hist.SetLineColor(ROOT.kBlack)
   hist_smooth.SetLineColor(ROOT.kRed)
   hist_smooth_up.SetLineColor(ROOT.kGreen)
   hist_smooth_down.SetLineColor(ROOT.kBlue)
   
   c = ROOT.TCanvas()
   c.SetLogy()
   hist.Draw("HIST") 
   hist_smooth.Draw("HIST,same")
   hist_smooth_up.Draw("HIST,same")
   hist_smooth_down.Draw("HIST,same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

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
 parser.add_argument('-i', '--inFile', dest='inFile', required=True, type=str)
 parser.add_argument('-N', '--name', dest='name', required=False, type=str)
 parser.add_argument('-n', '--nBins', dest='nBins', required=False, type=int)
 parser.add_argument('-m', '--min', dest='min', required=False, type=float)
 parser.add_argument('-M', '--max', dest='max', required=False, type=float)
 
 args = parser.parse_args()
 inFile = args.inFile

 nBins = 190
 if args.nBins: nBins = args.nBins
 min = -0.9
 if args.min: nBins = args.min
 max = 1.
 if args.max: nBins = args.max
 h_name = "h_bdt"
 if args.name: h_name = args.name
 
 print "inFile:",inFile
 print "Hist:",h_name
 print "nBins:",nBins
 print "Min:",min
 print "Max:",max

 file = ROOT.TFile(inFile,"READ")
 h_input = file.Get(h_name)

 #algos = ['SmoothLowess', 'SmoothSuper','SmoothKern']
 algos = ['SmoothSuper']
 hist = rebinHist(h_input,nBins,min,max)

 for algo in algos:
  outFile_name = inFile.replace('.root','_smoothing_'+algo+'.root') 
  hist_smooth = smoothing(hist,algo)
  if hist_smooth!=-1: 
     drawHistos(hist,hist_smooth[0],hist_smooth[1],hist_smooth[2],hist.GetName()+"_smoothing_"+algo)
     drawHisto(hist_smooth[4],'h_bdt_diff_smoothing_'+algo) 
     outFile = ROOT.TFile(outFile_name,"RECREATE")
     outFile.cd()
     hist_smooth[0].Write() 
     hist_smooth[1].Write() 
     hist_smooth[2].Write()  
     outFile.Close()

