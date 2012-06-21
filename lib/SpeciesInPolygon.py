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


### Extend "species_list" with records found inside user polygon,
### in countries not fully included in user polygon.
def additional_species(ISO_code_list, species_list, raw_species_list, polygon):	
	for code in ISO_code_list:
		print code		# Devel.
		additional_species_list = []
		con = mdb.connect(uim.host, uim.user, uim.password, uim.gbif_db) # Host, user name, password, GBIF database name
		cur = con.cursor()
		cur.execute("SELECT taxon_name_id, longitude, latitude FROM occurrence_record_%s" % code)
#		out = cur.fetchall()
#		cur.close()
#		additional_species_list.append(out)
	additional_species_list = cur.fetchall()
	cur.close()
	print "additional_species_list: %s" % len(additional_species_list)		# Devel.
#	return remove_redundant_FIRST_REINCARNATION(additional_species_list, species_list, raw_species_list, polygon)
	remove_redundant_FIRST_REINCARNATION(additional_species_list, species_list, raw_species_list, polygon)	# Devel.
	print "species_list: %s" % len(species_list)						# Devel.


def remove_redundant_FIRST_REINCARNATION(additional_species_list, species_list, raw_species_list, polygon):
	for record in additional_species_list:
		# Test if this species is already logged for donwstreame analyses
		if record in species_list:
			continue
		else:
			# Include sample in "species_list" if found inside 
			# user defined polygon and cutoff value is zero.
			if int(uid.occurrence_nr) == 0:
#				print 'Test 1'								# Devel.
				if geo_test(polygon, record) == True:
					species_list.append(record[0])
#					print species_list						# Devel.
#				# Test if the occurrence record has longitude data
#				if record[1] != None:


			# Test if including this record will reach the
			# cutoff value for inclusion (which has to be >0)... 
			if int(raw_species_list.count(record[0])) == int(uid.occurrence_nr)-1 and int(uid.occurrence_nr) > 0:
#				print 'Test 2'								# Devel.
				if geo_test(polygon, record) == True:
					species_list.append(record[0])
#				# Test if the occurrence record has longitude data
#				if record[1] != None:
#					if pip(polygon, record[1], record[2]) == True:
#						print "###  Match   ###"            # Devel.
#						species_list.append(record)
#					else:									# Devel.
#						print 'No'							# Devel.
			# ...or else test if record is found inside user polygon, and if so, 
			# add species id to "raw_species_list".
			if int(raw_species_list.count(record[0])) > int(uid.occurrence_nr) and int(uid.occurrence_nr) > 0:
#				print 'Test 3'								# Devel.
				if geo_test(polygon, record) == True:
					raw_species_list.append(record[0])
				# Test if the occurrence record has longitude data
#				if record[1] != None:
#					if pip(polygon, record[1], record[2]) == True:
#						print "###  Match-2   ###"            # Devel.
#						raw_species_list.append(record)

			# ...and so on. ADD MORE TESTS!!!
	return species_list, raw_species_list


def geo_test(polygon, record):
	# Test if the occurrence record has longitude data
	if record[1] != None:
		if pip(polygon, record[1], record[2]) == True:
#			print "###  Match  ###"            # Devel.
			return True
#			container.append(record)
		else:
#			print 'No'                          # Devel.
			return  False
	else:
		return False

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
	ISO_code_list = ['IS'] #,'NO']
	polygon = uid.user_polygons.split(':')[0]
	additional_species(ISO_code_list, list(species_list), list(raw_species_list), polygon)
