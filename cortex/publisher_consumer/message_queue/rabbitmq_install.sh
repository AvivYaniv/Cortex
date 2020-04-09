#!/bin/bash

( 
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' rabbitmq-server|grep "install ok installed")
	
	# If rabbitmq-server not installed
	if [ "" == "$PKG_OK" ]; then
	  # Install sudo
	  apt-get update
	  apt-get install -y sudo
	  ## Install rabbitmq-server and its dependencies
	  sudo apt-get install rabbitmq-server -y --fix-missing
	fi
)