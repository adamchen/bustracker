from django.db import models
from geoposition.fields import GeopositionField

def new_bus_stop(name, bearing, lat, lon):
	bus_stop = BusStop.objects.create(name=name,bearing=bearing)
	bus_stop.location.latitude = lat
	bus_stop.location.longitude = lon
	bus_stop.save()
	return bus_stop

def add_journies(route, fileName, weekdays, saturdays, sundays, stops):
	import csv
	with open(fileName, "rb") as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar="\"")
		for row in reader:
			journey = RouteJourney.objects.create(weekdays=weekdays,saturdays=saturdays,sunday=sundays,route=route)
			last_stop = None
			data = row[0].split("\t")
			print data
			for i in range(0,len(data)-1):
				stop = RouteStop.objects.create(stop=stops[i], time = timeFormat(data[i]))	
				if (last_stop is not None):
					last_stop.next_stop = stop
					last_stop.save()
				else:
					journey.first_stop = stop
					journey.save()
				last_stop = stop
def timeFormat(time):
	return time[:2] + ":" + time[2:]

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
		return u"at stop {} at time {}. Next stop: {}".format(self.stop, self.time, self.next_stop if self.next_stop is not None else "END OF LINE")

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
