from random import randint

def diceroll(number, sides):
    for x in range(number):
        total += randint(1, sides)
        print(f"total: {total}")
    return total