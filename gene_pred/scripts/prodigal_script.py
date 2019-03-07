#!/usr/bin/env python3

import os, subprocess, argparse

def prodigal(fasta, gff_output, fna_output, faa_output):
	subprocess.run(['prodigal', '-i', fasta, '-o', gff_output+".gff", '-a', faa_output+".faa", '-f', 'gff', '-d', fna_output+".fna"])