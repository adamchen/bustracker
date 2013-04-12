from timetableData.models import *
from django.db.models import Q
import requests
import json
import datetime

def get_from(origins, destinations, arrival_time, day, number_of_journies=3, arrival=True):
	if not isinstance(destinations, list):
		destinations = [destinations]
	if not isinstance(origins, list):
		origins = [origins]
	journies = RouteJourney.objects.filter(stops__stop__in=origins).filter(stops__stop__in=destinations).filter(weekdays=(day >= 0 and day <= 4), saturdays = (day == 5), sunday = (day == 6))
	if arrival:
		#That is, if the time given is the time to arrive, then search for that.
		route_stops = RouteStop.objects.filter(stop__in=destinations,journey__in=journies,time__lt=arrival_time).order_by("-time").distinct()
	else:
		#Otherwise it's when they're leaving.
		route_stops = RouteStop.objects.filter(stop__in=origins,journey__in=journies,time__gt=arrival_time).order_by("time").distinct()
	i = 0
	routes_to_use = []
	while (i < route_stops.count()):
		if (isBefore(origins,destinations,route_stops[i].journey)) and not any((route_stops[i].journey == journey) for journey in routes_to_use):
			routes_to_use.append(route_stops[i].journey)
			if (len(routes_to_use) >= number_of_journies):
				break
		i += 1
	return routes_to_use

def reduce_routes(important_stops, journies):
	new_journies = []
	for journey in journies:
		current_journey = {"route_stops" : [], "route_name" : journey.route.name}
		for stop in journey.stops.select_related():
			for stop_to_check in important_stops:
				if stop.stop == stop_to_check:
					current_journey["route_stops"].append(stop)
					break
		new_journies.append(current_journey)
	return new_journies

def isBefore(stops, stopB, journey):
	a = False
	b = False
	stop = journey.first_stop
	while stop is not None:
		if any((stop.stop == stopA) for stopA in stops):
			if not b:
				a = True
			else:
				return False
		if any((stop.stop == stopBs) for stopBs in stopB):
			if not a:
				return False
			else:
				return True
		stop = stop.next_stop
	return False

def get_nearest_stops(lat, lng, n_to_get=9):
	stops = []
	for stop in BusStop.objects.all():
		#Length of a latitude degree and length of a longitude degree assumed to be equal.
		stops.append({"stop" : stop, "distance_from" : math.sqrt((float(stop.location.longitude) - lng) ** 2 + (float(stop.location.latitude) - lat) ** 2)})
	sorted_stops = sorted(stops,key=lambda x : x.get("distance_from"))
	return_val = []
	for stop in sorted_stops[:n_to_get]:
		return_val.append(stop["stop"])
	return return_val


def get_lat_long(postcode):
	r = requests.get("http://uk-postcodes.com/postcode/{}.json".format(postcode.replace(" ","")))
	data = json.loads(r.text)
	return float(data[u"geo"][u"lat"]), float(data[u"geo"][u"lng"])