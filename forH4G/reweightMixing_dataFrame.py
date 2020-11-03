import ROOT
import itertools
from array import array
from sklearn.utils import shuffle
import numpy as np
import pandas as pd
import xgboost as xgb
import root_pandas
import sys
import os

def findVal(trre,var):
   val = -999.
   if(var=="cosThetaStarCS_dM"): val = trre.cosThetaStarCS_dM
   elif(var=="cosTheta_a1_dM"): val = trre.cosTheta_a1_dM
   elif(var=="cosTheta_a2_dM"): val = trre.cosTheta_a2_dM 
   elif(var=="a1_mass_dM"): val = trre.a1_mass_dM
   elif(var=="a2_mass_dM"): val = trre.a2_mass_dM
   elif(var=="a1_mass_dM_M_a2_mass_dM"): val = trre.a1_mass_dM-trre.a2_mass_dM
   elif(var=="a1_pt_dM"): val = trre.a1_pt_dM
   elif(var=="a2_pt_dM"): val = trre.a2_pt_dM
   elif(var=="a1_eta_dM"): val = trre.a1_eta_dM
   elif(var=="a2_eta_dM"): val = trre.a2_eta_dM
   elif(var=="a1_dR_dM"): val = trre.a1_dR_dM
   elif(var=="a2_dR_dM"): val = trre.a2_dR_dM
   elif(var=="a1_a2_dR_dM"): val = trre.a1_a2_dR_dM
   elif(var=="tp_pt"): val = trre.tp_pt
   elif(var=="tp_eta"): val = trre.tp_eta
   elif(var=="pho1_MVA"): val = trre.pho1_MVA
   elif(var=="pho2_MVA"): val = trre.pho2_MVA
   elif(var=="pho3_MVA"): val = trre.pho3_MVA 
   elif(var=="pho4_MVA"): val = trre.pho4_MVA 
   elif(var=="pho1_pt"): val = trre.pho1_pt 
   elif(var=="pho2_pt"): val = trre.pho2_pt 
   elif(var=="pho3_pt"): val = trre.pho3_pt 
   elif(var=="pho4_pt"): val = trre.pho4_pt 
   elif(var=="pho1_eta"): val = trre.pho1_eta  
   elif(var=="pho2_eta"): val = trre.pho2_eta 
   elif(var=="pho3_eta"): val = trre.pho3_eta 
   elif(var=="pho4_eta"): val = trre.pho4_eta 
   else: print "findVal ---> WARNING MISSING VAR: ",var

   return val

def clf_reweight(df_mc,df_data,n_jobs=1,cut=None, features=['a1_pt_dM','a2_pt_dM','a1_mass_dM_M_a2_mass_dM']):
   clf = xgb.XGBClassifier(learning_rate=0.05,n_estimators=500,max_depth=10,gamma=0,n_jobs=n_jobs)
   if cut is not None:
      X_data = df_data.query(cut, engine='python').sample(min(min(df_mc.query(cut, engine='python').index.size,df_data.query(cut, engine='python').index.size), 1000000)).loc[:,features].values
      X_mc = df_mc.query(cut, engine='python').sample(min(min(df_mc.query(cut, engine='python').index.size,df_data.query(cut, engine='python').index.size), 1000000)).loc[:,features].values
   else:
      X_data = df_data.sample(min(min(df_mc.index.size,df_data.index.size), 1000000)).loc[:,features].values
      X_mc = df_mc.sample(min(min(df_mc.index.size,df_data.index.size), 1000000)).loc[:,features].values
   X = np.vstack([X_data,X_mc])
   y = np.vstack([np.ones((X_data.shape[0],1)),np.zeros((X_mc.shape[0],1))])
   X, y = shuffle(X,y)
    
   clf.fit(X,y)
   eps = 1.e-3
   return np.apply_along_axis(lambda x: x[1]/(x[0]+eps), 1, clf.predict_proba(df_mc.loc[:,features].values))

