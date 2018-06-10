# This file contains all the elliptic curve functions that are used by
# numerous different cryptographic algorithms. Much of this code will
# be adapted/ported/borrowed from the code examples in the Crypto
# Math module supplied by Professor Krumm as part of Colby College's
# MA398 class.

import common
import math

"""
    Elliptic curve point addition is fundamental to many different elliptic curve based
    crypto-systems. The basis of elliptic curve addition is rooted in the properties
    garaunteed to the elliptic curve group:

    1. [Closure]: the elements of the group are points on the elliptic curve
    2. [Identity]: there exists a point at infinity ('0') such that P + '0'  = '0' + P = P
    3. [Inverse]: the inverse of P, -P, is the point symmetric across the x-axis
    4. [Associativity]: P + Q = Q + P
    
    And the group is even abelian, meaning it also has the property:
    5. [Commutative]: P+(Q+R)=Q+(P+R)=R+(P+Q)=... =0

    Note, addition is on an elliptic curve is defined as:

        given three alligned, non-zero points P, Q, R,
        their sum is P + Q + R = 0.

    With these properties in hand, you can begin to conceptualize elliptic curve addition.
    The function below has an extra parameter, p. P is a prime number, used to denote a 
    finite field mod p, which our elliptic curve is defined over. Elliptic Curve Cryptography
    uses finite fields to give elliptic curves a few interesting additional properties,
    very useful for things such as ECDSA (elliptic curve digital signature algorithm) or 
    ECDH (elliptic curve diffie helman).

    Learn more:
    http://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/
"""
def addition(a, b, p, P, Q):
    # Case 1: P = 0 or Q = 0, where 0 is the point at infinity.
    if P == '0':
        return Q
    if Q == '0':
        return P

    x1, y1 = P
    x2, y2 = Q
    
    # Case 2: P == -Q, so we get P - P = 0
    if (x1 - x2) % p == 0 and (y1 + y2) % p == 0:
        return '0'
    
    # Case 3: P == Q, so we must use the derivative of the slope
    # to find the line tangent to the curve.
    if P == Q:
        slope_numerator = (3*x1**2 + a) % p
        slope_denominator = 2*y1 % p

    # Case 4: P =/ Q, allowing us to find the simple slope.
    else:
        slope_numerator = (y2 - y1) % p
        slope_denominator = (x2 - x1) % p
    
    slope = (slope_numerator * common.mod_inverse(slope_denominator, p)) % p

    x3 = (slope**2 - x1 - x2) % p
    y3 = (slope*(x1 - x3) - y1) % p

    return [x3,y3]

"""
    Elliptic curve multiplication utilizes elliptic curve addtion and a 'double and add'
    algorithm. 

    Double and add: consider the binary representation of the number 111.

        67 = 11011 
           = 1 * 2**4 + 1 * 2**3 + 0 * 2**2 + 1 * 2**1 + 1 * 2**0 
           = 2**4 + 2**3 + 2**1 + 2**0

        Thus:
        67 * P = 2**4 * P + 2**3 * P + 2**1 * P + 2**0 * P

    We can take this concept and apply it to elliptic curve multiplication.

    To get 67P for a point P, we would do:
        2**0P = P   = P
        2**1P = 2P  = P + P
        2**3P = 8P  = 2P + 2P + 2P
        2**4P = 16P = 2P + 2P + 2P + 2P

        67P = P + (P + P) + ((P + P) + (P + P) + (P + P)) + ((P + P) + (P + P) + (P + P) + (P + P))

    Learn more:
    http://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/
"""
def multiplication(a, b, p, P, n):
    Q = P
    R = '0'
    multiples_of_P = [P]

    bits = common.base_b_digits(n, 2)

    # Creates an array of 2**n multiples of P equal to length of bit array.
    # EX: 
    #   n=12 --> [0,0,1,1] 
    #   thus multiples of P = [1P, 2P, 4P, 8P]
    for i in bits:
        Q = addition(a, b, p, Q, Q)
        multiples_of_P.append(Q)
    
    # Starts with the point at infinity and adds this to
    # all the bits where bit = 1.
    # EX:
    #   For [0, 0, 1, 1]
    #     R       |  Bit  | Operation
    #   R = 0     |   0   | PASS
    #   R = 0     |   0   | PASS
    #   R = 4P    |   1   | '0' + 4P
    #   R = 12P   |   1   |  4P + 8P
    for i in range(len(bits)):
        if bits[i] == 1:
            R = addition(a, b, p, R, multiples_of_P[i])
    return R

"""
    Simple test to check whether a point is on the elliptic curve.
"""
def is_valid_point(a, b, p, P):
    if P == '0':
        return True
    x, y = P
    left = math.pow(y,2) % p
    right = (math.pow(x,3) + (a * x) + b) % p
    return math.isclose(left, right)