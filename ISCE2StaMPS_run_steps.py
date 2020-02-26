#!/usr/bin/env python3
'''#!/usr/bin/env python'''

'''This is a script used to run steps listed in directory "run_files" in order to adapt ISCE to StaMPS.

Parameters:
		Input parameters
Returns:
		Output results: multi outputs
'''

import os, sys
import datetime
import subprocess
import glob

appdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
##sys.path.append(appdir)
sys.path.insert(0, appdir)

from modules.basictools import LoggingGen


sttm = datetime.datetime.now()		# Luyen cmt: start time running for all prog.

print
print ('##########################################################################################################################')
print ('#                                                                                                                        #')
print ('#         This is the app. used to run steps listed in directory "run_files" in order to adapt ISCE to StaMPS            #')
print ('#                                     (Script used: ISCE2StaMPS_run_steps.py)                                            #')
print ('#                                                                                                                        #')
print ('##########################################################################################################################')

#######################
##### CREATE A LOG FILE
logfile = 'ISCE2StaMPS_run_steps_log.txt'
'''if os.path.isfile(logfile):
	print ('\r\nThe logging file: ' + logfile + ' is already existent. Please delete or change its name.\r\n')
	sys.exit()'''

logger = LoggingGen(logfile)

logger.info ('##########################################################################################################################')
logger.info ('#                                                                                                                        #')
logger.info ('#         This is the app. used to run steps listed in directory "run_files" in order to adapt ISCE to StaMPS            #')
logger.info ('#                                     (Script used: ISCE2StaMPS_run_steps.py)                                            #')
logger.info ('#                                                                                                                        #')
logger.info ('##########################################################################################################################')

crdir = os.getcwd()		# Current dir
rfdir = 'run_files'		# The dir of which "run_files" dir is included
rflog = 'run_files_reports'	# The dir of which log/reports of "run_files" line-by-line are included
if os.path.isdir(rflog):
	cmd = 'rm -r ' + rflog
	subprocess.call(cmd, shell=True)
cmd = "mkdir " + rflog
subprocess.call(cmd, shell=True)

print ('\r\nSteps being run is listed in the directory ' + repr(rfdir))
logger.info ('Steps being run is listed in the directory ' + repr(rfdir))

rffle = [file for file in glob.glob(rfdir + '/' + "run_*")]		# List all files included in 'run_files' dir
rffle = [os.path.split(f)[1] for f in rffle]				# Split to keep just file names only (i.e., remove its directory ('run_files'))
rffle.sort(key=lambda f: int("".join(filter(str.isdigit, f[4:6]))))	# Sort list of run files so that it will be: [run_1_...; run_2_..., ..., run_10_...]

print ('\r\nNumber of run files: ' + str(len(rffle)))
logger.info ('Number of run files: ' + str(len(rffle)))

for ii, file in enumerate(rffle):
	print ('\r\nRun commands listed in run file number: ' + str(ii + 1).zfill(len(str(len(rffle)))) + ' / ' + str(len(rffle)) + '\t: ' + file)
	logger.info ('Run commands listed in run file number: ' + str(ii + 1).zfill(len(str(len(rffle)))) + ' / ' + str(len(rffle)) + '\t: ' + file)
	
	rfile = open(os.path.join(rfdir, file), "r")	
	cnt = rfile.readlines()
	rfile.close()
		
	for jj, line in enumerate(cnt):
		print ('\tCall command from line number: ' + str(jj + 1).zfill(len(str(len(cnt)))) + ' / ' + str(len(cnt)) + '\t: ' + str(line).rstrip("\n\r"))
		logger.info ('\tCall command from line number: ' + str(jj + 1).zfill(len(str(len(cnt)))) + ' / ' + str(len(cnt)) + '\t: ' + str(line).rstrip("\n\r"))		

		if ii+1 < 10:
			cmd = line.rstrip("\n\r") + ' >> ' + rflog + '/' + file + '_line_' + str(jj + 1).zfill(len(str(len(cnt)))) + '_' + str(len(cnt)) + '.txt'
		else:
			cmd = line.rstrip("\n\r") + ' >> ' + rflog + '/' + file + '_line_' + str(jj + 1).zfill(len(str(len(cnt)))) + '_' + str(len(cnt)) + '.txt'
		
		subprocess.call(cmd, shell=True)

