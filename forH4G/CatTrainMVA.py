import ROOT
import argparse

parser =  argparse.ArgumentParser(description='cat MVA')
parser.add_argument('-o', '--output', dest='output', required=True, type=str)

args = parser.parse_args()
output = args.output

## Files used for VBF related training
bkg_file = ROOT.TChain()
bkg_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/data_mix_weight.root/Data_13TeV_H4GTag_0')

sig_file = ROOT.TChain()
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_60.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_55.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_55_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_50.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_50_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_45.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_45_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_40.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_40_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_35.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_35_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_30.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_30_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_25.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_25_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_20.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_20_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_15.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_15_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_10.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_10_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')
sig_file.AddFile('/eos/user/t/twamorka/h4g_fullRun2/2016/hadd/withEnergyVar/signal_m_5.root/tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_5_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0')

f_out = ROOT.TFile(output+'.root','RECREATE')

ROOT.TMVA.Tools.Instance()
factory = ROOT.TMVA.Factory("TMVAClassification", f_out,"AnalysisType=Classification")

mvaVars = [
'cosThetaStarCS_dM',
'cosTheta_a1_dM',
'cosTheta_a2_dM',
#'a1_mass_dM',
#'a2_mass_dM',
'a1_pt_dM',
'a2_pt_dM',
'a1_energy_dM',
'a2_energy_dM',
# 'a1_eta_dM',
# 'a2_eta_dM',
'a1_dR_dM',
'a2_dR_dM',
'a1_a2_dR_dM',
'fabs(a1_mass_dM-a2_mass_dM)/tp_mass',
#'tp_pt',
#'tp_eta',
'pho1_MVA',
'pho2_MVA',
'pho3_MVA',
'pho4_MVA',
#'pho1_pt',
#'pho2_pt',
#'pho3_pt',
#'pho4_pt',
#'pho1_eta',
#'pho2_eta',
#'pho3_eta',
#'pho4_eta'
]

dataloader = ROOT.TMVA.DataLoader("dataset")

for x in mvaVars:
    #factory.AddVariable(x,"F")
    dataloader.AddVariable(x,"F")

dataloader.AddSignalTree(sig_file)
dataloader.AddBackgroundTree(bkg_file)

Cut_Signal = 'abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180&& pho1_MVA > -999. && pho2_MVA > -999. && pho3_MVA > -999. && pho4_MVA > -999 && pho1_pt > -999. && pho2_pt > -999. && pho3_pt > -999. && pho4_pt > -999.'

Cut_Background = 'abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass <180 && pho1_MVA > -999. && pho2_MVA > -999. && pho3_MVA > -999. && pho4_MVA > -999 && pho1_pt > -999. && pho2_pt > -999. && pho3_pt > -999. && pho4_pt > -999.'

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

