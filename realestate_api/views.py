from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view


from django.core.cache import cache


import requests
import json


API_KEY = "AIzaSyDrwomkGD3UmrS-M3nO4reGRAJiLEk78PY"


params = {
"size": "600x300",
"location": "46.414382,10.013988",
"heading": 151.78,
"pitch": -0.76,
"key": API_KEY,


}

street_view = "https://maps.googleapis.com/maps/api/streetview"




@api_view(['GET'])
def get_realestates(request, format=None):

    params = {
    
        "action" : "search_listings",
        "encoding" : "json",

    }


    print(request.GET.values())
    for key, value in request.GET.items():
        params[key] = value


    response = requests.get("http://api.nestoria.de/api?", params = params)

    d = json.loads(response.text)

    lat, lon = d["response"]["listings"][0]["latitude"], d["response"]["listings"][0]["longitude"]
    url = d["response"]["listings"][0]["lister_url"]

    params_google = {

        "size" : "600x300",
        "location" : "%d,%d" %(lat, lon),
        "heading" : 151.78,
        "pitch" : -0.76,
        "key" : API_KEY,

    }

    google_resp = requests.get(street_view, params_google)

    cache.add(url, google_resp.content)
    print("Cached image: "  + google_resp.text)

    d["response"]["streetview_image"] = url 


    return Response(d)



@api_view(['GET'])
def test(request, format=None):
    return Response("Alles in Ordnung!")



@api_view(['POST'])
def get_streetview(request, format=None):

    key = request.json["key"]
    print(key)

    img = cache.get(key)

    return Response(img)





