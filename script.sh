#!/bin/bash

# 1. download the file
curl -O https://www.amfiindia.com/spages/NAVAll.txt

# 2. extracting the Scheme Name and Asset Value and save in a TSV file
awk -F ';' 'NF >= 5 {print $4 "\t" $5}' NAVAll.txt > extracted_data.tsv

# 3. converting the TSV data to JSON format
awk -F '\t' 'BEGIN {
    print "["
}
{
    gsub(/"/, "\\\"", $1);  # Escape quotes for JSON
    gsub(/"/, "\\\"", $2);  # Escape quotes for JSON
    print "  { \"SchemeName\": \"" $1 "\", \"AssetValue\": \"" $2 "\" },"
}
END {
    print "]"
}' extracted_data.tsv > extracted_data.json

# cleanup
rm NAVAll.txt
