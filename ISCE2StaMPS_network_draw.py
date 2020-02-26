#!/usr/bin/env python3
'''#!/usr/bin/env python'''

'''This is a script used to draw InSAR network in temp and perp bsln relative to 1st scene.

Parameters:	
		Add something here
Returns:	
'''

import numpy as np
import os, sys
import datetime
import argparse
from datetime import date
import matplotlib.pyplot as plt
from os.path import abspath as abspath
from os.path import join as join
from os.path import dirname as dirname
from os.path import abspath as abspath
appdir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, appdir)
from modules.geotools import DecimalYearComp as decyrcomp
'''import subprocess
import glob

from modules.basictools import LoggingGen'''

def cmdLineParse():
	'''
	Command Line Parser.
	'''
	parser = argparse.ArgumentParser(description='Generate InSAR network to choose master date.')
	parser.add_argument('-fs', '--fontsize', type=float, required=False, help='Font size of text of image in the map', dest='ftsz')
	parser.add_argument('-ms', '--markersize', type=float, required=False, help='Marker size of scatters of images in the map', dest='mksz')
	parser.add_argument('-ma', '--masterdate', type=str, required=False, help='Master date in string format as YYYYMMDD', dest='msdt')
	parser.add_argument('-o', '--outfile', type=str, required=False, help='Name of output file', dest='ofle')
	inputs = parser.parse_args()
	#if (not inputs.input):
	#	print('Error!!! No input list is provided.')
	#	sys.exit(0)    
    
	return inputs
	

def PSIFGnetGen(tims, rbperp, imgname=None, masteridx=None, plttit=None, xunit=None, yunit=None, imshow=True, fname=None, figdpi = 1000, ftsz=None, mksz=None):
	plt.clf()	
	if masteridx != None:	
		for imgidx in range(len(tims)):
			if imgidx != msid:
				plt.plot([tims[imgidx], tims[masteridx]], [rbperp[imgidx], rbperp[masteridx]], '-k')

	'''if mksz != None:
		plt.scatter(tims, rbperp, marker = 'o', c = 'red', s = mksz)
	else:
		plt.scatter(tims, rbperp, marker = 'o', c = 'red')'''

	plt.plot(tims, rbperp, 'ro')
	
	if imgname != None:
		if masteridx == None:
			for idx in range(len(imgname)):
				if ftsz != None:
					plt.text(tims[idx], rbperp[idx], imgname[idx], horizontalalignment='center', verticalalignment='bottom', fontsize=ftsz)
				else:
					plt.text(tims[idx], rbperp[idx], imgname[idx], horizontalalignment='center', verticalalignment='bottom')
			if ftsz != None:
				plt.text(tims[masteridx], rbperp[masteridx], imgname[masteridx], horizontalalignment='center', verticalalignment='bottom', fontsize=ftsz)
		'''else:
			plt.text(tims[masteridx], rbperp[masteridx], imgname[masteridx], horizontalalignment='center', verticalalignment='bottom', color='blue')'''

	trange = max(tims) - min(tims)
	rrange = max(rbperp) - min(rbperp)
	plt.axis([min(tims) - trange/10, max(tims) + trange/10, min(rbperp) - rrange/10, max(rbperp) + rrange/10])

	if plttit == None:
		plt.title('InSAR network')
	else:
		plt.title(plttit)

	if xunit == None:
		#plt.xlabel('Time [year]')
		plt.xlabel('Temporal Baseline [year]', fontsize = 14, color = 'r')
	else:
		#plt.xlabel('Time [' + xunit + ']', fontsize = 14, color = 'r')
		plt.xlabel('Temporal Baseline [' + xunit + ']', fontsize = 14, color = 'r')
	
	if yunit == None:
		#plt.ylabel('Perpendicular Baseline [m]')		
		plt.ylabel('Perpendicular Baseline [m]', fontsize = 14, color = 'b')
	else:
		plt.ylabel('Perpendicular Baseline [' + yunit + ']', fontsize = 14, color = 'b')
		
		
	plt.grid()
	plt.draw()
	
	#IFGnetplotfile1 = 'step_2_IFG_Net_1.png'
	
	'''if verbose == 'True':
		print('\r\n\tMake an IFG network plot 1:')
		print('\t\tIFG network plot 1 will be save to file: ' + repr(IFGnetplotfile1))'''

	'''logger.info('\tMake an IFG network plot 1:')
	logger.info('\t\tIFG network plot 1 will be save to file: ' + repr(IFGnetplotfile1))'''

	if fname !=None:
		#plt.savefig(IFGnetplotfile1, dpi = 100)
		plt.savefig(fname, dpi = figdpi)
		
	if imshow == True:		
		plt.show()
		
		
def tempbperpread(ifile):
	
	mimg = (os.path.split(ifile)[1]).split('_')[0]						# master image in yyyymmdd format
	simg = ((os.path.split(ifile)[1]).split('_')[1]).split('.')[0]		# slave  image in yyyymmdd format
		
	mdate = date(int(mimg[:4]), int(mimg[4:6]), int(mimg[6:8]))			# master date in datetime format
	sdate = date(int(simg[:4]), int(simg[4:6]), int(simg[6:8]))			# slave  date in datetime format
	
	rfile = open(ifile, "r")	
	cnt = rfile.readlines()	
	rfile.close()
	
	bperp = []	
	bpar  = []
	for line in cnt:
		if line.split()[0] == 'Bperp':
			bperp.append(float(line.split()[-1]))
			
		if line.split()[0] == 'Bpar':
			bpar.append(float(line.split()[-1]))
			
	return mimg, simg, mdate, sdate, bperp, bpar


		

