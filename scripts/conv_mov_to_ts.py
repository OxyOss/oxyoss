#!/usr/bin/env python


'''
conv_command = "ffmpeg -i %s -s hd720 -acodec mp2 -vcodec mpeg2video -r 25 -ar 44100 -vb 7500k %s" % ( input_file, output_file)
'''


def convertToTS(inputFile, outputFile):
    conv_command = "ffmpeg -i %s -s hd720 -acodec mp2 -vcodec mpeg2video -r 25 -ar 44100 -vb 7500k %s" % ( inputFile, outputFile)

'''
some colourful crap!
                    if status == u"up to date":
                        init, cleanup = "\x1b[32;1m", "\x1b[0m"
                    elif status == u"syncing":
                        init, cleanup = "\x1b[36;1m", "\x1b[0m"
                    elif status == u"unsyncable":
                        init, cleanup = "\x1b[41;1m", "\x1b[0m"
                    elif status == u"selsync":
                        init, cleanup = "\x1b[37;1m", "\x1b[0m"
'''
    
def stuff():
    for root, dirs, files in os.walk(splicer_base):
        try: 
            dirs.remove('Archive') ## Don't play with Archive directory...
        except: pass
    #for filename in files:
     
     
class converter:
    def __init__(self, debug=True):
        
        return
    
    def main(self):
        
        print "\x1b[0mHello there!"
        
        return
    
    def execute_main_function(self, arglist=None):
        import sys
        #Fake the arg list for debugging
        if arglist == None: argv = sys.argv
        else: argv = [self.PROGNAME] + arglist.split()
        
        try: 
            #self.initialise(argv)
            ret = self.main()
        except Exception, why:
            print "Had an exception: %s" % str(why)
            os._exit(-9)
        return
def main(arglist=None):
    # Do the basic stuff.
    import getopt, sys
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd", ["help", "debug"])
    except getopt.GetoptError, err:
        # Print help inforamtion and exit:
        print str(err) # Will print something like "option -a not recognised"
        usage()
        sys.exit(2)
    
    debug = False
    for o, a in opts:
        if o in ('-d', '--debug'):
            debug = True
        else:
            assert False, "unhandled option"

    print "Debug: " + str(debug)
    
    cmd = converter(debug)
    
    cmd.execute_main_function(arglist)
    return 0

if __name__ == '__main__':
    main()
    
