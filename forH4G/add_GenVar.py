import ROOT
import itertools
from array import array
import argparse

if __name__ == '__main__':

 parser =  argparse.ArgumentParser(description='cat MVA')
 parser.add_argument('-i', '--input', dest='input', required=True, type=str)
 parser.add_argument('-m', '--mass',  dest='mass',  required=True, type=float) 
 
 args = parser.parse_args()
 inputtree = args.input
 mass = args.mass

 if mass==-1: print "Running on dataMix!"

 tree = ROOT.TChain() 
 tree.AddFile(inputtree) 
 
 indices = [i for i, elem in enumerate(inputtree.split("/")) if '.root' in elem]
 output_name = inputtree.split("/")[indices[0]]
 output_name = output_name.replace('.root','_genMass.root')
 tree_name = inputtree.split("/")[len(inputtree.split("/"))-1] 
 print "Output: ",output_name, tree_name

 gRandom = ROOT.TRandom3()
 outfile = ROOT.TFile(output_name, "RECREATE")
 outtree = tree.CopyTree("");
 outtree.SetName(tree_name);
 outtree.SetTitle(tree_name);
 genMass = array('f', [0])
 _genMass = outtree.Branch('genMass', genMass, 'genMass/F')     
 nentries = outtree.GetEntries()
 masses = [15.,25.,35.,45.,60.]
 for i in range(0, nentries):
    if mass!= -1: genMass[0] = mass
    else: 
       index = int(gRandom.Uniform(0.,4.999999))
       genMass[0] = masses[index]
       #print index,masses[index]
    _genMass.Fill() 
 outtree.Write()
 outfile.Close()

      

