import itertools

l=[i for i in range(15)]
print(l)
n=3
print([l[i:i+n] for i in range(0,len(l),n)])

s='1629182480982'
print(len(s))