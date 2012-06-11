DROP TABLE IF EXISTS `country_polygons`;
CREATE TABLE IF NOT EXISTS `country_polygons` (
		`polygon_type` varchar(12) NOT NULL,
		`polygons` MEDIUMTEXT NOT NULL,
		`FIPS` varchar(2) NOT NULL,
		`ISO2` varchar(2) NOT NULL PRIMARY KEY,
		`ISO3` varchar(3) NOT NULL,
		`UN` int NOT NULL,
		`country` varchar(150) NOT NULL,
		`AREA` int NOT NULL,
		`POP2005` int NOT NULL,
		`REGION` int NOT NULL,
		`SUBREGION`int NOT NULL,
		`LON` varchar(10) NOT NULL,
		`LAT` varchar(10) NOT NULL
     );
