'''
Mar 31 
sub->prd is connected with double arrow,
ligand with single arrow, 
inhibit with tee and 
modifier with diamond
legends is added
constant is added 

Apr 7:
group is added

Apr 8:
eqns added with pluse and sigma 

May4:
HillTau API is called for reading json file
'''

import json
from subprocess import call
import pygraphviz
import re
import matplotlib
import random
import numpy as np
import collections #import defaultdict

import sys,os
sys.path.insert(1, '../../PythonCode/')
from hillTau import *


matplotcolors = ["aqua","aquamarine","blue","blueviolet","brown","burlywood","cadetblue","chartreuse","chocolate","cornflowerblue","crimson","darkblue","darkcyan","darkgoldenrod","darkgray","darkgreen","darkmagenta","darkolivegreen","darkorange","darkorchid","darkred","darksalmon","darkseagreen","darkslateblue","darkslategrey","darkturquoise","deeppink","deepskyblue","dimgrey","dodgerblue","firebrick","forestgreen","gold","goldenrod","green","indianred","indigo","lightgreen","lightsalmon","lightseagreen","lightskyblue","lime","limegreen","magenta","maroon","mediumturquoise","mediumvioletred","midnightblue","olive","orange","orangered","orchid","rebeccapurple","red","rosybrown","royalblue","saddlebrown","salmon","seagreen","sienna","slateblue","teal","turquoise"]

def getRandColor():
	k = random.choice(matplotcolors)
	if k in ["white","wheat","whitesmoke","mintcream","oldlace"]:
		return getRandColor()
	else:
		return k

def getRandcolorX(reaction_color_list):
	reaction_color = random.choice(matplotcolors)
	if reaction_color not in reaction_color_list:
		reaction_color_list.append(reaction_color)
		return reaction_color
	else:
		return getRandcolorX(reaction_color_list)


def countX(lst, x):
	return lst.count(x)

def unique(list1):
	x = np.array(list1)
	return np.unique(x)

def checkdigit(startstringdigit,sp):
	if sp.startswith(tuple('0123456789')):
		startstringdigit[sp] = "s"+sp
		
def checkdigitEqu(statstringdigit,sp):
	if sp in startstringdigit:
		sp = startstringdigit[sp]
	return(sp)


def jsontoPng(modelpath, outputfile):
	group_no = 0;
	groupmap = dict()
	global startstringdigit
	startstringdigit= {}
	lig_exist = False
	kmod_exist = False
	inhibit_exist = False
	s = ""

	f_graph = open(outputfile+".dot", "w")
	f_graph.write("digraph mygraph {\n\trank=TB;\n")
	f_graph.write("node [shape=box; penwidth=2];")
	
	specielist = writeSpecies(modelpath,groupmap,f_graph)
	funclist = writeFunc(modelpath,groupmap,f_graph)
	edgelist,node_color,lig_exist,kmod_exist,inhibit_exist = writeReac(modelpath,groupmap,f_graph)
	

	for grp,items in groupmap.items():
		color = getRandColor()
		s = s + "\nsubgraph cluster_"+str(group_no)+"i\n{"
		s = s+"\nsubgraph cluster_"+str(group_no)+"\n{"+"\n"+"label=\""+grp+"\";\npenwidth=4;\ncolor=\""+color+"\";\n"
		sps = ""
		items = list(unique(items))
		for sp in items:
			if items.index(sp) != 0:
				sps = sps+','+sp
			else:
				sps = sps+sp
		s = s+sps+"\n} style=invisible\n}"
		group_no += 1;
	
	f_graph.write(s)
	f_graph.write(edgelist)
	f_graph.write(funclist)
	for k,v in node_color.items():
		f_graph.write("\n"+k+"[color=\""+v+"\"]")
	for p,q in startstringdigit.items():
		f_graph.write("\n"+q+"[label=\""+p+"\"]")	
	
	f_graph.write("\nnode [shape=plaintext]\nsubgraph cluster_01 {\n\tlabel = \"Legend\";\n\t{ rank=sink;\n\tkey [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\n\t<tr><td align=\"right\" port=\"i1\">Input</td></tr>\n")
	if lig_exist:
		f_graph.write("\t<tr><td align=\"right\" port=\"i2\">ligand</td></tr>\n")
	if kmod_exist:
		f_graph.write("\t<tr><td align=\"right\" port=\"i3\">Modifier</td></tr>\n")
	if inhibit_exist:
		f_graph.write("\t<tr><td align=\"right\" port=\"i4\">inhibit</td></tr>\n")
	f_graph.write("\t</table>>]\n\tkey2 [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\n\t<tr><td port=\"i1\">&nbsp;</td></tr>\n")
	if lig_exist:
		f_graph.write("\t<tr><td port=\"i2\">&nbsp;</td></tr>\n")
	if kmod_exist:
		f_graph.write("\t<tr><td port=\"i3\">&nbsp;</td></tr>\n")
	if inhibit_exist:
		f_graph.write("\t<tr><td port=\"i4\">&nbsp;</td></tr>\n")
	f_graph.write("\t</table>>]\n\tkey:i1:e -> key2:i1:w [arrowhead=normal color=\"black:white:black\"]\n")
	if lig_exist:
		f_graph.write("\tkey:i2:e -> key2:i2:w [arrowhead=onormal]\n")
	if kmod_exist:
		f_graph.write("\tkey:i3:e -> key2:i3:w [arrowhead=odiamond]\n")
	if inhibit_exist:
		f_graph.write("\tkey:i4:e -> key2:i4:w [arrowhead=tee]\n")

	f_graph.write("\t}\n\t}\n}")
	f_graph.close()
	
	command = "dot -Tpng "+ outputfile+".dot -o "+outputfile+".png"
	call([command], shell=True)

