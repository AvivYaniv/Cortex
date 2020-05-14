#!/bin/bash

{
	python -m pip install sphinx-autobuild
} &> /dev/null

DIR="$(pwd)"
PARENT="$(readlink -m "${DIR}")"
SOURCE="$(readlink -m $PARENT/docs/source)"
DOCS="$(readlink -m $PARENT/docs/build)"

sphinx-autobuild ${SOURCE} ${DOCS}
