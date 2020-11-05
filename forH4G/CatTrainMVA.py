import ROOT
import argparse

parser =  argparse.ArgumentParser(description='cat MVA')
parser.add_argument('-o', '--output', dest='output', required=True, type=str)

args = parser.parse_args()
output = args.output

Cut_Signal = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180)'

Cut_Background = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180)'

Cut_Data = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180 && !(tp_mass > 115 && tp_mass <135))'

#sig_list = [5,10,15,20,25,30,35,40,45,50,55,60]
sig_list = [60]
sig_nums_2016 = []
sig_nums_2017 = []
sig_nums_2018 = []
sig_file_2016 = []
sig_file_2017 = []
sig_file_2018 = []

for mass in sig_list:

   sig_file_2016_tmp = ROOT.TChain()
   tree_name_2016 = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+str(mass)+'_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0'
   sig_file_2016_tmp.AddFile(tree_name_2016)
   sig_file_2016.append(sig_file_2016_tmp)      
   sig_nums_2016.append(float(sig_file_2016_tmp.GetEntries(Cut_Signal))) 
   
   sig_file_2017_tmp = ROOT.TChain()
   tree_name_2017 = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+str(mass)+'_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0'
   sig_file_2017_tmp.AddFile(tree_name_2017)
   sig_file_2017.append(sig_file_2017_tmp)      
   sig_nums_2017.append(float(sig_file_2017_tmp.GetEntries(Cut_Signal))) 

   sig_file_2018_tmp = ROOT.TChain()
   tree_name_2018 = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/HAHMHToAA_AToGG_MA_'+str(mass)+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0'
   sig_file_2018_tmp.AddFile(tree_name_2018)
   sig_file_2018.append(sig_file_2018_tmp)      
   sig_nums_2018.append(float(sig_file_2018_tmp.GetEntries(Cut_Signal))) 

lumi_2016 = 35.9
data_file_2016 = ROOT.TChain()
data_file_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_2016.root/tagsDumper/trees/Data_13TeV_H4GTag_0')
datamix_file_2016 = ROOT.TChain()
datamix_file_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_mix_weight_v8.root/Data_13TeV_H4GTag_0')
data_2016 = float(data_file_2016.GetEntries(Cut_Data))
datamix_2016 = float(datamix_file_2016.GetEntries(Cut_Background))

lumi_2017 = 41.5
data_file_2017 = ROOT.TChain()
data_file_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_2017.root/tagsDumper/trees/Data_13TeV_H4GTag_0')
datamix_file_2017 = ROOT.TChain()
datamix_file_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_mix_weight_v8.root/Data_13TeV_H4GTag_0')
data_2017 = float(data_file_2017.GetEntries(Cut_Data))
datamix_2017 = float(datamix_file_2017.GetEntries(Cut_Background))

lumi_2018 = 54.38
data_file_2018 = ROOT.TChain()
data_file_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_2018.root/tagsDumper/trees/Data_13TeV_H4GTag_0')
datamix_file_2018 = ROOT.TChain()
datamix_file_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_mix_weight_v8.root/Data_13TeV_H4GTag_0')
data_2018 = float(data_file_2018.GetEntries(Cut_Data))
datamix_2018 = float(datamix_file_2018.GetEntries(Cut_Background))

f_out = ROOT.TFile(output+'.root','RECREATE')
ROOT.TMVA.Tools.Instance()
factory = ROOT.TMVA.Factory("TMVAClassification", f_out,"AnalysisType=Classification")

dataloader = ROOT.TMVA.DataLoader("dataset")
#mvaVars = ['pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']
mvaVars = ['a1_mass_dM-a2_mass_dM', 'cosTheta_a1_dM', 'a1_pt_dM', 'a2_pt_dM', 'pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']
#mvaVars = ['genMass', 'a1_mass_dM-a2_mass_dM', 'cosTheta_a1_dM', 'a1_pt_dM', 'a2_pt_dM', 'pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']
for x in mvaVars:
   #factory.AddVariable(x,"F")
   dataloader.AddVariable(x,"F")

for i,mass in enumerate(sig_list):
   print "---> Signal normalization 2016: mass",mass,"-",float(sig_nums_2016[i])
   dataloader.AddSignalTree(sig_file_2016[i],lumi_2016/float(sig_nums_2016[i]))
   print "---> Signal normalization 2017: mass",mass,"-",float(sig_nums_2017[i])
   dataloader.AddSignalTree(sig_file_2017[i],lumi_2017/float(sig_nums_2017[i])) 
   print "---> Signal normalization 2018: mass",mass,"-",float(sig_nums_2018[i])
   dataloader.AddSignalTree(sig_file_2018[i],lumi_2018/float(sig_nums_2018[i]))

print "---> Background normalization 2016: ",datamix_2016/data_2016
dataloader.AddBackgroundTree(data_file_2016,datamix_2016/data_2016)
print "---> Background normalization 2017: ",datamix_2017/data_2017
dataloader.AddBackgroundTree(data_file_2017,datamix_2017/data_2017)
print "---> Background normalization 2018: ",datamix_2018/data_2018
dataloader.AddBackgroundTree(data_file_2018,datamix_2018/data_2018)

sigCut = ROOT.TCut(Cut_Signal)
bkgCut = ROOT.TCut(Cut_Background)

print "S Cut: ", sigCut
print "B Cut: ", bkgCut

dataloader.SetWeightExpression("weight","Signal")
dataloader.SetWeightExpression("weight","Background")

dataloader.PrepareTrainingAndTestTree(sigCut,bkgCut,"nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V")
method = factory.BookMethod( dataloader,ROOT.TMVA.Types.kBDT, "BDTG", "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" )

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

