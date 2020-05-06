#!/usr/bin/python

""" Open ebuild with vi from equery list output. """

# Import
import sys
import subprocess
import re
import os.path

# Check number of arguments
if len(sys.argv) != 2:
    print("Error ", sys.argv[0], " needs 1 argument")
    sys.exit(-1)

# Store agument in variable
ebuild = sys.argv[1]

# Test if argument matches right format
regex = re.compile(r'[a-z]+\-[a-z]+\/[a-z0-9\-\.]+')
if not regex.match(ebuild):
    print("Error : argument format is incorrect")
    sys.exit(-2)

# Extract remove version from argument
# First : split argument with '-' as delimiter
category = ebuild.split('-')
# Second : remove that element (version here)
category.pop()
# Finally : join everything back together
clean_category = "-".join(category)

# Generate complete path
complete_path = "/usr/portage/"+clean_category+"/"+ebuild.split('/')[1]+".ebuild"

# If file exists, open it in VI
if os.path.isfile(complete_path):
    subprocess.call(['vi', complete_path])
else:
    print("Error : ebuild doesn't exist")
