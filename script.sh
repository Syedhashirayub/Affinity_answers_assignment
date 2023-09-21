#!/bin/bash

# 1. Downloading the file
curl -O https://www.amfiindia.com/spages/NAVAll.txt

# 2. Extracting the scheme name and asset value fields and saving them in a TSV file
awk -F ';' '{print $2 "\t" $5}' NAVAll.txt > output.tsv

# 3. Converting the TSV data to JSON format
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
