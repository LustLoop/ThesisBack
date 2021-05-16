#!/bin/bash

source /etc/environment
LOCATION=$(pwd)

echo $ROOT_PASSWORD | sudo -S su - root -c "bash $LOCATION/shell_scripts/create_contest.sh $1 $2"
echo $USER_PASSWORD | sudo -S su - ejudge -c "bash $LOCATION/shell_scripts/restart_ejudge.sh"
