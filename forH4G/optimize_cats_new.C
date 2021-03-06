#include <iostream>
#include <fstream>
#include <TH1F.h>
#include <TTree.h>
#include <TPaveText.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TLorentzVector.h"
#include <iomanip>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "TFile.h"
#include "TROOT.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TGraph.h"
#include <algorithm>    // std::min_element, std::max_element

using namespace std;

//g++ optimize_cats.C -g -o opt `root-config --cflags --glibs` -lMLP -lXMLIO

// int main(int argc, char* argv[]){
void optimize_cats_new(const int NCAT){
	// gROOT->ProcessLine(".x /afs/cern.ch/work/n/nchernya/setTDRStyle.C");

	TString s;
	// TString date = "OldPairing_M60";
	TString date = "20201501";
	      TString path_sig = s.Format("/eos/home-t/twamorka/1April2020_CatTrainign/vLoose_limKinPlusPhotonID/");
				TString path_bkg_data = s.Format("/eos/home-t/twamorka/1April2020_CatTrainign/vLoose_limKinPlusPhotonID/");
        // TString path_sig = s.Format("/eos/user/t/twamorka/21March2020_Mixing/hadd/OldPairing/catMVA_Medium_wMVA/");
        // TString path_bkg_data = s.Format("/eos/user/t/twamorka/21March2020_Mixing/hadd/OldPairing/catMVA_Medium_wMVA/");
	// cout << "date" << date << endl;
	// TString path=s.Format("/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/optimization_files/%s/",date.Data());
	// TString path_sig=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/OldDiphoPairing/wCatMVA_20Jan2020/m_60/");
	// TString path_bkg_dipho40to80=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/OldDiphoPairing/wCatMVA_20Jan2020/m_60/");
	// TString path_bkg_dipho80toInf=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/OldDiphoPairing/wCatMVA_20Jan2020/m_60/");
	// TString path_bkg_data=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/OldDiphoPairing/wCatMVA_20Jan2020/m_60/");
	//TString path_sig=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/BDTPairing/m_%d/wCatMVA/",mass);
	//TString path_bkg_dipho40to80=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/BDTPairing/m_%d/wCatMVA/",mass);
	//TString path_bkg_dipho80toInf=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/BDTPairing/m_%d/wCatMVA/",mass);
	//TString path_bkg_data=s.Format("/eos/user/t/twamorka/Jan2020/2016Samples/BDTPairing/m_%d/wCatMVA/",mass);


	// const int NCAT=4;
	// const int NC

	TString what_to_opt = "bdt";
	double xmin = -1.0;
	double xmax = 1.0;
	Double_t precision=0.01;  //0.01 for MVA, 5 for MX

	TString Mgg_window = "*((tp_mass>115)&&(tp_mass<135))";
        TString Mgg_window_mix = "*((tp_mass>115)&&(tp_mass<135))";
	TString Mgg_sideband = "*((tp_mass<=115)||(tp_mass>=135))";
        TString Mgg_sideband_mix = "*((tp_mass<=115)||(tp_mass>=135))";
	TString selection_sig = "weight*36*((1>0&& pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1&& pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.9 && pho4_MVA > -0.9&& tp_mass > 110 && tp_mass < 180 ))";
        TString selection_bg_data = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1&& pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.9 && pho4_MVA > -0.9 && tp_mass > 110 && tp_mass < 180 )*(467/5162)";
	// TString Mgg_sideband = "*((Mgg<=115)||(Mgg>=135))";
	// TString selection_sig = "weight*lumi*2*eventTrainedOn*0.587*normalization/SumWeight";
	//TString selection_bg_dipho40to80 = "weight*36*((1>0&& pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_pixelseed==0 && pho2_pixelseed==0 && pho3_pixelseed==0 && pho4_pixelseed==0&& pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.9 && pho4_MVA > -0.9&& tp_mass > 110 && tp_mass < 180))";
	//TString selection_bg_dipho80toInf = "weight*36*((1>0&& pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_pixelseed==0 && pho2_pixelseed==0 && pho3_pixelseed==0 && pho4_pixelseed==0&& pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.9 && pho4_MVA > -0.9&& tp_mass > 110 && tp_mass < 180))";
	//TString selection_bg_data = "((pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_pixelseed==0 && pho2_pixelseed==0 && pho3_pixelseed==0 && pho4_pixelseed==0 && tp_mass > 110 && tp_mass < 180 &&((pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA < -0.9 && pho4_MVA < -0.9) || (pho1_MVA > -0.9 && pho3_MVA > -0.9 && pho2_MVA < -0.9 && pho4_MVA < -0.9) || (pho1_MVA > -0.9 && pho4_MVA > -0.9 && pho2_MVA < -0.9 && pho3_MVA < -0.9) || (pho2_MVA > -0.9 && pho3_MVA > -0.9 && pho1_MVA < -0.9 && pho4_MVA < -0.9) || (pho2_MVA > -0.9 && pho4_MVA > -0.9 && pho1_MVA < -0.9 && pho3_MVA < -0.9) || (pho3_MVA > -0.9 && pho4_MVA > -0.9 && pho1_MVA < -0.9 && pho2_MVA < -0.9))))*(509.30470/1807)";
	// TString selection_bg = "weight*lumi*overlapSave*normalization/SumWeight";
	// TString selection_diphoton = "*1.5"; //SF needed to match data normalization

	TString subcategory = "";
	TString outstr = "h4g_test";
	double minevents = 20; //for bkg  # for MVA : 70 data in sidebands after tth killer -> 70/1.5 -> before tth killer *1.2 = 56,  because still need to be able to split in MX

