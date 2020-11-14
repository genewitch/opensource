#!/usr/bin/python3
import math
import psycopg2

stationsconn = psycopg2.connect("dbname=postgres user=g password=foo")
zonesconn = psycopg2.connect("dbname=postgres user=g password=foo")
distanceconn = psycopg2.connect("dbname=postgres user=g password=foo")
closestconn = psycopg2.connect("dbname=postgres user=g password=foo")
#stationscursor.execute("select * from stations where latitude is not null and longitude is not null;")
zonescursor = zonesconn.cursor()

zonescursor.execute("select city,region_code,latitude,longitude,zip from zones where city is not null and country_code = 'US';")

def iter_row(cursor):
    while True:
        rows = cursor.fetchall()
        if not rows:
            break
        for row in rows:
            yield row

#let's go through the stations one at a time and
#check distance to every city in zones in the US
for row in iter_row(zonescursor):
	distance = 99999
	wxcall = ''
	zonecity,zonestate,zonelat,zonelong,zonezip = row
	stationscursor = stationsconn.cursor()
	SQL= "select call, round((point(stations.longitude,stations.latitude) <@> point(%s,%s))::numeric, 3) as miles from stations order by point(stations.longitude,stations.latitude) <-> point(%s,%s) limit 1;"
	DATA= (zonelong,zonelat,zonelong,zonelat,)
	stationscursor.execute(SQL, DATA)
	closeststation = [zonecity,zonestate,zonezip,distance,wxcall]
	tmpcall,tmpdist = stationscursor.fetchall()[0]
	closeststation[3] = tmpdist
	closeststation[4] = tmpcall
	print(closeststation)

	stationscursor.close()
	closestcursor = closestconn.cursor()
	INSERTSQL = "insert into closestfaster (city, state, zipcode, distance, wxcall) values (%s, %s, %s, %s, %s);"
	INSERTDATA = (closeststation[0],closeststation[1],closeststation[2],closeststation[3],closeststation[4],)
	closestcursor.execute(INSERTSQL, INSERTDATA)
	closestconn.commit()
	closestcursor.close()
zonescursor.close()


#stationscursor.execute("select * from stations where latitude is not null and longitude is not null;")
	#closeststation = [zonecity,zonestate,zonezip,distance,wxcall]
	#let's get the distance from the current station to every city in the US. you know, for fun!
	# for station in iter_row(stationscursor):
		# stationcall,stationlat,stationlong = station
		# distancecursor = distanceconn.cursor()
		# SQL = "select ((select point(%s,%s))<@>(select point(%s,%s))) as result;"
		# DATA = (zonelong,zonelat,stationlong,stationlat,)
		# distancecursor.execute(SQL,DATA)
		# checkdist = distancecursor.fetchall()[0][0]
		# #print(closeststation,checkdist)
		# if checkdist < closeststation[3]:
			# closeststation[3] = checkdist
			# closeststation[4] = stationcall
