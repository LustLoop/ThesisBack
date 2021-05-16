#!/bin/bash

LOCATION=$1
DB_LOCATION="/home/judges/data/db/userlist.xml"
echo "$LOCATION"
cd "$LOCATION/input_files"
cp $DB_LOCATION "$LOCATION/input_files/users_db.xml"
chmod 755 "$LOCATION/input_files/users_db.xml"