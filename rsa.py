#!/usr/bin/env python3
import subprocess, math


### Maths ###

# x^y mod N
def mod_exp(x, y, N):
    if N == 1:
        return 0
    result = 1
    x = x % N
    while y > 0:
        if (y % 2 == 1):
            result = (result * x) % N
        y >>= 1
        x = (x * x) % N
    return result

# Returns (x, y, gcd) such that ax + by = gcd(a, b)
def extended_euclid(a, b):
    if b == 0:
        return (1, 0, a)
    xp, yp, d = extended_euclid(b, a % b)
    return (yp, xp - ((a // b) * yp), d)

# Determine whether a and b are relatively prime
def rel_prime(a, b):
    return extended_euclid(a, b)[2] == 1


### RSA Functions ###

def generate_prime(bits):
    while True:
        # Generate prime with OpenSSL
        cmd = 'openssl prime -generate -bits ' + str(bits)
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        prime = proc.stdout.read().decode("utf-8")
        prime = int(prime[:-1])

        # Return if high order bit is set
        high_bit = 1 << (bits-1)
        if prime & high_bit:
            return prime

def calculate_d(e, phi_n):
    return extended_euclid(e, phi_n)[0] % phi_n

def generate_keys(bits, e, passoff=False):
    # Find primes p and q such that (p-1)(q-1) is relatively prime to e
    p = 0
    q = 0
    while True:
        p = generate_prime(bits)
        q = generate_prime(bits)
        if p == q:
            continue
        if rel_prime((p-1) * (q-1), e):
            break

    # Calculate secret d
    n = p * q
    pn = (p-1) * (q-1)
    d = calculate_d(e, pn)

    # Print values for passoff
    if passoff:
        print('p: ', p)
        print('q: ', q)
        print('n: ', n)
        print('e: ', e)
        print('d: ', d)

    return n, d


### Main ###

def test():
    e = 65537
    n, d = generate_keys(512, e)

    ## Tests

    # "Random" message
    m = 437895243789523524789
    encrypted = mod_exp(m, e, n)
    decrypted = mod_exp(encrypted, d, n)
    assert(m == decrypted)
    # "Random" large message
    m = 9723947239754602546092689254689327546893268954638926389475634563456345634563456345634563409278546230978465
    encrypted = mod_exp(m, e, n)
    decrypted = mod_exp(encrypted, d, n)
    assert(m == decrypted)
    # Edge case 0
    m = 0
    encrypted = mod_exp(m, e, n)
    decrypted = mod_exp(encrypted, d, n)
    assert(m == decrypted)
    # Edge case (maximum message size)
    m = n-1
    encrypted = mod_exp(m, e, n)
    decrypted = mod_exp(encrypted, d, n)
    assert(m == decrypted)

def passoff():
    e = 65537
    n, d = generate_keys(512, e, passoff=True)
    print()
    to_encrypt = int(input("Value to encrypt:\t "))
    encrypted = mod_exp(to_encrypt, e, n)
    print("Encrypted value:\t", encrypted)
    to_decrypt = int(input("Value to decrypt:\t "))
    decrypted = mod_exp(to_decrypt, d, n)
    print("Decrypted value:\t", decrypted)

passoff()