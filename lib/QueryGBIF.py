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

uim = UserInput.MySQL()

def qgd(ISO_code_list, taxon='%', taxon_name='%'):
	# ISO_code_list is a list of ISO coutry code(s)
	# Default values for "taxon" and "taxon_name" is
	# the sql wildcard character "%".
	# Function queries the GBIF database and returns 
	# tree lists of plant, animal and fungi species names
	# in the form "['Potentilla alba', 'Potentilla alba']
	for code in ISO_code_list:
		raw_species_list_plants = []
		raw_species_list_animals = []
		raw_species_list_fungi = []
		raw_species_list_other = []
		for i in species_list(code, taxon, taxon_name):
			genus = str(i[0])
			species = str(i[1])
			kingdom = str(i[2])
			species_name = str(str(i[0]) + " " + str(i[1]))
			species_name_and_kingdom = str(str(i[0]) + " " + str(i[1]) + " " + str(i[2]))
			if kingdom.lower() == 'animalia':
				raw_species_list_animals.append(species_name)
			if kingdom.lower() == 'fungi':
				raw_species_list_fungi.append(species_name)
			if kingdom.lower() == 'plantae':
				raw_species_list_plants.append(species_name)
			else:
				raw_species_list_other.append(species_name_and_kingdom)
	print raw_species_list_plants
	return raw_species_list_plants, raw_species_list_animals, raw_species_list_fungi
"""		for i in species_list(code):					# Turn into a listcomp. 
			if i[1] == 1:								# IF the record is for an animal sample ...
				raw_species_list_animals.append(i[0])
			if i[1] == 5:								# Fungi
				raw_species_list_fungi.append(i[0])
			if i[1] == 6:								# Plant
				raw_species_list_plants.append(i[0])
			else:										# Other organism group (2 - Archaea, 3 - Bacteria
				raw_species_list_other.append(i[0])		# 4 - Stramenopiles, 7 - Alveolata, Foraminifera, Amoebozoa etc.)	
	return raw_species_list_plants, raw_species_list_animals, raw_species_list_fungi
"""			

def species_list(ISO_code, taxon, taxon_name):
	con = mdb.connect(uim.host, uim.user, uim.password, uim.gbif_db) # Host, user name, password, GBIF database name
	cur = con.cursor()
	# cur.execute("SELECT taxon_name_id, kingdom_concept_id FROM occurrence_record_%s" % ISO_code)
	cur.execute('SELECT genus,species,kingdom FROM raw_occurrence_record_%s where %s LIKE "%s"' % (ISO_code, taxon, taxon_name))
	data = cur.fetchall()
#	print data		# Devel.
	cur.close()
	return data


def species_name(taxon_name_id):
	con = mdb.connect(uim.host, uim.user, uim.password, uim.gbif_db) # Host, user name, password, GBIF database name
	cur = con.cursor()
	cur.execute("SELECT generic, specific_epithet FROM taxon_name WHERE id=%s" % taxon_name_id)
	name = cur.fetchall()
	cur.close()
	return name[0]
