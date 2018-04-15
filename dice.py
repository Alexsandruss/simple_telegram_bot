import random


def throw_dice(command):
    # command looks like '/dice N-edged M times'
    numbers = command.split(" ")
    # n - number of edges (default)
    try:
        n = int(numbers[1].split("-")[0])
    except:
        n = 6
    finally:
        if n < 2 or n > 99:
            n = 6
    # m - number of dices
    try:
        m = int(numbers[2])
    except:
        m = 1
    finally:
        if m < 1 or m > 100:
            m = 1
    result = ""
    for i in range(m):
        result += str(random.randint(1, n))
        if i == m - 1:
            continue
        result += ", "
    return result
