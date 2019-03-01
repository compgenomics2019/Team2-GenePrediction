import sys
import os
import re
import subprocess

def generateGlimOP(argDir):
	contigFileNames = []
	for file in os.listdir(argDir):
		if os.path.isfile(argDir + file):
			contigFN = file.split(".")[0]
			subprocess.run(["glimmer3.02/scripts/g3-from-scratch.csh", argDir + file, contigFN])
			contigFileNames.append("temp/" + contigFN + ".predict")
	subprocess.run(["mkdir", "-p", "./temp/"])
	for file in contigFileNames:
		subprocess.run(["mv", file, "./temp/"])
	return contigFileNames

def convertToGFF(content):
	header = ""
	formatted_content = []
	for line in content:
		if line.startswith(">"):
			header = line[1:].rstrip()
			formatted_content.append(line.replace(">", "#"))
		else:
			line_format = line.split()
			if int(line_format[2]) < int(line_format[1]):
				formatted_content.append("{}\tGLIMMER\tgene\t{}\t{}\t{}\t{}\t{}\tID={}\n".format(header,line_format[2],line_format[1],line_format[4],line_format[3][0],line_format[3][1:],line_format[0]))
			else:
				formatted_content.append("{}\tGLIMMER\tgene\t{}\t{}\t{}\t{}\t{}\tID={}\n".format(header,line_format[1],line_format[2],line_format[4],line_format[3][0],line_format[3][1:],line_format[0]))
	return formatted_content

def readWriteFile(fileName):
	with open(fileName, 'r') as frh:
		pr_file_content = frh.readlines()
		new_content = convertToGFF(pr_file_content)
		writeFName = fileName.split(".")[0] + ".gff"
		with open(writeFName, 'w') as fwh:
			fwh.writelines(new_content)

def convertAllToGFF(contNames):
	for file in contNames:
		readWriteFile(file)

def main():
	argDir = sys.argv[1]
	glim_files = generateGlimOP(argDir)
	convertAllToGFF(glim_files)

main()