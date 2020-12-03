import ROOT
import itertools
from array import array

def MakeTree(inputTree, ouputFile, h_ratio):
 outfile = ROOT.TFile(ouputFile, "RECREATE")
 outtree = inputTree.CloneTree(0)
 bdt_weight = array('f', [0])
 _bdt_weight = outtree.Branch('bdt_weight', bdt_weight, 'bdt_weight/F')     
 nentries = inputTree.GetEntries()
 for i in range(0, nentries):
    inputTree.GetEntry(i)
    inputTree.bdt
    if h_ratio.GetBinContent(h_ratio.FindBin(inputTree.bdt))!=0.: 
        bdt_weight[0] = h_ratio.GetBinContent(h_ratio.FindBin(inputTree.bdt))
    else: bdt_weight[0] = 1. 
    outtree.Fill() 
 outfile.cd()
 outtree.Write()
 outfile.Close()

if __name__ == '__main__': 
 
 f_datamix_SB = ROOT.TFile('/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_19Nov2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m60_2Dec2020/BDT_DataMix_SB.root',"READ")
 h_bdt_datamix_SB = f_datamix_SB.Get('locHist_DataMix') 
 
 f_data_SB = ROOT.TFile('/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_19Nov2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m60_2Dec2020/BDT_Data_SB.root',"READ")
 h_bdt_data_SB = f_data_SB.Get('dataHist') 
 
 h_bdt_data_SB.Divide(h_bdt_datamix_SB)

 print "Filling 2016 datamix..."
 tree_datamix_2016 = ROOT.TChain() 
 tree_datamix_2016.AddFile('/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_19Nov2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m60_2Dec2020/data_mix_2016_kinWeight.root/Data_13TeV_H4GTag_0') 
 MakeTree(tree_datamix_2016, 'data_mix_2016_bdtWeight_kinWeight.root', h_bdt_data_SB) 

 print "Filling 2017 datamix..."
 tree_datamix_2017 = ROOT.TChain() 
 tree_datamix_2017.AddFile('/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_19Nov2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m60_2Dec2020/data_mix_2017_kinWeight.root/Data_13TeV_H4GTag_0') 
 MakeTree(tree_datamix_2017, 'data_mix_2017_bdtWeight_kinWeight.root', h_bdt_data_SB) 

 print "Filling 2018 datamix..."
 tree_datamix_2018 = ROOT.TChain() 
 tree_datamix_2018.AddFile('/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_19Nov2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m60_2Dec2020/data_mix_2018_kinWeight.root/Data_13TeV_H4GTag_0') 
 MakeTree(tree_datamix_2018, 'data_mix_2018_bdtWeight_kinWeight.root', h_bdt_data_SB) 
 
