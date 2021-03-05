#!/usr/bin/bash

curl -XPOST "http://127.0.0.1:9200/filebeat-*/_delete_by_query?conflicts=proceed" -H 'Content-Type: application/json' -d'{ "query": { "match_all": {} }}'
