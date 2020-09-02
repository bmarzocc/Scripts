import ROOT
import argparse

parser =  argparse.ArgumentParser(description='cat MVA')
parser.add_argument('-o', '--output', dest='output', required=True, type=str)

args = parser.parse_args()
output = args.output

bkg_file_2016 = ROOT.TChain()
bkg_file_2017 = ROOT.TChain()
bkg_file_2018 = ROOT.TChain()
bkg_file_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_mix_weight_v3.root/Data_13TeV_H4GTag_0')
bkg_file_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_mix_weight_v3.root/Data_13TeV_H4GTag_0')
bkg_file_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_mix_weight_v3.root/Data_13TeV_H4GTag_0')

#sig_list = [5,10,15,20,25,30,35,40,45,50,55,60]
#sig_list = [15,25,35,45,60]
sig_list = [45]
sig_file_2016 = ROOT.TChain()
sig_file_2017 = ROOT.TChain()
sig_file_2018 = ROOT.TChain()
for mass in sig_list:
   sig_file_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+str(mass)+'_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
   sig_file_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+str(mass)+'_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0')
   sig_file_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/signal_m_'+str(mass)+'.root/tagsDumper/trees/HAHMHToAA_AToGG_MA_'+str(mass)+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0')


f_out = ROOT.TFile(output+'.root','RECREATE')

ROOT.TMVA.Tools.Instance()
factory = ROOT.TMVA.Factory("TMVAClassification", f_out,"AnalysisType=Classification")

#mvaVars = ['pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']

mvaVars = ['a1_mass_dM-a2_mass_dM', 'cosTheta_a1_dM', 'a1_pt_dM', 'a2_pt_dM', 'pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']

#mvaVars = ['a1_mass_dM-a2_mass_dM', 'cosThetaStarCS_dM', 'a1_pt_dM', 'a2_pt_dM', 'pho4_pt', 'pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']

#mvaVars = ['a1_mass_dM-a2_mass_dM', 'a1_dR_dM', 'a2_dR_dM', 'a1_pt_dM', 'a2_pt_dM', 'pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']

#mvaVars = ['a1_mass_dM-a2_mass_dM', 'cosThetaStarCS_dM', 'cosTheta_a1_dM', 'cosTheta_a2_dM', 'a1_pt_dM', 'a2_pt_dM', 'a1_energy_dM', 'a2_energy_dM', 'a1_dR_dM', 'a2_dR_dM', 'a1_a2_dR_dM', 'pho1_pt', 'pho2_pt', 'pho3_pt', 'pho4_pt', 'pho1_MVA', 'pho2_MVA', 'pho3_MVA', 'pho4_MVA']

Cut_Signal = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180 && pho1_MVA > -999. && pho2_MVA > -999. && pho3_MVA > -999. && pho4_MVA > -999)'

Cut_Background = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180 && pho1_MVA > -999. && pho2_MVA > -999. && pho3_MVA > -999. && pho4_MVA > -999)'

lumi_2016 = 35.9
norm_2016 = float(bkg_file_2016.GetEntries(Cut_Background))

lumi_2017 = 41.5
norm_2017 = float(bkg_file_2017.GetEntries(Cut_Background))

lumi_2018 = 54.38
norm_2018 = float(bkg_file_2018.GetEntries(Cut_Background))

dataloader = ROOT.TMVA.DataLoader("dataset")

for x in mvaVars:
    #factory.AddVariable(x,"F")
    dataloader.AddVariable(x,"F")

dataloader.AddSignalTree(sig_file_2016,lumi_2016)
dataloader.AddBackgroundTree(bkg_file_2016,lumi_2016/norm_2016)

dataloader.AddSignalTree(sig_file_2017,lumi_2017)
dataloader.AddBackgroundTree(bkg_file_2017,lumi_2017/norm_2017)

dataloader.AddSignalTree(sig_file_2018,lumi_2018)
dataloader.AddBackgroundTree(bkg_file_2018,lumi_2018/norm_2018)

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

