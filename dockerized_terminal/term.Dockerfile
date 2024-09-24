# dockerized_terminal/term.Dockerfile
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Docker socket to the container
VOLUME /var/run/docker.sock:/var/run/docker.sock

# Expose the port the application runs on
EXPOSE 5000

# Set the command to run the application
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "app:app", "--bind", "0.0.0.0:5000"]