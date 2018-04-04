#!/bin/bash

USER_ID=$(id -u)
GROUP_ID=$(id -g)

echo "app:x:$USER_ID:$GROUP_ID:app:/app:/bin/bash" >> /etc/passwd
sudo groupadd app -g $GROUP_ID
sudo usermod -a -G app app

sudo chown $USER_ID:$GROUP_ID /app
export HOME=/app

# Execute command
exec "$@"
