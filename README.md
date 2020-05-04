# Scripts
Repository to keep track of useful scripts

python applyVBFWeight.py --i /eos/user/t/twamorka/21March2020_Mixing/hadd/OldPairing/data_all_skim_small_forVBF_Loose.root -t Data_13TeV_4photons -s dataCR -o /eos/user/t/twamorka/1April2020_CatTrainign/11April2020_VBFTraining_LooseWP/data_CR.root

python applyVBFWeight.py --i /eos/user/t/twamorka/21March2020_Mixing/hadd/OldPairing/data_all_skim.root -t Data_13TeV_4photons -s data -o /eos/user/t/twamorka/1April2020_CatTrainign/11April2020_VBFTraining_LooseWP/data_all_skim.root

python applyVBFWeight.py --i /eos/user/t/twamorka/Jan2020/2016Samples/OldDiphoPairing/signal_m_60_skim.root -t SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons -s signal -o /eos/user/t/twamorka/1April2020_CatTrainign/11April2020_VBFTraining_LooseWP/signal_m_60_skim.root

python applyVBFWeight.py --i /eos/user/t/twamorka/Jan2020/2016Samples/OldDiphoPairing/DiPho40to80_skim.root -t DiPhotonJetsBox_M40_80_Sherpa_13TeV_4photons -s dipho -o /eos/user/t/twamorka/1April2020_CatTrainign/11April2020_VBFTraining_LooseWP/DiPho40to80_skim.root

python applyVBFWeight.py --i /eos/user/t/twamorka/Jan2020/2016Samples/OldDiphoPairing/DiPho80toInf_skim.root -t DiPhotonJetsBox_MGG_80toInf_13TeV_Sherpa_13TeV_4photons -s dipho -o /eos/user/t/twamorka/1April2020_CatTrainign/11April2020_VBFTraining_LooseWP/DiPho80toInf_skim.root

python runSoBOptimization.py -v "bdt" -M 1. -m 0 -n 2000

python runSoBOptimization_Condor.py -v "pho1_MVA,pho2_MVA,pho3_MVA,pho4_MVA" -M "1.,1.,1.,1." -m "-1.,-1.,-1.,-1." -n 40 -b 500

python computeSoBMaximum.py -i output/



