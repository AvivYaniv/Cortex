#!/bin/bash

( 
	PKG_1_OK=$(dpkg-query -W --showformat='${Status}\n' postgresql|grep "install ok installed")
	PKG_2_OK=$(dpkg-query -W --showformat='${Status}\n' postgresql-contrib|grep "install ok installed")
	
	# If postgresql not installed
	if [ "" == "$PKG_1_OK" ] || [ "" == "$PKG_2_OK" ]; then
	  # Install sudo
	  apt-get update
	  apt-get install -y sudo
	  ## Install postgresql and its dependencies
	  sudo apt-get install postgresql postgresql-contrib -y --fix-missing
	fi
)