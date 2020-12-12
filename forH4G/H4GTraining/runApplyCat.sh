#!/bin/bash

mass='60 45 35 25 15'
# mass='60'

year='2016 2017 2018'

training='dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m'

for m in $mass;
do
     for t1 in $training;
     do
       mkdir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/${t1}${m}/
       for y in $year;
       do
         echo 'Running on data mix'
         echo python ApplyCatBDT.py -f /eos/user/t/twamorka/h4g_fullRun2/withSystematics/${y}/hadd/data_mix_${y}_kinWeight.root  -y ${y} -t ${t1}${m} -W /eos/user/b/bmarzocc/H4G/${t1}${m}/weights/TMVAClassification_BDTG.weights.xml -O /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/${t1}${m}/data_mix_${y}_kinWeight.root
         python ApplyCatBDT.py -f /eos/user/t/twamorka/h4g_fullRun2/withSystematics/${y}/hadd/data_mix_${y}_kinWeight.root  -y ${y} -t ${t1}${m} -W /eos/user/b/bmarzocc/H4G/${t1}${m}/weights/TMVAClassification_BDTG.weights.xml -O /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/${t1}${m}/data_mix_${y}_kinWeight.root

         echo 'Running on data'
         echo python ApplyCatBDT.py -f /eos/user/t/twamorka/h4g_fullRun2/withSystematics/${y}/hadd/data_${y}.root  -y ${y} -t ${t1}${m} -W /eos/user/b/bmarzocc/H4G/${t1}${m}/weights/TMVAClassification_BDTG.weights.xml -O /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/${t1}${m}/data_${m}_${y}.root
         python ApplyCatBDT.py -f /eos/user/t/twamorka/h4g_fullRun2/withSystematics/${y}/hadd/data_${y}.root  -y ${y} -t ${t1}${m} -W /eos/user/b/bmarzocc/H4G/${t1}${m}/weights/TMVAClassification_BDTG.weights.xml -O /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/${t1}${m}/data_${m}_${y}.root

         echo 'Running on Signal'
         echo python ApplyCatBDT.py -f /eos/user/t/twamorka/h4g_fullRun2/withSystematics/${y}/hadd/signal_m_${m}.root  -m ${m} -y ${y} -t ${t1}${m} -W /eos/user/b/bmarzocc/H4G/${t1}${m}/weights/TMVAClassification_BDTG.weights.xml -O /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/${t1}${m}/signal_m_${m}_${y}.root
         python ApplyCatBDT.py -f /eos/user/t/twamorka/h4g_fullRun2/withSystematics/${y}/hadd/signal_m_${m}.root  -m ${m} -y ${y} -t ${t1}${m} -W /eos/user/b/bmarzocc/H4G/${t1}${m}/weights/TMVAClassification_BDTG.weights.xml -O /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/${t1}${m}/signal_m_${m}_${y}.root

       done
     done
done
