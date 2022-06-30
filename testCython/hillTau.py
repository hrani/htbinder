# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 

'''
*******************************************************************
 * File:            hillTau.py
 * Description:     Wrapper for HillTau, hillTauNum from Cython
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/
 '''
from __future__ import print_function
import sys
import json
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt
import hillTauNum as htn

lookupQuantityScale = { "M": 1000.0, "mM": 1.0, "uM": 1e-3, "nM": 1e-6, "pM": 1e-9 }

SIGSTR = "{:.4g}" # Used to format floats to keep to 4 sig fig. Helps when dumping JSON files.

def loadHillTau( fname ):
    with open( fname ) as json_file:
        model = json.load( json_file )
    return model

def subsetModel( model, subsetInfo ):
    return

def getQuantityScale( jsonDict ): 
    qu = jsonDict.get( "quantityUnits" )
    qs = 1.0
    if qu:
        qs = lookupQuantityScale[qu]
    return qs

def scaleDict( jsonDict, qs ):
    for grpname, grp in jsonDict["Groups"].items():
        sp = grp.get( "Species" )
        if sp:
            for m in sp:
                sp[m] = float( SIGSTR.format( sp[m] * qs ) )
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                # Check if it is a single substrate reac
                if len( reac["subs"] ) == 1:
                    reac["KA"] = float( SIGSTR.format( reac["KA"] ) )
                else:
                    reac["KA"] = float( SIGSTR.format( reac["KA"] * qs ) )
                reac["tau"] = float( SIGSTR.format( reac["tau"] ) )
                tau2 = reac.get( "tau2" )
                if tau2:
                    reac["tau2"] = float( SIGSTR.format( tau2 ) )
                bl = reac.get( "baseline" )
                if bl:
                    reac["baseline"] = float( SIGSTR.format( bl * qs ) )

def parseModel( jsonDict ):
    model = htn.Model( jsonDict )

    # First, pull together all the species names. They crop up in
    # the Species, the Reacs, and the Eqns. They should be used as
    # an index to the conc and concInit vector.
    # Note that we have an ordering to decide which mol goes in which group:
    # Species; names of reacs, First term of Eqns, substrates.
    # This assumes that every quantity term has already been scaled to mM.
    for grpname, grp in model.jsonDict['Groups'].items():
        # We may have repeats in the species names as they are used 
        # in multiple places.
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                for subname in reac["subs"]:
                    model.molInfo[subname] = htn.MolInfo( subname, grpname, order=0)

    for grpname, grp in model.jsonDict['Groups'].items():
        if "Eqns" in grp:
            for lhs, expr in grp["Eqns"].items():
                model.eqnInfo[lhs] = htn.EqnInfo( lhs, grpname, expr )
                model.molInfo[lhs] = htn.MolInfo( lhs, grpname, order=-1)
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                model.molInfo[reacname] = htn.MolInfo( reacname, grpname, order=-1 )

    for grpname, grp in model.jsonDict['Groups'].items():
        if "Species" in grp:
            for molname, conc in grp['Species'].items():
                model.molInfo[molname] = htn.MolInfo( molname, grpname, order=0, concInit = conc )
                grp['Species'][molname] = conc

    # Then assign indices to these unique molnames, and build up the
    # numpy arrays for concInit and conc.
    numMols = len( model.molInfo )
    model.conc = np.zeros( numMols )
    model.concInit = np.zeros( numMols )
    i = 0
    for molname, info in model.molInfo.items():
        info.index = i
        model.conc[i] = model.concInit[i] = info.concInit
        i += 1

    # Now set up the reactions. we need the mols all defined first.
    for grpname, grp in model.jsonDict['Groups'].items():
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                r = htn.ReacInfo( reacname, grpname, reac, model.molInfo )
                model.reacInfo[reacname] = r
                # Eval concInit ONLY if it is not explicitly defined.
                if model.molInfo[ reacname ].order == -1:
                    if r.inhibit:
                        model.concInit[ r.prdIndex ] = r.concInf( model.concInit ) + r.baseline
                        if model.concInit[r.prdIndex] < 0.0:
                            #print( "oops, starting -ve:", r.name, self.concInit[r.prdIndex] )
                            model.concInit[r.prdIndex] = 0.0
                    else:
                        model.concInit[ r.prdIndex ] = r.baseline

    # Now set up the equation, again, we need the mols defined.
    for eqname, eqn in model.eqnInfo.items():
        eqn.parseEqn( model.molInfo )

    model.reinit()
    sortReacs( model )
    return model

def breakloop( model, maxOrder, numLoopsBroken  ):
    for reacname, reac in model.reacInfo.items():
        if model.molInfo[reacname].order < 0:
            model.molInfo[reacname].order = maxOrder
            #print("Warning; Reaction order loop. Breaking {} loop for {}, assigning order: {}".format( numLoopsBroken, reacname, maxOrder ) )
            break

def sortReacs( model ):
    # Go through and assign levels to the mols and reacs within a group.
    # This will be used later for deciding evaluation order.
    numOrdered = sum( [ ( m.order >= 0 ) for m in model.molInfo.values() ] )
    maxOrder = 0
    numLoopsBroken = 0
    while numOrdered < len( model.molInfo ): 
        stuck = True
        for reacname, reac in sorted( model.reacInfo.items() ):
            order = [ model.molInfo[i].order for i in reac.subs ]
            #print( "{}@{}: {}".format( reacname, model.molInfo[reacname].order, order ) )
            if min( order ) >= 0:
                mo = max( order ) + 1
                model.molInfo[reacname].order = mo
                maxOrder = max( maxOrder, mo )
                numOrdered += 1
                stuck = False
        if stuck:
            breakloop( model, maxOrder, numLoopsBroken )
            numLoopsBroken += 1
            #quit()

        for eqname, eqn in sorted( model.eqnInfo.items() ):
            order = [ model.molInfo[i].order for i in eqn.subs ]
            model.molInfo[eqname].order = max(order)

    maxOrder += 1
    model.sortedReacInfo = [[]] * maxOrder    
    for name, reac in model.reacInfo.items():
        order = model.molInfo[name].order
        model.sortedReacInfo[order].append( reac )

def main():
    parser = argparse.ArgumentParser( description = 'This is the hillTau simulator.\n'
    'This program simulates abstract kinetic/neural models defined in the\n'
    'HillTau formalism. HillTau is an event-driven JSON form to represent\n'
    'dynamics of mass-action chemistry and neuronal activity in a fast, \n'
    'reduced form. The hillTau program loads and checks HillTau models,\n'
    'and optionally does simple stimulus specification and plotting\n')
    parser.add_argument( 'model', type = str, help='Required: filename of model, in JSON format.')
    parser.add_argument( '-r', '--runtime', type = float, help='Optional: Run time for model, in seconds. If flag is not set the model is not run and there is no display', default = 0.0 )
    parser.add_argument( '-s', '--stimulus', type = str, nargs = '+', action='append', help='Optional: Deliver stimulus as follows: --stimulus molecule conc [start [stop]]. Any number of stimuli may be given, each indicated by --stimulus. By default: start = 0, stop = runtime', default = [] )
    parser.add_argument( '-p', '--plots', type = str, help='Optional: plot just the specified molecule(s). The names are specified by a comma-separated list.', default = "" )
    args = parser.parse_args()
    jsonDict = loadHillTau( args.model )
    qs = getQuantityScale( jsonDict )
    scaleDict( jsonDict, qs )
    model = parseModel( jsonDict )

    runtime = args.runtime
    if runtime <= 0.0:
        return

    model.dt = 10 ** (np.floor( np.log10( runtime )) - 2.0)
    if runtime / model.dt > 500:
        model.dt *= 2

    stimvec = []
    
    for i in args.stimulus:
        if len( i ) < 2:
            print( "Warning: need at least 2 args for stimulus, got {i}".format( i ) )
            continue
        i[1] = float( i[1] ) * qs # Assume stim units same as model units.
        if len(i) == 2:
            i.extend( [0.0, runtime] )
        if len(i) == 3:
            i.extend( [runtime] )
        i[2] = float( i[2] )
        i[3] = float( i[3] )
        runtime = max( runtime, i[3] )
        stimvec.append( htn.Stim( i, model ) )
        stimvec.append( htn.Stim( i, model, off = True ) )

    stimvec.sort( key = htn.Stim.stimOrder )

    model.reinit()
    currTime = 0.0
    for s in stimvec:
        model.advance( s.time - currTime )
        model.conc[s.mol.index] = s.value
        currTime = s.time
    if runtime > currTime:
        model.advance( runtime - currTime )

    plotvec = np.transpose( np.array( model.plotvec ) )
    x = np.array( range( plotvec.shape[1] ) ) * model.dt
    clPlots = args.plots.split(',')
    if len( args.plots ) > 0 :
        clPlots = [ i.strip() for i in clPlots if i in model.molInfo]
    else: 
        clPlots = [ i for i in model.molInfo ]

    qu = jsonDict.get( "quantityUnits" )
    if qu:
        ylabel = 'Conc ({})'.format( qu )
        qs = lookupQuantityScale[qu]
    else:
        ylabel = 'Conc (mM)'
        qs = 1

    for name in clPlots:
        mi = model.molInfo[name]
        i = mi.index
        plt.plot( x, plotvec[i]/qs, label = name )

    plt.xlabel('Time (s)')
    plt.ylabel(ylabel)
    plt.title( args.model )
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
