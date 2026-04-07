# generator.py
from random import choice, randint, shuffle

def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_list = (
        [choice(letters) for _ in range(randint(8, 10))] +
        [choice(symbols) for _ in range(randint(2, 4))] +
        [choice(numbers) for _ in range(randint(2, 4))]
    )
    shuffle(password_list)
    return "".join(password_list)