def writeSpecies(modelpath, groupmap,f_graph):
	# getting all the species
	specieslist = ""
	for molname, mol in sorted( modelpath.molInfo.items() ):
		checkdigit(startstringdigit,molname)
		molname = checkdigitEqu(startstringdigit,molname)
		if mol.grp in groupmap:
			groupmap[mol.grp].append(molname)
		else:
			groupmap[mol.grp] = [molname]
	return specieslist
		
def writeFunc(modelpath,groupmap,f_graph):
	equation_pluse = 0
	equation_sigma = 0
	edgelist = ""
	constants_list = []
	for e,t in modelpath.eqnInfo.items():
		checkdigit(startstringdigit,t.name)
		t.name = checkdigitEqu(startstringdigit,t.name)
		allpluse = True
		mathSym = []
		for i in t.eqnStr:
			if i in ["*","-","/","+"]:
				mathSym.append(i)
		if len(unique(mathSym)) == 1 and mathSym[0] == "+":
			allpluse = True
		else:
			allpluse = False
		if allpluse:
			plusesize = "pluse"+str(equation_pluse)
			equation_pluse+=1
			edgelist = edgelist+"\n"+plusesize+"[label=\"+\",shape=circle]"
			groupmap[t.grp].append(plusesize)
		else:
			plusesize = "sigma"+str(equation_sigma)
			equation_sigma+=1
			edgelist = edgelist+"\n"+plusesize+"[label=<&Sigma;>,shape=circle]"
			groupmap[t.grp].append(plusesize)
		for tsubs in unique(t.subs):
			c = countX(t.subs,tsubs)
			edgelist = edgelist+"\n"+tsubs+"->"+plusesize+"[arrowhead=onormal"
			if c > 1:
				edgelist = edgelist+ " label="+str(c)
			edgelist = edgelist+"]"
		edgelist = edgelist+"\n"+plusesize+"->"+t.name+"[arrowhead=onormal]"
	return edgelist

def writeReac(modelpath,groupmap,f_graph):
	edgelist = ""
	node_color = {}
	reaction_color_list =[]
	lig_exist = False
	kmod_exist = False
	inhibit_exist = False
	for reacname, reac in sorted( modelpath.reacInfo.items() ):
		checkdigit(startstringdigit,reacname)
		reacname = checkdigitEqu(startstringdigit,reacname)
		if reac.grp in groupmap:
			groupmap[reac.grp].append(reacname)
		else:
			groupmap[reac.grp] = [reacname]
		sublist = reac.subs
		sublistU = unique(reac.subs)
		prd = reacname
		reaction_color = getRandcolorX(reaction_color_list)
		for sub in sublistU:
			if sub in node_color:
				reaction_color = node_color[sub]
			checkdigit(startstringdigit,sub)

			if reac.inhibit == 1.0 and sublist.index(sub) == 1:
				c = countX(sublist,sub)
				sub = checkdigitEqu(startstringdigit,sub)
				inhibit_exist = True
				if c >1:
					edgelist = edgelist+"\n"+sub+"->"+prd+"[arrowhead=tee color="+reaction_color+" label="+str(c)+"]"
				else:
					edgelist = edgelist+"\n"+sub+"->"+prd+"[arrowhead=tee color="+reaction_color+"]"
			elif reac.Kmod != 1.0 and sublist.index(sub) == 1:
				sub = checkdigitEqu(startstringdigit,sub)
				edgelist = edgelist+"\n"+sub+"->"+prd+"[arrowhead=odiamond color="+reaction_color+"]"
				kmod_exist = True
			else:
				if sublist.index(sub) >= 1:
					c = countX(sublist,sub)
					lig_exist = True
					sub = checkdigitEqu(startstringdigit,sub)
					if c >1:
						edgelist = edgelist+"\n"+sub+"->"+prd+"[arrowhead=onormal color="+reaction_color+" label="+str(c)+"]"
					else:
						edgelist = edgelist+"\n"+sub+"->"+prd+"[arrowhead=onormal color="+reaction_color+"]"				
				else:
					if  sublist.index(sub) == 0:
						sub = checkdigitEqu(startstringdigit,sub)
						edgelist = edgelist +"\n"+sub+"->"+prd+"[arrowhead=normal color=\""+reaction_color+":white:"+reaction_color+"\"]"
				node_color[prd] = reaction_color
	return(edgelist,node_color,kmod_exist,lig_exist,inhibit_exist)


if __name__ == "__main__":

	parser = argparse.ArgumentParser( description = 'This file convert json file to dot which is further converted to png\n')
	parser.add_argument( 'model', type = str, help='Required: filename of model, in JSON format.')
	parser.add_argument( '-o', '--output', type = str, help='Optional: writes out the png model into named file. default takes json filename')
	args = parser.parse_args()

	if args.output != None:
		dirpath = os.path.basename(args.output)
		if not dirpath:
			outputfile = dirpath+"/"+os.path.splitext(args.output)[0]
		else:
			outputfile = os.path.splitext(args.output)[0]
	else:
		dirpath = os.path.basename(args.model)
		if not dirpath:
			outputfile = dirpath+"/"+os.path.splitext(args.model)[0]
		else:
			outputfile = os.path.splitext(args.model)[0]
		
	jsonDict = loadHillTau( args.model )
	modelpath = parseModel( jsonDict )
	jsontoPng(modelpath, outputfile)
