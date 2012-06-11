#!/usr/bin/env python

table_name = 'country_polygons'
db_name = 'neotropis_pipeline'		# Change eventually


output_file = open('%s.sql' % table_name, 'w')

output_file.write('DROP TABLE %s;\n' % table_name)
output_file.write('CREATE TABLE IF NOT EXISTS `%s` (\n' % table_name)

output_file.write('		`polygon_type` varchar(12) NOT NULL,\n')
output_file.write('		`polygons` MEDIUMTEXT NOT NULL,\n')
output_file.write('		`FIPS` varchar(2) NOT NULL,\n')
output_file.write('		`ISO2` varchar(2) NOT NULL PRIMARY KEY,\n')
output_file.write('		`ISO3` varchar(3) NOT NULL,\n')
output_file.write('		`UN` int NOT NULL,\n')
output_file.write('		`country` varchar(150) NOT NULL,\n')
output_file.write('		`AREA` int NOT NULL,\n')
output_file.write('		`POP2005` int NOT NULL,\n')
output_file.write('		`REGION` int NOT NULL,\n')
output_file.write('		`SUBREGION`int NOT NULL,\n')
output_file.write('		`LON` varchar(10) NOT NULL,\n')
output_file.write('		`LAT` varchar(10) NOT NULL\n')
output_file.write('     );')
output_file.close()

