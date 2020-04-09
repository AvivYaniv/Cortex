#!/bin/bash

( 
	PKG_1_OK=$(dpkg-query -W --showformat='${Status}\n' postgresql|grep "install ok installed")
	
	# If postgresql not installed
	if [ "" == "$PKG_1_OK" ]; then
	  # Install sudo
	  apt-get update
	  apt-get install -y sudo
	  ## Install rabbitmq-server and its dependencies
	  sudo apt-get install postgresql -y --fix-missing
	fi
	
	PKG_2_OK=$(dpkg-query -W --showformat='${Status}\n' postgresql-contrib|grep "install ok installed")
	
	# If postgresql-contrib not installed
	if [ "" == "$PKG_2_OK" ]; then
	  # Install sudo
	  apt-get update
	  apt-get install -y sudo
	  ## Install rabbitmq-server and its dependencies
	  sudo apt-get install postgresql-contrib -y --fix-missing
	fi
)