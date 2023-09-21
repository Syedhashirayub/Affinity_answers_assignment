#!/bin/bash

# Downloading the file
curl -O https://www.amfiindia.com/spages/NAVAll.txt

# Extract the Scheme Name (4th field) and Asset Value (5th field) and save them in a TSV file
awk -F ';' 'NF > 4 {print $4 "\t" $5}' NAVAll.txt > output.tsv

# Convert the TSV data to JSON format
awk 'BEGIN {
    OFS="\t";
    print "["
}
{
    print "{ \"SchemeName\": \"" $1 "\", \"AssetValue\": \"" $2 "\" },"
}
END {
    print "]"
}' output.tsv > output.json

# Cleaning up the downloaded file
rm NAVAll.txt
