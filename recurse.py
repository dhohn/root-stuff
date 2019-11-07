#! /usr/bin/env python

def ls_a_recursive(here, to=None):
    '''
    lists recursively all objects in all subdirs of TDirectory,
    uses cd() and then only knows about the actual objects,
    not sure I can get the path from them

    here is TDirectory
    to is TKey
    '''
    #print "here", here, "to", to
    #print "gDir", ROOT.gDirectory

    if not to:
        #print "we dont know where to go yet"
        for tkey in here.GetListOfKeys():
            if tkey:
                #print "tkey", tkey
                oldhere = here.GetDirectory("")
                print ls_a_recursive(here,tkey)
                ROOT.gDirectory = oldhere
                here = oldhere
            
    obj = tryGet(here,to)
    if obj and not obj.InheritsFrom("TDirectory"):
        #print "were at the end of a branch"
        return str(obj.Print())
    if obj and obj.InheritsFrom("TDirectory"):
        #print "we keep going down"
        here.cd(to.GetName())
        print ls_a_recursive(ROOT.gDirectory)

def tryGet(tdir,tkey):
    obj = None
    if isinstance(tkey,ROOT.TKey):
        obj = tdir.Get(tkey.GetName())
    elif isinstance(tkey,str):
        obj = tdir.Get(tkey)
    
    if obj:
        return obj
    else:
        return None

def ls_a_path(tdir,path="",l=[]):
    '''
    recursively lists all objects in all subdirs of a TDirectory with path relative to tdir
    tdir is TDirectory
    path is str, to start listing there
    l is list, holds output, may have to be cleaned for spurious None's

    '''
    #print l

    if not path:
        obj = tdir
    else:
        obj = tryGet(tdir,path)
    if obj and obj.InheritsFrom("TDirectory"):
        for tkey in obj.GetListOfKeys():
            if not path:
                newpath = tkey.GetName()
            else:
                newpath = "/".join([path]+[tkey.GetName()])
            l.append( ls_a_path(tdir,newpath,l) )
    if obj and not obj.InheritsFrom("TDirectory"):
        return path

def ls_a_path_for(tdir):
    '''
    tdir is TDirectory
    apparently you can also append to a list while iterating over it,
    but Im not sure whether this is possible in one pass,
    abandoned
    '''
    path_list = [ tkey.GetName() for tkey in tdir.GetListOfKeys() ]

    for path in path_list:
        obj = tryGet(tdir,path)
        
    
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

    rfile = ROOT.TFile(sys.argv[1],'READ')
    #ls_a_recursive(rfile)
    thislist = []
    print ls_a_path(rfile,l=thislist)
    for t in [t for t in thislist if t]:
        print t

    rfile.Close()

        
    #print sys.argv
    #try:
    #    subdir = '/'.join(sys.argv[2].split('/')[:-1])
    #    #print subdir
    #    ls(sys.argv[1],subdir)
    #except IndexError:
    #    ls(sys.argv[1])
