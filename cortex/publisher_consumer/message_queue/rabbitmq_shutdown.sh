#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	sudo rabbitmqctl stop
	sudo invoke-rc.d rabbitmq-server stop
)