if __name__ == '__main__':

 features = []
 features.append("pho1_MVA")
 features.append("pho2_MVA")
 features.append("pho3_MVA")
 features.append("pho4_MVA")
 #features.append("pho1_pt")
 #features.append("pho2_pt")
 #features.append("pho3_pt")
 #features.append("pho4_pt")
 #features.append("pho1_eta")
 #features.append("pho2_eta")
 #features.append("pho3_eta")
 #features.append("pho4_eta") 
 #features.append("a1_a2_dR_dM")
 #features.append("a1_dR_dM")
 #features.append("a2_dR_dM")
 features.append("a1_pt_dM")
 features.append("a2_pt_dM")
 #features.append("a1_eta_dM")
 #features.append("a2_eta_dM") 
 #features.append("a1_mass_dM")
 #features.append("a2_mass_dM")
 features.append("a1_mass_dM_M_a2_mass_dM")  
 #features.append("cosThetaStarCS_dM")
 features.append("cosTheta_a1_dM")
 #features.append("cosTheta_a2_dM")
 #features.append("tp_pt")
 #features.append("tp_eta")

 
 tree_datamix = ROOT.TChain() 
 tree_datamix.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_mix.root/Data_13TeV_H4GTag_0') 
 #tree_datamix.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_mix.root/Data_13TeV_H4GTag_0')  
 #tree_datamix.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_mix.root/Data_13TeV_H4GTag_0')  

 tree_data = ROOT.TChain() 
 tree_data.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_2016.root/tagsDumper/trees/Data_13TeV_H4GTag_0') 
 #tree_data.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_2017.root/tagsDumper/trees/Data_13TeV_H4GTag_0') 
 #tree_data.AddFile('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_2018.root/tagsDumper/trees/Data_13TeV_H4GTag_0')  

 #Cut = '1>0' 
 Cut = 'pho1_pt > 30 and pho2_pt > 18 and pho3_pt > 15 and pho4_pt > 15 and  abs(pho1_eta) < 2.5 and abs(pho2_eta) < 2.5 and abs(pho3_eta) < 2.5 and abs(pho4_eta) < 2.5 and (abs(pho1_eta) < 1.4442 or abs(pho1_eta) > 1.566) and (abs(pho2_eta) < 1.4442 or abs(pho2_eta) > 1.566) and (abs(pho3_eta) < 1.4442 or abs(pho3_eta) > 1.566) and (abs(pho4_eta) < 1.4442 or abs(pho4_eta) > 1.566) and pho1_electronveto==1 and pho2_electronveto==1 and pho3_electronveto==1 and pho4_electronveto==1 and pho1_MVA>=-1. and pho2_MVA>=-1. and pho3_MVA>=-1. and pho4_MVA>=-1. and tp_mass > 110 and tp_mass < 180 and not(tp_mass > 115 and tp_mass < 135)'
 
 df_datamix = root_pandas.read_root('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_mix.root','Data_13TeV_H4GTag_0') 
 #df_datamix = root_pandas.read_root('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_mix.root/Data_13TeV_H4GTag_0',columns=columns) 
 #df_datamix = root_pandas.read_root('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_mix.root/Data_13TeV_H4GTag_0',columns=columns) 

 df_data = root_pandas.read_root('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2016/hadd/data_2016.root','tagsDumper/trees/Data_13TeV_H4GTag_0')
 #df_data = root_pandas.read_root('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2017/hadd/data_2017.root/tagsDumper/trees/Data_13TeV_H4GTag_0',columns=columns) 
 #df_data = root_pandas.read_root('/eos/user/t/twamorka/h4g_fullRun2/withSystematics/2018/hadd/data_2018.root/tagsDumper/trees/Data_13TeV_H4GTag_0',columns=columns)     
 
 df_datamix['weight'] = clf_reweight(df_datamix, df_data, n_jobs=10, cut=Cut, features=features) 
 df_datamix.to_root('datamix_weight.root', key='Data_13TeV_H4GTag_0')

