import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
#sys.path.insert(1, '/home/bhalla/homework/HILLTAU/REPO/HillTau/PythonCode')
import hillTau

# To add: 
# Check for subsetting
# Check for automatic buffering of stimulated molecules

ERR_LIMIT = 1e-6

stimVec = [
    ["exc", "input", [1e-3, 10, 0, 20], "output", [0.2638e-3, 10.75, 0.5e-3, 20, 0.0, 30]],
    ["inh", "input", [1e-3, 10, 0, 20], "output", [0.7362e-3, 10.75, 0.5e-3, 20, 1e-3, 30]],
    ["osc", "mol", [], "output", [0.3977e-3, 500, 0.294e-3, 2000, 0.1008e-3, 3000]],
    ["bcm", "Ca", [0.01e-3, 0, 0.5e-3, 20, 2e-3, 40, 10e-3, 60], "synAMPAR", [0.403e-3, 15, 0.136e-3, 35, 0.465e-3, 55, 0.48e-3, 75]],
    ["eqn", "input", [1e-3, 10, 0, 20], "eq", [3.46e-3, 10.75, 3.7e-3, 15, 1.2e-3, 30]],
    ["eqn_with_constants", "input", [1e-3, 10, 0, 20], "eq", [3.46e-3, 10.75, 3.7e-3, 15, 1.2e-3, 30]],
    ["exc2ndOrder", "input", [1e-3, 10, 0, 20], "output", [0.2638e-3, 10.75, 0.5e-3, 20, 0.0, 30]],
    ["conv", "input", [1e-3, 10, 0, 20], "output", [0.5276e-3, 10.75, 1e-3, 20, 0.0, 30]],
    ["conv2ndOrder", "input", [1e-3, 10, 0, 20], "output", [0.5276e-3, 10.75, 1e-3, 20, 0.0, 30]],
    ["exc_tau_baseline", "input", [1e-3, 10, 0, 20], "output", [0.7638e-3, 10.75, 1.0e-3, 20, 0.684e-3, 25]],
    ["ff_inhib", "input", [1e-3, 20, 0, 40], "output", [0.289e-3, 25, 0.0619e-3, 40, 0, 60]],
    ["fb_inhib", "input", [1e-3, 20, 0, 60], "output", [0.74e-3, 25, 0.189e-3, 60, 0, 100]],
    ["gain", "input", [1e-3, 10, 0, 20], "output", [0.5276e-3, 10.75, 1e-3, 20, 0.0, 30]],
    ["modifier", "input", [1e-3, 10, 0, 20], "output", [0.474e-3, 11, 0.75e-3, 20, 0.0, 30]],
    ["bistable", "stim", [1, 0, 100, 20, 1, 30, 0.01, 50, 1, 51, .01, 70, 1, 80], "output", [0.0217, 20, 0.52, 50, 0.52, 70, 0.0217, 100]],
    ["bcm_bistable", "Ca", [2e-3, 15, 0.08e-3, 16, 0.4e-3, 35, 0.08e-3, 45], "synAMPAR", [0.207e-6, 15, 0.8205e-3, 20, 0.8331e-3, 30, 0.21e-6, 60 ]],
]

class Event():
    def __init__( self, mol, conc, t, isStim ):
        self.mol = mol
        self.isStim = isStim
        self.t = float(t)
        self.conc = float( conc )

def parseEvents( mol, f, isStim ):
    ret = []
    idx = range( 0, len(f), 2 )
    for i in idx:
        ret.append( Event( mol, f[i], f[i+1], isStim ) )
    return ret


def runit( f ):
    jsonDict = hillTau.loadHillTau( f[0] + ".json" )
    qs = hillTau.getQuantityScale( jsonDict )
    hillTau.scaleDict( jsonDict, qs )
    model = hillTau.parseModel( jsonDict )
    model.dt = 1.0

    ev = []
    ev.extend( parseEvents( f[1], f[2], 1 ) )
    ev.extend( parseEvents( f[3], f[4], 0 ) )
    sev = sorted( ev, key = lambda x: x.t )

    model.reinit()
    lastt = 0.0 
    ans = []
    maxconc = 0.0
    for s in sev:
        delta = s.t - lastt
        if delta > 0.0:
            model.advance( delta )
        if s.isStim:
            model.conc[ model.molInfo[ s.mol ].index ] = s.conc
        else:
            c = model.conc[ model.molInfo[ s.mol ].index ]
            #print( "Conc @ {} = {}".format( s.t, c ) )
            maxconc = max( maxconc, c )
            ans.append( s.conc - model.conc[ model.molInfo[ s.mol ].index ] )
        lastt = s.t
    err = 0.0
    #print( "ANS = ", ans )
    for d in ans:
        err += d*d / ( maxconc * maxconc )
    return err / len( ans ), model

def checkGroups( model ):
    # Assumes that the last loaded model was bcm_bistable
    grps = {"internal": "ampar_g", "synAMPAR": "ampar_g", "on_CaMKII":"CaMKII_g", "CaN":"CaN_g", "fb": "CaMKII_g"}
    print( "Checking groups{:20s}".format( "" ), end = "....     " )
    OK = True
    for mol, grp in grps.items():
        if model.molInfo[mol].grp != grp:
            print( "failed, group of mol '{}' should be '{}', but is '{}'".format( mol, grp, model.molInfo[mol].grp ) )
            OK = False
    if OK:
        print( "OK, all objects are in correct group" )


def main():
    parser = argparse.ArgumentParser( description = "This program runs regression tests for HillTau" )
    parser.add_argument( "-s", "--source", type=str, help= "Optional: specifiy source version for hillTau. Defaults to system installed hillTau." )
    parser.add_argument( "-p", "--plot", nargs=1, metavar = "testName", help="Optional: Plot the output of the specified test model" )

    args = parser.parse_args()
    if args.plot:
        name = args.plot[0].split( "." )[0]
        sdict = { v[0]:v for v in stimVec }
        stim = sdict.get( name )
        if stim:
            fig = plt.figure( figsize = (6, 12) )
            ax1 = plt.subplot( 2, 1, 1 )
            ax2 = plt.subplot( 2, 1, 2 )
            err, model = runit( stim )
            endtime = stim[4][-1]
            xstim = [0]
            for s in stim[2][1::2]:
                xstim.extend( [s,s] )
            xstim.append( endtime )
            ystim = [0]
            last = 0

            for s in stim[2][::2]:
                ystim.extend( [last,s] )
                last = s
            ystim.append(last)
            ax1.plot( xstim, ystim, "-ro",label="stim" )
            ax1.legend()

            xout = stim[4][1::2]
            yout = stim[4][::2]
            ax2.plot( xout, yout, "-g+",label="expected" )
            ysim = model.getConcVec( model.molInfo[stim[3]].index )
            xsim = np.array( range( len( ysim ) ) ) * model.dt
            ax2.plot( xsim, ysim, ":b",label="result" )
            ax2.legend()

        if err > ERR_LIMIT:
            print( "failed, err = {:.5g}".format( err ) )
        else:
            print( "OK, err = {:.5g}".format( err ) )
        plt.show()
        quit()




    for s in stimVec:
        print( "Checking model {:20s}".format( s[0] ), end = "....     " )
        err, model = runit( s )
        if err > ERR_LIMIT:
            print( "failed, err = {:.5g}".format( err ) )
        else:
            print( "OK, err = {:.5g}".format( err ) )
    checkGroups( model )

if __name__ == '__main__':
    main()
