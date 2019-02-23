#!/usr/bin/env python3

from random import SystemRandom
import subprocess

# Modular exponentiation
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

# Generate a cryptographically strong prime p where (p-1)/2 is also prime
def generate_prime(bits=512):
    while True:
        # Generate 512-bit prime with OpenSSL
        cmd = 'openssl prime -generate -bits ' + str(bits)
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        prime = proc.stdout.read().decode("utf-8")
        prime = int(prime[:-1])

        # Calculate p and check for primality with OpenSSL
        p = int ((prime * 2) + 1 )
        is_prime = 0
        cmd = 'openssl prime -checks 20 ' + str(p)
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        output = proc.stdout.read().decode("utf-8")
        output = output[:-1]
        words = output.split(" ")
        is_prime = words[-2] != 'not'

        # Return p if it is prime
        if is_prime:
            return p

# Generate random n-bit number through os.urandom()
def generate_random(bits=512):
    return int(SystemRandom().random() * (2**bits))

