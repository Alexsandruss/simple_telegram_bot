import random


def throw_dice(command):
    # command looks like '/dice N-edged M times'
    numbers = command.split(" ")
    incorrect_command = False
    # n - number of edges (default)
    try:
        n = int(numbers[1].split("-")[0])
    except:
        n = 6
        incorrect_command = True
    finally:
        if n < 2 or n > 99:
            n = 6
            incorrect_command = True
    # m - number of dices
    try:
        m = int(numbers[2])
    except:
        m = 1
        incorrect_command = True
    finally:
        if m < 1 or m > 100:
            m = 1
            incorrect_command = True
    result = ""
    for i in range(m):
        result += str(random.randint(1, n))
        if i == m - 1:
            continue
        result += ", "
    if incorrect_command:
        result += "\nType command correctly, please"
    return result
