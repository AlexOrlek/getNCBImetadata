#############Python modules

###wrapper for the subprocess command
def runsubprocess(args,verbose=False):
    import subprocess,sys #os
    try:
        import thread
    except:
        import _thread
    """takes a subprocess argument list and runs Popen/poll(); if verbose=True, processname (string giving command call) is printed to screen (processname is always printed if a process results in error); errors are handled at multiple levels i.e. subthread error handling"""
    processname=(" ".join(a for a in args))
    if verbose==True:
        print('{} {}'.format(processname, 'processname'))
    try:
        p=subprocess.Popen(args, stdout=subprocess.PIPE)
        while True:
            stdout=p.stdout.readline()
            if p.poll() is not None:
                break
            if stdout: #if stdout not empty...
                print('{}'.format(stdout.decode().strip()))

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

