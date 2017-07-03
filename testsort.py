#!/usr/bin/env python
#
# Test for VideoSort post-processing script for NZBGet.
#
# Copyright (C) 2014-2017 Andrey Prygunkov <hugbug@users.sourceforge.net>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
from os.path import dirname
import os
import traceback
import re
import shutil
import subprocess
import json
import getopt

print('Test script for VideoSort')

root_dir = dirname(__file__)
test_dir = root_dir + '/__'
verbose = False
test_ids = []

options, _ = getopt.getopt(sys.argv[1:], 't:v', ['testid=', 'verbose'])
for opt, arg in options:
	if opt in ('-v', '--verbose'):
		verbose = True
	elif opt in ('-t', '--testid'):
		test_ids.append(arg)

def set_defaults():
	# NZBGet global options
	os.environ['NZBOP_SCRIPTDIR'] = 'test'

	# script options
	os.environ['NZBPO_MOVIESDIR'] = root_dir + '/movies'
	os.environ['NZBPO_SERIESDIR'] = root_dir + '/series'
	os.environ['NZBPO_DATEDDIR'] = root_dir + '/dated'
	os.environ['NZBPO_OTHERTVDIR'] = root_dir + '/tv'
	os.environ['NZBPO_VIDEOEXTENSIONS'] = '.mkv,.mp4,.avi'
	os.environ['NZBPO_SATELLITEEXTENSIONS'] = '.srt'
	os.environ['NZBPO_MULTIPLEEPISODES'] = 'list'
	os.environ['NZBPO_EPISODESEPARATOR'] = '-'
	os.environ['NZBPO_MINSIZE'] = '0'
	os.environ['NZBPO_TVCATEGORIES'] = 'tv'
	os.environ['NZBPO_MOVIESFORMAT'] = '%fn'
	os.environ['NZBPO_OTHERTVFORMAT'] = '%fn'
	os.environ['NZBPO_SERIESFORMAT'] = '%fn'
	os.environ['NZBPO_DATEDFORMAT'] = '%fn'
	os.environ['NZBPO_LOWERWORDS'] = 'the,of,and,at,vs,a,an,but,nor,for,on,so,yet'
	os.environ['NZBPO_UPPERWORDS'] = 'III,II,IV'
	os.environ['NZBPO_SERIESYEAR'] = 'yes'
	os.environ['NZBPO_OVERWRITE'] = 'no'
	os.environ['NZBPO_CLEANUP'] = 'no'
	os.environ['NZBPO_PREVIEW'] = 'yes'
	os.environ['NZBPO_VERBOSE'] = 'yes'

	# properties of nzb-file
	os.environ['NZBPP_DIRECTORY'] = test_dir
	os.environ['NZBPP_NZBNAME'] = 'test'
	os.environ['NZBPP_PARSTATUS'] = '2'
	os.environ['NZBPP_UNPACKSTATUS'] = '2'
	os.environ['NZBPP_CATEGORY'] = ''

	# pp-parameters of nzb-file, including DNZB-headers
	os.environ['NZBPR__DNZB_USENZBNAME'] = 'no'
	os.environ['NZBPR__DNZB_PROPERNAME'] = ''
	os.environ['NZBPR__DNZB_EPISODENAME'] = ''

def run_test(testobj):
	set_defaults()
	for prop_name in testobj:
		os.environ[str(prop_name)] = str(testobj[prop_name])
		if verbose:
			print('%s: %s' % (prop_name, os.environ[prop_name]))
	input_file = testobj['INPUTFILE']
	output_file = testobj['OUTPUTFILE']
	shutil.rmtree(test_dir, True)
	os.mkdir(test_dir)
	dir_name, file_name = os.path.split(input_file)
	if dir_name <> '':
		os.mkdir(test_dir + '/' + dir_name)
	full_file_name = test_dir + '/' + input_file
	out_file = open(full_file_name, 'w')
	out_file.write('empty file')
	out_file.close()

	if verbose:
		print('Executing...')
	sys.stdout.flush()
	proc = subprocess.Popen(['python', root_dir + '/VideoSort.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
	out, err = proc.communicate()
	out += err
	ret = proc.returncode
	if verbose:
		print('Return code: %i' % ret)
	success = False
	dest = ''

	if ret == 93:
		for line in out.split('\n'):
			if line.startswith('destination path: '):
				line = line[len('destination path: '):]
				if line.startswith(root_dir):
					line = line[len(root_dir):]
				dest = line.replace('\\', '/')
		success = dest == output_file and output_file <> ''

	if success:
		print('%s: SUCCESS' % testobj['id'])
	if not success:
		if verbose:
			print('********************************************************')
			print('*** FAILURE')
			print(out)
			print('*** FAILURE')
			print('id: %s' % testobj['id'])
			print('expected   : %s' % output_file)
			print('destination: %s' % dest)
			print('********************************************************')
			sys.exit(1)
		else:
			print('%s: FAILED' % testobj['id'])
			if output_file == '':
				print('destination: %s' % dest)
	elif verbose:
		print('expected   : %s' % output_file)
		print('destination: %s' % dest)

testdata = json.load(open(root_dir + '/testdata.json'))
for testobj in testdata:
	if test_ids == [] or testobj['id'] in test_ids:
		run_test(testobj)
