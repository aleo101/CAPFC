#!/usr/bin/env python
#This script removes all lines from the NY times covid CSV file that don't contain counties listed in most_populated_counties_CA.
#Created by Alexander Leones for the CAPFC project  
# June 2020
import sys
import csv
counties_names = open(r'most_populated_counties_CA.txt', 'r')
csvfile = open(r'data_6_18_CA.csv', 'r')
lines=[]
cn_list=[]
for l in counties_names:
    cn_list.append(l.strip())
for row in csvfile:
    for ln in cn_list:
        if ln in row:
            lines.append(row) 
counties_names.close()
csvfile.close()
with open(r'top_data_6_18_CA.csv', 'w') as f:
        for line in lines:
            #print(line)
            f.write(line)

# def usage():
    # print sys.argv[0], "filename new_file"
    # print 'remove all lines not ending with ",-,.txt"'
    # print 'print the resulting lines, up to their last "/" to new file'


# if __name__ == '__main__':
    # if len(sys.argv) == 3:
        # main(sys.argv[1], sys.argv[2])
    # else:
        # usage()