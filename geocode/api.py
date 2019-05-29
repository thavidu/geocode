import json
import urllib
import urllib2
from keys import *

def here_query(address):
	safe_address = urllib.quote(address)
	try:
		here_url = "https://geocoder.api.here.com/6.2/geocode.json?app_id=%s&app_code=%s&searchtext=%s" % (HERE_APP_ID, HERE_APP_CODE, safe_address)
		req = urllib2.Request(url=here_url)
		f = urllib2.urlopen(req)
		response = f.read()
	except urllib2.HTTPError, e:
		print "Error with HERE API", e
		return -1
	# response = '{"Response":{"MetaInfo":{"Timestamp":"2019-05-27T23:29:50.480+0000"},"View":[{"_type":"SearchResultsViewType","ViewId":0,"Result":[{"Relevance":1.0,"MatchLevel":"houseNumber","MatchQuality":{"City":1.0,"Street":[0.9],"HouseNumber":1.0},"MatchType":"pointAddress","Location":{"LocationId":"NT_Opil2LPZVRLZjlWNLJQuWB_0ITN","LocationType":"point","DisplayPosition":{"Latitude":41.88432,"Longitude":-87.63877},"NavigationPosition":[{"Latitude":41.88449,"Longitude":-87.63877}],"MapView":{"TopLeft":{"Latitude":41.8854442,"Longitude":-87.64028},"BottomRight":{"Latitude":41.8831958,"Longitude":-87.63726}},"Address":{"Label":"425 W Randolph St, Chicago, IL 60606, United States","Country":"USA","State":"IL","County":"Cook","City":"Chicago","District":"West Loop","Street":"W Randolph St","HouseNumber":"425","PostalCode":"60606","AdditionalData":[{"value":"United States","key":"CountryName"},{"value":"Illinois","key":"StateName"},{"value":"Cook","key":"CountyName"},{"value":"N","key":"PostalCodeType"}]}}}]}]}}'
	try:
		jdict = json.loads(response)
		results = list()
		if not jdict['Response']['View']:
			return results
		for match in jdict['Response']['View'][0]['Result']:
			result = {'resolved_address': match['Location']['Address']['Label'],
					'lat': match['Location']['DisplayPosition']['Latitude'],
					'lng': match['Location']['DisplayPosition']['Longitude']}
			results.append(result)
	except:
		print "Error parsing HERE response, upstream service may have changed."
		return -1
	return results

def gmaps_query(address):
	safe_address = urllib.quote(address)
	try:
		gmaps_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (safe_address,GMAPS_API_KEY)
		req = urllib2.Request(url=gmaps_url)
		f = urllib2.urlopen(req)
		response = f.read()
	except urllib2.HTTPError, e:
		print "Error with GMAPS API", e
		return -1
	# response = '{\n   "results" : [\n      {\n         "address_components" : [\n            {\n               "long_name" : "425",\n               "short_name" : "425",\n               "types" : [ "street_number" ]\n            },\n      {\n               "long_name" : "West Randolph Street",\n               "short_name" : "W Randolph St",\n              "types" : [ "route" ]\n            },\n            {\n               "long_name" : "West Loop",\n              "short_name" : "West Loop",\n               "types" : [ "neighborhood", "political" ]\n },\n            {\n               "long_name" : "Chicago",\n               "short_name" : "Chicago",\n      "types" : [ "locality", "political" ]\n            },\n            {\n               "long_name" : "Cook County",\n               "short_name" : "Cook County",\n               "types" : [ "administrative_area_level_2", "political" ]\n            },\n            {\n               "long_name" : "Illinois",\n               "short_name" : "IL",\n               "types" : [ "administrative_area_level_1", "political" ]\n            },\n   {\n               "long_name" : "United States",\n               "short_name" : "US",\n               "types" : [ "country", "political" ]\n            },\n            {\n               "long_name" : "60606",\n    "short_name" : "60606",\n               "types" : [ "postal_code" ]\n            },\n            {\n       "long_name" : "1515",\n               "short_name" : "1515",\n               "types" : [ "postal_code_suffix" ]\n            }\n         ],\n         "formatted_address" : "425 W Randolph St, Chicago, IL 60606, USA",\n         "geometry" : {\n            "location" : {\n               "lat" : 41.884179,\n               "lng" : -87.63884899999999\n            },\n            "location_type" : "ROOFTOP",\n            "viewport" : {\n         "northeast" : {\n                  "lat" : 41.88552798029149,\n                  "lng" : -87.6375000197085\n               },\n               "southwest" : {\n                  "lat" : 41.88283001970849,\n        "lng" : -87.6401979802915\n               }\n            }\n         },\n         "place_id" : "ChIJK7itjMcsDogRbvEVSJYgYT8",\n         "plus_code" : {\n            "compound_code" : "V9M6+MF Chicago, Illinois, United States",\n            "global_code" : "86HJV9M6+MF"\n         },\n         "types" : [ "street_address" ]\n   }\n   ],\n   "status" : "OK"\n}\n'
	try:
		jdict = json.loads(response)
		results = list()
		for match in jdict['results']:
			result = {'resolved_address': match['formatted_address'],
					'lat': match['geometry']['location']['lat'],
					'lng': match['geometry']['location']['lng']}
			results.append(result)
	except:
		print "Error parsing GMAPS response, upstream service may have changed."
		raise
		return -1
	return results

def geocode(address):
	final = dict()
	results = here_query(address)
	if not results or results == -1:
		print "Falling back to GMAPS"
		results = gmaps_query(address)
	if not results:
		final['message'] = 'No matching results found'
	elif results == -1:
		final['error'] = 'Error utilizing upstream services'
	else:
		final = results[0]
		if len(results) > 1:
			final['other_results'] = results[1:]
	return final
