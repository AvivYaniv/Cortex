#!/bin/bash

( 
	# Install sudo
	apt-get update
	apt-get install -y sudo
	
	## Install rabbitmq-server and its dependencies
	sudo apt-get install rabbitmq-server -y --fix-missing
)