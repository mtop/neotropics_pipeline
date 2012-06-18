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

uid = UserInput.Data()

""" Only include species that have been recorded 
	in the polygon >= times what is indicated in 
	'occurrence_nr' """
def occurrence_nr(raw_species_list):
	# Test if this filter should be used
#	print uid.occurrence_nr						# Devel.
	if uid.occurrence_nr != 0:
		print "[--] occurrence_nr is not zero"		# Devel.
		species_list = []
		for record in set(raw_species_list):
#			print record							# Devel.
#			print raw_species_list.count(record)	# Devel.
			if int(raw_species_list.count(record)) >= int(uid.occurrence_nr) and record not in species_list:
				species_list.append(record)
#				print "%s occurres more than %s times" % (record, uid.occurrence_nr) # Devel
#		print species_list
		return species_list
	else:
		print "[WW] occurrence_nr is zero"
		return raw_species_list

