# functions shared across multiple scripts

import sys
import gzip
import re
import os
import gffutils
import array as arr
from subprocess import Popen,PIPE

def create_job_script(name, outDir, queue, nCores, time, mem, command):
	outFile = open('job_%s.sh' % name , 'w')
	print("#!/bin/bash", file=outFile)
	print("#SBATCH -J "+ str(name), file=outFile)
	print("#SBATCH -o out." + str(name), file=outFile)
	print("#SBATCH -e err." + str(name), file=outFile)
	print("#SBATCH -p " + queue, file=outFile)
	print("#SBATCH -n " + str(nCores), file=outFile)
	print("#SBATCH -t " + str(time), file=outFile)
	print("#SBATCH --mem=" + str(mem), file=outFile)
	print(command, file=outFile)
	outFile.close()
	jobId = sbatch_submit(outFile.name)
	print(jobId)
	os.system("mv job_" + str(name) + ".sh " + outDir)
	return(jobId)

#Submit filename to slurm with sbatch, returns job id number
def sbatch_submit(filename):
	proc = Popen('sbatch %s'%filename,shell=True,stdout=PIPE,stderr=PIPE)
	stdout,stderr = proc.communicate()
	stdout = stdout.decode("utf-8","ignore")
	stdout = stdout.strip()
	stdout = stdout.strip('Submitted batch job ')
	return(stdout)

def create_job_script(name, outDir, queue, nCores, time, mem, command):
        outFile = open('job_%s.sh' % name , 'w')
        print("#!/bin/bash", file=outFile)
        print("#SBATCH -J "+ str(name), file=outFile)
        print("#SBATCH -o out." + str(name), file=outFile)
        print("#SBATCH -e err." + str(name), file=outFile)
        print("#SBATCH -p " + queue, file=outFile)
        print("#SBATCH -n " + str(nCores), file=outFile)
        print("#SBATCH -t " + str(time), file=outFile)
        print("#SBATCH --mem=" + str(mem), file=outFile)
        print(command, file=outFile)
        outFile.close()
        jobId = sbatch_submit(outFile.name)
        print(jobId)
        os.system("mv job_" + str(name) + ".sh " + outDir)
        return(jobId)

#Submit filename to slurm with sbatch, returns job id number
def sbatch_submit(filename):
        proc = Popen('sbatch %s'%filename,shell=True,stdout=PIPE,stderr=PIPE)
        stdout,stderr = proc.communicate()
        stdout = stdout.decode("utf-8","ignore")
        stdout = stdout.strip()
        stdout = stdout.strip('Submitted batch job ')
        return(stdout)

