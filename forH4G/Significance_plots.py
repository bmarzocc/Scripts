import ROOT
import argparse
import os
from array import array

def getExtremes(graphs):
  x_vec=[]
  y_vec=[]
  for graph in graphs: 
    for point in range(0,graph.GetN()):
      x = ROOT.double(0.)
      y = ROOT.double(0.)
      graph.GetPoint(point,x,y)
      x_vec.append(x)
      y_vec.append(y)
      #print "getExtremes:",x,y
  #print "Final extremes:",[min(x_vec),min(y_vec),max(x_vec),max(y_vec)]
  return [min(x_vec),min(y_vec),max(x_vec),max(y_vec)]     

def makeGraph(points):
  i=0
  graph = ROOT.TGraph()
  for key in points: 
    graph.SetPoint(i,key[0],key[1])
    i+=1
  return graph

def makeGraph_vs_nCat(nBins, points_1Cat, points_2Cat, points_3Cat, points_4Cat, points_5Cat):

 graph = ROOT.TGraph()
 for val in points_1Cat:
   if int(val[0]) == nBins: 
     graph.SetPoint(0,1,val[1])
 for val in points_2Cat:
   if int(val[0]) == nBins: 
     graph.SetPoint(1,2,val[1])
 for val in points_3Cat:
   if int(val[0]) == nBins: 
     graph.SetPoint(2,3,val[1])
 for val in points_4Cat:
   if int(val[0]) == nBins: 
     graph.SetPoint(3,4,val[1])
 for val in points_5Cat:
   if int(val[0]) == nBins: 
     graph.SetPoint(4,5,val[1])

 return graph  
     
