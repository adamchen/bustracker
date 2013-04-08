from django import forms
from timetableData.models import *
import timetableData.query
from django.shortcuts import render
from django.contrib.localflavor.gb.forms import GBPostcodeField


import datetime
# Create your views here.
def one_journey(request):
	if request.method == 'POST':
		stops_form = PickStops(request.POST)
		if stops_form.is_valid():
			source = stops_form.cleaned_data['source']
			destination = stops_form.cleaned_data['destination']
			date = stops_form.cleaned_data['date']
			time = stops_form.cleaned_data['time']
			stops = timetableData.query.get_from([source], destination, time, date.weekday())
			important_stops = [source]
			important_stops.append(destination)
			stops = timetableData.query.reduce_routes(important_stops, stops)
			return render(request,"bus_stop_to.html", {"bus_stop_form" : stops_form, "stops" : stops})
	stops_form = PickStops()
	return render(request,"bus_stop_to.html", {"bus_stop_form" : stops_form})

def get_nearest(request):
	if request.method == 'POST':
		nearest_form = GetNearestStops(request.POST)
		if nearest_form.is_valid():
			postcode = nearest_form.cleaned_data['postcode']
			lat, lng = timetableData.query.get_lat_long(postcode)
			nearest_stops = timetableData.query.get_nearest_stops(lat, lng)
			return render(request, "get_stops_from_postcode.html", {"stops" : nearest_stops, "nearest_form" : nearest_form})
	nearest_form = GetNearestStops()
	return render(request, "get_stops_from_postcode.html", {"nearest_form" : nearest_form})

class BusStopModelFormChoice(forms.ModelChoiceField):
	def label_from_instance(self,obj):
		if not isinstance(obj, BusStop):
			raise
		return obj.name

class PickStops(forms.Form):
	source = BusStopModelFormChoice(queryset=BusStop.objects.all(), label="From: ")
	destination = BusStopModelFormChoice(queryset=BusStop.objects.all(), label="To: ")

	date = forms.DateField(initial=datetime.date.today(), label="Date: ")
	time = forms.TimeField(initial=datetime.time(7,0,0), label="Arrival by: ")

class GetNearestStops(forms.Form):
	postcode = GBPostcodeField(label="Postcode: ")
