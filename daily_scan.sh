#!/bin/bash

# Check for mandatory parameters
if [ "$#" -ne 2 ]; then
  echo "Missing parameters"
  echo "Usage: $0 <virtualenv activate script> <CKAN config file>" >&2
  exit 1
fi

PYTHON_VERSION=`python -c "import sys;t=int('{0}{1}'.format(sys.version_info[0],sys.version_info[1]));sys.exit(t)"`

if [ $PYTHON_VERSION -eq 27 ]
then
  echo `which python`
  echo "Requires Python 2.7"
  exit
fi

LOCKFILE=./.daily_scan.lock
DUMPFILE=./geo-$(date +"%Y_%m_%d").jsonl
XFORMFILE=./geo-$(date +"%Y_%m_%d")-xform.jsonl

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

echo "Step 4: Transform the 2.3 json to version 2.5"
if [ -f  ${DUMPFILE} ]; then 
  cat  ${DUMPFILE} | paster canada metadata-xform --portal -c /var/www/html/open_gov/staging-portal/ckan/production.ini > $XFORMFILE

  echo "Step 5: Load the scanned data into the local CKAN"
  ckanapi load datasets -I ${XFORMFILE} -c $2 -l ckanapi-load.log
else
  echo "No GeoGratis records found to be loaded"
fi

# Done

rm -f ${LOCKFILE}

