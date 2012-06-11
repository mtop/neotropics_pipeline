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


# Determine if a country is fully, partially or not at all part of a user defined polygon
# Usage: ./CountryInPolygon.py <ISO2_code>

import MySQLdb as mdb
from PointInPolygon import pip
import UserInput

uim = UserInput.MySQL()

def cip(polygon, iso_code):
	con = mdb.connect(uim.host, uim.user, uim.password, uim.db)
	with con:
		cur = con.cursor()
		sql_string = "SELECT polygons FROM country_polygons WHERE ISO2='%s'" % iso_code
		cur.execute(sql_string)
		country_polygon = list(cur.fetchall()[0])[0]
		F = 0
		T = 0
		# The contry polygon may be made up of several polygons separated by ':'.
		for poly in country_polygon.split(':'):
			for node in poly.split(' '):
				x = float(node.split(',')[0])
				y = float(node.split(',')[1])
				test = pip(polygon, x, y)
				if test == True:
					T = 1
				elif test == False:
					F = 1

	# Country in polygon
	if T == 1 and F == 0:
		return True
	# Country not in polygon
	if T == 0 and F == 1:
		return False
	# Part of the country in the polygon
	if T == 1 and F == 1:
		return None


if __name__ == '__main__':
	import ConfigParser
	import sys
	config = ConfigParser.RawConfigParser()
	config.read('neotropis.cfg')
	host = config.get('MySQL', 'host')
	database_name = config.get('MySQL', 'db')
	user = config.get('MySQL', 'user')	
	password = config.get('MySQL', 'password')
	polygon1 = config.get('Polygons', 'Northen_EU')
	polygon1_name = config.get('Polygons', 'polygon1_name')
	iso_code = sys.argv[1]
	print cip(polygon1, iso_code)
