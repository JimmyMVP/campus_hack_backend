import requests
import json
import random



data = open("./data", "r")

data = data.read()



#Returns the best options on the market, takes the list of the houses
def rate(houses):

#Property type, room_number,size_min,size_max, price_min, price_max 

    to_rent = filter(lambda x: x["listing_type"] == "rent", houses)
    houses = sorted(houses, key = lambda x: (x["price_high"], x["size"]))


    #Calculate average rent
    avg = 0.
    for rent in to_rent:
        avg += rent["price_high"]
    avg = avg / (len(to_rent)+1)


    for house in houses:
        house["average_rent"] = avg


    print("To rent: " + str(len(to_rent)))

    #Return top 5
    return houses[0:5]

def other_options():

    ne = (53.561577, 14.046648)
    sw = (47.784556, 7.858369)


    other = []

    for i in range(0,5):

        neapi = (round((ne[0] - sw[0])*random.random() + sw[0], 6), round((ne[1] - sw[1])*random.random() + sw[1], 6))
        swapi = (round((neapi[0] - sw[0])*random.random() + sw[0], 6), round((neapi[1] - sw[1])*random.random(), 6))
        params = {

            "action" : "search_listings",
            "encoding" : "json", 
            "south_west" : "%f,%f" %(swapi[0], swapi[1]),
            "north_east" : "%f,%f" %(neapi[0], neapi[1])
        }


        #Call to the astoria API
        response = requests.get("http://api.nestoria.de/api?", params = params)
        d = json.loads(response.text)
        #Extend with top 5 of this group
        other.extend(rate(d["response"]["listings"]))

    print(other)  
    return other

other_options()
#rate(json.loads(data)["response"]["listings"])