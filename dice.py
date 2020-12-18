from random import randint

def roll(number, sides):
    total = 0
    for x in range(number):
        total += randint(1, sides)
        # print(f"total: {total}")
    return total