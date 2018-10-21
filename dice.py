import random


def throw_dice(command="/dice", output_type=str):
    # command looks like '/dice N-edged M times'
    numbers = command.split(" ")
    # n - number of edges (default)
    try:
        n = int(numbers[1].split("-")[0])
        m = int(numbers[2])
    except:
        n = 6
        m = 1
    finally:
        if n < 2 or n > 99:
            n = 6
        if m < 1 or m > 100:
            m = 1
    if output_type is str:
        return str([random.randint(1, n) for _ in range(m)])[1:-1]
    else:
        return [random.randint(1, n) for _ in range(m)]
