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
 * File:            conv_to_sbml.py
 * Description:
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/

/**********************************************************************
** This program uses MOOSE to convert model definitions from .g to sbml.
**           copyright (C) 2020 Upinder S. Bhalla. and NCBS
**********************************************************************/
'''
from __future__ import print_function
import sys
import os
import json
import numpy as np
import moose

def conv( fname ):
    kfile = "./KKIT_MODELS/" + fname + ".g"
    modelId = moose.loadModel( "./KKIT_MODELS/" + fname + ".g", 'model', 'none' )[0]
    sfile = "./SBML_MODELS/" + fname + ".xml"
    moose.mooseWriteSBML( '/model', sfile )
    moose.delete( modelId )


def main():
    fnames = os.listdir( "./KKIT_MODELS" )
    for f in fnames:
        if f[-2:] == ".g":
            print( f[:-2] )
            conv( f[:-2] )

if __name__ == '__main__':
    main()







