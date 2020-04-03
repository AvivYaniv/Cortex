# Use the official image as a parent image.
FROM python:3

# Set the working directory.
WORKDIR /usr/src/app

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8080

# Copy the rest of the app's source code from the host to the image filesystem.
# COPY . .

# Running commad to start the server
CMD [ "python", "cortex/hello.py" ]
