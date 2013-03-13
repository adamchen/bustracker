from django.db import models
from geoposition.fields import GeopositionField

class Operator(models.Model):
	name = models.CharField(max_length=250)

class BusRoute(models.Model):
	name = models.CharField(max_length=250)
	operator = models.ForeignKey(Operator, related_name="bus_services")

class BusStop(models.Model):
	location = GeopositionField()
	name = models.CharField(max_length=250)

class RouteJourney(models.Model):
	first_stop = models.OneToOneField('RouteStop', related_name="journey")
	weekdays = models.BooleanField(default=False)
	saturdays = models.BooleanField(default=False)
	sunday = models.BooleanField(default=False)

	@property
	def stops():
		stops = []
		last_stop = first_stop
		while (last_stop != null):
			stops.append(last_stop)
			last_stop = last_stop.next_stop
		return stops

class RouteStop(models.Model):
	stop = models.ForeignKey(BusStop, related_name="route_stops")
	time = models.TimeField()
	next_stop = models.OneToOneField('RouteStop', related_name="previous_stop")

	@property
	def route_journey():
		last_stop = self
		while (last_stop.journey == null):
			last_stop = last_stop.previous_stop
		return last_stop.journey

	def add_next_stop(stop):
		if stop.time >= time:
			next_stop = stop
		else:
			raise
