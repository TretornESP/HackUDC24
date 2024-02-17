#!/bin/sh

python3 extract_data.py $1 $2

curl -X POST -H "Content-Type: application/json" -d "$2/full_output.json" backend:5000