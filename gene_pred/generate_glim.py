import sys
import os
import re
import subprocess

def generateGlimOP(argDir):
	lastFileIndex = 0
	for (dirpath, dirnames, filenames) in os.walk(argDir):
		if not filenames:
			print ('Empty directory!')
		for file in filenames:
			run = "run"+str(filenames.index(file))
			subprocess.run(["glimmer3.02/scripts/g3-from-scratch.csh", argDir+file, run])
			lastFileIndex = str(filenames.index(file))
	subprocess.run(["mkdir", "-p", "./temp/"])
	supbprocess.run(["mv", "run*", "./temp/"])
	return (lastFileIndex+1)

def convertToGFF(content):
	header = ""
	formatted_content = []
	for line in content:
		if line.startswith(">"):
			header = line.split("|")[2].split()[0]
			formatted_content.append(line.replace(">","#"))
		else:
			line_format = line.split()
			formatted_content.append("{}\tGLIMMER\tgene\t{}\t{}\t{}\t{}\t{}\tID={}\n".format(header,line_format[1],line_format[2],line_format[4],line_format[3][0],line_format[3][1:],line_format[0]))
	return formatted_content

def readWriteFile(fileName):
	with open(fileName, 'r') as frh:
		pr_file_content = frh.readlines()
		new_content = convertToGFF(pr_file_content)
		writeFName = fileName.split(".")[0] + ".gff"
		with open(writeFName, 'w') as fwh:
			fwh.writelines(new_content)

def convertAllToGFF(tempDir, contNum):
	for (dirpath, dirnames, filenames) in os.walk(tempDir):
		if not filenames:
			print ('Empty directory!')
		for fileNum in range(contNum):
			fileN = "{}run{}.predict".format(tempDir, fileNum)
			readWriteFile(fileN)

def main():
	argDir = sys.argv[1]
	num_files = generateGlimOP(argDir)
	convertAllToGFF("./temp/", num_files)

main()