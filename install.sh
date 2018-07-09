#!/bin/bash
reset
echo "Begin Evolution Cli installation..."

CLIENT="/client.sh"
CLIENT_PATH="$PWD$CLIENT"
chmod a+x $CLIENT_PATH

SERVER_PATH="/server.py"
SERVER_PATH="$PWD$TP"
chmod a+x $SERVER_PATH

sudo ln -s $CLIENT_PATH /usr/bin/evo
sudo ln -s $SEVER_PATH /usr/bin/evo-client

echo "Links created."
