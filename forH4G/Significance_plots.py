import ROOT
import argparse
import os

def fillGraph(graph,points):
  iPoint = 0
  for val in points:
    graph.SetPoint(iPoint,val[0],val[1])
    iPoint += 1

def drawGraph(hist,name,xTitle,yTitle, logX=True, logY=False):

   hist.SetLineWidth(2)
   hist.SetLineColor(ROOT.kBlue)
   hist.SetMarkerColor(ROOT.kBlue)
   hist.SetMarkerStyle(20)

   hist.GetXaxis().SetTitle(xTitle)
   hist.GetYaxis().SetTitle(yTitle)
   
   c = ROOT.TCanvas()
   if logX: c.SetLogx()
   if logY: c.SetLogy()
   c.SetGrid()
   hist.Draw("APL") 
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 


if __name__ == '__main__':

 ROOT.gROOT.SetBatch(ROOT.kTRUE)

 parser =  argparse.ArgumentParser(description='mergeTrees')
 parser.add_argument('-d', '--inDir', dest='inDir', required=True, type=str)
 
 args = parser.parse_args()
 inDir = args.inDir
 #inDir = /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/15/

 g_Significance_vs_nCats = []

 g_Significance_vs_nBins_1Cat = ROOT.TGraph() 
 g_Significance_vs_nBins_2Cat = ROOT.TGraph() 
 g_Significance_vs_nBins_3Cat = ROOT.TGraph() 
 g_Significance_vs_nBins_4Cat = ROOT.TGraph() 
 g_Significance_vs_nBins_5Cat = ROOT.TGraph() 

 g_nSig_vs_nBins_1Cat = ROOT.TGraph() 
 g_nSig_vs_nBins_2Cat = ROOT.TGraph() 
 g_nSig_vs_nBins_3Cat = ROOT.TGraph() 
 g_nSig_vs_nBins_4Cat = ROOT.TGraph() 
 g_nSig_vs_nBins_5Cat = ROOT.TGraph() 

 g_nBkg_vs_nBins_1Cat = ROOT.TGraph() 
 g_nBkg_vs_nBins_2Cat = ROOT.TGraph() 
 g_nBkg_vs_nBins_3Cat = ROOT.TGraph() 
 g_nBkg_vs_nBins_4Cat = ROOT.TGraph() 
 g_nBkg_vs_nBins_5Cat = ROOT.TGraph() 

 g_dataSB_vs_nBins_1Cat = ROOT.TGraph() 
 g_dataSB_vs_nBins_2Cat = ROOT.TGraph() 
 g_dataSB_vs_nBins_3Cat = ROOT.TGraph() 
 g_dataSB_vs_nBins_4Cat = ROOT.TGraph() 
 g_dataSB_vs_nBins_5Cat = ROOT.TGraph() 
 
 os.system('ls '+inDir+'/categorize_nBins_*_nCat_*.txt >> file_dump.txt')
 with open('file_dump.txt') as f_List:
   data_List = f_List.read()
 lines_List = data_List.splitlines() 

 points_1Cat = {} 
 points_2Cat = {} 
 points_3Cat = {} 
 points_4Cat = {} 
 points_5Cat = {}  

 points_1Cat_nSig = {} 
 points_2Cat_nSig = {} 
 points_3Cat_nSig = {} 
 points_4Cat_nSig = {} 
 points_5Cat_nSig = {}  

 points_1Cat_nBkg = {} 
 points_2Cat_nBkg = {} 
 points_3Cat_nBkg = {} 
 points_4Cat_nBkg = {} 
 points_5Cat_nBkg = {}  

 points_1Cat_dataSB = {} 
 points_2Cat_dataSB = {} 
 points_3Cat_dataSB = {} 
 points_4Cat_dataSB = {} 
 points_5Cat_dataSB = {}  

 for i,line in enumerate(lines_List):
   line_split = line.split('_')
   #print i,line_split
   nCats = line_split[-2]
   nBins = line_split[-4]
   with open(str(line)) as f_List:
     data_List = f_List.read()
   lines_List = data_List.splitlines() 
   significance = 0.
   nSig = 0.
   nBkg = 0.
   nDataSB = 0.
   for j,cat in enumerate(lines_List):
     #print j,cat 
     if 'Tot_Significance:' in cat: significance = cat.split()[-1]
     if len(cat.split())>1 and float(cat.split()[1]) == 1.: 
       nSig = float(cat.split()[5])
       nBkg = float(cat.split()[7])
       nDataSB = float(cat.split()[-1])
   #print nCats, nBins, significance
   if int(nCats)==1: 
     points_1Cat[int(nBins)] = float(significance)
     points_1Cat_nSig[int(nBins)] = float(nSig)
     points_1Cat_nBkg[int(nBins)] = float(nBkg) 
     points_1Cat_dataSB[int(nBins)] = float(nDataSB) 
   elif int(nCats)==2: 
     points_2Cat[int(nBins)] = float(significance)
     points_2Cat_nSig[int(nBins)] = float(nSig)
     points_2Cat_nBkg[int(nBins)] = float(nBkg) 
     points_2Cat_dataSB[int(nBins)] = float(nDataSB) 
   elif int(nCats)==3: 
     points_3Cat[int(nBins)] = float(significance)
     points_3Cat_nSig[int(nBins)] = float(nSig)
     points_3Cat_nBkg[int(nBins)] = float(nBkg) 
     points_3Cat_dataSB[int(nBins)] = float(nDataSB) 
   elif int(nCats)==4: 
     points_4Cat[int(nBins)] = float(significance)
     points_4Cat_nSig[int(nBins)] = float(nSig)
     points_4Cat_nBkg[int(nBins)] = float(nBkg) 
     points_4Cat_dataSB[int(nBins)] = float(nDataSB) 
   elif int(nCats)==5: 
     points_5Cat[int(nBins)] = float(significance)
     points_5Cat_nSig[int(nBins)] = float(nSig)
     points_5Cat_nBkg[int(nBins)] = float(nBkg) 
     points_5Cat_dataSB[int(nBins)] = float(nDataSB) 
   
 points_1Cat = sorted(points_1Cat.items())
 points_2Cat = sorted(points_2Cat.items())
 points_3Cat = sorted(points_3Cat.items())
 points_4Cat = sorted(points_4Cat.items())
 points_5Cat = sorted(points_5Cat.items())
 points_1Cat_nSig = sorted(points_1Cat_nSig.items())
 points_2Cat_nSig = sorted(points_2Cat_nSig.items())
 points_3Cat_nSig = sorted(points_3Cat_nSig.items())
 points_4Cat_nSig = sorted(points_4Cat_nSig.items())
 points_5Cat_nSig = sorted(points_5Cat_nSig.items()) 
 points_1Cat_nBkg = sorted(points_1Cat_nBkg.items())
 points_2Cat_nBkg = sorted(points_2Cat_nBkg.items())
 points_3Cat_nBkg = sorted(points_3Cat_nBkg.items())
 points_4Cat_nBkg = sorted(points_4Cat_nBkg.items())
 points_5Cat_nBkg = sorted(points_5Cat_nBkg.items())  
 points_1Cat_dataSB = sorted(points_1Cat_dataSB.items())
 points_2Cat_dataSB = sorted(points_2Cat_dataSB.items())
 points_3Cat_dataSB = sorted(points_3Cat_dataSB.items())
 points_4Cat_dataSB = sorted(points_4Cat_dataSB.items())
 points_5Cat_dataSB = sorted(points_5Cat_dataSB.items())  

 vec_bins = []
 for val in points_1Cat:
   vec_bins.append(int(val[0])) 

 for nBins in vec_bins:
   graph = ROOT.TGraph()
   graph_gain = ROOT.TGraph() 
   ref = 0.
   for val in points_1Cat:
     if int(val[0]) == nBins: 
       graph.SetPoint(0,1,val[1])
       #graph_gain.SetPoint(0,1,(val[1]/ref-1.)*100.)   
       ref = val[1]
   for val in points_2Cat:
     if int(val[0]) == nBins: 
       graph.SetPoint(1,2,val[1])
       graph_gain.SetPoint(0,2,(val[1]/ref-1.)*100.)
       ref = val[1]
   for val in points_3Cat:
     if int(val[0]) == nBins: 
       graph.SetPoint(2,3,val[1])
       graph_gain.SetPoint(1,3,(val[1]/ref-1.)*100.)
       ref = val[1]
   for val in points_4Cat:
     if int(val[0]) == nBins: 
       graph.SetPoint(3,4,val[1])
       graph_gain.SetPoint(2,4,(val[1]/ref-1.)*100.)
       ref = val[1]
   for val in points_5Cat:
     if int(val[0]) == nBins: 
       graph.SetPoint(4,5,val[1])
       graph_gain.SetPoint(3,5,(val[1]/ref-1.)*100.)
   drawGraph(graph,'Significance_vs_nCats_'+str(nBins)+'Bins','nCats','Significance',False)
   drawGraph(graph_gain,'SignificanceGain_vs_nCats_'+str(nBins)+'Bins','nCats','Significance Gain (%)',False,True)

 fillGraph(g_Significance_vs_nBins_1Cat,points_1Cat)
 drawGraph(g_Significance_vs_nBins_1Cat,'Significance_vs_nBins_1Cat','nBins','Significance')

 fillGraph(g_Significance_vs_nBins_2Cat,points_2Cat)
 drawGraph(g_Significance_vs_nBins_2Cat,'Significance_vs_nBins_2Cat','nBins','Significance')

 fillGraph(g_Significance_vs_nBins_3Cat,points_3Cat)
 drawGraph(g_Significance_vs_nBins_3Cat,'Significance_vs_nBins_3Cat','nBins','Significance')

 fillGraph(g_Significance_vs_nBins_4Cat,points_4Cat)
 drawGraph(g_Significance_vs_nBins_4Cat,'Significance_vs_nBins_4Cat','nBins','Significance')

 fillGraph(g_Significance_vs_nBins_5Cat,points_5Cat)
 drawGraph(g_Significance_vs_nBins_5Cat,'Significance_vs_nBins_5Cat','nBins','Significance')

 fillGraph(g_nSig_vs_nBins_1Cat,points_1Cat_nSig)
 drawGraph(g_nSig_vs_nBins_1Cat,'nSig_vs_nBins_1Cat','nBins','nSignals')

 fillGraph(g_nSig_vs_nBins_2Cat,points_2Cat_nSig)
 drawGraph(g_nSig_vs_nBins_2Cat,'nSig_vs_nBins_2Cat','nBins','nSignals')

 fillGraph(g_nSig_vs_nBins_3Cat,points_3Cat_nSig)
 drawGraph(g_nSig_vs_nBins_3Cat,'nSig_vs_nBins_3Cat','nBins','nSignals')

 fillGraph(g_nSig_vs_nBins_4Cat,points_4Cat_nSig)
 drawGraph(g_nSig_vs_nBins_4Cat,'nSig_vs_nBins_4Cat','nBins','nSignals')

 fillGraph(g_nSig_vs_nBins_5Cat,points_5Cat_nSig)
 drawGraph(g_nSig_vs_nBins_5Cat,'nSig_vs_nBins_5Cat','nBins','nSignals')
 
 fillGraph(g_nBkg_vs_nBins_1Cat,points_1Cat_nBkg)
 drawGraph(g_nBkg_vs_nBins_1Cat,'nDatamix_vs_nBins_1Cat_SR','nBins','nBkgs')

 fillGraph(g_nBkg_vs_nBins_2Cat,points_2Cat_nBkg)
 drawGraph(g_nBkg_vs_nBins_2Cat,'nDatamix_vs_nBins_2Cat_SR','nBins','nBkgs')

 fillGraph(g_nBkg_vs_nBins_3Cat,points_3Cat_nBkg)
 drawGraph(g_nBkg_vs_nBins_3Cat,'nDatamix_vs_nBins_3Cat_SR','nBins','nBkgs')

 fillGraph(g_nBkg_vs_nBins_4Cat,points_4Cat_nBkg)
 drawGraph(g_nBkg_vs_nBins_4Cat,'nDatamix_vs_nBins_4Cat_SR','nBins','nBkgs')

 fillGraph(g_nBkg_vs_nBins_5Cat,points_5Cat_nBkg)
 drawGraph(g_nBkg_vs_nBins_5Cat,'nDatamix_vs_nBins_5Cat_SR','nBins','nBkgs')

 fillGraph(g_dataSB_vs_nBins_1Cat,points_1Cat_dataSB)
 drawGraph(g_dataSB_vs_nBins_1Cat,'nData_vs_nBins_1Cat_SB','nBins','nData')

 fillGraph(g_dataSB_vs_nBins_2Cat,points_2Cat_dataSB)
 drawGraph(g_dataSB_vs_nBins_2Cat,'nData_vs_nBins_2Cat_SB','nBins','nData')

 fillGraph(g_dataSB_vs_nBins_3Cat,points_3Cat_dataSB)
 drawGraph(g_dataSB_vs_nBins_3Cat,'nData_vs_nBins_3Cat_SB','nBins','nData')

 fillGraph(g_dataSB_vs_nBins_4Cat,points_4Cat_dataSB)
 drawGraph(g_dataSB_vs_nBins_4Cat,'nData_vs_nBins_4Cat_SB','nBins','nData')

 fillGraph(g_dataSB_vs_nBins_5Cat,points_5Cat_dataSB)
 drawGraph(g_dataSB_vs_nBins_5Cat,'nData_vs_nBins_5Cat_SB','nBins','nData')

 os.system('rm file_dump.txt')
   
