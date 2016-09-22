import requests
import json
import random

from django.core.cache import cache

#data = open("./data", "r")

#data = data.read()

#Genetics
mutation_rate = 0.2
crossover_rate = 0.2

sorting_key = lambda x : (x["ppsm"],x["price"], x["construction_year"])



<<<<<<< HEAD
=======


#Property type, room_number,size_min,size_max, price_min, price_max 
    print(houses)
    to_rent = list(filter(lambda x: x["listing_type"] == "rent", houses))
    houses = list(filter(lambda x: x["listing_type"] == "buy", houses))
>>>>>>> 654ca6707ff4b45ed5d787c9245a83aa69cd7782


#Returns the best options on the market, takes the list of the houses
def rate(houses):

#Property type, room_number,size_min,size_max, price_min, price_max

    houses = sorted(houses, key = sorting_key)


    #Calculate average rent
    avg = 0.
    for rent in to_rent:
        avg += rent["price_high"]
    avg = avg / (len(to_rent)+1)


    for house in houses:
        house["average_rent"] = avg


    #Return top 5
    return houses[0:5]


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
                    fake["rented_out"] = 1
                else:
                    fake["rented_out"] = 0
            else:
                fake["listing_type"] = "rent"
                fake["price_low"] = fake["price"] / 500
                fake["price_high"] = fake["price"]
        if fake["size"] == 0:
            if fake["property_type"] == "flat":
                fake["size"] = random.randrange(70, 120)
            else:
                fake["size"] = random.randrange(90, 180)
        fake["ppsm"] = fake["price"] / fake["size"]
        fake["kaltmiete"] = fake["price_high"] - (random.randrange(0,5) * fake["price_high"] / 100)
        d["listings"][num] = fake

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

    print(other)
    return other


#houses = json.loads(data)["response"]["listings"]



#d = format_response(json.loads(data))
#print(rate(d["response"]["listings"]))
