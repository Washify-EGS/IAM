FROM python:3.9-slim

# Install system dependencies for MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pkg-config
RUN apt-get update && apt-get install -y pkg-config

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install requests-oauthlib==1.1.0
RUN pip3 install flask-swagger-ui
RUN pip3 install mysql-connector
RUN pip3 install PyJWT

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV NAME iam_washify

# Run iamService.py when the container launches
CMD ["python3", "iamService.py"]