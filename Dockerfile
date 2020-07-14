# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /myhao_service

# Set the working directory to /myhao_service
WORKDIR /myhao_service

# Copy the current directory contents into the container at /myhao_service
ADD . /myhao_service/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt