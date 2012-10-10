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


# determine if a point is inside a given polygon or not
# Polygon is a list of Longitude/Latitude (x,y) pairs.
# Code modified from  http://www.ariel.com.au/a/python-point-int-poly.html
def pip(poly, x, y):
	x = float(x)
#	print x		# Devel.
	y = float(y)
	poly = prepare_poly(poly)
	n = len(poly)
	inside = False
	p1x = float('%s' % poly[0].split(',')[0])
#	print type(p1x)		# Devel.
#	print p1x			# Devel.
	p1y = float('%s' % poly[0].split(',')[1])
#	print type(p1y)		# Devel.
#	print p1y			# Devel.
	for i in range(n+1):
		p2x = float('%s' % poly[i % n].split(',')[0])
#		print type(p2x)	# Devel.
#		print p2x		# Devel.
		p2y = float('%s' % poly[i % n].split(',')[1])
#		print type(p2y)	# Devel.
#		print p2y		# Devel.
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y
	return inside



def prepare_poly(poly):
	poly = poly.split(' ')
	poly_2 = []
	for node in list(poly):
		mod = ('%s') % node
		poly_2.append(mod)
	return poly_2



if __name__ == '__main__':
	import ConfigParser
	import sys
	config = ConfigParser.RawConfigParser()
	config.read('neotropis.cfg')
#	polygon = config.get('Polygons', 'Northen_EU')
	polygon = config.get('Polygons', 'polygon_USA_Long_Lat')
	x = sys.argv[1] # Longitude
	y = sys.argv[2]	# Latitude
	print pip(polygon, x, y)
