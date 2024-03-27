# Use an official Python runtime as a parent image
FROM python:3.12-alpine3.18

# Set metadata
LABEL maintainer="honeyready.com"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Install system dependencies
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev

# Install any needed packages specified in requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = 'true' ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    apk del .tmp-build-deps

# Clean up
RUN rm -rf /tmp

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for build-time
ARG DEV=false

# Create a non-root user
RUN adduser --disabled-password --no-create-home django-user

# Switch to the non-root user
USER django-user

# Command to run the application
CMD ["python", "app.py"]
