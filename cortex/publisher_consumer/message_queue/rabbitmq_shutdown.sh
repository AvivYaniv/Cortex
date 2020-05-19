#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	# If not on Travis (where not priviledged to stop service)
	if [ -z "$TRAVIS" ]; then
		sudo rabbitmqctl stop
		sudo invoke-rc.d rabbitmq-server stop
	fi	
)
