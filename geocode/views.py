# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse

# Create your views here.

#For showing the docs
class HelpView(generic.TemplateView):
	template_name = 'geocode/docs.html'

def resolve(request, address):
	return JsonResponse({"lat": 123, "long": 456})
