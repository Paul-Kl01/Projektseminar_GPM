from functools import partial
from geopy.geocoders import Nominatim # Openstreatmaps 

class Location: 
    def __init__(self, location): 
        self.location = location
    
    ## return Postleitzahl
    def getPostalCode(self):
        geolocator = Nominatim(user_agent="LocationApiPruefen")
        geocode = partial(geolocator.geocode, language="de")
        postleitzahl = geocode(self.location).raw.get("display_name")
        x_split = postleitzahl.split(", ")
        post_sub = x_split[4]
        print(post_sub)
        
        return post_sub

## Testing 
l1 = Location("Langenweddingen")
l1.getPostalCode()