# bonyan_static/static.Dockerfile
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the application runs on
EXPOSE 8080

# Set the command to run the application
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:8080"]