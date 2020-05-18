#!/bin/bash

{
	sudo apt-get install dos2unix
} &> /dev/null

# Go up once to get to root folder
DIR="$(pwd)"
PARENT="$(readlink -m "${DIR}")"
cd ${PARENT}

# Convert all '*.sh' scripts to unix EOL format
find . -type f -name "*.sh" -exec dos2unix {} \+;
