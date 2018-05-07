import random


def throw_dice(command="/dice", output_format="text"):
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
    if output_format == "text":
        result = ""
        for i in range(m):
            result += str(random.randint(1, n))
            if i == m - 1:
                continue
            result += ", "
        return result
    else:
        result = []
        for i in range(m):
            result.append(random.randint(1, n))
        return result
