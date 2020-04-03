# Use the official image as a parent image.
FROM python:3

# Set the working directory.
WORKDIR /usr/src/app

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8080

# Upon container execution; setupping requirments for project in docker container
ENTRYPOINT "./scripts/run_container.sh"
