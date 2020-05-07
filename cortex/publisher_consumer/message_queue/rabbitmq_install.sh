#!/bin/bash

( 
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' rabbitmq-server|grep "install ok installed")
	
	# If rabbitmq-server not installed
	if [ "" == "$PKG_OK" ]; then
	  # Install sudo	  
	  apt-get update
	  apt-get install -y sudo
	  # Install rabbitmq-server and its dependencies
	  sudo apt-get install rabbitmq-server -y --fix-missing	  
	fi
	
	STATUS="$(systemctl is-active rabbitmq-server)"
	if [ "${STATUS}" = "active" ]; then
	    echo " MessageQueue service is running..."
	else 
	    echo " Starting MessageQueue service..."  
		# Start RabbitMQ service
		sudo systemctl start rabbitmq-server
		sudo service rabbitmq-server start 
		sudo rabbitmq-plugins enable rabbitmq_management	  
	fi
)