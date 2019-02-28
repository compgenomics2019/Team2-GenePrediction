#!/usr/bin/env python
import os, subprocess, argparse


parser = argparse.ArgumentParser(description='Running Prodigal')

parser.add_argument('-i', '--input_folder',  help='Directory containing input genomes files (.fasta)', type=str)
parser.add_argument('-f', '--output_format', help='Output Format (gff, gbk, sqn, sco)', default='gff', type=str, nargs='?')
parser.add_argument('-o', '--output', help='Output foler, default to ./output ', default='output', type=str, nargs='?')
parser.add_argument('-a', '--proteins', help='fna folder, default to ./proteins', default='proteins', type=str, nargs='?')
parser.add_argument('-d', '--nucleotides', help='fna folder, default to ./nucleotides ', default='nucleotides', type=str, nargs='?')
# parser.add_argument('-o', '--output', help='Output file name, default to “./output” if -o is provided with noadditionalstrings. If-oisnotprovided,writetoSTDOUT', const='./output', nargs='?', type=str)
# parser.add_argument('-t', '--threads', help='Number of theads/processes to run the analysis, defaults to 1', default=1, type=int, nargs='?')
# parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
# parser.add_argument('-f', '--force', help='Overwrite files if they exist. Do not overwrite by default', action='store_true')
args = parser.parse_args()

for file in os.listdir(args.input_folder):
	if os.path.isfile(os.path.join(args.input_folder, file)):
		input_file = os.path.join(args.input_folder, file)
		faa = os.path.join(args.input_folder, args.proteins, file.split('.')[0])
		#Create Protein Directory if it does not exists
		if not os.path.exists(os.path.join(args.input_folder, args.proteins)):
		    os.makedirs(os.path.join(args.input_folder, args.proteins))
		fna = os.path.join(args.input_folder, args.nucleotides, file.split('.')[0])
		#Create Nucelotide Directory if it does not exists
		if not os.path.exists(os.path.join(args.input_folder, args.nucleotides)):
		    os.makedirs(os.path.join(args.input_folder, args.nucleotides))
		output = os.path.join(args.input_folder, args.output, file.split('.')[0])
		#Create Output Directory if it does not exists
		if not os.path.exists(os.path.join(args.input_folder, args.output)):
		    os.makedirs(os.path.join(args.input_folder, args.output))
		subprocess.run(['prodigal', '-i', input_file, '-o', output, '-a', faa, '-f', args.output_format, '-d', fna])
		print ('Processing ' + input_file)