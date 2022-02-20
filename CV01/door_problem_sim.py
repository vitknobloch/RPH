import random

#strategy to play - switch, stay, random


def simulate(strategy):
    door_options = (1, 2, 3)

    #assign car to one of the door
    car = random.choice(door_options)
    #randomly select my answer
    my_choice = random.choice(door_options)

    #open random doors from the ones which are not choosen by me and dont have the car in it
    opened = random.choice([d for d in door_options if d!= car and d != my_choice])

    if(strategy == 'switch'):
        my_choice = next(d for d in door_options if d!=my_choice and d != opened)
    elif(strategy == 'stay'):
        pass
    elif(strategy == 'random'):
        r= random.randint(0,1)
        if(r):
            my_choice = next(d for d in door_options if d!=my_choice and d != opened)

    return my_choice == car

if __name__ == '__main__':
    iterations = 10**6
    
    #random
    counter = 0
    for i in range(iterations):
        if(simulate('random')):
            counter += 1
    print("Random: ", end="")
    print(round(counter/iterations*100))

    #stay
    counter = 0
    for i in range(iterations):
        if(simulate('stay')):
            counter += 1
    print("Stay:   ", end="")
    print(round(counter/iterations*100))

    #switch
    counter = 0
    for i in range(iterations):
        if(simulate('switch')):
            counter += 1
    print("Switch: ", end="")
    print(round(counter/iterations*100))
    



