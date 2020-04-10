#!/bin/bash

( 
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' mongodb|grep "install ok installed")
	
	# If mongodb not installed
	if [ "" == "$PKG_OK" ]; then
	  # Install sudo
	  apt-get update
	  apt-get install -y sudo
	  ## Install mongodb and its dependencies
	  sudo apt-get install mongodb -y --fix-missing
	fi
)