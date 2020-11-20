#!/usr/bin/python
import numpy as n
import ROOT
# from ROOT import *
import sys, getopt
from array import array
from H4GSkimTools import *
from optparse import OptionParser
import operator
import argparse

if __name__ == '__main__':


  # parser = argparse.ArgumentParser(description='Mixing')
  # parser.add_argument(   "-i", "--inputFile",   dest="inputFile",    default="input.root",       type=str,  help="Input file" )
  # # parser.add_argument(   "-t", "--tree",  dest="tree",   default="tree",      type=str,  help="tree")
  # parser.add_argument(   "-e", "--e",  dest="e",   default=0,      type=int,  help="e")
  # # parser.add_argument(   "-i2", "--i2",  dest="i2",   default=0,      type=int,  help="p2")
  # # parser.add_argument(   "-i3", "--i3",  dest="i3",   default=0,      type=int,  help="p3")
  # # parser.add_argument(   "-i4", "--i4",  dest="i4",   default=0,      type=int,  help="p4")
  # # parser.add_argument(   "-y", "--y",  dest="year",   default="2016",      type=str,  help="year")
  # # parser.add_argument(   "-o", "--outputDir",  dest="outputDir",   default="",      type=str,  help="Output Dir")
  #
  # options = parser.parse_args()

  # parser = OptionParser()
  # parser.add_option("-i", "--inputFile",   dest="inputFile",    default="",       type=str,  help="Input file" )
  # parser.add_option("-e", "--e",  dest="e",   default=0,      type=int,  help="e")
  #
  # (options, args) = parser.parse_args()
  # print len(sys.argv)
  # print sys.argv[1]
  # print sys.argv[1]
  # inputFile = sys.argv[1]
  e = sys.argv[1]
  year = sys.argv[2]
  era = sys.argv[3]
  # itree = ROOT.TChain(str(options.tree))
  print "Mixing from event: ",e
  #print "Input file: ",'/eos/user/t/twamorka/h4g_fullRun2/withSystematics/'+str(year)+'/hadd/data_'+str(year)+'_skim.root'
  itree = ROOT.TChain('tagsDumper/trees/Data_13TeV_H4GTag_0')
  # itree.AddFile(options.inputFile)
  #itree.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/'+str(year)+'/hadd/data_'+str(year)+'_skim.root')
  itree.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/Data_NoPreselectionsApplied/hadd/data_'+str(era)+'.root')

  print "Total number of events to be analyzed:", itree.GetEntries()

  # outRoot = ROOT.TFile(options.outputDir+"/data_mix_"+str(options.e)+".root", "RECREATE")
  outRoot = ROOT.TFile("/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/Data_NoPreselectionsApplied/Mixing/data_mix_"+str(era)+"_"+str(year)+"_"+str(e)+".root", "RECREATE")

  treeSkimmer = SkimmedTreeTools()
  otree = treeSkimmer.MakeSkimmedTree()

  eventsToRun = itree.GetEntries()
  print " itree.GetListOfBranches = ", itree.GetListOfBranches

  for evt in range(0, eventsToRun):
    if evt%1000 == 0: print "## Analyzing event ", evt
    itree.GetEntry(evt)

    # treeSkimmer.FillEvent(itree)

    dp1_p1i = itree.a1_p1i_dM
    dp1_p2i = itree.a1_p2i_dM
    dp2_p1i = itree.a2_p1i_dM
    dp2_p2i = itree.a2_p2i_dM

    if evt == eventsToRun :
      itree.GetEntry(0)
    else :
       # print "1st photon from event#: ", options.i1
       itree.GetEntry(evt+int(e))

    ObjList = [key.GetName() for key in  itree.GetListOfBranches()]
    for branch in ObjList:
      nameToSearch1 = "pho" + str(int(dp1_p1i)+1) + "_"

      if branch.startswith(nameToSearch1) :
        getattr(treeSkimmer, branch)[0] = getattr(itree, branch)


    if evt == eventsToRun :
      itree.GetEntry(0)
    else :
      # print "2nd photon from event#: ", options.i2
      itree.GetEntry(evt+int(e)+1)

    ObjList = [key.GetName() for key in  itree.GetListOfBranches()]
    for branch in ObjList:
      nameToSearch1 = "pho" + str(int(dp1_p2i)+1) + "_"
      if branch.startswith(nameToSearch1) :
        getattr(treeSkimmer, branch)[0] = getattr(itree, branch)


    if evt == eventsToRun :
      itree.GetEntry(1)
    elif evt == (eventsToRun-1) :
      itree.GetEntry(0)
    else :
        # print "3rd photon from event#: ", options.i3
        itree.GetEntry(evt+int(e)+2)

    ObjList = [key.GetName() for key in  itree.GetListOfBranches()]
    for branch in ObjList:
      nameToSearch1 = "pho" + str(int(dp2_p1i)+1) + "_"
      if branch.startswith(nameToSearch1) :
        getattr(treeSkimmer, branch)[0] = getattr(itree, branch)

    if evt == eventsToRun :
      itree.GetEntry(2)
    elif evt == (eventsToRun-1) :
      itree.GetEntry(1)
    elif evt == (eventsToRun-2) :
      itree.GetEntry(0)
    else :
      # print "4th photon from event#: ", options.i4
      itree.GetEntry(evt+int(e)+3)
    ObjList = [key.GetName() for key in  itree.GetListOfBranches()]
    for branch in ObjList:
      nameToSearch1 = "pho" + str(int(dp2_p2i)+1) + "_"
      if branch.startswith(nameToSearch1) :
        getattr(treeSkimmer, branch)[0] = getattr(itree, branch)

    order_photons = {
          1: treeSkimmer.pho1_pt,
          2: treeSkimmer.pho2_pt,
          3: treeSkimmer.pho3_pt,
          4: treeSkimmer.pho4_pt
          }
    sorted_order_photons = sorted(order_photons.items(), key=operator.itemgetter(1))
    sorted_order_photons.reverse()   # from high to low

    sPhos = []
    sPhos_mva = []
    sPhos_full5x5_r9 = []
    sPhos_chHadIso = []
    sPhos_HoE = []
    sPhos_SCEta = []
    sPhos_PSV = []
    sPhos_EV = []
    sPhos_pfPhoIso = []
    sPhos_trkSumPt = []
    sPhos_full5x5_iEta = []
    sPhos_rho = []
    pho1_vec = []
    pho2_vec = []
    pho3_vec = []
    pho4_vec = []

    for iphoton in sorted_order_photons:
      p4 = ROOT.TLorentzVector(0,0,0,0)
      name_pt  = "pho" + str( int(iphoton [0] ) ) + "_pt"
      name_eta = "pho" + str( int(iphoton [0] ) ) + "_eta"
      name_phi = "pho" + str( int(iphoton [0] ) ) + "_phi"
      name_mva = "pho" + str( int(iphoton [0] ) ) + "_MVA"
      name_full5x5_r9 = "pho" + str( int(iphoton [0] ) ) + "_full5x5_r9"
      name_chHadIso = "pho" + str(int(iphoton [0])) + "_chHadIso"
      name_HoE = "pho" + str(int(iphoton [0])) + "_HoE"
      name_SCEta = "pho" + str(int(iphoton [0])) + "_SC_Eta"
      name_PSV = "pho" + str(int(iphoton [0])) + "_pixelseed"
      name_EV = "pho" + str(int(iphoton [0])) + "_electronveto"
      name_pfPhoIso03 = "pho" + str(int(iphoton [0])) + "_pfPhoIso03"
      name_trkSumPtHollowConeDR03 = "pho" + str(int(iphoton [0])) + "_trkSumPtHollowConeDR03"
      name_full5x5_sigmaIetaIeta = "pho" + str(int(iphoton [0])) + "_full5x5_sigmaIetaIeta"

      p4.SetPtEtaPhiM( getattr(treeSkimmer, name_pt),  getattr(treeSkimmer, name_eta),    getattr(treeSkimmer, name_phi) , 0 )
      sPhos.append(p4)
      sPhos_mva.append(getattr(treeSkimmer, name_mva))
      sPhos_full5x5_r9.append(getattr(treeSkimmer, name_full5x5_r9))
      sPhos_chHadIso.append(getattr(treeSkimmer, name_chHadIso))
      sPhos_HoE.append(getattr(treeSkimmer, name_HoE))
      sPhos_SCEta.append(getattr(treeSkimmer, name_SCEta))
      sPhos_PSV.append(getattr(treeSkimmer, name_PSV))
      sPhos_EV.append(getattr(treeSkimmer,name_EV))
      sPhos_pfPhoIso.append(getattr(treeSkimmer,name_pfPhoIso03))
      sPhos_trkSumPt.append(getattr(treeSkimmer,name_trkSumPtHollowConeDR03))
      sPhos_full5x5_iEta.append(getattr(treeSkimmer,name_full5x5_sigmaIetaIeta))
      sPhos_rho.append(itree.rho)
      
    pho1_vec.append(sPhos[0]) ##==0
    pho1_vec.append(sPhos_full5x5_r9[0]) ##==1
    pho1_vec.append(sPhos_chHadIso[0]) ##==2
    pho1_vec.append(sPhos_HoE[0]) ##==3
    pho1_vec.append(sPhos_SCEta[0]) ##==4
    pho1_vec.append(sPhos_PSV[0]) ##==5
    pho1_vec.append(sPhos_pfPhoIso[0])  ##==6
    pho1_vec.append(sPhos_trkSumPt[0]) ##==7
    pho1_vec.append(sPhos_full5x5_iEta[0]) ##==8
    pho1_vec.append(sPhos_rho[0])

    pho2_vec.append(sPhos[1])
    pho2_vec.append(sPhos_full5x5_r9[1])
    pho2_vec.append(sPhos_chHadIso[1])
    pho2_vec.append(sPhos_HoE[1])
    pho2_vec.append(sPhos_SCEta[1])
    pho2_vec.append(sPhos_PSV[1])
    pho2_vec.append(sPhos_pfPhoIso[1])
    pho2_vec.append(sPhos_trkSumPt[1])
    pho2_vec.append(sPhos_full5x5_iEta[1])
    pho2_vec.append(sPhos_rho[1])

    pho3_vec.append(sPhos[2]) ## 0
    pho3_vec.append(sPhos_full5x5_r9[2]) ## 1
    pho3_vec.append(sPhos_chHadIso[2]) ## 2
    pho3_vec.append(sPhos_HoE[2]) ## 3
    pho3_vec.append(sPhos_SCEta[2]) ## 4
    pho3_vec.append(sPhos_PSV[2]) ## 5
    pho3_vec.append(sPhos_pfPhoIso[2])
    pho3_vec.append(sPhos_trkSumPt[2])
    pho3_vec.append(sPhos_full5x5_iEta[2])
    pho3_vec.append(sPhos_rho[2])

    pho4_vec.append(sPhos[3])
    pho4_vec.append(sPhos_full5x5_r9[3])
    pho4_vec.append(sPhos_chHadIso[3])
    pho4_vec.append(sPhos_HoE[3])
    pho4_vec.append(sPhos_SCEta[3])
    pho4_vec.append(sPhos_PSV[3])
    pho4_vec.append(sPhos_pfPhoIso[3])
    pho4_vec.append(sPhos_trkSumPt[3])
    pho4_vec.append(sPhos_full5x5_iEta[3])
    pho4_vec.append(sPhos_rho[3]) 

    if (year == "2016"):
        Pho12_presel = treeSkimmer.Preselection_2016(pho1_vec, pho2_vec)
        Pho13_presel = treeSkimmer.Preselection_2016(pho1_vec, pho3_vec)
        Pho14_presel = treeSkimmer.Preselection_2016(pho1_vec, pho4_vec)
        Pho23_presel = treeSkimmer.Preselection_2016(pho2_vec, pho3_vec)
        Pho24_presel = treeSkimmer.Preselection_2016(pho2_vec, pho4_vec)
        Pho34_presel = treeSkimmer.Preselection_2016(pho3_vec, pho4_vec)

    elif (year == "2017"):
       Pho12_presel = treeSkimmer.Preselection_2017(pho1_vec, pho2_vec)
       Pho13_presel = treeSkimmer.Preselection_2017(pho1_vec, pho3_vec)
       Pho14_presel = treeSkimmer.Preselection_2017(pho1_vec, pho4_vec)
       Pho23_presel = treeSkimmer.Preselection_2017(pho2_vec, pho3_vec)
       Pho24_presel = treeSkimmer.Preselection_2017(pho2_vec, pho4_vec)
       Pho34_presel = treeSkimmer.Preselection_2017(pho3_vec, pho4_vec)

    elif (year == "2018"):
       Pho12_presel = treeSkimmer.Preselection_2018(pho1_vec, pho2_vec)
       Pho13_presel = treeSkimmer.Preselection_2018(pho1_vec, pho3_vec)
       Pho14_presel = treeSkimmer.Preselection_2018(pho1_vec, pho4_vec)
       Pho23_presel = treeSkimmer.Preselection_2018(pho2_vec, pho3_vec)
       Pho24_presel = treeSkimmer.Preselection_2018(pho2_vec, pho4_vec)
       Pho34_presel = treeSkimmer.Preselection_2018(pho3_vec, pho4_vec)


    treeSkimmer.isPresel[0] = Pho12_presel or Pho13_presel or Pho14_presel or Pho23_presel or Pho24_presel or Pho34_presel

    treeSkimmer.pho1_pt[0] = sPhos[0].Pt()
    treeSkimmer.pho2_pt[0] = sPhos[1].Pt()
    treeSkimmer.pho3_pt[0] = sPhos[2].Pt()
    treeSkimmer.pho4_pt[0] = sPhos[3].Pt()
    treeSkimmer.pho1_eta[0] = sPhos[0].Eta()
    treeSkimmer.pho2_eta[0] = sPhos[1].Eta()
    treeSkimmer.pho3_eta[0] = sPhos[2].Eta()
    treeSkimmer.pho4_eta[0] = sPhos[3].Eta()
    treeSkimmer.pho1_phi[0] = sPhos[0].Phi()
    treeSkimmer.pho2_phi[0] = sPhos[1].Phi()
    treeSkimmer.pho3_phi[0] = sPhos[2].Phi()
    treeSkimmer.pho4_phi[0] = sPhos[3].Phi()
    treeSkimmer.pho1_electronveto[0] = sPhos_EV[0]
    treeSkimmer.pho2_electronveto[0] = sPhos_EV[1]
    treeSkimmer.pho3_electronveto[0] = sPhos_EV[2]
    treeSkimmer.pho4_electronveto[0] = sPhos_EV[3]
    treeSkimmer.pho1_pixelseed[0] = sPhos_PSV[0]
    treeSkimmer.pho2_pixelseed[0] = sPhos_PSV[1]
    treeSkimmer.pho3_pixelseed[0] = sPhos_PSV[2]
    treeSkimmer.pho4_pixelseed[0] = sPhos_PSV[3]
    treeSkimmer.pho1_MVA[0] = sPhos_mva[0]
    treeSkimmer.pho2_MVA[0] = sPhos_mva[1]
    treeSkimmer.pho3_MVA[0] = sPhos_mva[2]
    treeSkimmer.pho4_MVA[0] = sPhos_mva[3]
    treeSkimmer.pho12_pt[0] = (sPhos[0]+sPhos[1]).Pt()
    treeSkimmer.pho13_pt[0] = (sPhos[0]+sPhos[2]).Pt()
    treeSkimmer.pho14_pt[0] = (sPhos[0]+sPhos[3]).Pt()
    treeSkimmer.pho23_pt[0] = (sPhos[1]+sPhos[2]).Pt()
    treeSkimmer.pho24_pt[0] = (sPhos[1]+sPhos[3]).Pt()
    treeSkimmer.pho34_pt[0] = (sPhos[2]+sPhos[3]).Pt()
    treeSkimmer.pho12_eta[0] = (sPhos[0]+sPhos[1]).Eta()
    treeSkimmer.pho13_eta[0] = (sPhos[0]+sPhos[2]).Eta()
    treeSkimmer.pho14_eta[0] = (sPhos[0]+sPhos[3]).Eta()
    treeSkimmer.pho23_eta[0] = (sPhos[1]+sPhos[2]).Eta()
    treeSkimmer.pho24_eta[0] = (sPhos[1]+sPhos[3]).Eta()
    treeSkimmer.pho34_eta[0] = (sPhos[2]+sPhos[3]).Eta()
    treeSkimmer.pho12_mass[0] = (sPhos[0]+sPhos[1]).M()
    treeSkimmer.pho13_mass[0] = (sPhos[0]+sPhos[2]).M()
    treeSkimmer.pho14_mass[0] = (sPhos[0]+sPhos[3]).M()
    treeSkimmer.pho23_mass[0] = (sPhos[1]+sPhos[2]).M()
    treeSkimmer.pho24_mass[0] = (sPhos[1]+sPhos[3]).M()
    treeSkimmer.pho34_mass[0] = (sPhos[2]+sPhos[3]).M()
    treeSkimmer.pho12_dR[0] = sPhos[0].DeltaR(sPhos[1])
    treeSkimmer.pho13_dR[0] = sPhos[0].DeltaR(sPhos[2])
    treeSkimmer.pho14_dR[0] = sPhos[0].DeltaR(sPhos[3])
    treeSkimmer.pho23_dR[0] = sPhos[1].DeltaR(sPhos[2])
    treeSkimmer.pho24_dR[0] = sPhos[1].DeltaR(sPhos[3])
    treeSkimmer.pho34_dR[0] = sPhos[2].DeltaR(sPhos[3])


    pairedDiphos = treeSkimmer.MakePairing(sPhos)
    PP1 = pairedDiphos[0][0]
    PP2 = pairedDiphos[1][0]

    # print PP1.M()
    treeSkimmer.a1_mass_dM[0] = PP1.M()
    treeSkimmer.a2_mass_dM[0] = PP2.M()
    treeSkimmer.a1_pt_dM[0] = PP1.Pt()
    treeSkimmer.a2_pt_dM[0] = PP2.Pt()
    treeSkimmer.a1_eta_dM[0] = PP1.Eta()
    treeSkimmer.a2_eta_dM[0] = PP2.Eta()
    treeSkimmer.a1_dR_dM[0] = pairedDiphos[0][1].DeltaR(pairedDiphos[0][3])
    treeSkimmer.a2_dR_dM[0] = pairedDiphos[1][1].DeltaR(pairedDiphos[1][3])
    treeSkimmer.a1_a2_dR_dM[0] = PP1.DeltaR(PP2)
    treeSkimmer.a1_p1i_dM[0] = pairedDiphos[0][2]
    treeSkimmer.a1_p2i_dM[0] = pairedDiphos[0][4]
    treeSkimmer.a2_p1i_dM[0] = pairedDiphos[1][2]
    treeSkimmer.a2_p2i_dM[0] = pairedDiphos[1][4]
    treeSkimmer.cosThetaStarCS_dM[0] = treeSkimmer.getCosThetaStar_CS(PP1, PP2)
    treeSkimmer.cosTheta_a1_dM[0] = treeSkimmer.CosThetaAngles(PP1,PP2,pairedDiphos[0][1], pairedDiphos[1][1])[0]
    treeSkimmer.cosTheta_a2_dM[0] = treeSkimmer.CosThetaAngles(PP1,PP2,pairedDiphos[0][1], pairedDiphos[1][1])[1]
    treeSkimmer.a1_energy_dM[0] = PP1.Energy()
    treeSkimmer.a2_energy_dM[0] = PP2.Energy()
    Pgggg = sPhos[0] + sPhos[1] + sPhos[2] + sPhos[3]
    treeSkimmer.tp_pt[0] = Pgggg.Pt()
    treeSkimmer.tp_eta[0] = Pgggg.Eta()
    treeSkimmer.tp_mass[0] = Pgggg.M()

    #if (treeSkimmer.isPresel[0] == 1):
    otree.Fill()
    # else: print "Failed preselection"
  outRoot.cd()
  otree.Write()
  outRoot.Close()
