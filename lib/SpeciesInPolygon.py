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

import UserInput
import MySQLdb as mdb
from PointInPolygon import pip

uim = UserInput.MySQL()
uid = UserInput.Data()


### Extend "species_list" with records found inside user polygon
def additional_species(ISO_code_list, species_list, raw_species_list, polygon):	
	for code in ISO_code_list:
		con = mdb.connect(uim.host, uim.user, uim.password, uim.gbif_db) # Host, user name, password, GBIF database name
		cur = con.cursor()
		cur.execute("SELECT taxon_name_id, longitude, latitude FROM occurrence_record_%s" % code)
		additional_species_list = cur.fetchall()
		cur.close()
	return remove_redundant(additional_species_list, species_list, raw_species_list, polygon)


### Add non redundant species_id's to "species_list"
def remove_redundant(additional_species_list, species_list, raw_species_list, polygon):
	for record in additional_species_list: 
		# Add all species_id's in "additional_species_list" to "raw_species_list"
		raw_species_list.append(record[0])
	for record in additional_species_list:
		print record									# Devel.
		print int(raw_species_list.count(record[0]))	# Devel.
		print int(uid.occurrence_nr)					# Devel.
		# Test if 
		if int(raw_species_list.count(record[0])) >= int(uid.occurrence_nr) and record not in species_list:
			# Test if the occurrence record has longitude data
			if record[1] != None:
				print pip(polygon, record[1], record[2])	# Devel.
				print record[1]								# Devel.
				print record[2]								# Devel.
				if pip(polygon, record[1], record[2]) == True:
					print "###	Match	###"			# Devel.
					species_list.append(record)
	return species_list
			

if __name__ == "__main__":
	raw_species_list = [8703741, 8703741, 8703741, 10330253, 10330253, 10330253, 10330253, 2003706]
	species_list = [8703741, 10330253]
	ISO_code_list = ['IS']
	polygon = uid.user_polygons.split(':')[0]
	additional_species(ISO_code_list, list(species_list), list(raw_species_list), polygon)
