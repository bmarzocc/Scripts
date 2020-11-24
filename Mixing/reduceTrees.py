import ROOT
import argparse

parser =  argparse.ArgumentParser(description='Skim data ntuples')
parser.add_argument('-y', '--y', dest='y', required=True, type=str)
parser.add_argument('-e', '--e', dest='e', required=True, type=str)
opt = parser.parse_args()

infile = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/'+str(opt.y)+'/Data_NoPreselectionsApplied/hadd/data_'+str(opt.e)
f1 = ROOT.TFile(infile+'.root')
ntuple = f1.Get('tagsDumper/trees/Data_13TeV_H4GTag_0')
f2 = ROOT.TFile(infile+'_skim.root','recreate')
small = ntuple.CopyTree('pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1  && tp_mass > 110 && tp_mass < 180')
small.Write()
