# This file contains all the common math functions that are used by
# numerous different cryptographic algorithms. Much of this code will
# be adapted/ported/borrowed from the code examples in the Crypto
# Math module supplied by Professor Krumm as part of Colby College's
# MA398 class.

"""
    The Euclidean Algorithm is used to find the GCD, or greatest common
    divisor of two elements. The basic idea is, given two integers, a
    and b, your can find the GCD by utilizing the following definition:

                a = b * q + r       where 0 <= r <= a
    
    Continuously solving this, setting a = b and b = r, you will eventually
    get r = 0. Once r = 0, b is the gcd.

    Example: Find the GCD of 37 and 22.

        37 = 22 * 1 + 15
        22 = 15 * 1 + 7
        15 =  7 * 2 + 1
         7 =  1 * 7 + 0

    Thus, the GCD(37, 22) = 1.

    Learn more: 
    https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm
"""
def gcd(a,b):
    x,y = a,b
    while y != 0:
        r = x % y
        x,y = y,r

    return x


"""
    The Extended Euclidean Algorithm is used to calculate integers u, v
    such that:
            
             au + bv = gcd(a,b)
    
    Essentially, this algorithm first calculates the gcd, then works backwars
    to construct a linear combination of the original a and b.

    Example: Find the GCD of 37 and 22.

    First calculate GCD using the Euclidean Algorithm:
    37 = 22 * 1 + 15
    22 = 15 * 1 + 7
    15 =  7 * 2 + 1
     7 =  1 * 7 + 0

    Next, work backwards via linear combination and substitution:
    1 = (15 * 1) - (7 * 2)
    
    1 = (15 * 1) - ((22 - (15 * 1)) * 2)
    1 = (15 * 3) - (22 * 2)

    1 = ((37 - (22 * 1)) * 3) - (22 * 2)
    1 = (37 * 3) - (22 * 5)
        
    Check your work:  
    1 = 111 - 110
    1 = 1 

    So, for a = 37 and b = 22, we get u = 3 and v = -5.

    Learn more:
    https://brilliant.org/wiki/extended-euclidean-algorithm/#extended-euclidean-algorithm
"""
def extended_euclidean_algorithm(a,b):
    r, old_r = a,b
    s, old_s = 1,0
    t, old_t = 0,1

    while r != 0:
        q = old_r / r

        r, old_r = old_r - q * r, r
        s, old_s = old_s - q * s, s
        t, old_t = old_t - q * t, t

    return (old_s, old_t)

"""
    The multiplicative modular inverse is related to the two above functions.
    First, a number can only have a modular inverse if the gcd of the number
    and the modulo is 1; this is known as coprime or relatively prime. If this
    test passes, then you return the coefficient of a from  the extended 
    euclidean algorithm.
"""
def mod_inverse(a, m):
    if gcd(a,m) != 1:
        return False
    
    (u,_) = extended_euclidean_algorithm(a,m)
    return u % m