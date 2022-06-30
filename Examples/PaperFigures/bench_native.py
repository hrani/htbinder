from __future__ import print_function
import pstats, cProfile
import hillTau
import time

runtime = 1e5

jsonDict = hillTau.loadHillTau( "HT_MODELS/aut6.json" )
model = hillTau.parseModel( jsonDict )
model.dt = 1
model.reinit()
t = time.time()

def advance():
    model.advance( runtime )


#cProfile.runctx("advance()", globals(), locals(), "Profile.prof" )

#s = pstats.Stats( "Profile.prof" )
#s.strip_dirs().sort_stats("time").print_stats()

model.advance( runtime )
print( "Ran it in ", str( time.time() - t ) )

