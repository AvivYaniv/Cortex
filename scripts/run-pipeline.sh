#!/bin/bash

# Variable Definition
DIR="$(cd "$(dirname "$0")" && pwd)"

# Commands Section
echo "Preparing to run..."
# echo "Cleaning previous remmants"
# sudo sh $DIR/remove_containers.sh
echo "Building containers"
sudo docker-compose build
echo "Bringing up containers"
sudo docker-compose up
