#!/bin/bash

source /etc/environment
LOCATION=$(pwd)
echo "$LOCATION"
echo $ROOT_PASSWORD | sudo -S su - root -c "bash $LOCATION/shell_scripts/get_users.sh $LOCATION"