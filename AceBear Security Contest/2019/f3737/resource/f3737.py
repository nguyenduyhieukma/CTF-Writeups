#!/usr/bin/env python3

# ********************************************************** #
# Today, we will work with F37^37. Good luck and have fun :) #
# ********************************************************** #

# Part 1: DEFINITION OF MYHASH
from hashlib import sha512

BLOCKSIZE = 16


def reduce_modulo_37(i):
    return int(i % 37)


class F3737(object):
    """
    This class represents a vector in F37^37. Only basic operations (addition
    and scalar multiplication) are provided.
    """

    def __init__(self, components):
        self.components = list(map(reduce_modulo_37, components))
        assert len(self.components) == 37

    def __add__(self, other):
        return F3737(
            map(lambda x, y: x + y, self.components, other.components))

    def __mul__(self, scalar):
        return F3737(map(lambda x: x * scalar, self.components))

    def __eq__(self, other):
        return self.components == other.components

    def __str__(self):
        return str(self.components)

    def __repr__(self):
        return repr(self.components)


def f3737_hash(input):
    """
    This function somehow makes the output of sha512 become a vector of F37^37.
    """
    if input == b'EVALUATE_TO_ZERO':
        return F3737([0] * 37)
    h = int(sha512(input).hexdigest(), 16)
    result = [0] * 37
    for i in range(37):
        result[i] = h % 37
        h = h // 37
    return F3737(result)


def myhash(innput):
    """
    `f3737_hash` is used as a block hash function to construct this one.
    """
    i = 0
    result = F3737([0] * 37)
    while True:
        block = innput[BLOCKSIZE * i: BLOCKSIZE * (i + 1)]
        if not block:
            break
        result += f3737_hash(block) * i
        i += 1
    return result


# Part 2: THE CHALLENGE
import string
import random

ALLOWED_LETTERS = string.ascii_letters + string.digits + '_'


def generate_password(size):
    rand = random.SystemRandom()
    password = ''.join(rand.choice(ALLOWED_LETTERS) for _ in range(size))
    password_hash_value = myhash(password.encode())
    return password, password_hash_value


def verify_password(password, hash_value):
    if all(c in ALLOWED_LETTERS for c in password):
        if myhash(password.encode()) == hash_value:
            return True
    return False


def main():
    # You have 10 seconds to guess my 3 passwords. Good luck!
    import signal
    signal.alarm(10)

    for level in [1, 2, 3]:
        _, hash_value = generate_password(32 * level)
        print("Hash value: {}".format(hash_value))
        try:
            user_input_password = input("Your guess: ")
            if not verify_password(user_input_password, hash_value):
                raise Exception()
        except:
            print("Wrong password!")
            return

    print("Congratulations! Here's the FLAG:")
    from secret import flag
    print(flag)


if __name__ == '__main__':
    main()