print ('\r\nLogging/Report files of the above steps are saved in: ' + repr(rflog) + ' that should be carefully read to check if any error issued.')
logger.info ('Logging/Report files of the above steps are saved in: ' + repr(rflog) + ' that should be carefully read to check if any error issued.')
		
print ("\r\nCreate 'input_file' used for running in the next step: 'make_single_master_stack_isce'")
logger.info ("Create 'input_file' used for running in the next step: 'make_single_master_stack_isce'")
stkpth = os.path.abspath('merged/SLC')
stkmst = 'UNKNOWN'
geopth = os.path.abspath('merged/geom_master')
bslpth = os.path.abspath('merged/baselines')
rglook = 40
azlook = 10
asrtio = 4
lmbda  = 0.056
slcsuf = '.full'
geosuf = '.full'

ofile = 'input_file'
print ('\tslc_stack_path         : ' + stkpth)
print ('\tslc_stack_master       : ' + stkmst)
print ('\tslc_stack_geom_path    : ' + geopth)
print ('\tslc_stack_baseline_path: ' + bslpth)
print ('\trange_looks            : ' + str(rglook))
print ('\tazimuth_looks          : ' + str(azlook))
print ('\tlambda                 : ' + str(lmbda))
print ('\tslc_suffix             : ' + slcsuf)
print ('\tgeo_suffix             : ' + geosuf)

logger.info ('\tslc_stack_path         : ' + stkpth)
logger.info ('\tslc_stack_master       : ' + stkmst)
logger.info ('\tslc_stack_geom_path    : ' + geopth)
logger.info ('\tslc_stack_baseline_path: ' + bslpth)
logger.info ('\trange_looks            : ' + str(rglook))
logger.info ('\tazimuth_looks          : ' + str(azlook))
logger.info ('\tlambda                 : ' + str(lmbda))
logger.info ('\tslc_suffix             : ' + slcsuf)
logger.info ('\tgeo_suffix             : ' + geosuf)

outputFile = open(ofile,'w')
outputFile.write('source_data\t\tslc_stack\n')
outputFile.write('slc_stack_path\t\t%s\n' % stkpth)
outputFile.write('slc_stack_master\t%s\n' % stkmst)
outputFile.write('slc_stack_geom_path\t%s\n' % geopth)
outputFile.write('slc_stack_baseline_path\t%s\n\n' % bslpth)
outputFile.write('range_looks\t\t%i\n' % rglook)
outputFile.write('azimuth_looks\t\t%i\n' % azlook)
outputFile.write('aspect_ratio\t\t%i\n\n' % asrtio)
outputFile.write('lambda\t\t\t%.3f\n' % lmbda)
outputFile.write('slc_suffix\t\t%s\n' % slcsuf)
outputFile.write('geom_suffix\t\t%s\n' % geosuf)
outputFile.close()
		
fntm = datetime.datetime.now()		# Luyen cmt: finish time running for all prog.

logger.info('==============================================')
logger.info('----------------------------------------------')
logger.info('Prog. started at  : ' + str(sttm))
logger.info('Prog. finished at : ' + str(fntm))
logger.info('total running time: ' + str(fntm - sttm))
logger.info('Program finished !')
logger.info('----------------------------------------------')
logger.info('==============================================')

print ('\r\n==========================================================================================================================')
print ('--------------------------------------------------------------------------------------------------------------------------')
print ('Prog. started at  : ' + str(sttm))
print ('Prog. finished at : ' + str(fntm))
print ('total running time: ' + str(fntm - sttm))
print ('Program finished !')
print ('--------------------------------------------------------------------------------------------------------------------------')
print ('==========================================================================================================================')
