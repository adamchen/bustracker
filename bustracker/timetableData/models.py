from django.db import models
from geoposition.fields import GeopositionField
import math
from decimal import *

class Operator(models.Model):
	name = models.CharField(max_length=250)
	def __unicode__(self):
		return u"Operator: {}".format(self.name)

class BusRoute(models.Model):
	name = models.CharField(max_length=250)
	operator = models.ForeignKey(Operator, related_name="bus_services")
	def __unicode__(self):
		return u"BusRoute {} - operator {}".format(self.name,self.operator)

class BusStop(models.Model):
	location = GeopositionField()
	bearing = models.CharField(max_length=2)
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return u"BusStop {}, bearing: {}, location: {}".format(self.name,self.bearing,self.location)
	def distance_from(self,lat, lon):
	#We'll assume that 1 degree lat = 1 degree lon in terms of distance
	#Not actually true, but good enough for our scale.	
		return math.sqrt((Decimal(lat)-self.location.latitude)**2 + (Decimal(lon)-self.location.longitude)**2)

class RouteJourney(models.Model):
	first_stop = models.OneToOneField('RouteStop', related_name="journey",null=True)
	weekdays = models.BooleanField(default=False)
	saturdays = models.BooleanField(default=False)
	sunday = models.BooleanField(default=False)
	route = models.ForeignKey(BusRoute, related_name="routeJournies",null=True)
	
	def __unicode__(self):
		return u"RouteJourney on route {}. Availability: {} {} {}. First Stop: {}".format(self.route, self.weekdays, self.saturdays, self.sunday, self.first_stop)
	@property
	def stop(self):
		stops = []
		last_stop = first_stop
		while last_stop is not None:
			stops.append(last_stop)
			last_stop = last_stop.next_stop
		return stops

class RouteStop(models.Model):
	stop = models.ForeignKey(BusStop, related_name="route_stops")
	time = models.TimeField()
	next_stop = models.OneToOneField('RouteStop', related_name="previous_stop", null=True)
	
	def __unicode__(self):
		return u"at stop {} at time {}. {}".format(self.stop, self.time, "NEXT STOP: "+self.next_stop if self.next_stop is not None else "END OF LINE")

	@property
	def route_journey(self):
		last_stop = self
		while last_stop.journey is None:
			last_stop = last_stop.previous_stop
		return last_stop.journey

	def add_next_stop(stop):
		if stop.time >= time:
			next_stop = stop
		else:
			raise
