#!/usr/bin/env python3

S = [
    7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,
]

K = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
]

INIT_STATE = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)


def leftrotate(x, c):
    """Implementation of 32-bit integer left rotation."""
    return ((x << c) | (x >> (32-c))) % 2**32


def transit(state, chunk):
    """
    Perform a state transition.

    Args:
        state: a tuple of 4 32-bit integers.
        chunk: a 64-byte data chunk which makes the state transit.

    Returns:
        Another tuple of 4 integers representing the new state.

    """
    A, B, C, D = state
    M = [int.from_bytes(chunk[j:j+4], "little") for j in range(0, 64, 4)]

    for i in range(64):
        if i < 16:
            F = (B & C) | ((~B) & D)
            g = i
        elif i < 32:
            F = (D & B) | ((~D) & C)
            g = (5*i + 1) % 16
        elif i < 48:
            F = B ^ C ^ D
            g = (3*i + 5) % 16
        else:
            F = C ^ (B | (~D)%2**32)
            g = (7*i) % 16

        F = (F + A + K[i] + M[g]) % 2**32
        A = D
        D = C
        C = B
        B = (B + leftrotate(F, S[i])) % 2**32

    return (A, B, C, D)


def md5(input):
    """Return the md5 digest of input."""
    zeroes_pad = b"\x00" * ((-len(input) - 9) % 64)
    padded_input = (
        input +
        b"\x80" +
        zeroes_pad +
        (len(input) * 8 % 2**64).to_bytes(8, "little")
    )

    state = INIT_STATE
    for i in range(0, len(padded_input), 64):
        state = transit(state, padded_input[i: i + 64])

    return b"".join(X.to_bytes(4, "little") for X in state)


if __name__ == "__main__":
    from secret import key, flag
    assert len(key) == 64

    # timeout in 10 seconds
    import signal
    signal.alarm(10)

    # give user the guest token so he/she can login as a guest
    guest_token = md5(key + b"GUEST")
    print("Guest token: {}".format(guest_token.hex()))

    print("Login now!")
    try:
        username = input("Username: ")
        token = bytes.fromhex(input("Token: "))

        if md5(key + username.encode()) == token:
            print("Login successfully!")
            if username == "ADMIN":
                print(flag)
            else:
                print("Nothing to do here!")
        else:
            raise Exception()
    except:
        print("Login failed!")
