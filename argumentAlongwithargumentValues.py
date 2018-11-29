#code snippet for getting argument name along with parameter passsed in the form of dictionary


import inspect

d = {}
def TestFunc(a,b):
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    #print ('function name "%s"' % inspect.getframeinfo(frame)[2])
# =============================================================================
#     for i in args:
#         print ("    %s = %s" % (i, values[i]))
# =============================================================================
    d = dict([(i, values[i]) for i in args])
    return d


TestFunc(1,2)
