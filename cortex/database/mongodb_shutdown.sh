#!/bin/bash

( 
	sudo update-rc.d mongodb disable 
  	sudo update-rc.d -f mongodb remove 
  	sudo systemctl disable mongodb
)
