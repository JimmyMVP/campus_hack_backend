import requests
import json


API_KEY = "AIzaSyDrwomkGD3UmrS-M3nO4reGRAJiLEk78PY"
street_view = "https://maps.googleapis.com/maps/api/streetview"



params = {
"size" : "600x300",
"location" : "46.414382,10.013988",
"heading" : 151.78,
"pitch" : -0.76,
"key" : API_KEY,


}



resp = requests.get(street_view, params = params)

print(resp.text)
