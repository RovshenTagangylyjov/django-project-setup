import random


# pylint: disable=C0103
def generate_random_number(length: int) -> int:
    return random.randrange(10 ** (length - 1), int("9" * length))
