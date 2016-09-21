from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view

import requests
import json



@api_view(['GET'])
def get_realestates(request, format=None):

    params = {
    
        "action" : "search_listings",
        "encoding" : "json",
        "foo" : "bar",
        "place_name" : "karlsruhe"

    }



    response = requests.get("http://api.nestoria.de/api?", params = params)

    d = json.loads(response.text)

    print(response.text)

    return Response(d)








