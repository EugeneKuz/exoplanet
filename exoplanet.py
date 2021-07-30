from collections import OrderedDict
import requests
import json
import sys

exoplanet_data_url = 'https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets'

def get_json_file(data_file):
	formatted_string = ""
	with open(data_file) as f:
	    formatted_string = " ".join(line.strip() for line in f)
	data = json.loads(formatted_string)
	return data

def get_json_url(url):
	url_file_path = "expo_data"
	req = requests.get(url)
	open(url_file_path, 'wb').write(req.content)
	formatted_string = ""
	with open(url_file_path) as f:
	    formatted_string = " ".join(line.strip() for line in f)
	data = json.loads(formatted_string)
	return data

def print_orphans(orphans):
	print("\n--1--")
	if orphans == 1:
		print("There is 1 orphan planet (no star).")
	else:
		print("There are %d orphan planets (no star)." % (orphans))

def print_planet_hottest_star(hottest_star):
	if len(hottest_star) == 0:
		return 0
	print("\n--2--")
	if len(hottest_star) == 1:
		print(str(hottest_star[0]) + " is the planet orbiting the hottest star.")
	else:
		# If more than one planet shares same max temp
		for index in range(len(hottest_star)-1):
			print(hottest_star[index], end=", ")
		print("and %s are planets orbiting the hottest stars." % (hottest_star[index+1]))	

def print_discovery_timeline(unsorted_timeline,debug=False):
	print("\n--3--")
	timeline = OrderedDict(sorted(unsorted_timeline.items()))
	for year in timeline:

		# Grammar check
		sml = "planets"
		med = "planets"
		lrg = "planets"
		if timeline[year][1] == 1:
			sml = "planet"
		if timeline[year][2] == 1:
			med = "planet"
		if timeline[year][3] == 1:
			lrg = "planet"
		if year == 0:
			print("Unrecorded discovery year. We discovered %d small %s, %d medium %s, and %d large %s." % (timeline[year][1], sml, timeline[year][2], med, timeline[year][3], lrg))
		else:
			print("In %d, we discovered %d small %s, %d medium %s, and %d large %s." % (year, timeline[year][1], sml, timeline[year][2], med, timeline[year][3], lrg))	
		if debug and timeline[year][0] > 0:
			print(" - %d planets were discovered for this year but do not have a recorded size." % (timeline[year][0]))

def parse_planet_data(data):

	# init variables
	orphan_planets 	= 0
	max_star_temp 	= 0
	hottest_star 	= []
	unique_planets	= []
	timeline 		= {}
	
	# Define sizes
	sml_jpt = 1
	med_jpt = 2

	for item in data:

		# Get variables
		type_flag 	= item["TypeFlag"]
		planet_name = item["PlanetIdentifier"]
		radius_jpt 	= item["RadiusJpt"]
		star_temp 	= item["HostStarTempK"]
		discover_yr = item["DiscoveryYear"]

		# Check for valid values
		if planet_name == "":
			planet_name = "NoName"
		if discover_yr == "":
			discover_yr = 0
		if radius_jpt == "":
			radius_jpt 	= 0
		if star_temp == "":
			star_temp = 0

		# Set types
		type_flag 	= int(type_flag)
		discover_yr = int(discover_yr)
		radius_jpt 	= float(radius_jpt)
		star_temp 	= float(star_temp)
		planet_name = str(planet_name)

		# Check for duplicate entries
		if planet_name in unique_planets:
			continue
		unique_planets.append(planet_name)

		# Count orphans
		if type_flag == 3:
			orphan_planets += 1

		# Check max star temp
		if star_temp > max_star_temp:
			max_star_temp = star_temp
			hottest_star = [planet_name]

		# Check if multiple planets share same max temp
		elif star_temp == max_star_temp:
			hottest_star.append(planet_name)

		# Initialize timeline entry
		if discover_yr not in timeline:
			init_counters = [0,0,0,0] # [undefined, small, medium, large]
			timeline[discover_yr] = init_counters

		# Group by size
		if radius_jpt <= 0:
			timeline[discover_yr][0] += 1 # undefined
		elif radius_jpt < sml_jpt:
			timeline[discover_yr][1] += 1 # small
		elif radius_jpt < med_jpt:
			timeline[discover_yr][2] += 1 # medium
		else:
			timeline[discover_yr][3] += 1 # large

	return orphan_planets,hottest_star,timeline

if __name__ == "__main__":

	data = ""
	test_file = ""
	debug = False
	for arg in sys.argv:
		if '--help' in arg:
			print("Normal execution: python %s" % (sys.argv[0]))
			print("\n--Optional flags--\n")
			print("test_file=<filepath> 	: Test using local file")
			print("debug=<True/False> 	: Print # undefined occurrences")
			print("")
			sys.exit()
		if 'test_file=' in arg:
			test_file = arg.split('test_file=')[1].strip()
		if 'debug=True' in arg or 'debug=true' in arg:
			debug = True

	if test_file:
		print("Testing using file: %s" % (test_file))
		data = get_json_file(test_file)
	else:
		data = get_json_url(exoplanet_data_url)

	if data:
		orphans,hottest_star,timeline = parse_planet_data(data)
		print_orphans(orphans)
		print_planet_hottest_star(hottest_star)
		print_discovery_timeline(timeline,debug)



# Corner cases. more than one max hottest temp
# Corent case. missing disovery year
# HOw do i find what is an orphan planet?
# Corner case. What if radiuJpt is empty?
# Corenr case. what if planetnae is empty? This doesnt exist apparnetly
# What if temp is empty?
# 1 planet, what about grammar?



