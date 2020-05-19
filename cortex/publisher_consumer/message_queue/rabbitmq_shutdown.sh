#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	# If on Travis, not priviledged to stop service
	if [[ $TRAVIS ]]; then
	    sudo rabbitmqctl stop
		sudo invoke-rc.d rabbitmq-server stop
	fi	
)
