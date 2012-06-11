#!/usr/bin/env python


#import ConfigParser
#from PointInPolygon import pip		# (polygon, x, y)
#import PointInPolygon
#from CountryInPolygon import cip		# (polygon, iso_code)
#import CountryInPolygon
##from PolygonInCountry import pic 	# (polygon)
#import PolygonInCountry
#import UserInput
import Countries


c = Countries.all_species()
print c[0]
print c[1]
print Countries.some_species(c[1])


'''
uid = UserInput.Data()
all_species_in_country_list = []
some_species_in_country_list = []

""" 	Identify countries from where all species 
		should be included in downstream analyses.
"""
for polygon in uid.user_polygons.split(':'):
	for iso_code in PolygonInCountry.get_iso():
		the_test = CountryInPolygon.cip(polygon, iso_code)
		if the_test == True:
#			print iso_code[0]		# Devel.
			all_species_in_country_list.append(iso_code[0])
#			print country_list		# Devel.
		elif the_test == None:
			some_species_in_country_list.append(iso_code[0])

print "all_species_in_country_list = %s" % all_species_in_country_list
print "some_species_in_country_list = %s" % some_species_in_country_list


""" 	Check if the polygon is only part of a country
 		Returns a list of countries from where collecions 
 		should be tested using "pip".
"""
print "#### Now in second function ####"	# Devel.
for polygon in uid.user_polygons.split(':'):
	print polygon		# Devel.
	second_test =  PolygonInCountry.pic(polygon)
	print second_test	# Devel.
	if second_test != None and second_test not in some_species_in_country_list:
		some_species_in_country_list.append(second_test)
#	for country in 

print "some_species_in_country_list is now = %s" % some_species_in_country_list		# Devel.
#print some_species_in_country_list		# Devel.

'''