//borders of categories : 0.0025	0.2925	0.5125	0.6725	0.9975
//borders of categories : 0.0025	0.3125	0.5725	0.6925	0.9975

//borders of categories : 0.005	0.285	0.505	0.685	0.995
/*	TString subcategory = "*((MVAOutputTransformed>0.685)&&(MVAOutputTransformed<1.))";
	TString outstr = "_MVA0";
	double minevents = 6; //for bkg  # for MVA :100,  because still need to be able to split in MX
*/
/*	TString subcategory = "*((MVAOutputTransformed>0.6725)&&(MVAOutputTransformed<1.))";
	TString outstr = "_MVA0";
	double minevents = 40; //ttH before everything, 0 min events
*/

	// selection_sig += subcategory;
	// selection_bg += subcategory;


	TString sel;
	TString outname = s.Format("output_SB_%s_cat%d_minevents%.0f_%s",what_to_opt.Data(),NCAT,minevents,outstr.Data());


	// TFile *file_s =  TFile::Open(path+"Total_runII_20191126.root");
	TFile *file_s =  TFile::Open(path_sig+"signal_m_60.root");
	TTree *tree_sig = (TTree*)file_s->Get("SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons");
	TH1F *hist_S = new TH1F("hist_S","hist_S",int((xmax-xmin)/precision),xmin,xmax);
  s.Form("%s>>hist_S",what_to_opt.Data());
  sel.Form("%s",(selection_sig+Mgg_window).Data());
	tree_sig->Draw(s,sel,"goff");
	cout << "signal tree entries: " << tree_sig->GetEntries() << endl;

	//TFile *file_bg_dipho40to80 =  TFile::Open(path_bkg_dipho40to80+"DiPho40to80_skim.root");
	//TTree *tree_bg_dipho40to80 = (TTree*)file_bg_dipho40to80->Get("DiPhotonJetsBox_M40_80_Sherpa_13TeV_4photons");

	//TFile *file_bg_dipho80toInf =  TFile::Open(path_bkg_dipho80toInf+"DiPho80toInf_skim.root");
	//TTree *tree_bg_dipho80toInf = (TTree*)file_bg_dipho80toInf->Get("DiPhotonJetsBox_MGG_80toInf_13TeV_Sherpa_13TeV_4photons");

	//TFile *file_bg_data =  TFile::Open(path_bkg_data+"data_all_2016_wCollTree_skim.root");
	//TTree *tree_bg_data = (TTree*)file_bg_data->Get("Data_13TeV_4photons");
        TFile *file_bg_data =  TFile::Open(path_bkg_data+"data_mix.root");
        TTree *tree_bg_data = (TTree*)file_bg_data->Get("Data_13TeV_4photons");


	//TH1F *hist_B_dipho40to80 = new TH1F("hist_B_dipho40to80","hist_B_dipho40to80",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   //s.Form("%s>>hist_B_dipho40to80",what_to_opt.Data());
   /*sel.Form("%s",(selection_bg_dipho40to80+Mgg_window).Data());
	tree_bg_dipho40to80->Draw(s,sel,"goff");
	cout << "dipho40to80 entries: " << tree_bg_dipho40to80->GetEntries() << endl;

	TH1F *hist_B_dipho80toInf = new TH1F("hist_B_dipho80toInf","hist_B_dipho80toInf",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   s.Form("%s>>hist_B_dipho80toInf",what_to_opt.Data());
   sel.Form("%s",(selection_bg_dipho80toInf+Mgg_window).Data());
	tree_bg_dipho80toInf->Draw(s,sel,"goff");
	cout << "dipho80toInf entries: " << tree_bg_dipho80toInf->GetEntries() << endl; */

	TH1F *hist_B_data = new TH1F("hist_B_data","hist_B_data",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   s.Form("%s>>hist_B_data",what_to_opt.Data());
   sel.Form("%s",(selection_bg_data+Mgg_window_mix).Data());
	tree_bg_data->Draw(s,sel,"goff");
	cout << "data bkg entries: " << tree_bg_data->GetEntries() << endl;

	TH1F *hist_B = new TH1F("hist_B","hist_B",int((xmax-xmin)/precision),xmin,xmax); //200 bins
	//hist_B->Add(hist_B_dipho40to80);
	//hist_B->Add(hist_B_dipho80toInf);
	hist_B->Add(hist_B_data);

	/*TH1F *hist_B_sideband_dipho40to80 = new TH1F("hist_B_sideband_dipho40to80","hist_B_sideband_dipho40to80",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   s.Form("%s>>hist_B_sideband_dipho40to80",what_to_opt.Data());
   sel.Form("%s",(selection_bg_dipho40to80+Mgg_sideband).Data());
	 cout << "sel " << sel << endl;
	tree_bg_dipho40to80->Draw(s,sel,"goff");
	cout << "dipho40to80 sideband entries: " << tree_bg_dipho40to80->GetEntries() << endl;

	TH1F *hist_B_sideband_dipho80toInf = new TH1F("hist_B_sideband_dipho80toInf","hist_B_sideband_dipho80toInf",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   s.Form("%s>>hist_B_sideband_dipho80toInf",what_to_opt.Data());
   sel.Form("%s",(selection_bg_dipho80toInf+Mgg_sideband).Data());
	 cout << "sel " << sel << endl;
	tree_bg_dipho80toInf->Draw(s,sel,"goff");
	cout << "dipho80toInf sideband entries: " << tree_bg_dipho80toInf->GetEntries() << endl;
*/
	TH1F *hist_B_sideband_data = new TH1F("hist_B_sideband_data","hist_B_sideband_data",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   s.Form("%s>>hist_B_sideband_data",what_to_opt.Data());
   sel.Form("%s",(selection_bg_data+Mgg_sideband_mix).Data());
	 cout << "sel " << sel << endl;
	tree_bg_data->Draw(s,sel,"goff");
	cout << "data sideband entries: " << tree_bg_data->GetEntries() << endl;

	TH1F *hist_B_sideband = new TH1F("hist_B_sideband","hist_B_sideband",int((xmax-xmin)/precision),xmin,xmax); //200 bins
	//hist_B_sideband->Add(hist_B_sideband_dipho40to80);
	//hist_B_sideband->Add(hist_B_sideband_dipho80toInf);
	hist_B_sideband->Add(hist_B_sideband_data);

	// TH1F *hist_B_ttH = new TH1F("hist_B_ttH","hist_B_ttH",int((xmax-xmin)/precision),xmin,xmax); //200 bins
  //  s.Form("%s>>hist_B_ttH",what_to_opt.Data());
  //  sel.Form("%s",(selection_bg+Mgg_window).Data());
	// tree_bg_ttH->Draw(s,sel,"goff");
	// TH1F *hist_B_TTGJets = new TH1F("hist_B_TTGJets","hist_B_TTGJets",int((xmax-xmin)/precision),xmin,xmax); //200 bins
  //  s.Form("%s>>hist_B_TTGJets",what_to_opt.Data());
  //  sel.Form("%s",(selection_bg+Mgg_window).Data());
	// tree_bg_TTGJets->Draw(s,sel,"goff");
	// TH1F *hist_B_TTTo2L2Nu = new TH1F("hist_B_TTTo2L2Nu","hist_B_TTTo2L2Nu",int((xmax-xmin)/precision),xmin,xmax); //200 bins
  //  s.Form("%s>>hist_B_TTTo2L2Nu",what_to_opt.Data());
  //  sel.Form("%s",(selection_bg+Mgg_window).Data());
	// tree_bg_TTTo2L2Nu->Draw(s,sel,"goff");
	// TH1F *hist_B_TTGG_0Jets = new TH1F("hist_B_TTGG_0Jets","hist_B_TTGG_0Jets",int((xmax-xmin)/precision),xmin,xmax); //200 bins
  //  s.Form("%s>>hist_B_TTGG_0Jets",what_to_opt.Data());
  //  sel.Form("%s",(selection_bg+Mgg_window).Data());
	// tree_bg_TTGG_0Jets->Draw(s,sel,"goff");


//
	double END = hist_B->GetBinCenter(hist_B->FindLastBinAbove(-1.))+hist_B->GetBinWidth(1)/2.; //right end of BDT distibution
	double START = hist_B->GetBinCenter(hist_B->FindFirstBinAbove(-1.))-hist_B->GetBinWidth(1)/2.; //right end of BDT distibution
	cout<<"start = "<<START<<" , end = "<<END<<endl;
//
//
	hist_S->SetLineColor(kRed);
	hist_S->SetFillColor(kRed-7);
	hist_S->SetLineWidth(2);
	hist_B->SetLineColor(kBlue+1);
	hist_B->SetFillColor(kBlue-10);
	hist_B->SetLineWidth(2);
	// hist_B_ttH->SetLineColor(kGreen+1);
	// hist_B_ttH->SetLineWidth(2);
	// hist_B_TTGJets->SetLineColor(kOrange+1);
	// hist_B_TTGJets->SetLineWidth(2);
	// hist_B_TTTo2L2Nu->SetLineColor(kMagenta+1);
	// hist_B_TTTo2L2Nu->SetLineWidth(2);
	// hist_B_TTGG_0Jets->SetLineColor(kViolet+1);
	// hist_B_TTGG_0Jets->SetLineWidth(2);
//
//
//
// // CMS info
	float left2 = gStyle->GetPadLeftMargin();
	float right2 = gStyle->GetPadRightMargin();
	float top2 = gStyle->GetPadTopMargin();
	float bottom2 = gStyle->GetPadBottomMargin();
//
//
	TPaveText pCMS1(left2,1.-top2,0.4,1.,"NDC");
	pCMS1.SetTextFont(62);
	pCMS1.SetTextSize(top2*0.75);
	pCMS1.SetTextAlign(12);
	pCMS1.SetFillStyle(-1);
	pCMS1.SetBorderSize(0);
	pCMS1.AddText("CMS");
	TPaveText pCMS12(left2+0.1,1.-top2*1.1,0.6,1.,"NDC");
	pCMS12.SetTextFont(52);
	pCMS12.SetTextSize(top2*0.75);
	pCMS12.SetTextAlign(12);
	pCMS12.SetFillStyle(-1);
	pCMS12.SetBorderSize(0);
	pCMS12.AddText("Preliminary");
	TPaveText pCMS2(0.5,1.-top2,1.-right2*0.5,1.,"NDC");
	pCMS2.SetTextFont(42);
	pCMS2.SetTextSize(top2*0.75);
	pCMS2.SetTextAlign(32);
	pCMS2.SetFillStyle(-1);
	pCMS2.SetBorderSize(0);
	pCMS2.AddText("(13 TeV)");
//
//
	TPaveText pave22(0.2,0.8,0.4,1.-top2*1.666,"NDC");
	pave22.SetTextAlign(11);
	pave22.SetFillStyle(-1);
	pave22.SetBorderSize(0);
	pave22.SetTextFont(62);
	pave22.SetTextSize(top2*0.5);
	pave22.AddText("HHbbgg");

	TPaveText pave33(0.2,0.75,0.4,0.8,"NDC");
	pave33.SetTextAlign(11);
	pave33.SetFillStyle(-1);
	pave33.SetBorderSize(0);
	pave33.SetTextFont(42);
	pave33.SetTextColor(kBlue);
	pave33.SetTextSize(top2*0.5);


	TLegend *leg = new TLegend(0.72,0.78,0.85,0.9);
	leg->SetFillColor(0);
	leg->SetBorderSize(0);
	leg->SetTextFont(42);
	leg->SetTextSize(0.025);
	leg->AddEntry(hist_S,"Sig (exp. exclusion)","F");
	leg->AddEntry(hist_B,"BG","F");
// 		// leg->AddEntry(hist_B_ttH,"ttH","L");
// 		// leg->AddEntry(hist_B_TTGJets,"tt#gamma+jets","L");
// 		// leg->AddEntry(hist_B_TTTo2L2Nu,"tt#rightarrow2l2#nu","L");
// 		// leg->AddEntry(hist_B_TTGG_0Jets,"tt#gamma#gamma","L");
//
//
//
	double bin=0.;
	double s1=0; double b1=0;
	int i=0;
	float max_all=0;
		do	{
     cout << "i " << i << endl;
			s1=hist_S->GetBinContent(i+1);
			b1=hist_B->GetBinContent(i+1);
			cout << "s1 " << s1 << endl;
			cout << "b1 " << b1 << endl;
      	  //  b1+=hist_B_ttH->GetBinContent(i+1);
        	// 	b1+=hist_B_TTGJets->GetBinContent(i+1);
        	// 	b1+=hist_B_TTTo2L2Nu->GetBinContent(i+1);
         	// b1+=hist_B_TTGG_0Jets->GetBinContent(i+1);
			bin=(double) hist_S->GetBinCenter(i+1+1);
			if ((b1)!=0) max_all += pow(s1,2)/(b1);
			i++;
		} while (bin < END);

// cout << max_all << endl;
//
double max = 0;
double borders[10] = {};   // including START and END
borders[0] = START;
double sig_n[10] = {0,0,0,0,0,0,0,0,0,0};
double bkg_n[10] = {0,0,0,0,0,0,0,0,0,0};
// // // double bkg_n_tth[10] = {0,0,0,0,0,0,0,0,0,0};
double bkg_sideband_n[10] = {0,0,0,0,0,0,0,0,0,0};
double max_n[10] = {0,0,0,0,0,0,0,0,0,0};
// // // double max_n_tth[10] = {0,0,0,0,0,0,0,0,0,0};
double max_final[10] = {0,0,0,0,0,0,0,0,0,0};
double max_total = 0;
// // // double tth_cut_final = 0;
double start_n[10] = {0,0,0,0,0,0,0,0,0,0};
double bkg_yields[10] = {0,0,0,0,0,0,0,0,0,0};
double bkg_yields_sideband[10] = {0,0,0,0,0,0,0,0,0,0};
double sig_yields[10] = {0,0,0,0,0,0,0,0,0,0};
for (int index=0;index<NCAT;index++)
	start_n[index]=START+(index+1)*precision;
int minevt_cond_n[10] = {};
//
//
// std::vector<double> categories_scans_tth;
// std::vector<double> significance_scans_tth;
//
// double tth_cut = 0.1;
// TString tth_cut_s;
// do {
// cout<<"tth cut : "<<tth_cut<<endl;
// 	categories_scans_tth.push_back(tth_cut);
//
for (int index=0;index<NCAT;index++)
	start_n[index]=START+(index+1)*precision;
//
// 	tth_cut_s.Form("*(ttHScore>%.3f)",tth_cut);
//
	TH1F *hist_S_cut = new TH1F("hist_S_cut","hist_S_cut",int((xmax-xmin)/precision),xmin,xmax);
   s.Form("%s>>hist_S_cut",what_to_opt.Data());
   sel.Form("%s",(selection_sig+Mgg_window).Data());
	tree_sig->Draw(s,sel,"goff");

/*	TH1F *hist_B_cut_dipho40to80 = new TH1F("hist_B_cut_dipho40to80","hist_B_cut_dipho40to80",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   s.Form("%s>>hist_B_cut_dipho40to80",what_to_opt.Data());
   sel.Form("%s",(selection_bg_dipho40to80+Mgg_window).Data());
	tree_bg_dipho40to80->Draw(s,sel,"goff");

	TH1F *hist_B_cut_dipho80toInf = new TH1F("hist_B_cut_dipho80toInf","hist_B_cut_dipho80toInf",int((xmax-xmin)/precision),xmin,xmax); //200 bins
	 s.Form("%s>>hist_B_cut_dipho80toInf",what_to_opt.Data());
	 sel.Form("%s",(selection_bg_dipho80toInf+Mgg_window).Data());
	tree_bg_dipho40to80->Draw(s,sel,"goff");
*/
	TH1F *hist_B_cut_data = new TH1F("hist_B_cut_data","hist_B_cut_data",int((xmax-xmin)/precision),xmin,xmax); //200 bins
	 s.Form("%s>>hist_B_cut_data",what_to_opt.Data());
	 sel.Form("%s",(selection_bg_data+Mgg_window_mix).Data());
	tree_bg_data->Draw(s,sel,"goff");

	TH1F *hist_B_cut = new TH1F("hist_B_cut","hist_B_cut",int((xmax-xmin)/precision),xmin,xmax); //200 bins
 // hist_B_cut->Add(hist_B_cut_dipho40to80);
	//hist_B_cut->Add(hist_B_cut_dipho80toInf);
	hist_B_cut->Add(hist_B_cut_data);

/*	TH1F *hist_B_cut_sideband_dipho40to80 = new TH1F("hist_B_cut_sideband_dipho40to80","hist_B_cut_sideband_dipho40to80",int((xmax-xmin)/precision),xmin,xmax); //200 bins
   s.Form("%s>>hist_B_cut_sideband_dipho40to80",what_to_opt.Data());
   sel.Form("%s",(selection_bg_dipho40to80+Mgg_sideband).Data());
	tree_bg_dipho40to80->Draw(s,sel,"goff");

	TH1F *hist_B_cut_sideband_dipho80toInf = new TH1F("hist_B_cut_sideband_dipho80toInf","hist_B_cut_sideband_dipho80toInf",int((xmax-xmin)/precision),xmin,xmax); //200 bins
	 s.Form("%s>>hist_B_cut_sideband_dipho80toInf",what_to_opt.Data());
	 sel.Form("%s",(selection_bg_dipho80toInf+Mgg_sideband).Data());
	tree_bg_dipho80toInf->Draw(s,sel,"goff");
*/
	TH1F *hist_B_cut_sideband_data = new TH1F("hist_B_cut_sideband_data","hist_B_cut_sideband_data",int((xmax-xmin)/precision),xmin,xmax); //200 bins
	 s.Form("%s>>hist_B_cut_sideband_data",what_to_opt.Data());
	 sel.Form("%s",(selection_bg_data+Mgg_sideband_mix).Data());
	tree_bg_data->Draw(s,sel,"goff");

	TH1F *hist_B_cut_sideband = new TH1F("hist_B_cut_sideband","hist_B_cut_sideband",int((xmax-xmin)/precision),xmin,xmax); //200 bins
  //hist_B_cut_sideband->Add(hist_B_cut_sideband_dipho40to80);
	//hist_B_cut_sideband->Add(hist_B_cut_sideband_dipho80toInf);
	hist_B_cut_sideband->Add(hist_B_cut_sideband_data);

//
// 	TH1F *hist_B_cut_tth = new TH1F("hist_B_cut_tth","hist_B_cut_tth",int((xmax-xmin)/precision),xmin,xmax); //200 bins
//    s.Form("%s>>+hist_B_cut",what_to_opt.Data());
//    sel.Form("%s",(selection_bg+Mgg_window+tth_cut_s).Data());
// 	tree_bg_ttH->Draw(s,sel,"goff");
// 	tree_bg_TTGJets->Draw(s,sel,"goff");
// 	tree_bg_TTTo2L2Nu->Draw(s,sel,"goff");
// 	tree_bg_TTGG_0Jets->Draw(s,sel,"goff");
//
//
//
	do {
		max_n[0]=0;
		sig_n[0] = hist_S_cut->Integral(1,hist_S_cut->FindBin(start_n[0])-1);
		bkg_n[0] = hist_B_cut->Integral(1,hist_B_cut->FindBin(start_n[0])-1);
// 		bkg_n_tth[0] = hist_B_cut_tth->Integral(1,hist_B_cut_tth->FindBin(start_n[0])-1);
		bkg_sideband_n[0] = hist_B_cut_sideband->Integral(1,hist_B_cut_sideband->FindBin(start_n[0])-1);
		// if (bkg_n[0]!=0) max_n[0]=pow(sig_n[0],2)/bkg_n[0];
		if (bkg_n[0]!=0) max_n[0]=pow(sig_n[0],2)/(bkg_n[0]);
		start_n[1]=start_n[0]+precision;
		do {
			max_n[1]=0;
			sig_n[1] = hist_S_cut->Integral(hist_S_cut->FindBin(start_n[0]),hist_S_cut->FindBin(start_n[1])-1);
			bkg_n[1] = hist_B_cut->Integral(hist_B_cut->FindBin(start_n[0]),hist_B_cut->FindBin(start_n[1])-1);
// 			bkg_n_tth[1] = hist_B_cut_tth->Integral(hist_B_cut_tth->FindBin(start_n[0]),hist_B_cut_tth->FindBin(start_n[0])-1);
			bkg_sideband_n[1] = hist_B_cut_sideband->Integral(hist_B_cut_sideband->FindBin(start_n[0]),hist_B_cut_sideband->FindBin(start_n[1])-1);
// 			//if (bkg_n[1]!=0) max_n[1]=pow(sig_n[1],2)/bkg_n[1];
			if (bkg_n[1]!=0) max_n[1]=pow(sig_n[1],2)/(bkg_n[1]);
			start_n[2]=start_n[1]+precision;
			do{
				max_n[2]=0;
				if (NCAT<=2) {
					sig_n[2] = 0;
					bkg_n[2] = 1;
					// bkg_n_tth[2] = 1;
					bkg_sideband_n[2] = 1;
				} else {
					sig_n[2] = hist_S_cut->Integral(hist_S_cut->FindBin(start_n[1]),hist_S_cut->FindBin(start_n[2])-1);
					bkg_n[2] = hist_B_cut->Integral(hist_B_cut->FindBin(start_n[1]),hist_B_cut->FindBin(start_n[2])-1);
// 					bkg_n_tth[2] = hist_B_cut_tth->Integral(hist_B_cut_tth->FindBin(start_n[1]),hist_B_cut_tth->FindBin(start_n[2])-1);
					bkg_sideband_n[2] = hist_B_cut_sideband->Integral(hist_B_cut_sideband->FindBin(start_n[1]),hist_B_cut_sideband->FindBin(start_n[2])-1);
				}
				// if (bkg_n[2]!=0) max_n[2]=pow(sig_n[2],2)/bkg_n[2];
				if (bkg_n[2]!=0) max_n[2]=pow(sig_n[2],2)/(bkg_n[2]);
				start_n[3]=start_n[2]+precision;
				do{
					max_n[3]=0;
					if (NCAT<=3) {
						sig_n[3] = 0;
						bkg_n[3] = 1;
// 						bkg_n_tth[3] = 1;
						bkg_sideband_n[3] = 1;
					} else {
						sig_n[3] = hist_S_cut->Integral(hist_S_cut->FindBin(start_n[2]),hist_S_cut->FindBin(start_n[3])-1);
						bkg_n[3] = hist_B_cut->Integral(hist_B_cut->FindBin(start_n[2]),hist_B_cut->FindBin(start_n[3])-1);
// 						bkg_n_tth[3] = hist_B_cut_tth->Integral(hist_B_cut_tth->FindBin(start_n[2]),hist_B_cut_tth->FindBin(start_n[3])-1);
						bkg_sideband_n[3] = hist_B_cut_sideband->Integral(hist_B_cut_sideband->FindBin(start_n[2]),hist_B_cut_sideband->FindBin(start_n[3])-1);
					}
// 					//if (bkg_n[3]!=0) max_n[3]=pow(sig_n[3],2)/bkg_n[3];
					if (bkg_n[3]!=0) max_n[3]=pow(sig_n[3],2)/(bkg_n[3]);
					max_n[4]=0;
               if (NCAT<=4) {
               	sig_n[4] = 0.;
                  bkg_n[4] = 1.;
// 						bkg_n_tth[4] = 1;
                  bkg_sideband_n[4] = 1.;
               } else {
						sig_n[4] = hist_S_cut->Integral(hist_S_cut->FindBin(start_n[3]),hist_S_cut->GetNbinsX()+1);
						bkg_n[4] = hist_B_cut->Integral(hist_B_cut->FindBin(start_n[3]),hist_B_cut->GetNbinsX()+1);
// 						bkg_n_tth[4] = hist_B_cut_tth->Integral(hist_B_cut_tth->FindBin(start_n[3]),hist_B_cut_tth->GetNbinsX()+1);
						bkg_sideband_n[4] = hist_B_cut_sideband->Integral(hist_B_cut_sideband->FindBin(start_n[3]),hist_B_cut_sideband->GetNbinsX()+1);
               }
// 				//	if (bkg_n[4]!=0) max_n[4]=pow(sig_n[4],2)/(bkg_n[4]);
					if (bkg_n[4]!=0) max_n[4]=pow(sig_n[4],2)/(bkg_n[4]);

					double max_sum = 0;
					int minevt_cond = 0; //condition is false
					for (int index=0;index<NCAT;index++){
						max_sum+=max_n[index];
						minevt_cond_n[index] = (bkg_sideband_n[index]>minevents);
					}
					minevt_cond = std::accumulate(minevt_cond_n, minevt_cond_n + NCAT, 0);
					if (((max_sum)>=max) && (minevt_cond==(NCAT))) {
						max = max_sum;
						for (int index=0;index<NCAT;index++){
							borders[index+1] = start_n[index]; //first and last are START and END
							max_final[index] = max_n[index];
							bkg_yields[index] = bkg_n[index];
							bkg_yields_sideband[index] = bkg_sideband_n[index];
							sig_yields[index] = sig_n[index];
							max_total = max_sum;
							// tth_cut_final = tth_cut;
						}
					}
					start_n[3]+=precision;
				} while (start_n[3]<=(END-(NCAT-4)*precision));
				start_n[2]+=precision;
			} while (start_n[2]<=(END-(NCAT-3)*precision));
			start_n[1]+=precision;
		} while (start_n[1]<=(END-(NCAT-2)*precision));
		start_n[0]+=precision;
	} while (start_n[0]<=(END-(NCAT-1)*precision));
// 	tth_cut+=0.02;
	std::cout<<"max_total " << max_total<<std::endl;
// 	significance_scans_tth.push_back(max_total);
//
// } while (tth_cut<0.4);
//
	borders[NCAT] = END;
//
//
cout << "NCAT " << NCAT << endl;
	ofstream out;
	out<<endl;
	out.open(s.Format("output_txt/%s/%s.txt",date.Data(),outname.Data()));
	out<<"subcategory : "<<subcategory<<endl;
	out<<"S2/B over all bins, sqrt : "<<max_all<<"  , "<<sqrt(max_all)<<endl;
	out<<endl;
	out<<"sqrt(S**2/B) total over the chosen categories : "<<max_total<<"  ,S/sqrt(B) =  "<<sqrt(max_total)<<endl;
	out<<endl;
	out<<"borders of categories : ";
	for (int index=0;index<NCAT+1;index++)
		out<<borders[index]<<"\t";
	out<<endl;
	out<<endl;
// 	out<<"tth_cut : "<<tth_cut_final;
// 	out<<endl;
// 	out<<endl;
	out<<"S**2/B in each category : ";
	for (int index=0;index<NCAT;index++)
		out<<max_final[index]<<"\t";
	out<<endl;
	out<<endl;
	out<<"sqrt(S**2/B) in each category : ";
	for (int index=0;index<NCAT;index++)
		out<<sqrt(max_final[index])<<"\t";
	out<<endl;
	out<<endl;
	out<<"Mgg sidebands bkg yields in categories : ";
	for (int index=0;index<NCAT;index++)
		out<<bkg_yields_sideband[index]<<"\t";
	out<<endl;
	out<<"bkg yields in categories : ";
	for (int index=0;index<NCAT;index++)
		out<<bkg_yields[index]<<"\t";
	out<<endl;
	out<<"sig yields in categories : ";
	for (int index=0;index<NCAT;index++)
		out<<sig_yields[index]<<"\t";
	out.close();

  string line;
  ifstream outfile(s.Format("output_txt/%s/%s.txt",date.Data(),outname.Data()));
  if (outfile.is_open()){
    while ( getline (outfile,line) )
      cout << line << '\n';
    outfile.close();
  }
//
//
//
	float ymin=hist_S->GetBinContent(hist_S->FindFirstBinAbove(0.))*0.1;
	float ymax=hist_B->GetMaximum()*1e02;
//
	TLine* lines[10];
	for (int index=0;index<NCAT-1;index++){
		lines[index] = new TLine(borders[index+1],ymin,borders[index+1],hist_B->GetBinContent(hist_B->FindBin(borders[index+1])));
		lines[index]->SetLineStyle(9);
		lines[index]->SetLineColor(1);
		lines[index]->SetLineWidth(2);
	}

	TCanvas *c1 = new TCanvas("Fit","",800,800);
	c1->SetLogy();
	c1->cd();
	TH1F *frame2 = new TH1F("frame2","",50,xmin,xmax);
	frame2->GetXaxis()->SetNdivisions(505);
	frame2->GetYaxis()->SetRangeUser(80,150);
   frame2->SetStats(0);
	frame2->SetYTitle("Events");
	frame2->SetXTitle(s.Format("%s",what_to_opt.Data()));
	frame2->SetMinimum(ymin);
	frame2->SetMaximum(ymax);
	frame2->Draw();

	hist_B->Draw("HISTsame");
	hist_S->Draw("HISTsame");
// 	hist_B_ttH->Draw("HISTsame");
//
	gPad->Update();
// 	pCMS1.Draw("same");
// 	pCMS2.Draw("same");
// 	pCMS12.Draw("same");
// 	pave22.Draw("same");
// 	pave33.Draw("same");
// 	leg->Draw("same");
	for (int index=0;index<NCAT-1;index++)
		lines[index]->Draw("same");
	gPad->RedrawAxis();
	c1->Print(s.Format("plots/%s/%s.png",date.Data(),outname.Data()));
	c1->Print(s.Format("plots/%s/%s.pdf",date.Data(),outname.Data()));
//
//
// 	double* cat_scan = &categories_scans_tth[0];
// 	double* sign_scan = &significance_scans_tth[0];
// 	int counter = significance_scans_tth.size();
// 	TGraph *gr =new TGraph(counter,cat_scan,sign_scan);
// 	ymin = *std::max_element(sign_scan,sign_scan+counter) * 0.5;
// 	ymax = *std::max_element(sign_scan,sign_scan+counter) * 1.1;
// 	int max_pos = std::distance(sign_scan, std::max_element(sign_scan,sign_scan+counter));
// //
// 	TCanvas *c2 = new TCanvas("B","",800,800);
// 	c2->cd();
// 	TH1F *frame3 = new TH1F("frame3","",50,xmin,xmax);
// 	frame3->GetXaxis()->SetNdivisions(505);
//    frame3->SetStats(0);
// // //	frame3->SetYTitle("S/#sqrt{B_{#gamma#gamma}+B_{ttH}}");
// 	frame3->SetYTitle("S/#sqrt{B}");
// 	frame3->GetYaxis()->SetTitleOffset(1.32);
// 	frame3->SetXTitle(s.Format("%s",what_to_opt.Data()));
// 	frame3->SetMinimum(ymin);
// 	frame3->SetMaximum(ymax);
// 	frame3->Draw();
// 	gr->Draw("Psame");
// 	gPad->Update();
// // 	pCMS1.Draw("same");
// // 	pCMS2.Draw("same");
// // 	pCMS12.Draw("same");
// // 	pave22.Draw("same");
// // 	pave33.Draw("same");
// 	gPad->RedrawAxis();
// 	c2->Print(s.Format("plots/%s/significance_tth_%s.pdf",date.Data(),outname.Data()));
// 	c2->Print(s.Format("plots/%s/significance_tth_%s.png",date.Data(),outname.Data()));
// 	cout<<counter<<endl;
//
// return 0;

}
