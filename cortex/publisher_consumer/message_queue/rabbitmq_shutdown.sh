#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	rabbitmqctl stop
	systemctl disable rabbitmq-server	
)
