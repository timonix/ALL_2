import random

ll = []
for i in range(1000000):
    a = [random.randint(1,6),random.randint(1,6)]
    if 4 in a:
        ll.append(a)

sixes = 0;
for roll in ll:
    if 6 in roll:
        sixes = sixes+1

print(sixes)
print(len(ll))
print(1/6)
print(2/11)
print(sixes/len(ll))