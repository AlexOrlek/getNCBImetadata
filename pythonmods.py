#############Python modules

###wrapper for subprocess command
def runsubprocess(args,verbose=False,shell=False,polling=False,printstdout=True,preexec_fn=None):
    """takes a subprocess argument list and runs Popen/communicate or Popen/poll() (if polling=True); if verbose=True, processname (string giving command call) is printed to screen (processname is always printed if a process results in error); errors are handled at multiple levels i.e. subthread error handling; fuction can be used fruitfully (returns stdout)"""
    #function setup
    import subprocess,sys,signal
    try:
        import thread
    except:
        import _thread
    def subprocess_setup(): #see: https://github.com/vsbuffalo/devnotes/wiki/Python-and-SIGPIPE
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    if preexec_fn=='sigpipefix':
        preexec_fn=subprocess_setup
    else:
        assert preexec_fn==None,'Error: unrecognised preexec_fn argument %s'%preexec_fn
    if shell==True:
        processname=args[0]
        processname=processname[0].split()
        processname=(" ".join(a for a in processname))
    else:
        processname=(" ".join(a for a in args))
    #
    if verbose==True:
        print('{0} {1}'.format(processname, 'processname'))
    try:
        if polling==True:
            p=subprocess.Popen(args, stdout=subprocess.PIPE,shell=shell,preexec_fn=preexec_fn)
            while True:
                stdout=p.stdout.readline()
                if p.poll() is not None:
                    break
                if stdout: #if stdout not empty...
                    if printstdout==True:
                        print('{0}'.format(stdout.decode().strip()))
        else:
            p=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=shell,preexec_fn=preexec_fn)
            stdout, stderr= p.communicate()
            if stdout:
                if printstdout==True:
                    print('{0}'.format(stdout.decode()))
            if stderr:
                try: #want to output to stderr stream
                    if (sys.version_info > (3, 0)):
                        print('{0}'.format(stderr.decode()),file=sys.stderr) #Python3
                    else:
                        print>>sys.stderr,stderr  #Python2
                except: #if above code block fails for some reason, print stderr (to stdout)
                    print('{0}'.format(stderr.decode()))

        if p.returncode==0:
            if verbose==True:
                print('{0} {1}'.format(processname, 'code has run successfully'))
        else:
            sys.exit() #triggers except below
    except:
        print('{0} {1}'.format(processname, '#this pipeline step produced error'))
        print('unexpected error; exiting')
        sys.exit()
        
    if p.returncode!=0:
        print('unexpected error; exiting')
        try:
            thread.interrupt_main()
        except:
            _thread.interrupt_main()
    else:
        if stdout:
            return stdout.decode().strip()

