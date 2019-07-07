import random


def throw_dice(command="/dice", output_type=str):
    # command looks like '/dice N-edged M times'
    numbers = command.split(" ")
    # n - number of edges (default - 6)
    # m - number of throws (default - 1)
    try:
        n = int(numbers[1].split("-")[0])
        m = int(numbers[2])
    except:
        n = 6
        m = 1
    finally:
        if not 1 < n < 100:
            n = 6
        if not 0 < m < 10:
            m = 1
    if output_type is str:
        return str([random.randint(1, n) for _ in range(m)])[1:-1]
    else:
        return [random.randint(1, n) for _ in range(m)]
