#!/usr/bin/env python
# -*- coding: utf-8 -*-

###   Copyright (C) 2012 Mats Töpel.

###   This program is free software: you can redistribute it and/or modify
###   it under the terms of the GNU General Public License as published by
###   the Free Software Foundation, either version 3 of the License, or
###   (at your option) any later version.
###   
###   This program is distributed in the hope that it will be useful,
###   but WITHOUT ANY WARRANTY; without even the implied warranty of
###   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
###   GNU General Public License for more details at
###   http://www.gnu.org/licenses/.


import CountryInPolygon
import PolygonInCountry
import UserInput

uid = UserInput.Data()

"""		"all_species_in_country_list" will contain a list    
		of countries from where all species should be 
		included in downstream analyses.
		"some_species_in_country_list" will contain a list
		or countries that are partially included in the user-
		defined polygon. Records from these countries should 
		be filtered using the "PointInPolygon.pip" function.
"""
def all_species():
	all_species_in_country_list = []
	some_species_in_country_list = []
	for polygon in uid.user_polygons.split(':'):
		for iso_code in PolygonInCountry.get_iso():
			the_test = CountryInPolygon.cip(polygon, iso_code)
			if the_test == True:
				all_species_in_country_list.append(iso_code[0])
			elif the_test == None:
				some_species_in_country_list.append(iso_code[0])
	return all_species_in_country_list, some_species_in_country_list
#print "all_species_in_country_list = %s" % all_species_in_country_list			# Devel.
#print "some_species_in_country_list = %s" % some_species_in_country_list		# Devel.



"""     Check if the one of the user-defined polygon are 
		only part of a country (fully enclosed by a country 
		polygon) and then appends these counties to the 
		"some_species_in_country_list". Records from these 
		countries should be filtered using the 
		"PointInPolygon.pip" function.
"""
def some_species(some_species_in_country_list):
	for polygon in uid.user_polygons.split(':'):
		second_test = PolygonInCountry.pic(polygon)
		if second_test != None and second_test not in some_species_in_country_list:
			some_species_in_country_list.append(second_test)
	return some_species_in_country_list

#print "some_species_in_country_list is now = %s" % some_species_in_country_list     # Devel.
