from django import forms
from timetableData.models import *
import timetableData.query
from django.shortcuts import render

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
			return render(request,"bus_stop_to.html", {"bus_stop_form" : stops_form, "stops" : timetableData.query.get_from([source], destination, time, date.weekday())})
	stops_form = PickStops()
	return render(request,"bus_stop_to.html", {"bus_stop_form" : stops_form})

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