# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your application will run on
EXPOSE 8000

# Command to run your app
CMD ["python", "-m", "src.main"]
