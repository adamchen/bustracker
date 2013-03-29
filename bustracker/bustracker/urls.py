from django.conf.urls import patterns, include, url
import timetableData.urls
import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bustracker.views.home', name='home'),
    # url(r'^bustracker/', include('bustracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^/?$', views.homepage),
	url(r'^index.html/?$', views.homepage),
	url(r'^about.html/?$', views.about),
	url(r'^timetableData/', include(timetableData.urls)),
)
