solutions = []


def find_packages(chosen, houses, budget):
    global solutions

    if(len(houses) <= 2):
        return

    candidate = houses[0]


    if(len(solutions > 10)):
        return
    
    cost =  sum([houses[x] for x in chosen])

    find_packages(chosen, houses[1:], budget)

    if(cost < budget and len(chosen) > 1):
        solutions.append(chosen)
    else:
        return




#Create investment packages that fit the budget
def create_packages(houses, budget):
    global solutions
    solutions = []
