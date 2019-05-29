# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse

# Create your views here.

from api import geocode

#For showing the docs
class HelpView(generic.TemplateView):
	template_name = 'geocode/docs.html'

def resolve(request, address):
	result = geocode(address)
	return JsonResponse(result)
