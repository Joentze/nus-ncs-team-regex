from geopy.geocoders import Nominatim

class geocode:
    def __init__(self, user_agent = "regex"):
        self.geolocator = Nominatim(user_agent = user_agent)

    async def forward(self, address):
        """Forward Geocodes from address

        Args:
            string: Name address of the location.

        Returns:
            string: latitude of location, longitude of location
        """
        location = self.geolocator.geocode(address)

        if location: 
            return f"{location.latitude}, {location.longitude}"
        else:
            return "Coordinates not found"

    async def reverse(self, coords):
        """Revese Geocodes from coordinations

        Args:
            string: latitude of location
            string: longitude of location

        Returns:
            string: Name address of the location.
        """
        location = self.geolocator.reverse(coords)

        if location: 
            return f"{location.address}"
        else:
            return "Location not found"
        
