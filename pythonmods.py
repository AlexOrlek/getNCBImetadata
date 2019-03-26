#Python modules

def runsubprocess(args,stderrpath=None, stdoutpath=None, writefile=None,shell=False,verbose=True):
    import subprocess,sys #os
    try:
        import thread
    except:
        import _thread
    """takes a subprocess argument list and runs Popen/communicate(); by default, both output and error are printed to screen; stderrpath and stdoutpath for saving output can be optionally set; a redirect can be optionally set (writefile argument); errors are handled at multiple levels i.e. subthread error handling; can set shell=True; the function can be used 'fruitfully' since stdout is returned"""
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
            if verbose==True:
                try:
                    print('{} {}'.format(stdout.decode(), 'stdout'))
                except:
                    pass
                try:
                    print('{} {}'.format(stderr.decode(), 'stderr'))
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
                if verbose==True:
                    try:
                        print('{} {}'.format(stdout.decode(), 'stdout'))
                    except:
                        pass
                    try:
                        print('{} {}'.format(stderr.decode(), 'stderr'))
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
            if verbose==False:
                print('{} {}'.format(processname, 'processname'))
            print('{} {}'.format('source code fail'))
    except:
        if verbose==False:
            print('{} {}'.format(processname, 'processname'))
        print('runsubprocess code fail')
        sys.exit()
        
    if p.returncode!=0:
        if 'driverscript' in str(sys.argv[0]):
            sys.exit()
        else:
            #os._exit
            try:
                thread.interrupt_main()
            except:
                _thread.interrupt_main()
            #keyboard interrupt is more drastic than sys.exit - only use for subscript subprocess errors which wouldn't otherwise trigger driverscript abort
    else:
        return stdout


