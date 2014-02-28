import sys
import re

while True:
	line = raw_input('--> ')
	r = re.split(r'\s+',line)
	print type(r)
	print r
