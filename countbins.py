import ROOT,sys

def main(argv):
    if len(argv)-1<1:
        raise RuntimeError('usage: python countins.py file.root')
    filename  = argv[1]
    f = ROOT.TFile.Open(filename,'READ')
    if not f: raise RuntimeError(filename+' doesnt exist')

    nbins_dict = {}
    
    for tkey in f.GetListOfKeys():
        if tkey.GetClassName().count('TH1'):
            histoname = tkey.GetName()


        h = f.Get(histoname)
        if not h: raise RuntimeError(histoname+' doesnt exist in '+filename)

        nbins = h.GetNbinsX()
        try:
            nbins_dict[nbins] += [histoname]
        except:
            nbins_dict[nbins] = [histoname]

    for n in sorted(nbins_dict.keys(),reverse=True):
        for histo in nbins_dict[n]:
            print n, histo

        

if __name__ == '__main__':
    main(sys.argv)
