import ROOT
import argparse
parser =  argparse.ArgumentParser(description='pairing MVA')
parser.add_argument('-o', '--output', dest='output', required=True, type=str)
# parser.add_argument('-oD', '--outputDir', dest='outputDir', required=True, type=str)

args = parser.parse_args()
output = args.output

bkg_file = ROOT.TChain()
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_60.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_55.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_50.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_45.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_40.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_35.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_30.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_25.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_20.root/diphotonPair_BDT_bkg')
bkg_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_15.root/diphotonPair_BDT_bkg')

sig_file = ROOT.TChain()
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_60.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_55.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_50.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_45.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_40.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_35.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_30.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_25.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_20.root/diphotonPair_BDT_sig')
sig_file.AddFile('/eos/user/t/twamorka/EOY_2019/24Dec2019/hadd/signal_m_15.root/diphotonPair_BDT_sig')


f_out = ROOT.TFile(output+'.root','RECREATE')

ROOT.TMVA.Tools.Instance()
factory = ROOT.TMVA.Factory("TMVAClassification", f_out,"AnalysisType=Classification")

Vars = [
'dipho1_energy',
'dipho1_pt',
'dipho1_eta',
'dipho1_dR',
'dipho2_energy',
'dipho2_pt',
'dipho2_eta',
'dipho2_dR',
'dipair_dR'
]

dataloader = ROOT.TMVA.DataLoader("dataset")

for var in Vars:
    dataloader.AddVariable(var,"F")

dataloader.AddSignalTree(sig_file)
dataloader.AddBackgroundTree(bkg_file)

sigCut = ROOT.TCut('1>0')
bkgCut = ROOT.TCut('1>0')
# sigCut = ROOT.TCut('abs(dipho1_energy)<999. and abs(dipho1_pt)<999. and abs(dipho1_eta)<999. and abs(dipho1_dR)<999.  and abs(dipho2_energy)<999. and abs(dipho2_pt)<999. and abs(dipho2_eta)<999. and abs(dipho2_dR)<999. and  abs(dipair_dR)<999.')
# bkgCut = ROOT.TCut('abs(dipho1_energy)<999. and abs(dipho1_pt)<999. and abs(dipho1_eta)<999. and abs(dipho1_dR)<999.  and abs(dipho2_energy)<999. and abs(dipho2_pt)<999. and abs(dipho2_eta)<999. and abs(dipho2_dR)<999. and  abs(dipair_dR)<999.')

# dataloader.PrepareTrainingAndTestTree(sigCut,bkgCut,"SplitMode=Random:NormMode=NumEvents:!V")
# method = factory.BookMethod( dataloader, ROOT.TMVA.Types.kBDT, "BDT", "UseRandomisedTrees=1:NTrees=1000:BoostType=Grad:NegWeightTreatment=IgnoreNegWeightsInTraining:MaxDepth=3:MinNodeSize=3:Shrinkage=0.1625:nCuts=200")
dataloader.PrepareTrainingAndTestTree(sigCut,bkgCut,"nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V")
#method = factory.BookMethod( dataloader,ROOT.TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=200")#:nCuts=200")
method = factory.BookMethod( dataloader,ROOT.TMVA.Types.kBDT, "BDTG", "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" )


factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
