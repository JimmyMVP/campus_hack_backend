import requests
import json


params = {
    
    "action" : "echo",
    "encoding" : "json",
    "foo" : "bar",

}
#response = requests.get("http://api.nestoria.co.uk/api?", params = params)


params = {
    
    "action" : "search_listings",
    "encoding" : "json",
    "foo" : "bar",
    "place_name" : "karlsruhe"

}

response = requests.get("http://api.nestoria.de/api?", params = params)


print(response.text)