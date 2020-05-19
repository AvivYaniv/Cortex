#!/bin/bash

( 
	echo "Shutdown rabbitmq-server"
	rabbitmqctl stop
	update-rc.d -f rabbitmq-server remove
 	systemctl disable rabbitmq-server	
)
