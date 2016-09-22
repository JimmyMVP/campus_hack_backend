import requests
import json
import random

from django.core.cache import cache
from realestate_api import genetics as g

import pdb


#Out REST service keys
rest_keys = [
    "summary",
    "net_cold_return",
    "square_meters",
    "rented",
    "cold_rent",
    "pot_rent_per_sm",
    "number_of_apartments",
    "number_of_rooms",
    "rent"
]


sorting_key = lambda x : (-x["rating"], -float(x["pot_rent_per_sm"]),float(x["price"]), x["construction_year"])



#Returns the best options on the market, takes the list of the houses
def rate(houses):

#Property type, room_number,size_min,size_max, price_min, price_max


    #Calculate average rent
    avg = 0.
    count = 0
    for rent in houses:
        count+=1
        avg+=rent["rent"] 
    avg = avg / count


    for house in houses:
        house["pot_rent_per_sm"] = avg / house["rent"]
        house["net_cold_return"] = house["cold_rent"] / house["price"]
    
   
    print(100*"-")
    for house in houses:
        print((house["pot_rent_per_sm"], house["price"], house["construction_year"]))

        ncr = house["net_cold_return"]*100
        rating = 0
        if(ncr < 2):
            rating = 1
        elif(ncr < 4):
            rating = 2
        elif(ncr < 6):
            rating = 3
        elif(ncr < 8):
            rating = 4
        else:
            rating = 5

        house["rating"] = rating
        house["net_cold_return"] = ncr
    
    houses = sorted(houses, key = sorting_key)


    return houses


#Adding some value to the data
def format_response(d):

    d["avg_user_queries"] = random.randrange(30, 400)
    d["avg_add_expiration"] = random.randrange(1,30)
    d["rent_trend_3months"] = random.randrange(-1,2)
    d["new_house_offerings_trend"] = random.randrange(-1,2)

    for num in range(0 ,len(d["listings"])):
        fake = d["listings"][num]

        stored = cache.get(fake["lister_url"])
        if(stored != None):
            d["listings"][num] = stored

        if fake["construction_year"] == 0:
            fake["construction_year"] = random.randrange(1990, 2016)
        if fake["img_url"] == "http://resources.nestimg.com/nestoria/img/cs4.2_v1.png":
            fake["img_url"] = "http://t2.gstatic.com/images?q=tbn:ANd9GcRliOf6pVeiyHjwS2_BN3sdKh_ak3VEQ4d_AfPdF6gFSYk9nKKu8qSO"
        if fake["thumb_url"] == "http://resources.nestimg.com/nestoria/img/cs4.2_v1.png":
            fake["thumb_url"] = "http://t2.gstatic.com/images?q=tbn:ANd9GcRliOf6pVeiyHjwS2_BN3sdKh_ak3VEQ4d_AfPdF6gFSYk9nKKu8qSO"
        if fake["listing_type"] == "buy":
            if random.randrange(0,2) > 0:
                if random.randrange(0,2) > 0:
                    fake["rented"] = 1
                else:
                    fake["rented"] = 0

            else:
                fake["listing_type"] = "rent"
                fake["rent"] = fake["price"] / random.random()
                fake["price_high"] = fake["price"]
        if fake["size"] == 0:
            if fake["property_type"] == "flat":
                fake["size"] = random.randrange(70, 120)
            else:
                fake["size"] = random.randrange(90, 180)
        fake["ppsm"] = fake["price"] / fake["size"]
        fake["rent"] = fake["price"] / (6 + random.random()*20)
        fake["cold_rent"] = fake["rent"]
        fake["rent_per_sm"] = (fake["rent"] / fake["size"])
        fake["number_of_apartments"] = 1



        #Removing unnecessary things and renaming
        fake["square_meters"] = fake["size"]
        
        filtered = {

            "price" : fake["price"],
            "rent" : fake["rent"],
            "construction_year" : fake["construction_year"],
            "cold_rent" : fake["rent"],
            "img_url" : fake["img_url"],
            "latitude" : fake["latitude"],
            "longitude" : fake["longitude"]

        }
        for key in rest_keys:
            if(key in fake):
                filtered[key] = fake[key]

        d["listings"][num] = filtered

        cache.add(fake["lister_url"], fake)

    return d





def other_options(params):

    ne = (53.561577, 14.046648)
    sw = (47.784556, 7.858369)


    other = []

    for i in range(0,5):

        neapi = (round((ne[0] - sw[0])*random.random() + sw[0], 6), round((ne[1] - sw[1])*random.random() + sw[1], 6))
        swapi = (round((neapi[0] - sw[0])*random.random() + sw[0], 6), round((neapi[1] - sw[1])*random.random(), 6))

        params["south_west"] = "%f,%f" %(swapi[0], swapi[1])
        params["north_east"] = "%f,%f"  %(neapi[0], neapi[1])


        #Call to the astoria API
        response = requests.get("http://api.nestoria.de/api?", params = params)
        d = json.loads(response.text)

        d = format_response(d["response"])

        #Extend with top 5 of this group
        other.extend(rate(d["listings"]))

    return sorted(other, key=sorting_key)


def create_packages(houses, budget):
    solutions = []
    g.find_packages([], houses, budget, solutions)
    return solutions




