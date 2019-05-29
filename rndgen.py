import random

with open('lmp/rnd.txt','w') as f:
    for x in range(1000):
        f.write("%d\n" % random.randint(100,10000))
