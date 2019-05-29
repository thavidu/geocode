A simple json-based REST service for geocoding given addresses

# Requirements

This service targets python2.7, and its only optional dependency is django<2

# How to run

## Django version

First start the server by running
```
python manage.py runserver
```
Then go to the given server/port url (default being <127.0.0.1:8000>) and append your address query as follows
```
http://127.0.0.1:8000/geocode/resolve/<ADDRESS QUERY>
```
eg. <http://127.0.0.1:8000/geocode/resolve/San Francisco>

## Command line version

```
python cmdline.py <ADDRESS QUERY>
```
eg. python cmdline.py 1600 Pennsylvania Avenue, Washington DC

