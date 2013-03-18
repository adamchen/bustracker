from timetableData.models import *
from django.db.models import Q

def get_from(origins, destination, arrival_time, day, number_of_journies=3):
	journies = RouteJourney.objects.filter(stops__stop__in=origins).filter(stops__stop=destination).filter(weekdays=(day >= 1 and day <= 5), saturdays = (day == 6), sunday = (day == 7))
	route_stops = RouteStop.objects.filter(stop=destination,journey__in=journies,time__lt=arrival_time).order_by("-time")
	i = 0
	routes_to_use = []
	while (i < route_stops.count()):
		print route_stops[i]
		if (isBefore(origins,destination,route_stops[i].journey)):
			routes_to_use.append(route_stops[i].journey)
			if (len(routes_to_use) >= number_of_journies):
				break
		i += 1
	return routes_to_use

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
		if stop.stop == stopB:
			if not a:
				return False
			else:
				return True
		stop = stop.next_stop
	return False
