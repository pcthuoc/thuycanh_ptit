# Use the official Python image as base image
FROM python:3.9-slim



# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY repo/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
# Install Redis
RUN apt-get update && apt-get install -y redis-server
