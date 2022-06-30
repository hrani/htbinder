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
 * Description:
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
import ht

lookupQuantityScale = { "M": 1000.0, "mM": 1.0, "uM": 1e-3, "nM": 1e-6, "pM": 1e-9 }

SIGSTR = "{:.4g}" # Used to format floats to keep to 4 sig fig. Helps when dumping JSON files.

def loadHillTau( fname ):
    with open( fname ) as json_file:
        model = json.load( json_file )
    return model

def subsetModel( model, subsetInfo ):
    return

class Stim():
    def __init__( self, stim, model, off = False ):
        self.objname = stim[0]
        self.mol = model.molInfo.get( stim[0] )
        if not self.mol:
            print( "Stimulus Molecule '{}' not found".format( stim[0] ) )
            quit()
        self.value = stim[1]
        self.isOff = off
        if off:
            self.time = stim[3]
            self.value = self.mol.concInit
        else:
            self.time = stim[2]

    @staticmethod
    def stimOrder( stim ):
        return stim.time

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
    model = ht.Model()

    # First, pull together all the species names. They crop up in
    # the Species, the Reacs, and the Eqns. They should be used as
    # an index to the conc and concInit vector.
    # Note that we have an ordering to decide which mol goes in which group:
    # Species; names of reacs, First term of Eqns, substrates.
    # This assumes that every quantity term has already been scaled to mM.
    for grpname, grp in jsonDict['Groups'].items():
        # We may have repeats in the species names as they are used 
        # in multiple places.
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                for subname in reac["subs"]:
                    model.makeMol( subname, grpname, order=0)
                    #mi[subname] = ht.MolInfo( subname, grpname, order=0)

    for grpname, grp in jsonDict['Groups'].items():
        if "Eqns" in grp:
            for lhs, expr in grp["Eqns"].items():
                #model.makeEqn( lhs, grpname, expr )
                #ei[lhs] = ht.EqnInfo( lhs, grpname, expr )
                model.makeMol( lhs, grpname, order=-1)
                #mi[lhs] = ht.MolInfo( lhs, grpname, order=-1)
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                model.makeMol( reacname, grpname, order=-1 )

    for grpname, grp in jsonDict['Groups'].items():
        if "Species" in grp:
            for molname, conc in grp['Species'].items():
                model.makeMol( molname, grpname, order=0, concInit = conc )
                #mi[molname] = ht.MolInfo( molname, grpname, order=0, concInit = conc )
                grp['Species'][molname] = conc

    # Then assign indices to these unique molnames, and build up the
    # numpy arrays for concInit and conc.
    model.allocConc();

    # Now set up the reactions. we need the mols all defined first.
    for grpname, grp in jsonDict['Groups'].items():
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                subs = reac['subs']
                # Hideous hack to interface with model::makeReac, which
                # expects all args in reac to be floats.
                reac['subs'] = 0.0 
                model.makeReac( reacname, grpname, subs, reac )
                reac['subs'] = subs

    # Now set up the equation, again, we need the mols defined.
    for grpname, grp in jsonDict['Groups'].items():
        if "Eqns" in grp:
            for lhs, expr in grp["Eqns"].items():
                model.makeEqn( lhs, grpname, expr )
                #ei[lhs] = ht.EqnInfo( lhs, grpname, expr )

    model.allocConc()
    sortReacs( model )
    model.reinit()
    return model

def breakReacLoop( model, maxOrder, numLoopsBroken  ):
    for reacname, reac in model.reacInfo.items():
        if model.molInfo[reacname].order < 0:
            model.molInfo[reacname].order = maxOrder
            #print( "    FIX_Reac ORDER = ", reacname, " ", maxOrder)
            #print("Warning; Reaction order loop. Breaking {} loop for {}, assigning order: {}".format( numLoopsBroken, reacname, maxOrder ) )
            return

def breakEqnLoop( model, maxOrder, numLoopsBroken  ):
    for eqname, eqn in model.eqnInfo.items():
        if model.molInfo[eqname].order < 0:
            model.molInfo[eqname].order = maxOrder
            #print( "    FIX_Eqn ORDER = ", eqname, " ", maxOrder)
            return

def sortReacs( model ):
    # Go through and assign levels to the mols and reacs within a group.
    # This will be used later for deciding evaluation order.
    maxOrder = 0
    numLoopsBroken = 0
    numOrdered = 0
    numReac = len( model.reacInfo )
    while numOrdered < numReac: 
        numOrdered = 0
        stuck = True
        for reacname, reac in sorted( model.reacInfo.items() ):
            prevOrder = model.molInfo[reacname].order
            maxOrder = max( maxOrder, prevOrder )
            if prevOrder >= 0:
                numOrdered += 1
            else:
                order = [ model.molInfo[i].order for i in reac.subs ]
                if min( order ) >= 0:
                    mo = max( order ) + 1
                    model.molInfo[reacname].order = mo
                    maxOrder = max( maxOrder, mo )
                    numOrdered += 1
                    stuck = False
        #print ( "               numOrdered = ", numOrdered, " / ", numReac )
        if stuck:
            breakReacLoop( model, maxOrder+1, numLoopsBroken )
            numLoopsBroken += 1

    numEqn = len( model.eqnInfo )
    numOrdered = 0
    while numOrdered < numEqn: 
        numOrdered = 0
        stuck = True
        for eqname, eqn in sorted( model.eqnInfo.items() ):
            prevOrder = model.molInfo[eqname].order
            maxOrder = max( maxOrder, prevOrder )
            if prevOrder >= 0:
                numOrdered += 1
                continue
            order = [ model.molInfo[i].order for i in eqn.subs ]
            if min( order ) >= 0:
                mo = max( order ) + 1
                maxOrder = max( maxOrder, mo )
                model.molInfo[eqname].order = mo
                numOrdered += 1
                stuck = False
        if stuck:
            breakEqnloop( model, maxOrder+1, numLoopsBroken )
            numLoopsBroken += 1

    maxOrder += 1
    model.setReacSeqDepth( maxOrder )
    for name, reac in model.reacInfo.items():
        order = model.molInfo[name].order
        model.assignReacSeq( name, order )

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
        stimvec.append( Stim( i, model ) )
        stimvec.append( Stim( i, model, off = True ) )

    stimvec.sort( key = Stim.stimOrder )

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
