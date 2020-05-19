#!/bin/bash

( 
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' mongodb-org|grep "install ok installed")
	
	# If mongodb not installed
	if [ "" == "$PKG_OK" ]; then
	  SUDO_OK=$(dpkg-query -W --showformat='${Status}\n' sudo|grep "install ok installed")
	  if [ "" == "$SUDO_OK" ]; then
		  # Install sudo
		  apt-get update
		  apt-get install -y sudo
	  fi	
	  # Preparation for MongoDB installation 
	  sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
	  echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
	  sudo apt-get update
	  sudo apt-get install dirmngr gnupg apt-transport-https software-properties-common ca-certificates curl -y
	  curl -fsSL https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
	  sudo add-apt-repository 'deb https://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main'
	  sudo apt-get update	  
	  ## Install mongodb and its dependencies
	  sudo apt-get install mongodb-org -y --fix-missing
	fi
)