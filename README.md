# Team2-GenePrediction
Developed By: Sachin Kumar, Mansi Gupta, Vineeth Aljapur, Manu Tej Sharma Arrojwala, Mingming Cao

## Overview
This pipeline of gene prediction is part of outbreak detection project of Computational Genomics course. The goal of this pipeline is identify the coding regions of DNA. To do this we tried to quantitatively evaluate state of the art tools for our purpose and come up with a pipeline which gives out the best results according to our analysis.

This pipeline includes tools like Prodigal, GeneMarkS2 for identifying genes and tools like Aragon, Infernal and RNAmmer for identifying non-coding regions of RNA. You can find further information on the tools from the links provided below.

## Requirements
We recommend installing these dependencies from the links provided. 
[Python3](https://www.python.org/downloads/release/python-372/) To get python3 \
[GeneValidator](https://genevalidator.wurmlab.com/) To validate the results \
[Prodigal](https://github.com/hyattpd/Prodigal) To predict the genes \
[GeneMark-S2](http://exon.gatech.edu/GeneMark/license_download.cgi) To predict the genes \
[Glimmer](https://ccb.jhu.edu/software/glimmer/) To predict the genes \
[Blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) To validate the results\

**RNA**

We recommend using [``conda``](https://conda.io/en/latest/) to install latest version of  python and other python modules.



## QuickStart
1. ``chmod 755 gene_prediction.py``
2. ``gene_prediction.py -h``
