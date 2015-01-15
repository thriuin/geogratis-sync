#!/bin/bash

# Check for mandatory parameters
if [ "$#" -ne 2 ]; then
  echo "Missing parameters"
  echo "Usage: $0 <virtualenv activate script> <CKAN config file>" >&2
  exit 1
fi

LOCKFILE=./.daily_scan.lock
DUMPFILE=./geo-$(date +"%Y_%m_%d").jsonl

if [ -e ${LOCKFILE} ] && kill -0 `cat ${LOCKFILE}`; then
    echo "already running"
    exit
fi

# make sure the lockfile is removed when we exit and then claim it
trap "rm -f ${LOCKFILE}; exit" INT TERM EXIT
echo $$ > ${LOCKFILE}

#activate the geo virtual environment

. $1

# Scan geogratis, transform the data, and load it into the local CKAN

echo "Step 1: Scanning"
python scanner.py -m -l geogratis_scan.log

echo "Step 2: Data transformation running"
python converter.py -m

echo "Step 3: Extracting latest data for CKAN"
python dump_geogratis.py -m -f ${DUMPFILE}

echo "Step 4: Load the scanned data into the local CKAN"
ckanapi load datasets -I ${DUMPFILE} -c $2 -l ckanapi-load.log

# Done

rm -f ${LOCKFILE}

