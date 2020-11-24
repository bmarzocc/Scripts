#!/usr/bin/python

from ROOT import *
import sys, getopt
from array import array
import numpy as n
import math

DEBUG = 0

class SkimmedTreeTools:
   def __init__(self):
      self.candidate_id = n.zeros(1,dtype=float)
      self.weight = n.zeros(1,dtype=float)
      self.CMS_hgg_mass = n.zeros(1,dtype=float)
      self.pho1_pt = n.zeros(1,dtype=float)
      self.pho2_pt = n.zeros(1,dtype=float)
      self.pho3_pt = n.zeros(1,dtype=float)
      self.pho4_pt = n.zeros(1,dtype=float)
      self.pho1_eta = n.zeros(1,dtype=float)
      self.pho2_eta = n.zeros(1,dtype=float)
      self.pho3_eta = n.zeros(1,dtype=float)
      self.pho4_eta = n.zeros(1,dtype=float)
      self.pho1_phi = n.zeros(1,dtype=float)
      self.pho2_phi = n.zeros(1,dtype=float)
      self.pho3_phi = n.zeros(1,dtype=float)
      self.pho4_phi = n.zeros(1,dtype=float)
      self.pho1_MVA = n.zeros(1,dtype=float)
      self.pho2_MVA = n.zeros(1,dtype=float)
      self.pho3_MVA = n.zeros(1,dtype=float)
      self.pho4_MVA = n.zeros(1,dtype=float)
      self.pho1_electronveto = n.zeros(1,dtype=float)
      self.pho2_electronveto = n.zeros(1,dtype=float)
      self.pho3_electronveto = n.zeros(1,dtype=float)
      self.pho4_electronveto = n.zeros(1,dtype=float)
      self.pho1_pixelseed = n.zeros(1,dtype=float)
      self.pho2_pixelseed = n.zeros(1,dtype=float)
      self.pho3_pixelseed = n.zeros(1,dtype=float)
      self.pho4_pixelseed = n.zeros(1,dtype=float)
      self.pho1_full5x5_r9 = n.zeros(1,dtype=float)
      self.pho2_full5x5_r9 = n.zeros(1,dtype=float)
      self.pho3_full5x5_r9 = n.zeros(1,dtype=float)
      self.pho4_full5x5_r9 = n.zeros(1,dtype=float)
      self.pho1_chHadIso = n.zeros(1,dtype=float)
      self.pho2_chHadIso = n.zeros(1,dtype=float)
      self.pho3_chHadIso = n.zeros(1,dtype=float)
      self.pho4_chHadIso = n.zeros(1,dtype=float)
      self.pho1_HoE = n.zeros(1,dtype=float)
      self.pho2_HoE = n.zeros(1,dtype=float)
      self.pho3_HoE = n.zeros(1,dtype=float)
      self.pho4_HoE = n.zeros(1,dtype=float)
      self.pho1_pfPhoIso03 = n.zeros(1,dtype=float)
      self.pho2_pfPhoIso03 = n.zeros(1,dtype=float)
      self.pho3_pfPhoIso03 = n.zeros(1,dtype=float)
      self.pho4_pfPhoIso03 = n.zeros(1,dtype=float)
      self.pho1_trkSumPtHollowConeDR03 = n.zeros(1,dtype=float)
      self.pho2_trkSumPtHollowConeDR03 = n.zeros(1,dtype=float)
      self.pho3_trkSumPtHollowConeDR03 = n.zeros(1,dtype=float)
      self.pho4_trkSumPtHollowConeDR03 = n.zeros(1,dtype=float)
      self.pho1_full5x5_sigmaIetaIeta = n.zeros(1,dtype=float)
      self.pho2_full5x5_sigmaIetaIeta = n.zeros(1,dtype=float)
      self.pho3_full5x5_sigmaIetaIeta = n.zeros(1,dtype=float)
      self.pho4_full5x5_sigmaIetaIeta = n.zeros(1,dtype=float)
      self.pho1_SC_Eta = n.zeros(1,dtype=float)
      self.pho2_SC_Eta = n.zeros(1,dtype=float)
      self.pho3_SC_Eta = n.zeros(1,dtype=float)
      self.pho4_SC_Eta = n.zeros(1,dtype=float)
      self.pho1_genType = n.zeros(1,dtype=float)
      self.pho2_genType = n.zeros(1,dtype=float)
      self.pho3_genType = n.zeros(1,dtype=float)
      self.pho4_genType = n.zeros(1,dtype=float)
      self.pho1_energy = n.zeros(1,dtype=float)
      self.pho1_energy_init = n.zeros(1,dtype=float)
      self.pho2_energy = n.zeros(1,dtype=float)
      self.pho3_energy = n.zeros(1,dtype=float)
      self.pho4_energy = n.zeros(1,dtype=float)
      self.pho12_pt = n.zeros(1,dtype=float)
      self.pho13_pt = n.zeros(1,dtype=float)
      self.pho14_pt = n.zeros(1,dtype=float)
      self.pho23_pt = n.zeros(1,dtype=float)
      self.pho24_pt = n.zeros(1,dtype=float)
      self.pho34_pt = n.zeros(1,dtype=float)
      self.pho12_eta = n.zeros(1,dtype=float)
      self.pho13_eta = n.zeros(1,dtype=float)
      self.pho14_eta = n.zeros(1,dtype=float)
      self.pho23_eta = n.zeros(1,dtype=float)
      self.pho24_eta = n.zeros(1,dtype=float)
      self.pho34_eta = n.zeros(1,dtype=float)
      self.pho12_mass = n.zeros(1,dtype=float)
      self.pho13_mass = n.zeros(1,dtype=float)
      self.pho14_mass = n.zeros(1,dtype=float)
      self.pho23_mass = n.zeros(1,dtype=float)
      self.pho24_mass = n.zeros(1,dtype=float)
      self.pho34_mass = n.zeros(1,dtype=float)
      self.pho12_dR = n.zeros(1,dtype=float)
      self.pho13_dR = n.zeros(1,dtype=float)
      self.pho14_dR = n.zeros(1,dtype=float)
      self.pho23_dR = n.zeros(1,dtype=float)
      self.pho24_dR = n.zeros(1,dtype=float)
      self.pho34_dR = n.zeros(1,dtype=float)
      self.diphoPair_MVA = n.zeros(1,dtype=float)
      self.a1_mass_bdt = n.zeros(1,dtype=float)
      self.a2_mass_bdt = n.zeros(1,dtype=float)
      self.a1_pt_bdt = n.zeros(1,dtype=float)
      self.a2_pt_bdt = n.zeros(1,dtype=float)
      self.a1_eta_bdt = n.zeros(1,dtype=float)
      self.a2_eta_bdt = n.zeros(1,dtype=float)
      self.a1_dR_bdt = n.zeros(1,dtype=float)
      self.a2_dR_bdt = n.zeros(1,dtype=float)
      self.a1_a2_dR_bdt = n.zeros(1,dtype=float)
      self.cosThetaStarCS_bdt = n.zeros(1,dtype=float)
      self.cosTheta_a1_bdt = n.zeros(1,dtype=float)
      self.cosTheta_a2_bdt = n.zeros(1,dtype=float)
      self.a1_p1i_bdt = n.zeros(1,dtype=float)
      self.a1_p2i_bdt = n.zeros(1,dtype=float)
      self.a2_p1i_bdt = n.zeros(1,dtype=float)
      self.a2_p2i_bdt = n.zeros(1,dtype=float)
      self.a1_mass_dM = n.zeros(1,dtype=float)
      self.a2_mass_dM = n.zeros(1,dtype=float)
      self.a1_energy_dM = n.zeros(1,dtype=float)
      self.a2_energy_dM = n.zeros(1,dtype=float)
      self.a1_pt_dM = n.zeros(1,dtype=float)
      self.a2_pt_dM = n.zeros(1,dtype=float)
      self.a1_eta_dM = n.zeros(1,dtype=float)
      self.a2_eta_dM = n.zeros(1,dtype=float)
      self.a1_dR_dM = n.zeros(1,dtype=float)
      self.a2_dR_dM = n.zeros(1,dtype=float)
      self.a1_a2_dR_dM = n.zeros(1,dtype=float)
      self.cosThetaStarCS_dM = n.zeros(1,dtype=float)
      self.cosTheta_a1_dM = n.zeros(1,dtype=float)
      self.cosTheta_a2_dM = n.zeros(1,dtype=float)
      self.a1_energy_dM = n.zeros(1,dtype=float)
      self.a2_energy_dM = n.zeros(1,dtype=float)
      self.a1_p1i_dM = n.zeros(1,dtype=int)
      self.a1_p2i_dM = n.zeros(1,dtype=int)
      self.a2_p1i_dM = n.zeros(1,dtype=int)
      self.a2_p2i_dM = n.zeros(1,dtype=int)
      self.dZ_bdtVtx = n.zeros(1,dtype=float)
      self.tp_pt = n.zeros(1,dtype=float)
      self.tp_eta = n.zeros(1,dtype=float)
      self.tp_mass = n.zeros(1,dtype=float)
      self.rho = n.zeros(1,dtype=float)
      self.nvtx = n.zeros(1,dtype=int)
      self.event = n.zeros(1,dtype=int)
      self.lumi = n.zeros(1,dtype=int)
      self.processIndex = n.zeros(1,dtype=float)
      self.run = n.zeros(1,dtype=int)
      self.npu = n.zeros(1,dtype=float)
      self.puweight = n.zeros(1,dtype=float)
      self.isPresel = n.zeros(1,dtype=int)



   def MakeSkimmedTree(self):
      outTree = TTree("Data_13TeV_H4GTag_0", "Data_13TeV_H4GTag_0")
      SetOwnership(outTree,0)
      outTree.Branch('pho1_pt', self.pho1_pt, 'pho1_pt/D')
      outTree.Branch('pho2_pt', self.pho2_pt, 'pho2_pt/D')
      outTree.Branch('pho3_pt', self.pho3_pt, 'pho3_pt/D')
      outTree.Branch('pho4_pt', self.pho4_pt, 'pho4_pt/D')
      outTree.Branch('pho1_eta', self.pho1_eta, 'pho1_eta/D')
      outTree.Branch('pho2_eta', self.pho2_eta, 'pho2_eta/D')
      outTree.Branch('pho3_eta', self.pho3_eta, 'pho3_eta/D')
      outTree.Branch('pho4_eta', self.pho4_eta, 'pho4_eta/D')
      outTree.Branch('pho1_phi', self.pho1_phi, 'pho1_phi/D')
      outTree.Branch('pho2_phi', self.pho2_phi, 'pho2_phi/D')
      outTree.Branch('pho3_phi', self.pho3_phi, 'pho3_phi/D')
      outTree.Branch('pho4_phi', self.pho4_phi, 'pho4_phi/D')
      outTree.Branch('pho1_electronveto', self.pho1_electronveto, 'pho1_electronveto/D')
      outTree.Branch('pho2_electronveto', self.pho2_electronveto, 'pho2_electronveto/D')
      outTree.Branch('pho3_electronveto', self.pho3_electronveto, 'pho3_electronveto/D')
      outTree.Branch('pho4_electronveto', self.pho4_electronveto, 'pho4_electronveto/D')
      outTree.Branch('pho1_pixelseed', self.pho1_pixelseed, 'pho1_pixelseed/D')
      outTree.Branch('pho2_pixelseed', self.pho2_pixelseed, 'pho2_pixelseed/D')
      outTree.Branch('pho3_pixelseed', self.pho3_pixelseed, 'pho3_pixelseed/D')
      outTree.Branch('pho4_pixelseed', self.pho4_pixelseed, 'pho4_pixelseed/D')
      outTree.Branch('pho1_full5x5_r9', self.pho1_full5x5_r9, 'pho1_full5x5_r9/D')
      outTree.Branch('pho2_full5x5_r9', self.pho2_full5x5_r9, 'pho2_full5x5_r9/D')
      outTree.Branch('pho3_full5x5_r9', self.pho3_full5x5_r9, 'pho3_full5x5_r9/D')
      outTree.Branch('pho4_full5x5_r9', self.pho4_full5x5_r9, 'pho4_full5x5_r9/D')
      outTree.Branch('pho1_chHadIso', self.pho1_chHadIso, 'pho1_chHadIso/D')
      outTree.Branch('pho2_chHadIso', self.pho2_chHadIso, 'pho2_chHadIso/D')
      outTree.Branch('pho3_chHadIso', self.pho3_chHadIso, 'pho3_chHadIso/D')
      outTree.Branch('pho4_chHadIso', self.pho4_chHadIso, 'pho4_chHadIso/D')
      outTree.Branch('pho1_HoE', self.pho1_HoE, 'pho1_HoE/D')
      outTree.Branch('pho2_HoE', self.pho2_HoE, 'pho2_HoE/D')
      outTree.Branch('pho3_HoE', self.pho3_HoE, 'pho3_HoE/D')
      outTree.Branch('pho4_HoE', self.pho4_HoE, 'pho4_HoE/D')
      outTree.Branch('pho1_pfPhoIso03', self.pho1_pfPhoIso03, 'pho1_pfPhoIso03/D')
      outTree.Branch('pho2_pfPhoIso03', self.pho2_pfPhoIso03, 'pho2_pfPhoIso03/D')
      outTree.Branch('pho3_pfPhoIso03', self.pho3_pfPhoIso03, 'pho3_pfPhoIso03/D')
      outTree.Branch('pho4_pfPhoIso03', self.pho4_pfPhoIso03, 'pho4_pfPhoIso03/D')
      outTree.Branch('pho1_trkSumPtHollowConeDR03', self.pho1_trkSumPtHollowConeDR03, 'pho1_trkSumPtHollowConeDR03/D')
      outTree.Branch('pho2_trkSumPtHollowConeDR03', self.pho2_trkSumPtHollowConeDR03, 'pho2_trkSumPtHollowConeDR03/D')
      outTree.Branch('pho3_trkSumPtHollowConeDR03', self.pho3_trkSumPtHollowConeDR03, 'pho3_trkSumPtHollowConeDR03/D')
      outTree.Branch('pho4_trkSumPtHollowConeDR03', self.pho4_trkSumPtHollowConeDR03, 'pho4_trkSumPtHollowConeDR03/D') 
      outTree.Branch('pho1_full5x5_sigmaIetaIeta', self.pho1_full5x5_sigmaIetaIeta, 'pho1_full5x5_sigmaIetaIeta/D')
      outTree.Branch('pho2_full5x5_sigmaIetaIeta', self.pho2_full5x5_sigmaIetaIeta, 'pho2_full5x5_sigmaIetaIeta/D')
      outTree.Branch('pho3_full5x5_sigmaIetaIeta', self.pho3_full5x5_sigmaIetaIeta, 'pho3_full5x5_sigmaIetaIeta/D')
      outTree.Branch('pho4_full5x5_sigmaIetaIeta', self.pho4_full5x5_sigmaIetaIeta, 'pho4_full5x5_sigmaIetaIeta/D')   
      outTree.Branch('pho1_MVA', self.pho1_MVA, 'pho1_MVA/D')
      outTree.Branch('pho2_MVA', self.pho2_MVA, 'pho2_MVA/D')
      outTree.Branch('pho3_MVA', self.pho3_MVA, 'pho3_MVA/D')
      outTree.Branch('pho4_MVA', self.pho4_MVA, 'pho4_MVA/D')
      outTree.Branch('pho12_pt', self.pho12_pt, 'pho12_pt/D')
      outTree.Branch('pho13_pt', self.pho13_pt, 'pho13_pt/D')
      outTree.Branch('pho14_pt', self.pho14_pt, 'pho14_pt/D')
      outTree.Branch('pho23_pt', self.pho23_pt, 'pho23_pt/D')
      outTree.Branch('pho24_pt', self.pho24_pt, 'pho24_pt/D')
      outTree.Branch('pho34_pt', self.pho34_pt, 'pho34_pt/D')
      outTree.Branch('pho12_eta', self.pho12_eta, 'pho12_eta/D')
      outTree.Branch('pho13_eta', self.pho13_eta, 'pho13_eta/D')
      outTree.Branch('pho14_eta', self.pho14_eta, 'pho14_eta/D')
      outTree.Branch('pho23_eta', self.pho23_eta, 'pho23_eta/D')
      outTree.Branch('pho24_eta', self.pho24_eta, 'pho24_eta/D')
      outTree.Branch('pho34_eta', self.pho34_eta, 'pho34_eta/D')
      outTree.Branch('pho12_mass', self.pho12_mass, 'pho12_mass/D')
      outTree.Branch('pho13_mass', self.pho13_mass, 'pho13_mass/D')
      outTree.Branch('pho14_mass', self.pho14_mass, 'pho14_mass/D')
      outTree.Branch('pho23_mass', self.pho23_mass, 'pho23_mass/D')
      outTree.Branch('pho24_mass', self.pho24_mass, 'pho24_mass/D')
      outTree.Branch('pho34_mass', self.pho34_mass, 'pho34_mass/D')
      outTree.Branch('pho12_dR', self.pho12_dR, 'pho12_dR/D')
      outTree.Branch('pho13_dR', self.pho13_dR, 'pho13_dR/D')
      outTree.Branch('pho14_dR', self.pho14_dR, 'pho14_dR/D')
      outTree.Branch('pho23_dR', self.pho23_dR, 'pho23_dR/D')
      outTree.Branch('pho24_dR', self.pho24_dR, 'pho24_dR/D')
      outTree.Branch('pho34_dR', self.pho34_dR, 'pho34_dR/D')
      outTree.Branch('a1_mass_dM', self.a1_mass_dM, 'a1_mass_dM/D')
      outTree.Branch('a2_mass_dM', self.a2_mass_dM, 'a2_mass_dM/D')
      outTree.Branch('a1_pt_dM', self.a1_pt_dM, 'a1_pt_dM/D')
      outTree.Branch('a2_pt_dM', self.a2_pt_dM, 'a2_pt_dM/D')
      outTree.Branch('a1_eta_dM', self.a1_eta_dM, 'a1_eta_dM/D')
      outTree.Branch('a2_eta_dM', self.a2_eta_dM, 'a2_eta_dM/D')
      outTree.Branch('a1_dR_dM', self.a1_dR_dM, 'a1_dR_dM/D')
      outTree.Branch('a2_dR_dM', self.a2_dR_dM, 'a2_dR_dM/D')
      outTree.Branch('a1_a2_dR_dM', self.a1_a2_dR_dM, 'a1_a2_dR_dM/D')
      outTree.Branch('a1_p1i_dM', self.a1_p1i_dM, 'a1_p1i_dM/I')
      outTree.Branch('a1_p2i_dM', self.a1_p2i_dM, 'a1_p2i_dM/I')
      outTree.Branch('a2_p1i_dM', self.a2_p1i_dM, 'a2_p1i_dM/I')
      outTree.Branch('a2_p2i_dM', self.a2_p2i_dM, 'a2_p2i_dM/I')
      outTree.Branch('cosThetaStarCS_dM', self.cosThetaStarCS_dM, 'cosThetaStarCS_dM/D')
      outTree.Branch('cosTheta_a1_dM', self.cosTheta_a1_dM, 'cosTheta_a1_dM/D')
      outTree.Branch('cosTheta_a2_dM', self.cosTheta_a2_dM, 'cosTheta_a2_dM/D')
      outTree.Branch('a1_energy_dM', self.a1_energy_dM, 'a1_energy_dM/D')
      outTree.Branch('a2_energy_dM', self.a2_energy_dM, 'a2_energy_dM/D')
      outTree.Branch('tp_pt', self.tp_pt, 'tp_pt/D')
      outTree.Branch('tp_eta', self.tp_eta, 'tp_eta/D')
      outTree.Branch('tp_mass', self.tp_mass, 'tp_mass/D')
      outTree.Branch('isPresel',self.isPresel, 'isPresel/I')

      return outTree

   def FillEvent(self, inputTree):

      ObjList = [key.GetName() for key in  inputTree.GetListOfBranches()]
      print " ObjList = ", ObjList

      for b in ObjList:
        print b
        getattr(self, b)[0] = getattr(inputTree, b)
        #setattr(self, b + "[0]", getattr(inputTree, b) ) ---> this does not work!!! Remember! Since [0] will not be interpreted as an operation

   ## For each photon a vector is defined this way:
   ##[p4, Full 5x5 r9, ChHadIso, HOE, SCEta, PSV, pfPhoIso, trkSumPt, full5x5 iEta, rho]
   def getBin(self,val,vals):
       bin = -1
       for i in range(len(vals)-1):
          if val>vals[i] and val<=vals[i+1]: bin = i
       if bin==-1: bin = len(vals)-1 
       return bin

   def inCategories(self,eta_range,r9_range,psv_range,trkSumPt_range,pfPhoIso_range,sigmaIetaIeta_range):  
       if (eta_range[0]>eta_range[1] and eta_range[0]<eta_range[2]) and (r9_range[0]>r9_range[1] and r9_range[0]<=r9_range[2]) and (psv_range[0]>psv_range[1] and psv_range[0]<psv_range[2]) and (trkSumPt_range[0]>trkSumPt_range[1] and trkSumPt_range[0]<trkSumPt_range[2]) and (pfPhoIso_range[0]>pfPhoIso_range[1] and pfPhoIso_range[0]<pfPhoIso_range[2]) and (sigmaIetaIeta_range[0]>sigmaIetaIeta_range[1] and sigmaIetaIeta_range[0]<sigmaIetaIeta_range[2]): return True
       else: return False 
           
   def rediscoveryHLTcutsV1_2016(self,Pho1_vec,Pho2_vec): 

       pho1_r9 = Pho1_vec[1]
       pho2_r9 = Pho2_vec[1]
       pho1_SCeta = abs(Pho1_vec[4])
       pho2_SCeta = abs(Pho2_vec[4])
       pho1_psv = Pho1_vec[5]
       pho2_psv = Pho2_vec[5]
       pho1_trkSumPt = Pho1_vec[7]
       pho2_trkSumPt = Pho2_vec[7]
       pho1_sigmaIetaIeta = Pho1_vec[8]
       pho2_sigmaIetaIeta = Pho2_vec[8]
       
       eta_vals = (0.,0.9,1.5,2.,2.2,3.) 
       eta_bin1 = self.getBin(abs(pho1_SCeta),eta_vals)+1
       eta_bin2 = self.getBin(abs(pho2_SCeta),eta_vals)+1
       effArea = {
        1: 0.16544,
        2: 0.16544,
        3: 0.13212,
        4: 0.13212,
        5: 0.13212
       }
       pho1_pfPhoIso = Pho1_vec[6] - Pho1_vec[9]*effArea.get(int(eta_bin1))
       pho2_pfPhoIso = Pho2_vec[6] - Pho2_vec[9]*effArea.get(int(eta_bin2))
       
 
       if(
          (self.inCategories([pho1_SCeta,0.,1.4442],[pho1_r9,0.85,9999.],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.0105]) or self.inCategories([pho1_SCeta,0.,1.4442],[pho1_r9,0.5,0.85],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.0105]) or self.inCategories([pho1_SCeta,1.566,9999.],[pho1_r9,0.9,9999.],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.0275]) or self.inCategories([pho1_SCeta,1.566,9999.],[pho1_r9,0.9,0.9],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,0.],[pho1_pfPhoIso,-9999,0.],[pho1_sigmaIetaIeta,-9999,0.0275])) and (self.inCategories([pho2_SCeta,0.,1.4442],[pho2_r9,0.85,9999.],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.0105]) or self.inCategories([pho2_SCeta,0.,1.4442],[pho2_r9,0.5,0.85],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.0105]) or self.inCategories([pho2_SCeta,1.566,9999.],[pho2_r9,0.9,9999.],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.0275]) or self.inCategories([pho2_SCeta,1.566,9999.],[pho2_r9,0.9,0.9],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,0.],[pho2_pfPhoIso,-9999,0.],[pho2_sigmaIetaIeta,-9999,0.0275]))   
       ): return True
       else: return False   
      
   def Preselection_2016(self, Pho1_vec, Pho2_vec):
       isPreselected = False
       if (
       (Pho1_vec[1] > 0.8 or Pho1_vec[2] < 20 or (Pho1_vec[2]/Pho1_vec[0].Pt()) < 0.3 )
       and (Pho2_vec[1] > 0.8 or Pho2_vec[2] < 20 or (Pho2_vec[2]/Pho2_vec[0].Pt() < 0.3))
       and (Pho1_vec[3] < 0.08 and Pho2_vec[3] < 0.08)
       and ( ((abs(Pho1_vec[4]) < 1.4442 and Pho1_vec[3] < 0.07)or (abs(Pho1_vec[4]) > 1.566 and Pho1_vec[3] < 0.035)) and ((abs(Pho2_vec[4]) < 1.4442 and  Pho2_vec[3] < 0.07)or(abs(Pho2_vec[4]) > 1.566 and Pho2_vec[3] < 0.035) ) )
       and ( ((abs(Pho1_vec[4]) < 1.4442) or (abs(Pho1_vec[4]) > 1.566)) and ((abs(Pho2_vec[4]) < 1.4442 )or(abs(Pho2_vec[4]) > 1.566 ) ) )
       and (Pho1_vec[0].Pt()> 30.0 and Pho2_vec[0].Pt()> 18.0)
       and (abs(Pho1_vec[4]) < 2.5 and abs(Pho2_vec[4]) < 2.5)
       and (abs(Pho1_vec[4]) < 1.4442 or abs(Pho1_vec[4]) > 1.566 )
       and (abs(Pho2_vec[4]) < 1.4442 or abs(Pho2_vec[4]) > 1.566)
       and ( (abs(Pho1_vec[4]) < 1.4442 and abs(Pho2_vec[4]) < 1.4442)
       or (abs(Pho1_vec[4]) < 1.4442 and Pho1_vec[1]>0.85 and abs(Pho2_vec[4]) > 1.566 and Pho2_vec[1]>0.90 )
       or (abs(Pho1_vec[4]) > 1.566 and Pho1_vec[1]>0.90 and abs(Pho2_vec[4]) < 1.4442 and Pho2_vec[1]>0.85 )
       or (abs(Pho1_vec[4]) > 1.566 and Pho1_vec[1]>0.90 and abs(Pho2_vec[4]) > 1.566 and Pho2_vec[1]>0.90 ) )
       and ((Pho1_vec[0]+Pho2_vec[0])).M() > 55
       and (Pho1_vec[0].Pt() > 0.47*((Pho1_vec[0]+Pho2_vec[0])).M() and Pho2_vec[0].Pt() > 0.28*((Pho1_vec[0]+Pho2_vec[0])).M())
       and (Pho1_vec[5] == 0) and (Pho2_vec[5]==0) 
       ):
        if self.rediscoveryHLTcutsV1_2016(Pho1_vec, Pho2_vec):
           isPreselected = True
         
       return isPreselected

   def rediscoveryHLTcutsV1_2017(self,Pho1_vec,Pho2_vec): 

       pho1_r9 = Pho1_vec[1]
       pho2_r9 = Pho2_vec[1]
       pho1_SCeta = abs(Pho1_vec[4])
       pho2_SCeta = abs(Pho2_vec[4])
       pho1_psv = Pho1_vec[5]
       pho2_psv = Pho2_vec[5]
       pho1_trkSumPt = Pho1_vec[7]
       pho2_trkSumPt = Pho2_vec[7]
       pho1_sigmaIetaIeta = Pho1_vec[8]
       pho2_sigmaIetaIeta = Pho2_vec[8]
       
       eta_vals = (0.0,1.0,1.479,2.0,2.2,2.3,2.4,5.0) 
       eta_bin1 = self.getBin(abs(pho1_SCeta),eta_vals)+1
       eta_bin2 = self.getBin(abs(pho2_SCeta),eta_vals)+1
       effArea = {
        1: 0.124,
        2: 0.109,
        3: 0.063,
        4: 0.078,
        5: 0.100,
        6: 0.115,
        7: 0.137    
       }
       pho1_pfPhoIso = Pho1_vec[6] - Pho1_vec[9]*effArea.get(int(eta_bin1))
       pho2_pfPhoIso = Pho2_vec[6] - Pho2_vec[9]*effArea.get(int(eta_bin2))
       
       if(
          (self.inCategories([pho1_SCeta,0.,1.4442],[pho1_r9,0.85,9999.],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho1_SCeta,0.,1.4442],[pho1_r9,0.5,0.85],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho1_SCeta,1.566,9999.],[pho1_r9,0.9,9999.],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.035]) or self.inCategories([pho1_SCeta,1.566,9999.],[pho1_r9,0.8,0.9],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.035])) and (self.inCategories([pho2_SCeta,0.,1.4442],[pho2_r9,0.85,9999.],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho2_SCeta,0.,1.4442],[pho2_r9,0.5,0.85],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho2_SCeta,1.566,9999.],[pho2_r9,0.9,9999.],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.035]) or self.inCategories([pho2_SCeta,1.566,9999.],[pho2_r9,0.8,0.9],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.035]))  
       ): return True
       else: return False 
       
     
   def Preselection_2017(self, Pho1_vec, Pho2_vec):
       isPreselected = False
       if (
       (Pho1_vec[1] > 0.8 or Pho1_vec[2] < 20 or (Pho1_vec[2]/Pho1_vec[0].Pt()) < 0.3 )
       and (Pho2_vec[1] > 0.8 or Pho2_vec[2] < 20 or (Pho2_vec[2]/Pho2_vec[0].Pt() < 0.3))
       and (Pho1_vec[3] < 0.08 and Pho2_vec[3] < 0.08)
       and (Pho1_vec[0].Pt()> 30.0 and Pho2_vec[0].Pt()> 18.0)  
       and (abs(Pho1_vec[4]) < 2.5 and abs(Pho2_vec[4]) < 2.5)
       and (abs(Pho1_vec[4]) < 1.4442 or abs(Pho1_vec[4]) > 1.566 )
       and (abs(Pho2_vec[4]) < 1.4442 or abs(Pho2_vec[4]) > 1.566)
       and ((Pho1_vec[0]+Pho2_vec[0])).M() > 55 
       and (((abs(Pho1_vec[4]) < 1.4442 and abs(Pho2_vec[4]) < 1.4442) and (Pho1_vec[1]>0.85 or Pho2_vec[1]>0.85))
       or ((abs(Pho1_vec[4]) < 1.4442 and abs(Pho2_vec[4]) > 1.566) and (Pho1_vec[1]>0.85 or Pho2_vec[1]>0.90))
       or ((abs(Pho1_vec[4]) > 1.566 and abs(Pho2_vec[4]) < 1.4442) and (Pho1_vec[1]>0.90 or Pho2_vec[1]>0.85))
       or ((abs(Pho1_vec[4]) > 1.566 and abs(Pho2_vec[4]) > 1.566) and (Pho1_vec[1]>0.90 or Pho2_vec[1]>0.90)))
       and (Pho1_vec[0].Pt() > 0.47*((Pho1_vec[0]+Pho2_vec[0])).M() and Pho2_vec[0].Pt() > 0.28*((Pho1_vec[0]+Pho2_vec[0])).M())
       and (Pho1_vec[5] == 0) and (Pho2_vec[5]==0) 
       ):
        if self.rediscoveryHLTcutsV1_2017(Pho1_vec, Pho2_vec):
           isPreselected = True
        
       return isPreselected

   def rediscoveryHLTcutsV1_2018(self,Pho1_vec,Pho2_vec): 

       pho1_r9 = Pho1_vec[1]
       pho2_r9 = Pho2_vec[1]
       pho1_SCeta = abs(Pho1_vec[4])
       pho2_SCeta = abs(Pho2_vec[4])
       pho1_psv = Pho1_vec[5]
       pho2_psv = Pho2_vec[5]
       pho1_trkSumPt = Pho1_vec[7]
       pho2_trkSumPt = Pho2_vec[7]
       pho1_sigmaIetaIeta = Pho1_vec[8]
       pho2_sigmaIetaIeta = Pho2_vec[8]
      
       eta_vals = (0.,0.9,1.5,2.,2.2,3.) 
       eta_bin1 = self.getBin(abs(pho1_SCeta),eta_vals)+1
       eta_bin2 = self.getBin(abs(pho2_SCeta),eta_vals)+1
       effArea = {
        1: 0.16544,
        2: 0.16544,
        3: 0.13212,
        4: 0.13212,
        5: 0.13212
       }
       pho1_pfPhoIso = Pho1_vec[6] - Pho1_vec[9]*effArea.get(int(eta_bin1))
       pho2_pfPhoIso = Pho2_vec[6] - Pho2_vec[9]*effArea.get(int(eta_bin2))
       
       if(
          (self.inCategories([pho1_SCeta,0.,1.4442],[pho1_r9,0.85,9999.],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho1_SCeta,0.,1.4442],[pho1_r9,0.5,0.85],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho1_SCeta,1.566,9999.],[pho1_r9,0.9,9999.],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.035]) or self.inCategories([pho1_SCeta,1.566,9999.],[pho1_r9,0.8,0.9],[pho1_psv,-9999,0.5],[pho1_trkSumPt,-9999,6.],[pho1_pfPhoIso,-9999,4.],[pho1_sigmaIetaIeta,-9999,0.035])) and (self.inCategories([pho2_SCeta,0.,1.4442],[pho2_r9,0.85,9999.],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho2_SCeta,0.,1.4442],[pho2_r9,0.5,0.85],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.015]) or self.inCategories([pho2_SCeta,1.566,9999.],[pho2_r9,0.9,9999.],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.035]) or self.inCategories([pho2_SCeta,1.566,9999.],[pho2_r9,0.8,0.9],[pho2_psv,-9999,0.5],[pho2_trkSumPt,-9999,6.],[pho2_pfPhoIso,-9999,4.],[pho2_sigmaIetaIeta,-9999,0.035]))    
       ): return True
       else: return False

   def Preselection_2018(self, Pho1_vec, Pho2_vec):
       isPreselected = False
       if (
       (Pho1_vec[1] > 0.8 or Pho1_vec[2] < 20 or (Pho1_vec[2]/Pho1_vec[0].Pt()) < 0.3 )
       and (Pho2_vec[1] > 0.8 or Pho2_vec[2] < 20 or (Pho2_vec[2]/Pho2_vec[0].Pt() < 0.3))
       and (Pho1_vec[3] < 0.08 and Pho2_vec[3] < 0.08)
       and (Pho1_vec[0].Pt()> 30.0 and Pho2_vec[0].Pt()> 18.0)  
       and (abs(Pho1_vec[4]) < 2.5 and abs(Pho2_vec[4]) < 2.5)
       and (abs(Pho1_vec[4]) < 1.4442 or abs(Pho1_vec[4]) > 1.566 )
       and (abs(Pho2_vec[4]) < 1.4442 or abs(Pho2_vec[4]) > 1.566)
       and ((Pho1_vec[0]+Pho2_vec[0])).M() > 55 
       and (((abs(Pho1_vec[4]) < 1.4442 and abs(Pho2_vec[4]) < 1.4442) and (Pho1_vec[1]>0.50 or Pho2_vec[1]>0.50))
       or ((abs(Pho1_vec[4]) < 1.4442 and abs(Pho2_vec[4]) > 1.566) and (Pho1_vec[1]>0.50 or Pho2_vec[1]>0.90))
       or ((abs(Pho1_vec[4]) > 1.566 and abs(Pho2_vec[4]) < 1.4442) and (Pho1_vec[1]>0.90 or Pho2_vec[1]>0.50))
       or ((abs(Pho1_vec[4]) > 1.566 and abs(Pho2_vec[4]) > 1.566) and (Pho1_vec[1]>0.50 or Pho2_vec[1]>0.50)))
       and (Pho1_vec[0].Pt() > 0.47*((Pho1_vec[0]+Pho2_vec[0])).M() and Pho2_vec[0].Pt() > 0.28*((Pho1_vec[0]+Pho2_vec[0])).M())
       and (Pho1_vec[5] == 0) and (Pho2_vec[5]==0) 
       ):
        if self.rediscoveryHLTcutsV1_2018(Pho1_vec, Pho2_vec):
           isPreselected = True

       return isPreselected



   # Phos: a list of 4 (and only 4!) TLorentzVectors
   def MakePairing(self, Phos):
      minDM = 100000
      P1 = 0
      iP1 = -99
      P2 = 0
      iP2 = -99
      P3 = 0
      iP3 = -99
      P4 = 0
      iP4 = -99
      Dipho1 = 0
      Dipho2 = 0
      for i1,p1 in enumerate(Phos):
         for i2,p2 in enumerate(Phos):
            if i2 <= i1: continue
            for i3,p3 in enumerate(Phos):
               if i3 == i2 or i3 == i1: continue
               for i4,p4 in enumerate(Phos):
                  if i4 <= i3: continue
                  if i4==i1 or i4==i2: continue
                  dipho1 = p1+p2
                  dipho2 = p3+p4
                  #Mass = dipho.M()
                  deltaM = abs(dipho1.M() - dipho2.M())
                  if(DEBUG): print deltaM, i1, i2, i3, i4
                  if deltaM < minDM:
                     minDM = deltaM
                     P1 = p1
                     iP1 = i1
                     P2 = p2
                     iP2 = i2
                     P3 = p3
                     iP3 = i3
                     P4 = p4
                     iP4 = i4
                     #print "Photon 1 M : " , p1.M()
                     #Max_mass = max(((p1.M()+p2.M()),(p1.M()+p3.M()),(p1.M()+p4.M()),(p2.M()+p3.M()),(p2.M()+p4.M()),(p3.M()+p4.M())))
                     #print Max_mass
                     Dipho1 = dipho1 if ((p1.Pt() + p2.Pt()) > (p3.Pt() + p4.Pt())) else dipho2
                     Dipho2 = dipho2 if ((p1.Pt() + p2.Pt()) > (p3.Pt() + p4.Pt())) else dipho1
      if(DEBUG): print 'minDr:', abs(Dipho1.M() - Dipho2.M()), iP1, iP2, iP3, iP4
      arr = [[Dipho1, P1, iP1, P2, iP2], [Dipho2, P3, iP3, P4, iP4]]
      return arr

   def getCosThetaStar_CS(self, PP1, PP2):
       h_lor = PP1 + PP2
       h = TLorentzVector(0,0,0,0)
       h.SetPxPyPzE(h_lor.Px(),h_lor.Py(),h_lor.Pz(),h_lor.E())
       a1_lor = PP1
       a_1 = TLorentzVector(0,0,0,0)
       a_1.SetPxPyPzE(a1_lor.Px(),a1_lor.Py(),a1_lor.Pz(),a1_lor.E())
       a_1.Boost(-h.BoostVector())
       return a_1.CosTheta()

   def helicityCosTheta(self, Booster, Boosted):
       BoostVector = Booster.BoostVector()
       Boosted.Boost( -BoostVector.x(), -BoostVector.y(), -BoostVector.z() );
       return Boosted.CosTheta()

   def CosThetaAngles(self, PP1, PP2, PP1_pho1, PP2_pho1):
        helicityThetas = []
        Boosted_a1 = TLorentzVector(0,0,0,0)
        Boosted_a1.SetPxPyPzE(PP1.Px(),PP1.Py(),PP1.Pz(),PP1.E())
        BoostedLeadingPhoton_a1 = TLorentzVector(0,0,0,0)
        BoostedLeadingPhoton_a1.SetPxPyPzE(PP1_pho1.Px(),PP1_pho1.Py(),PP1_pho1.Pz(),PP1_pho1.E())
        helicityThetas.append( self.helicityCosTheta(Boosted_a1, BoostedLeadingPhoton_a1))

        Boosted_a2 = TLorentzVector(0,0,0,0)
        Boosted_a2.SetPxPyPzE(PP2.Px(),PP2.Py(),PP2.Pz(),PP2.E())
        BoostedLeadingPhoton_a2 = TLorentzVector(0,0,0,0)
        BoostedLeadingPhoton_a2.SetPxPyPzE(PP2_pho1.Px(),PP2_pho1.Py(),PP2_pho1.Pz(),PP2_pho1.E())
        helicityThetas.append( self.helicityCosTheta(Boosted_a2, BoostedLeadingPhoton_a2))
        return helicityThetas
