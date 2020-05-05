#!/bin/bash

# Stopping Docker Compose
sudo docker-compose stop

# Prunning unused containers
sudo docker container prune  --force

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
