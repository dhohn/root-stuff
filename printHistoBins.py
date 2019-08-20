#! /usr/bin/env python


import ROOT
import sys
import tabulate
import argparse
from uncertainties import ufloat


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("histo_name")
    parser.add_argument("-e","--errors",    action="store_true" )
    parser.add_argument("-l","--binlabels", action="store_true" )
    parser.add_argument("--header",    action="store_true" )
    args = parser.parse_args()
    
    f = ROOT.TFile.Open(args.file_name,'READ')
    if not f: raise RuntimeError(args.file_name+' doesnt exist')
    h = f.Get(args.histo_name)
    if not h: raise RuntimeError(args.histo_name+' doesnt exist in '+args.file_name)
        

    bin_contents = []
    labels = []
    for b in range(1,h.GetNbinsX()+1):
        label = h.GetXaxis().GetBinLabel(b)
        if label == "":
            label = str(h.GetBinLowEdge(b))+" - "+str(h.GetBinLowEdge(b+1))
        bc = h.GetBinContent(b)
        if bc.is_integer(): bc = int(bc)
        else: bc = str(bc)
        if args.errors:
            bc = ufloat(h.GetBinContent(b),h.GetBinError(b))
        labels += [label]
        bin_contents += [bc]
        
    table = zip(bin_contents)
    header = [h.GetXaxis().GetTitle()]
    if args.binlabels:
        table = zip(labels,bin_contents)
        header += ["bin content"]
    if args.header:
        print tabulate.tabulate(table,header,tablefmt="orgtbl",numalign="decimal")
        return
    
    print tabulate.tabulate(table,tablefmt="orgtbl",numalign="decimal")

if __name__ == '__main__':    
    main(sys.argv)
