#!/bin/bash

CONTEST_PATH="/home/judges/data/contests"
CONTEST_DATA_PATH="/home/judges/$2"

cd $CONTEST_PATH
touch $1
mkdir -p "$CONTEST_DATA_PATH/conf" "$CONTEST_DATA_PATH/problems" "$CONTEST_DATA_PATH/var"
