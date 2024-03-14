ENTRYPOINT ["python", "./src/__main__.py"]
# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define the entry point of the application
ENTRYPOINT ["python", "./src/__main__.py"]
