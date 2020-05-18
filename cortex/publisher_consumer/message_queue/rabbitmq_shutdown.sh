#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	sudo update-rc.d -f rabbitmq-server remove
 	sudo systemctl disable rabbitmq-server	
)
