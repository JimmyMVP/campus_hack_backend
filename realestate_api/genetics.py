def find_packages(chosen, houses, budget, solutions):

    if(len(houses) <= 2):
        return

    candidate = houses[0]


    if(len(solutions) > 10):
        return
    
    cost =  sum([x["price"] for x in chosen])

    find_packages(chosen, houses[1:], budget, solutions)
    chosen.append(houses[0])
    find_packages(chosen[:], houses[1:], budget, solutions)

    if(cost < budget and len(chosen) > 1):
        solutions.append(chosen)
    else:
        return