if __name__ == '__main__':

	sttm = datetime.datetime.now()		# Luyen cmt: start time running for all prog.

	print
	print ('##########################################################################################################################')
	print ('#                                                                                                                        #')
	print ('#             This is the app. used to run draw InSAR network in temp and perp bsln relative to 1st scene                #')
	print ('#                                     (Script used: ISCE2StaMPS_bsln_draw.py)                                            #')
	print ('#                                                                                                                        #')
	print ('#                            This is carried out after running steps by ISCE2StaMPS_run_steps                            #')
	print ('#                                                                                                                        #')
	print ('##########################################################################################################################')

	'''#######################
	##### CREATE A LOG FILE
	logfile = 'ISCE2StaMPS_run_steps_log.txt'
	if os.path.isfile(logfile):
	print ('\r\nThe logging file: ' + logfile + ' is already existent. Please delete or change its name.\r\n')
	sys.exit()
	#logger = LoggingGen(logfile)'''

	'''logger.info ('##########################################################################################################################')
	logger.info ('#                                                                                                                        #')
	logger.info ('#         This is the app. used to run steps listed in directory "run_files" in order to adapt ISCE to StaMPS            #')
	logger.info ('#                                     (Script used: ISCE2StaMPS_run_steps.py)                                            #')
	logger.info ('#                                                                                                                        #')
	logger.info ('##########################################################################################################################')'''

	inputs  = cmdLineParse()
	ftsz = inputs.ftsz
	mksz = inputs.mksz
	msdt = inputs.msdt
	msdt = "20180111"
	if inputs.ofle != None:
		imgfile = inputs.ofle
	else:
		imgfile = 'IFGNet.png'
	
	crdir = os.getcwd()		# Current dir
	bsdir = 'baselines'		# The dir of which "run_files" dir is included

	print ('\r\nTemporal and perpendicular baselines will be identified from subdirectories located in: ' + repr(join(crdir, bsdir)))
	#logger.info ('Steps being run is listed in the directory ' + repr(rfdir))

	subdirlst = [item for item in os.listdir(join(crdir, bsdir)) if os.path.isdir(join(crdir, bsdir, item))]	# List of subdirs included in 'baselines' directory
	
	imgs   = []
	rbtemp = []
	rbperp = []
	
	for count, idir in enumerate(subdirlst):
		print ('\r\nSubdirectory #: ' + str(count + 1).zfill(len(str(len(subdirlst)))) + ' / ' + str(len(subdirlst)) + ': ' + abspath(join(crdir, bsdir, idir)))				
		print ('\tIdentify temporal and perpendicular baselines from file: ' + abspath(join(crdir, bsdir, idir, idir + '.txt')))
		
		
		mimg, simg, mdate, sdate, bperp, _ = tempbperpread(abspath(join(crdir, bsdir, idir, idir + '.txt')))		
		
		print ('\r\n\tMaster image in yyyymmdd format: ', mimg)
		print (    '\tSlave  image in yyyymmdd format: ', simg)
		
		print ('\r\n\tMaster image in datetime format: ', mdate)
		print (    '\tSlave  image in datetime format: ', sdate)		
		
		if count == 0:
			imgs.append(mimg)
			rbtemp.append(0)
			rbperp.append(0)
			
		imgs.append(simg)
		rbperp.append(np.mean(bperp))
		rbtemp.append((sdate - mdate).days)
		
		print ('\r\n\tMaster-Slave temp baseline [days]: ', rbtemp[-1])
		print (    '\tMaster-Slave perp baseline    [m]: ', rbperp[-1])

	if msdt != None and msdt in imgs:
		msid = imgs.index(msdt)
		rbperp = [elm - rbperp[msid] for elm in rbperp]
		rbtemp = [decyrcomp(int(elm[0:4]), int(elm[4:6]), int(elm[6:8])) for elm in imgs]		
	elif msdt != None and msdt not in imgs:
		print ('Input master date is nonexistent. Check it !')
		sys.exit()
	
	if msdt != None:
		PSIFGnetGen(rbtemp, rbperp, imgname=imgs, masteridx=msid, plttit=None, xunit='years', yunit='m', imshow=True, fname=imgfile, figdpi = 1000, ftsz = ftsz, mksz = mksz)
	else:
		PSIFGnetGen(rbtemp, rbperp, imgs, masteridx=None, plttit=None, xunit='days', yunit='meters', imshow=True, fname=imgfile, figdpi = 1000, ftsz = ftsz, mksz = mksz)		
	#IFGnetGen(tims, rbperp, imgname=None, plttit=None, xunit=None, yunit=None, imshow=True, fname=None, figdpi = 1000):	
	
	print ('\r\nInSAR network has been generated and saved in: ' + abspath(imgfile))
	
	fntm = datetime.datetime.now()		# Luyen cmt: finish time running for all prog.
	
	print ('\r\n==========================================================================================================================')
	print ('--------------------------------------------------------------------------------------------------------------------------')
	print ('Prog. started at  : ' + str(sttm))
	print ('Prog. finished at : ' + str(fntm))
	print ('total running time: ' + str(fntm - sttm))
	print ('Program finished !')
	print ('--------------------------------------------------------------------------------------------------------------------------')
	print ('==========================================================================================================================')
