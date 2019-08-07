#!/bin/sh

read -p "Enter DB Path: "  FILE

if [ -f "$FILE" ]; then
    sqlite3 "$FILE" <<END_SQL
.timeout 2000
.headers on
.mode csv
.output data.csv
SELECT * from user;
.quit
END_SQL
else
    echo "$FILE does not exist"
fi
