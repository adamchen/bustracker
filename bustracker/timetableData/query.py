from timetableData.models import *
from django.db.models import Q
def get_from(origin, destination, arrival_time):
	journies = RouteJourney.objects.filter(stops__stop=origin).filter(stops__stop=destination)
	route_stops = RouteStop.objects.filter(stop=destination,journey__in=journies,time__lt=arrival_time).order_by("-time")
	i = 0
	while (i < route_stops.count()):
		if (isBefore(origin,destination,route_stops[i].journey)):
			return route_stops[i].journey
	return None

def isBefore(stopA, stopB, journey):
	a = False
	b = False
	stop = journey.first_stop
	while stop is not None:
		if stop.stop == stopA:
			if b == False:
				a = True
			else:
				return False
		if stop.stop == stopB:
			if a == False:
				return False
			else:
				return True
		stop = stop.next_stop
	return False
