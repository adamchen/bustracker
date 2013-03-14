from timetableData.models import *
import datetime
def new_bus_stop(name, bearing, lat, lon):
	bus_stop = BusStop.objects.create(name=name,bearing=bearing)
	bus_stop.location.latitude = lat
	bus_stop.location.longitude = lon
	bus_stop.save()
	return bus_stop

def bus_stops(fileName):
	import csv
	with open(fileName, "rb") as csvfile:
		reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
		for row in reader:
			if len(row) == 5:
				new_bus_stop("{} ({})".format(row[0], row[1]), row[2], row[3], row[4])

def add_journies(route, fileName, weekdays, saturdays, sundays):
	import csv
	with open(fileName, "rb") as csvfile:
		reader = csv.reader(csvfile, delimiter='\t', quotechar="\"")
		stops = []
		for row in reader:
			if len(stops) == 0:
				for stop in row:
					stops.append(BusStop.objects.get(pk=stop))
				print stops
			else:
				journey = RouteJourney.objects.create(weekdays=weekdays,saturdays=saturdays,sunday=sundays,route=route)
				last_stop = None
				for i in range(0,len(row)):
					stop = RouteStop.objects.create(stop=stops[i], time = timeFormat(row[i]))	
					if (last_stop is not None):
						last_stop.next_stop = stop
						last_stop.save()
					else:
						journey.first_stop = stop
						journey.save()
					last_stop = stop
def timeFormat(time):
	return time[:2] + ":" + time[2:]

def reload_from_scratch():
	print "Reloading data from scratch"
	Operator.objects.create(name="Wessex")
	route = BusRoute.objects.create(name="U18", operator=Operator.objects.get(pk=1))
	print "Adding BusStops"
	print datetime.datetime.now()
	bus_stops("../U18_busStops.csv")
	print "BusStops added"
	print datetime.datetime.now()
	#Inbound to uni only, atm
	print "INBOUND JOURNIES"
	print "Adding Weekday Journies"
	print datetime.datetime.now()
	add_journies(route, "../U18_monfri_timetable.csv", True, False, False)
	print "Adding Saturday Journies"
	print datetime.datetime.now()
	add_journies(route, "../U18_sat_timetable.csv", False, True, False)
	print "Adding Sunday Journies"
	print datetime.datetime.now()
	add_journies(route, "../U18_sun_timetable.csv", False, False, True)
	print "OUTBOUND JOURNIES"
	print "Adding Weekday Journies"
	print datetime.datetime.now()
	add_journies(route, "../U18_monfri_timetable_back.csv", True, False, False)
	print "Adding Saturday Journies"
	print datetime.datetime.now()
	add_journies(route, "../U18_sat_timetable_back.csv", False, True, False)
	print "Adding Sunday Journies"
	print datetime.datetime.now()
	add_journies(route, "../U18_sun_timetable_back.csv", False, False, True)
	print "Journies added."
	print datetime.datetime.now()