def drawGraphs(graphs,name,xTitle,yTitle,logX,logY,massMin_pos,massMax_pos):

   legend = ROOT.TLegend(0.15,0.80,0.50,0.94)
   legend.SetFillColor(0)
   legend.SetFillStyle(1000)
   legend.SetTextFont(42)
   legend.SetTextSize(0.025)
   legend.SetNColumns(2)
 
   colors = (ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kViolet+1)
   for i,g in enumerate(graphs):
      g.SetLineWidth(2)
      g.SetLineColor(colors[i])
      g.SetMarkerColor(colors[i])
      g.SetMarkerStyle(20)
      legend.AddEntry(g,"["+str(int(massMin_pos[i]))+","+str(int(massMax_pos[i]))+"] GeV","PL");
   
   ranges = getExtremes(graphs)
   
   c = ROOT.TCanvas()
   c.SetGrid()
   graphs[0].GetXaxis().SetRangeUser(ranges[0]*0.95,ranges[2]*1.05)
   graphs[0].GetYaxis().SetRangeUser(ranges[1]*0.95,ranges[3]*1.15)
   graphs[0].GetXaxis().SetTitle(xTitle)
   graphs[0].GetYaxis().SetTitle(yTitle)
   graphs[0].Draw("APL")
   if logX: c.SetLogx()
   if logY: c.SetLogy()
   for i,g in enumerate(graphs):
     if i==0: continue
     g.Draw("PL,same") 
   legend.Draw("same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 


if __name__ == '__main__':

 ROOT.gROOT.SetBatch(ROOT.kTRUE)

 parser =  argparse.ArgumentParser(description='plot significance')
 parser.add_argument('-d', '--inDir',   dest='inDir',   required=True, type=str)
 parser.add_argument('-s', '--smooth',  dest='smooth',  required=True, type=int)
 parser.add_argument('-w', '--weight',  dest='weight',  required=True, type=int)
 
 
 args = parser.parse_args()
 inDir = args.inDir
 useSmoothing =  args.smooth
 useWeight = args.weight
 
 
 #inDir = /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/15/
 #inDir = /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2/15/

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
 
 os.system('ls '+inDir+'/categorize_nBins_*_nCat_*_massMin*.txt >> file_dump.txt')
 with open('file_dump.txt') as f_List:
   data_List = f_List.read()
 lines_List = data_List.splitlines() 

 nCats_pos = []
 nBins_pos = []
 massMin_pos = []
 massMax_pos = []

 points_1Cat_Total = [] 
 points_2Cat_Total = [] 
 points_3Cat_Total = [] 
 points_4Cat_Total = [] 
 points_5Cat_Total = [] 
 points_1Cat_Total_final = [] 
 points_2Cat_Total_final = [] 
 points_3Cat_Total_final = [] 
 points_4Cat_Total_final = [] 
 points_5Cat_Total_final = []  

 points_1Cat_nSig_Total = [] 
 points_2Cat_nSig_Total = [] 
 points_3Cat_nSig_Total = [] 
 points_4Cat_nSig_Total = [] 
 points_5Cat_nSig_Total = []  
 points_1Cat_nSig_Total_final = [] 
 points_2Cat_nSig_Total_final = [] 
 points_3Cat_nSig_Total_final = [] 
 points_4Cat_nSig_Total_final = [] 
 points_5Cat_nSig_Total_final = []  

 points_1Cat_nBkg_Total = []
 points_2Cat_nBkg_Total = [] 
 points_3Cat_nBkg_Total = [] 
 points_4Cat_nBkg_Total = [] 
 points_5Cat_nBkg_Total = [] 
 points_1Cat_nBkg_Total_final = []
 points_2Cat_nBkg_Total_final = [] 
 points_3Cat_nBkg_Total_final = [] 
 points_4Cat_nBkg_Total_final = [] 
 points_5Cat_nBkg_Total_final = []  

 points_1Cat_dataSB_Total = [] 
 points_2Cat_dataSB_Total = [] 
 points_3Cat_dataSB_Total = [] 
 points_4Cat_dataSB_Total = [] 
 points_5Cat_dataSB_Total = []  
 points_1Cat_dataSB_Total_final = [] 
 points_2Cat_dataSB_Total_final = [] 
 points_3Cat_dataSB_Total_final = [] 
 points_4Cat_dataSB_Total_final = [] 
 points_5Cat_dataSB_Total_final = []  

 for i,line in enumerate(lines_List):
   line_split = line.split('_')
 
   #print i,line_split
   nBins = line_split[14]
   nCats = line_split[16]
   massMin = line_split[17]
   massMin = massMin.replace('massMin','')
   massMax = line_split[18]
   massMax = massMax.replace('massMax','') 
  
   if useSmoothing==1 and 'noSmooth' in line: continue
   if useWeight==1 and 'noReweight' in line: continue

   if int(nCats) not in nCats_pos: nCats_pos.append(int(nCats))
   if int(nBins) not in nBins_pos: nBins_pos.append(int(nBins))
   if float(massMin) not in massMin_pos: massMin_pos.append(float(massMin)) 
   if float(massMax) not in massMax_pos: massMax_pos.append(float(massMax)) 

 for i,mMin in enumerate(massMin_pos):
  
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

  for nBins in nBins_pos:  
   for nCats in nCats_pos:     

    file = 0
    if useSmoothing==1 and useWeight==1:
     file = inDir+'/categorize_nBins_'+str(nBins)+'_nCat_'+str(nCats)+'_massMin'+str(massMin_pos[i])+'_massMax'+str(massMax_pos[i])+'_v2.txt'
    elif useSmoothing!=1 and useWeight==1:
     file = inDir+'/categorize_nBins_'+str(nBins)+'_nCat_'+str(nCats)+'_massMin'+str(massMin_pos[i])+'_massMax'+str(massMax_pos[i])+'_v2_noSmooth.txt'
    elif useSmoothing==1 and useWeight!=1:
     file = inDir+'/categorize_nBins_'+str(nBins)+'_nCat_'+str(nCats)+'_massMin'+str(massMin_pos[i])+'_massMax'+str(massMax_pos[i])+'_v2_noReweight.txt'
    elif useSmoothing!=1 and useWeight!=1:
     file = inDir+'/categorize_nBins_'+str(nBins)+'_nCat_'+str(nCats)+'_massMin'+str(massMin_pos[i])+'_massMax'+str(massMax_pos[i])+'_v2_noSmooth_noReweight.txt'
    if not os.path.exists(file): continue 
    with open(inDir+'/categorize_nBins_'+str(nBins)+'_nCat_'+str(nCats)+'_massMin'+str(massMin_pos[i])+'_massMax'+str(massMax_pos[i])+'_v2.txt') as f_List:
      data_List = f_List.read()
    lines_List = data_List.splitlines() 
    significance = 0.
    nSig = 0.
    nBkg = 0.
    nDataSB = 0.
    for j,cat in enumerate(lines_List):
     if 'Tot_Significance:' in cat: significance = cat.split()[-1]
     if len(cat.split())>1 and float(cat.split()[1]) == 1.: 
       nSig = float(cat.split()[5])
       nBkg = float(cat.split()[7])
       nDataSB = float(cat.split()[-1])
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

  points_1Cat_Total.append(points_1Cat)
  points_2Cat_Total.append(points_2Cat)
  points_3Cat_Total.append(points_3Cat)
  points_4Cat_Total.append(points_4Cat)
  points_5Cat_Total.append(points_5Cat)
  points_1Cat_Total_final.append(makeGraph(points_1Cat))
  points_2Cat_Total_final.append(makeGraph(points_2Cat))
  points_3Cat_Total_final.append(makeGraph(points_3Cat))
  points_4Cat_Total_final.append(makeGraph(points_4Cat))
  points_5Cat_Total_final.append(makeGraph(points_5Cat))

  points_1Cat_nSig_Total.append(points_1Cat_nSig)
  points_2Cat_nSig_Total.append(points_2Cat_nSig)
  points_3Cat_nSig_Total.append(points_3Cat_nSig)
  points_4Cat_nSig_Total.append(points_4Cat_nSig)
  points_5Cat_nSig_Total.append(points_5Cat_nSig)
  points_1Cat_nSig_Total_final.append(makeGraph(points_1Cat_nSig))
  points_2Cat_nSig_Total_final.append(makeGraph(points_2Cat_nSig))
  points_3Cat_nSig_Total_final.append(makeGraph(points_3Cat_nSig))
  points_4Cat_nSig_Total_final.append(makeGraph(points_4Cat_nSig))
  points_5Cat_nSig_Total_final.append(makeGraph(points_5Cat_nSig))

  points_1Cat_nBkg_Total.append(points_1Cat_nBkg)
  points_2Cat_nBkg_Total.append(points_2Cat_nBkg)
  points_3Cat_nBkg_Total.append(points_3Cat_nBkg)
  points_4Cat_nBkg_Total.append(points_4Cat_nBkg)
  points_5Cat_nBkg_Total.append(points_5Cat_nBkg) 
  points_1Cat_nBkg_Total_final.append(makeGraph(points_1Cat_nBkg))
  points_2Cat_nBkg_Total_final.append(makeGraph(points_2Cat_nBkg))
  points_3Cat_nBkg_Total_final.append(makeGraph(points_3Cat_nBkg))
  points_4Cat_nBkg_Total_final.append(makeGraph(points_4Cat_nBkg))
  points_5Cat_nBkg_Total_final.append(makeGraph(points_5Cat_nBkg)) 

  points_1Cat_dataSB_Total.append(points_1Cat_dataSB)
  points_2Cat_dataSB_Total.append(points_2Cat_dataSB)
  points_3Cat_dataSB_Total.append(points_3Cat_dataSB)
  points_4Cat_dataSB_Total.append(points_4Cat_dataSB)
  points_5Cat_dataSB_Total.append(points_5Cat_dataSB)  
  points_1Cat_dataSB_Total_final.append(makeGraph(points_1Cat_dataSB))
  points_2Cat_dataSB_Total_final.append(makeGraph(points_2Cat_dataSB))
  points_3Cat_dataSB_Total_final.append(makeGraph(points_3Cat_dataSB))
  points_4Cat_dataSB_Total_final.append(makeGraph(points_4Cat_dataSB))
  points_5Cat_dataSB_Total_final.append(makeGraph(points_5Cat_dataSB))  

 vec_bins = []
 for val in points_1Cat_Total[0]:
   vec_bins.append(int(val[0])) 

 for nBins in vec_bins:
   
   points_Significance = []
   points_nSig = []
   points_nBkg = []
   points_dataSB = []

   for i in range(0,len(points_1Cat_Total)): 
     points_Significance.append(makeGraph_vs_nCat(nBins, points_1Cat_Total[i], points_2Cat_Total[i], points_3Cat_Total[i], points_4Cat_Total[i], points_5Cat_Total[i]))
     points_nSig.append(makeGraph_vs_nCat(nBins, points_1Cat_nSig_Total[i], points_2Cat_nSig_Total[i], points_3Cat_nSig_Total[i], points_4Cat_nSig_Total[i], points_5Cat_nSig_Total[i]))
     points_nBkg.append(makeGraph_vs_nCat(nBins, points_1Cat_nBkg_Total[i], points_2Cat_nBkg_Total[i], points_3Cat_nBkg_Total[i], points_4Cat_nBkg_Total[i], points_5Cat_nBkg_Total[i]))
     points_dataSB.append(makeGraph_vs_nCat(nBins, points_1Cat_dataSB_Total[i], points_2Cat_dataSB_Total[i], points_3Cat_dataSB_Total[i], points_4Cat_dataSB_Total[i], points_5Cat_dataSB_Total[i]))
   
   #print "length:",len(points_Significance)
   if useSmoothing==1 and useWeight==1: 
     drawGraphs(points_Significance,"Significance_vs_nCats_nBins_"+str(nBins),"nCats","Significance",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nSig,"nSig_vs_nCats_nBins_"+str(nBins),"nCats","nSig",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nBkg,"nBkg_vs_nCats_nBins_"+str(nBins),"nCats","nBkg",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_dataSB,"dataSB_vs_nCats_nBins_"+str(nBins),"nCats","dataSB",False,False,massMin_pos,massMax_pos)
   elif useSmoothing!=1 and useWeight==1: 
     drawGraphs(points_Significance,"Significance_vs_nCats_nBins_"+str(nBins)+"_noSmooth","nCats","Significance",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nSig,"nSig_vs_nCats_nBins_"+str(nBins)+"_noSmooth","nCats","nSig",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nBkg,"nBkg_vs_nCats_nBins_"+str(nBins)+"_noSmooth","nCats","nBkg",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_dataSB,"dataSB_vs_nCats_nBins_"+str(nBins)+"_noSmooth","nCats","dataSB",False,False,massMin_pos,massMax_pos) 
   elif useSmoothing==1 and useWeight!=1: 
     drawGraphs(points_Significance,"Significance_vs_nCats_nBins_"+str(nBins)+"_noReweight","nCats","Significance",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nSig,"nSig_vs_nCats_nBins_"+str(nBins)+"_noReweight","nCats","nSig",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nBkg,"nBkg_vs_nCats_nBins_"+str(nBins)+"_noReweight","nCats","nBkg",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_dataSB,"dataSB_vs_nCats_nBins_"+str(nBins)+"_noReweight","nCats","dataSB",False,False,massMin_pos,massMax_pos) 
   elif useSmoothing!=1 and useWeight!=1: 
     drawGraphs(points_Significance,"Significance_vs_nCats_nBins_"+str(nBins)+"_noSmooth_noReweight","nCats","Significance",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nSig,"nSig_vs_nCats_nBins_"+str(nBins)+"_noSmooth_noReweight","nCats","nSig",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_nBkg,"nBkg_vs_nCats_nBins_"+str(nBins)+"_noSmooth_noReweight","nCats","nBkg",False,False,massMin_pos,massMax_pos)
     drawGraphs(points_dataSB,"dataSB_vs_nCats_nBins_"+str(nBins)+"_noSmooth_noReweight","nCats","dataSB",False,False,massMin_pos,massMax_pos) 

 if useSmoothing==1 and useWeight==1: 
   drawGraphs(points_1Cat_Total_final,"Significance_vs_nBins_nCats_1","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nSig_Total_final,"nSig_vs_nBins_nCats_1","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_1","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_1","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_2Cat_Total_final,"Significance_vs_nBins_nCats_2","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nSig_Total_final,"nSig_vs_nBins_nCats_2","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_2","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_2","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_3Cat_Total_final,"Significance_vs_nBins_nCats_3","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nSig_Total_final,"nSig_vs_nBins_nCats_3","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_3","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_3","nBins","dataSB",True,False,massMin_pos,massMax_pos) 
 
   drawGraphs(points_4Cat_Total_final,"Significance_vs_nBins_nCats_4","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nSig_Total_final,"nSig_vs_nBins_nCats_4","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_4","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_4","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_5Cat_Total_final,"Significance_vs_nBins_nCats_5","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nSig_Total_final,"nSig_vs_nBins_nCats_5","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_5","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_5","nBins","dataSB",True,False,massMin_pos,massMax_pos)
 elif useSmoothing!=1 and useWeight==1: 
   drawGraphs(points_1Cat_Total_final,"Significance_vs_nBins_nCats_1_noSmooth","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nSig_Total_final,"nSig_vs_nBins_nCats_1_noSmooth","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_1_noSmooth","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_1_noSmooth","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_2Cat_Total_final,"Significance_vs_nBins_nCats_2_noSmooth","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nSig_Total_final,"nSig_vs_nBins_nCats_2_noSmooth","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_2_noSmooth","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_2_noSmooth","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_3Cat_Total_final,"Significance_vs_nBins_nCats_3_noSmooth","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nSig_Total_final,"nSig_vs_nBins_nCats_3_noSmooth","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_3_noSmooth","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_3_noSmooth","nBins","dataSB",True,False,massMin_pos,massMax_pos) 
 
   drawGraphs(points_4Cat_Total_final,"Significance_vs_nBins_nCats_4_noSmooth","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nSig_Total_final,"nSig_vs_nBins_nCats_4_noSmooth","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_4_noSmooth","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_4_noSmooth","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_5Cat_Total_final,"Significance_vs_nBins_nCats_5_noSmooth","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nSig_Total_final,"nSig_vs_nBins_nCats_5_noSmooth","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_5_noSmooth","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_5_noSmooth","nBins","dataSB",True,False,massMin_pos,massMax_pos)
 elif useSmoothing==1 and useWeight!=1: 
   drawGraphs(points_1Cat_Total_final,"Significance_vs_nBins_nCats_1_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nSig_Total_final,"nSig_vs_nBins_nCats_1_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_1_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_1_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_2Cat_Total_final,"Significance_vs_nBins_nCats_2_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nSig_Total_final,"nSig_vs_nBins_nCats_2_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_2_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_2_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_3Cat_Total_final,"Significance_vs_nBins_nCats_3_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nSig_Total_final,"nSig_vs_nBins_nCats_3_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_3_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_3_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos) 
 
   drawGraphs(points_4Cat_Total_final,"Significance_vs_nBins_nCats_4","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nSig_Total_final,"nSig_vs_nBins_nCats_4","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_4","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_4","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_5Cat_Total_final,"Significance_vs_nBins_nCats_5_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nSig_Total_final,"nSig_vs_nBins_nCats_5_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_5_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_5_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos)
 elif useSmoothing!=1 and useWeight!=1: 
   drawGraphs(points_1Cat_Total_final,"Significance_vs_nBins_nCats_1_noSmooth_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nSig_Total_final,"nSig_vs_nBins_nCats_1_noSmooth_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_1_noSmooth_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_1Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_1_noSmooth_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_2Cat_Total_final,"Significance_vs_nBins_nCats_2_noSmooth_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nSig_Total_final,"nSig_vs_nBins_nCats_2_noSmooth_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_2_noSmooth_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_2Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_2_noSmooth_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_3Cat_Total_final,"Significance_vs_nBins_nCats_3_noSmooth_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nSig_Total_final,"nSig_vs_nBins_nCats_3_noSmooth_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_3_noSmooth_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_3Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_3_noSmooth_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos) 
 
   drawGraphs(points_4Cat_Total_final,"Significance_vs_nBins_nCats_4_noSmooth_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nSig_Total_final,"nSig_vs_nBins_nCats_4_noSmooth_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_4_noSmooth_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_4Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_4_noSmooth_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos)

   drawGraphs(points_5Cat_Total_final,"Significance_vs_nBins_nCats_5_noSmooth_noReweight","nBins","Significance",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nSig_Total_final,"nSig_vs_nBins_nCats_5_noSmooth_noReweight","nBins","nSig",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_nBkg_Total_final,"nBkg_vs_nBins_nCats_5_noSmooth_noReweight","nBins","nBkg",True,False,massMin_pos,massMax_pos)
   drawGraphs(points_5Cat_dataSB_Total_final,"dataSB_vs_nBins_nCats_5_noSmooth_noReweight","nBins","dataSB",True,False,massMin_pos,massMax_pos)

 os.system('rm file_dump.txt')
   
