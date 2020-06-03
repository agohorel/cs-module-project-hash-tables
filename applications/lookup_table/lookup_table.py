import random
import math
import json


def slowfun_too_slow(x, y):
    v = math.pow(x, y)
    v = math.factorial(v)
    v //= (x + y)
    v %= 982451653

    return v


def populate_lookup_table(min_x, max_x, min_y, max_y):
    lookup = {}

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            lookup[f"{x}-{y}"] = slowfun_too_slow(x, y)
            print(lookup[f"{x}-{y}"])
            print(x, y)

    data = json.dumps(lookup)
    f = open("lookup.json", "w")
    f.write(data)
    f.close()


# populate_lookup_table(2, 14, 3, 6)


def slowfun(x, y):
    """
    Rewrite slowfun_too_slow() in here so that the program produces the same
    output, but completes quickly instead of taking ages to run.
    """
    with open("lookup.json") as f:
        lookup = json.load(f)

    return lookup[f"{x}-{y}"]


# Do not modify below this line!
for i in range(50000):
    x = random.randrange(2, 14)
    y = random.randrange(3, 6)
    print(f'{i}: {x},{y}: {slowfun(x, y)}')
