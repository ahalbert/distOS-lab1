#!/bin/bash
tmp="tmp.py"
www="python_head"
for file in `ls *py`; do
	base_file=`basename $file`
	echo $base_file
	cat $www > $tmp
	cat $base_file >> $tmp
	cat $tmp > $base_file
done
rm $tmp
