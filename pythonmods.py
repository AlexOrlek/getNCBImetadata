#############Python modules

###wrapper for the subprocess command
def runsubprocess(args,stderrpath=None, stdoutpath=None, writefile=None,shell=False,verbose=False):
    import subprocess,sys #os
    try:
        import thread
    except:
        import _thread
    """takes a subprocess argument list and runs Popen/communicate(); if verbose=True, both output and error are printed to screen; stderrpath and stdoutpath for saving output can be optionally set; a redirect can be optionally set (writefile argument); errors are handled at multiple levels i.e. subthread error handling; can set shell=True; the function can be used 'fruitfully' since stdout is returned"""
    if shell==True: #e.g. args=['ls *.txt]
        processname=args[0] #ls *.txt
        processname=processname.split()#['ls', '*.txt'] #list argument syntax 
    else:
        processname=args
    processname=(" ".join(a for a in args))
    if stderrpath==None:
        pass
    else:
        if stderrpath.endswith('stderr.txt'): #want to make sure file ends with non-duplicated 'stderr.txt'
            stderrpath=str(stderrpath[:-10]).strip()
        stderrstrip=stderrpath.split('/')[-1]
        if stderrstrip=='': #there was nothing to strip after / i.e. was just /stderr.txt or stderr.txt
            pass
        else:
            stderrpath=stderrpath[:-(len(stderrstrip))]
        stderrpath=stderrpath+processname+'_'+stderrstrip+'stderr.txt'
    if stdoutpath==None:
        pass
    else:
        if stdoutpath.endswith('stdout.txt'): 
            stdoutpath=str(stdoutpath[:-10]).strip()
        stdoutstrip=stdoutpath.split('/')[-1]
        if stdoutstrip=='': 
            pass
        else:
            stdoutpath=stdoutpath[:-(len(stdoutstrip))]
        stdoutpath=stdoutpath+processname+'_'+stdoutstrip+'stdout.txt'
    if verbose==True:
        print('{} {}'.format(processname, 'processname'))
    try:
        if writefile==None:
            if shell==False:
                p=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if shell==True:
                p=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr= p.communicate()
            try:
                if stdout: #if stdout not empty...  #removed "and verbose==True" (always useful to show stdout)
                    print('{}'.format(stdout.decode()))
            except:
                pass
            try:
                if stderr:
                    print('{}'.format(stderr.decode()))
            except:
                pass
            if stdoutpath==None:
                pass
            else:
                with open(stdoutpath,'w') as stdoutfile:
                    stdoutfile.write(stdout)
            if stderrpath==None:
                pass
            else:
                with open(stderrpath,'w') as stderrfile:
                    stderrfile.write(stderr)
        else:
            with open(writefile,'w') as stdout:
                if shell==False:
                    p=subprocess.Popen(args,stdout=stdout, stderr=subprocess.PIPE)
                if shell==True:
                    p=subprocess.Popen(args,stdout=stdout, stderr=subprocess.PIPE, shell=True)
                stdout, stderr= p.communicate()
                try:
                    if stdout:
                        print('{}'.format(stdout.decode()))
                except:
                    pass
                try:
                    if stderr:
                        print('{}'.format(stderr.decode()))
                except:
                    pass
                #n.b stdout is None - can't write to file
                if stderrpath==None:
                    pass
                else:
                    with open(stderrpath,'w') as stderrfile:
                        stderrfile.write(stderr)
        if p.returncode==0:
            if verbose==True:
                print('{} {}'.format(processname, 'code has run successfully'))
        else:
            sys.exit() #triggers except below
    except:
        if verbose==False:
            print('{} {}'.format(processname, '#this pipeline step produced error'))
        print('unexpected error; exiting')
        sys.exit()
        
    if p.returncode!=0:
        print('unexpected error; exiting')
        try:
            thread.interrupt_main()
        except:
            _thread.interrupt_main()
    else:
        return stdout
