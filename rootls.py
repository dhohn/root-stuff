#! /usr/bin/env python

def ls(fname,curdir=''):

    rfile = ROOT.TFile(fname,'READ')

    if curdir:
        tdir = rfile.Get(curdir)
        curdir=curdir.rstrip('/')+'/'
    else:
        tdir = rfile
        
    for tkey in tdir.GetListOfKeys():
        toprint = curdir+tkey.GetName()
        if tkey.GetClassName().count('Directory'):
            toprint += '/'

        print toprint


if __name__=="__main__":
    import sys, os

    if not sys.stdout.isatty():
        # remember the original setting
        oldTerm = os.environ['TERM']
        os.environ['TERM'] = ''
        import ROOT
        # restore the orignal TERM setting
        os.environ['TERM'] = oldTerm
        del oldTerm
    else:
        import ROOT

    #print sys.argv
    try:
        subdir = '/'.join(sys.argv[2].split('/')[:-1])
        ls(sys.argv[1],subdir)
    except IndexError:
        ls(sys.argv[1])
