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

def qgd(ISO_code_list):
	for code in ISO_code_list:
#		print code	# Devel.
#		return list(species_list(code))
		raw_species_list = []
		for i in species_list(code):		# Turn into a listcomp. 
			raw_species_list.append(i[0])
	return raw_species_list
			

def species_list(ISO_code):
	con = mdb.connect(uim.host, uim.user, uim.password, uim.gbif_db) # Host, user name, password, GBIF database name
	cur = con.cursor()
	cur.execute("SELECT taxon_name_id FROM occurrence_record_%s" % ISO_code)
	data = cur.fetchall()
	cur.close()
	return data
