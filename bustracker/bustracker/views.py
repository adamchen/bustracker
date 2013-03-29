from django.views.generic import TemplateView
from django.shortcuts import render


#from timetableData.models import


def homepage(request):
	return render(request, "home.html")

def about(request):
	return render(request, "about.html")