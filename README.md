# Scripts
Repository to keep track of useful scripts

1) Make datamix sample:

    * cd forH4G/Mixing/
    * python runMixing_Condor.py  -m 50
    * condor_submit condor_job.txt 

2) Reweight the datamix sample:

    * cd forH4G/
    * python reweightMixing.py

3) Cut based optimization:

    * cd forH4G/
    * python runSoBOptimization.py -v "fabs(a1_mass_dM-a2_mass_dM)" -M 100. -m 0. -n 100 --maximize 0 -g 60 #run locally 
    * python runSoBOptimization_Condor.py -v "pho1_MVA,pho2_MVA,pho3_MVA,pho4_MVA" -M "1.,1.,1.,1." -m "-1.,-1.,-1.,-1." --maximize "1,1,1,1" -n 40 -b 500 -g 60 #run on HTCondor (OR)
    * python runSoBOptimization_Condor.py -v "pho3_MVA,pho4_MVA,fabs(a1_mass_dM-a2_mass_dM),fabs(cosTheta_a1_dM)" -M "1.,1.,100.,1." -m "-1.,-1.,0.,0." --maximize "1,1,0,0"  -n 40 -b 500 -g 60 #run on HTCondor
    * python computeSoBMaximum.py -i output_m60/ #find the optimal selection


4) BDT categorization:

    * cd forH4G/ 
    * python CatTrainMVA.py -m 60 -d dataset_m60 #train the BDT 
    * ./runApplyCat.sh # in H4GTraining to evaluate the BDT
    * python smooth_BDT.py -d /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m60/ -g 60 -n 190 -m -0.9 -M 1. # smooth the BDT distributions
    * python optimizeCategories.py -d /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m60/ -c 5 -n 190 #optimize categories on the BDT distributions
