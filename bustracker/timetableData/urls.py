from django.conf.urls import patterns, include, url
import timetableData.views
urlpatterns = patterns('',
	(r"^one_journey/?$", timetableData.views.one_journey),
)