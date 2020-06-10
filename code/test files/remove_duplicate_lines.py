lines_seen = set() # holds lines already seen
outfile = open("most_populated_counties_CA.txt", "w")
for line in open(r"..\resources\data\100_cities_AND_counties_cali.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
