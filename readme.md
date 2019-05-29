A simple json-based REST service for geocoding given addresses. It utilizes the [HERE service](https://developer.here.com/documentation/geocoder/topics/quick-start-geocode.html) upstream and falls back to [Google Maps](https://developers.google.com/maps/documentation/geocoding/start) if the HERE service either fails or does not return a result.

# Requirements

This service targets python2.7, and its only optional dependency is django<2

Obtain your own API keys for the HERE and GMAPS services from the links below, and then place them inside geocode/keys.py
* https://developer.here.com/documentation/geocoder/topics/quick-start-geocode.html?create=Freemium-Basic&keepState=true&step=account
* https://developers.google.com/maps/documentation/geocoding/start#get-a-key

# Usage

## Django version

First start the server by running
```
python manage.py runserver
```
Then go to the given server/port url (default being <127.0.0.1:8000>) and append your address query as follows
```
http://127.0.0.1:8000/geocode/resolve/<ADDRESS QUERY>
```
eg. <http://127.0.0.1:8000/geocode/resolve/San+Francisco>

## Command line version

```
python cmdline.py <ADDRESS QUERY>
```
eg. python cmdline.py 1600 Pennsylvania Avenue, Washington DC

## Standalone http version

This version doesn't take a dependency on Django, and its used the same way as the Django version is described above, except you run the server with
```
python simple.py
```

# Results format

The service returns results in JSON format. The most relevant result is provided in the first level, with its lat and lng coordinates given.
Also returned is the full address that the given address query was resolved to, it is strongly suggested this is displayed back to the user as confirmation.
```
{
	"lat": 51.5232439,
	"resolved_address": "221B Baker Street, London, NW1 6, United Kingdom",
	"lng": -0.1582649
}
```
If multiple address matches are returned, additional addresses will be available in the 'other_results' variable
```
{
	"lat": 38.89768,
	"resolved_address": "1600 Pennsylvania Ave NW, Washington, DC 20500, United States",
	"lng": -77.03655,
	other_results: [
		{
			"lat": 38.87912,
			"resolved_address": "1600 Pennsylvania Ave SE, Washington, DC 20003, United States",
			"lng": -76.98178
		}
	]
}
```
If either no results are returned, an message is returned instead:
```
{
	"message": "No matching results found"
}
```
or if there is an error in both the upstream services (including the fallback), an error message is returned:
```
{
	"error": "Error utilizing upstream services"
}
```
