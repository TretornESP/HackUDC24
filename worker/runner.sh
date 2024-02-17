#!/bin/sh

python3 /worker/extract_data.py $1 $2
curl http://backend:5000/
curl -X POST -H "Content-Type: application/json" -d @$2/full_output.json http://backend:5000/ > $2/log.txt
echo "Output saved to $2/log.txt"
ls -lsart $2
cat $2/log.txt
cat $2/full_output.json