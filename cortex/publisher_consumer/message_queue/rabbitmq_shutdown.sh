#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	sudo systemctl disable rabbitmq-server	
)
