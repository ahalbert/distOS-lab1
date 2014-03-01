#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import re

while True:
	line = raw_input('--> ')
	r = re.split(r'\s+',line)
	print type(r)
	print r
