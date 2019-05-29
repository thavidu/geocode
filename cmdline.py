import sys
from geocode.api import geocode

if __name__ == "__main__":
	if len(sys.argv) > 1:
		address = " ".join(sys.argv[1:])
		print "Using address", address
	else:
		print "Must provide address in arguments"
		exit()

	print geocode(address)
