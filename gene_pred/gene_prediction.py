#!/usr/bin/env python3

import sys
import os
import re
import subprocess
import argparse
from scripts.prodigal_script import prodigal
from scripts.genemarkS2 import genemarkS2
from scripts.RNAsearch import RNApredict

# creates the output directories for the output of prodigal
def createProdOutDirs():
	if not os.path.exists(os.getcwd()+"/output/"):
		os.makedirs(os.getcwd()+"/output")
	if not os.path.exists(os.getcwd()+"/output/out_prod/"):
		os.makedirs(os.getcwd()+"/output/out_prod")
	if not os.path.exists(os.getcwd()+"/output/out_prod/prot"):
		os.makedirs(os.getcwd()+"/output/out_prod/prot")
	if not os.path.exists(os.getcwd()+"/output/out_prod/nucl"):
		os.makedirs(os.getcwd()+"/output/out_prod/nucl")

# creates the op dirs for output of gene mark s2
def createGMOutDirs():
	if not os.path.exists(os.getcwd()+"/output/out_gms2/"):
		os.makedirs(os.getcwd()+"/output/out_gms2")
	if not os.path.exists(os.getcwd()+"/output/out_gms2/prot"):
		os.makedirs(os.getcwd()+"/output/out_gms2/prot")
	if not os.path.exists(os.getcwd()+"/output/out_gms2/nucl"):
		os.makedirs(os.getcwd()+"/output/out_gms2/nucl")

# get the intersection genes from prodigal output
def getProdIntGene(argDir):
	gm_out_dir = "./output/out_gms2/"
	prod_out_dir = "./output/out_prod/"
	for file in argDir:
		fName = file.split(".")[0] + ".gff"
		nFName = file.split(".")[0] + "_int1" + ".gff"
		oFName = file.split(".")[0] + "_int2" + ".gff"
		subprocess.run(['bedtools', 'intersect', '-f', '1.0', '-r', '-v', '-wa', '-a', prod_out_dir+fName, '-b', gm_out_dir+fName, '>', prod_out_dir+nFName])
		subprocess.run(['bedtools', 'intersect', '-f', '1.0', '-r', '-wa', '-a', prod_out_dir+fName, '-b', gm_out_dir+fName, '>', prod_out_dir+oFName])

# get intersection genes from genemark op
def getGMIntGene(argDir):
	gm_out_dir = "./output/out_gms2/"
	prod_out_dir = "./output/out_prod/"
	for file in argDir:
		fName = file.split(".")[0] + ".gff"
		nFName = file.split(".")[0] + "_int" + ".gff"
		subprocess.run(['bedtools', 'intersect', '-f', '1.0', '-r', '-v', '-wa', '-a', gm_out_dir+fName, '-b', prod_out_dir+fName, '>', gm_out_dir+nFName])

# gets the union of the genes from prodigal and gene mark
def mergeGFF(argDir):
	out_dir = "./output/"
	gm_out_dir = "./output/out_gms2/"
	prod_out_dir = "./output/out_prod/"
	for file in argDir:
		fName = out_dir + file.split(".")[0] + "_cds" + ".gff"
		fName1 = gm_out_dir + file.split(".")[0] + "_int" + ".gff"
		fName2 = prod_out_dir + file.split(".")[0] + "_int1" + ".gff"
		fName3 = prod_out_dir + file.split(".")[0] + "_int2" + ".gff"
		subprocess.run(['cat', fName1, fName2, fName3, '>', fName])

# merges the genes with the rna content generated
def mergeRNAGFF(argDir):
	out_dir = "./output/"
	out_dir_RNA = "./output/out_rna/"
	for file in argDir:
		fName = out_dir + file.split(".")[0] + "_final" + ".gff"
		fName1 = out_dir + file.split(".")[0] + "_cds" + ".gff"
		fName2 = out_dir_RNA + file.split(".")[0] + ".rna_merge" + ".gff"
		subprocess.run(['cat', fName1, fName2, '>', fName])

def main():
	parser = argparse.ArgumentParser(description='Gene Prediction tool')
	parser.add_argument('-i', '--input',  help='Directory containing input genomes files (.fasta)', type=str, required=True)
	parser.add_argument('-f', '--format', help='Output Format (gff, gbk, sqn, sco)', default='gff', type=str)
	parser.add_argument('-g', '--genemark', help='Optional arg for using genemark', action='store_true')
	args = parser.parse_args()
	# output dir for the rna results
	out_dir_RNA = "./output/out_rna/"
	# if gene mark need to be run on the contigs
	if args.genemark:
		createGMOutDirs()
		createProdOutDirs()
		gm_out_dir = "./output/out_gms2/"
		prod_out_dir = "./output/out_prod/"
		for file in os.listdir(args.input):
			if os.path.isfile(args.input + file):
				genemarkS2(args.input + file, gm_out_dir+file.split(".")[0], gm_out_dir+"nucl/"+file.split(".")[0], gm_out_dir+"prot/"+file.split(".")[0])
				prodigal(args.input + file, prod_out_dir+file.split(".")[0], prod_out_dir+"nucl/"+file.split(".")[0], prod_out_dir+"prot/"+file.split(".")[0])
		getProdIntGene(args.input)
		getGMIntGene(args.input)
		mergeGFF(args.input)
	else:
		createProdOutDirs()
		prod_out_dir = "./output/out_prod/"
		for file in os.listdir(args.input):
			if os.path.isfile(args.input + file):
				prodigal(args.input + file, prod_out_dir+file.split(".")[0], prod_out_dir+"nucl/"+file.split(".")[0], prod_out_dir+"prot/"+file.split(".")[0])
	RNApredict(args.input)
	mergeRNAGFF(args.input)

if __name__ == "__main__":
	main()