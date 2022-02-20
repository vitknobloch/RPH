import random

late = 0
trials = 1000000

for trial in range(trials):
    pupil= random.uniform(0,360)
    bus= random.uniform(180,420)
    if(bus<pupil):
        late += 1

print(late/trials)