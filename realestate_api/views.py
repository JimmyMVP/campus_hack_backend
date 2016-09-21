from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view


from django.core.cache import cache


import requests
import json


#Function to get and  filter the immobilia
@api_view(['GET'])
def get_realestates(request, format=None):

    params = {
    
        "action" : "search_listings",
        "encoding" : "json",

    }


    for key, value in request.GET.items():
        params[key] = value


    #Call to the astoria API
    response = requests.get("http://api.nestoria.de/api?", params = params)


    #TODO filter the results based on how good they are


    d = json.loads(response.text)

    return Response(d)


#Testing function
@api_view(['GET'])
def test(request, format=None):
    return Response("Alles in Ordnung!")



#Function fro getting street view from cache
@api_view(['GET'])
def get_streetview(request, format=None):

    key = request.GET["key"]
    print("This is the key: " + key)

    img = cache.get(key)

    print("And this is the image: " + str(img))

    return Response(img)





