from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view


from django.core.cache import cache
from django.shortcuts import render


import requests
import json
import random


MAPS_API_KEY = 'AIzaSyDBs7baI6Lq4B2A5sDtVVoFyhPOP6VBXLY'
random.seed()


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


    listings_info = format_response(response)

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

@api_view(['GET'])
def get_map(request):

    return render(request, "map.html", {})


def format_response(response):

    d = json.loads(response.text)


    d["response"]["avg_user_queries"] = random.randrange(30, 400)
    d["response"]["avg_add_expiration"] = random.randrange(1,30)
    d["response"]["rent_trend_3months"] = random.randrange(-1,2)
    d["response"]["new_house_offerings_trend"] = random.randrange(-1,2)

    for fake in d["response"]["listings"]:
        if fake["construction_year"] == 0:
            fake["construction_year"] = random.randrange(1990, 2016)
        if fake["img_url"] == "http://resources.nestimg.com/nestoria/img/cs4.2_v1.png":
            fake["img_url"] = "http://t2.gstatic.com/images?q=tbn:ANd9GcRliOf6pVeiyHjwS2_BN3sdKh_ak3VEQ4d_AfPdF6gFSYk9nKKu8qSO"
        if fake["thumb_url"] == "http://resources.nestimg.com/nestoria/img/cs4.2_v1.png":
            fake["thumb_url"] = "http://t2.gstatic.com/images?q=tbn:ANd9GcRliOf6pVeiyHjwS2_BN3sdKh_ak3VEQ4d_AfPdF6gFSYk9nKKu8qSO"
        if fake["listing_type"] == "buy":
            if random.randrange(0,2) > 0:
                fake["listing_type"] = "buy"
            else:
                fake["listing_type"] = "rent"
                fake["price"] = fake["price"] / 500
                fake["price_low"] = fake["price"]
                fake["price_high"] = fake["price"]
        if fake["size"] == 0:
            if fake["property_type"] == "flat":
                fake["size"] = random.randrange(70, 120)
            else:
                fake["size"] = random.randrange(90, 180)

    return d
