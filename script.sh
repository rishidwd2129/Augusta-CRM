#!/bin/bash

# Parse the env_var.yaml and export each variable
while IFS= read -r line || [ -n "$line" ]; do
  
  # Strip surrounding quotes and carriage returns
  var=$(echo "$line" | sed 's/[\r]//g')  
  
  # Export the cleaned variable
  export "$var"
done < env_var.yaml

# To verify, you can print all environment variables starting with FIREBASE_
env | grep FIREBASE_

# Default IP and port
IP="0.0.0.0"
PORT="8000"

# Check if IP and port are passed as arguments
if [ ! -z "$1" ]; then
  IP=$1
fi

if [ ! -z "$2" ]; then
  PORT=$2
fi

# Navigate to the Django project directory
cd AugustaCRM || exit

# Run Django server
echo "Running Django server on ${IP}:${PORT}"
python manage.py runserver $IP:$PORT