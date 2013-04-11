from django.conf.urls import patterns, include, url
import timetableData.views
urlpatterns = patterns('',
	(r"^one_journey/?$", timetableData.views.one_journey),
	(r"^get_nearest/?$", timetableData.views.get_nearest),
	(r"^five_day/?$", timetableData.views.five_days),
)