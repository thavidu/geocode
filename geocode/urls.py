from django.conf.urls import url
from django.http import HttpResponseRedirect

import views

urlpatterns = [
	url(r'^help/$', views.HelpView.as_view(), name='help'),
	url(r'^resolve/(?P<address>.+)$', views.resolve, name="resolve"),
	url(r'^$', lambda r: HttpResponseRedirect('help')),
]
