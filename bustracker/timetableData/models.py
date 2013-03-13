from django.db import models
from geoposition.fields import GeopositionField

# Create your models here.

class BusRoute(models.Model):
	name = models.CharField(length=250)
	operator = models.ForeignKey(Operator, related_name="bus_services")
	
class Operator(models.Model):
	name = models.CharField(length=250)
	
class RouteJourney(models.Model):
	first_stop = models.OneToOneField(RouteStop)
	weekdays = models.BooleanField(default=false)
	saturdays = models.BooleanField(default=false)
	sunday = models.BooleanField(default=false)

	@property
	def get_stops():
		stops = []
		if (first_stop != null):
			stops.append(first_stop)
			last_stop = first_stop
			while (last_stop != null):
				stops.append(last_stop)
				last_stop = last_stop.next_stop
			

class RouteStop(models.Model):
	stop = models.ForeignKey(BusStop, related_name="route_stops")
	journey = models.ForeignKey(RouteJourney, related_name="route_stops")
	time = models.TimeField()
	next_stop = models.OneToOneField(RouteStop, related_name="previous_stop")

	def add_next_stop(stop):
		if stop.time >= time:
			next_stop = stop
		else:
			raise

class BusStop(models.Model):
	location = GeopositionField()
	name = models.CharField(length=250)	
