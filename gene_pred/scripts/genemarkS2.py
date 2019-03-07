#!/usr/bin/env python3

import os
import sys
import subprocess

def genemarkS2(fasta, gff_output, fna_output, faa_output):
    type = 'bacteria'
    format = '--format gff --fnn ' + fna_output + '.fna ' + '--faa' + faa_output + '.faa'
    subprocess.call(['gms2.pl', '--seq', fasta, '--genome-type', type, '--output', gff_output + '.gff', format])