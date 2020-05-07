#!/bin/bash

# Stopping and removing previous containers and images
sudo docker-compose down

{
	sudo docker stop 			$(sudo docker ps -a -q) -t 1
	sudo docker rm 				$(sudo docker ps -a -q) -f
	sudo docker rmi 			$(sudo docker images --filter "dangling=true" -q --no-trunc)
} 2> /dev/null

{
	# Prunning unused containers
	sudo docker container prune					--force

	# Removing Cortex containers
	# Removing { Server, Client } containers
	sudo docker rmi cortex_server 				--force
	sudo docker rmi cortex_client 				--force

	# Removing parsers containers
	sudo docker rmi cortex_parser_pose 			--force
	sudo docker rmi cortex_parser_color_image 	--force
	sudo docker rmi cortex_parser_depth_image 	--force
	sudo docker rmi cortex_parser_user_feelings	--force

	# Removing Savers containers
	sudo docker rmi cortex_saver 				--force

	# Removing { API & GUI } containers
	sudo docker rmi cortex_gui 					--force
	sudo docker rmi cortex_api 					--force

	# Removing Database container
	sudo docker rmi cortex_database 			--force
	
	# Removing MessageQueue container
	sudo docker rmi cortex_messagequeue 		--force
} 2> /dev/null

echo "\nFinished remove remnants of old containers!\n"
