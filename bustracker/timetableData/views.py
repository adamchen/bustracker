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
	else:
		stops_form = PickStops()
		return render(request,"bus_stop_to.html", {"bus_stop_form" : stops_form})
class PickStops(forms.Form):
	source = forms.ModelChoiceField(queryset=BusStop.objects.all())
	destination = forms.ModelChoiceField(queryset=BusStop.objects.all())

	date = forms.DateField(initial=datetime.date.today())
	time = forms.TimeField(initial=datetime.time(7,0,0))