#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	systemctl disable rabbitmq-server	
)
