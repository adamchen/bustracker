from django import forms
from timetableData.models import *
import timetableData.query
from django.shortcuts import render
from django.contrib.localflavor.gb.forms import GBPostcodeField
from collections import namedtuple


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
		return render(request,"bus_stop_to.html", {"bus_stop_form" : stops_form})
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
		return render(request, "get_stops_from_postcode.html", {"nearest_form" : nearest_form})
	nearest_form = GetNearestStops()
	return render(request, "get_stops_from_postcode.html", {"nearest_form" : nearest_form})

def five_days(request):
	time_fields = ["mon_morn", "mon_eve", "tue_morn", "tue_eve", "wed_morn", "wed_eve", "thu_morn", "thu_eve", "fri_morn", "fri_eve"]
	if request.method == 'POST':
		postcode_form = GetNearestStops(request.POST)
		five_day_form = FiveDayForm(request.POST)
		if five_day_form.is_valid() and postcode_form.is_valid():
			TimePeriod = namedtuple("TimePeriod", ["time", "title", "routes", "slug"])
			time_period_times = [
								TimePeriod(time=five_day_form.cleaned_data["mon_morn"], title="Monday To",slug="mon_morn",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["mon_eve"],  title="Monday Back",slug="mon_eve",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["tue_morn"], title="Tuesday To",slug="tue_morn",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["tue_eve"],  title="Tuesday Back",slug="tue_eve",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["wed_morn"], title= "Wednesday To",slug="wed_morn",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["wed_eve"],  title="Wednesday Back",slug="wed_eve",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["thu_morn"], title="Thursday To",slug="thu_morn",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["thu_eve"],  title="Thursday Back",slug="thu_eve",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["fri_morn"], title="Friday To",slug="fri_morn",routes=None),
								TimePeriod(time=five_day_form.cleaned_data["fri_eve"],  title="Friday Back",slug="fri_eve",routes=None),
								]
			lat, lng = timetableData.query.get_lat_long(postcode_form.cleaned_data["postcode"])
			source_stops = timetableData.query.get_nearest_stops(lat, lng)
			destination = BusStop.objects.get(pk=19) #Hardcoded university stop
			important_stops = source_stops + [destination]
			for i in range(0,10):
				if i % 2 == 0:
					time_period_times[i] = time_period_times[i]._replace(routes=timetableData.query.reduce_routes(important_stops,timetableData.query.get_from(source_stops,destination,time_period_times[i].time,0)))
				else:
					time_period_times[i] = time_period_times[i]._replace(routes=timetableData.query.reduce_routes(important_stops,timetableData.query.get_from(destination,source_stops,time_period_times[i].time,0,arrival=False)))
			return render(request, "five_day.html", {"postcode_form" : postcode_form, "five_day_form" : five_day_form, "route_data" : time_period_times, "time_fields" : time_fields})
		return render(request, "five_day.html", {"postcode_form" : postcode_form, "five_day_form" : five_day_form, "time_fields" : time_fields})
	postcode_form = GetNearestStops()
	five_day_form = FiveDayForm()
	return render(request, "five_day.html", {"postcode_form" : postcode_form, "five_day_form" : five_day_form, "time_fields" : time_fields})

class FiveDayForm(forms.Form):
	mon_morn = forms.TimeField(initial=datetime.time(9,0,0),widget=forms.TimeInput(format='%H:%M'), label="To")
	mon_eve = forms.TimeField(initial=datetime.time(17,15,0),widget=forms.TimeInput(format='%H:%M'), label="Back")

	tue_morn = forms.TimeField(initial=datetime.time(9,0,0),widget=forms.TimeInput(format='%H:%M'), label="To")
	tue_eve = forms.TimeField(initial=datetime.time(17,15,0),widget=forms.TimeInput(format='%H:%M'), label="Back")

	wed_morn = forms.TimeField(initial=datetime.time(9,0),widget=forms.TimeInput(format='%H:%M'), label="To")
	wed_eve = forms.TimeField(initial=datetime.time(17,15,0),widget=forms.TimeInput(format='%H:%M'), label="Back")

	thu_morn = forms.TimeField(initial=datetime.time(9,0,0),widget=forms.TimeInput(format='%H:%M'), label="To")
	thu_eve = forms.TimeField(initial=datetime.time(17,15,0),widget=forms.TimeInput(format='%H:%M'), label="Back")

	fri_morn = forms.TimeField(initial=datetime.time(9,0,0),widget=forms.TimeInput(format='%H:%M'), label="To")
	fri_eve = forms.TimeField(initial=datetime.time(17,15,0),widget=forms.TimeInput(format='%H:%M'), label="Back")


class BusStopModelFormChoice(forms.ModelChoiceField):
	def label_from_instance(self,obj):
		if not isinstance(obj, BusStop):
			raise
		return obj.name

class PickStops(forms.Form):
	source = BusStopModelFormChoice(queryset=BusStop.objects.all(), label="From")
	destination = BusStopModelFormChoice(queryset=BusStop.objects.all(), label="To")

	date = forms.DateField(initial=datetime.date.today(), label="Date")
	time = forms.TimeField(initial=datetime.time(9,0,0), label="Arrival by")

class GetNearestStops(forms.Form):
	postcode = GBPostcodeField(label="Postcode")