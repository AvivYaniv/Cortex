#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	invoke-rc.d rabbitmq-server stop	
)
