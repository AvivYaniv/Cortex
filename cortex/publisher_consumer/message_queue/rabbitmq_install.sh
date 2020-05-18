#!/bin/bash

( 
	echo "Install rabbitmq-server"
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' rabbitmq-server|grep "install ok installed")
	
	# If rabbitmq-server not installed
	if [ "" == "$PKG_OK" ]; then
	  # Install sudo	  
	  apt-get update
	  apt-get install -y sudo
	  # Install rabbitmq-server and its dependencies
	  sudo apt-get install rabbitmq-server -y --fix-missing	  
	fi
	
	echo "Install systemd"
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' systemd|grep "install ok installed")
	
	# If systemd not installed
	if [ "" == "$PKG_OK" ]; then
	  # Install systemd	  
	  sudo apt-get install -y --reinstall systemd  
	fi
	
	echo "Starting service rabbitmq-server"
	echo "Enable rabbitmq-server"
	systemctl enable rabbitmq-server
	echo "Start rabbitmq-server"
	service rabbitmq-server start		
	#sudo systemctl start rabbitmq-server   
		
	echo "MessageQueue status check"
	STATUS=$(service rabbitmq-server status|grep inactive)
	if [ "" = "${STATUS}" ]; then
	    echo " MessageQueue service is running..."
	else
		exit -1
	fi
	
	echo "Start RabbitMQ management"
	IS_DEBIAN='$(lsb_release -d | grep Debian)'
	if [ "" = "${IS_DEBIAN}" ]; then		
	    rabbitmq-plugins enable rabbitmq_management
	fi
)