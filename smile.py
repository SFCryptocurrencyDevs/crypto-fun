# Smile is like grin (Mimble Wimble) but much simpler :)
# Here we will define certain parts of the mimble wimble
# protocol in order to enforce and solidify certain
# fundamental concepts.
#
# Here we will use the following parameters
a = 1
b = 6
p = 97.0
G = [3, 6]
H = [-1, -2]

import elliptic_curve
import random

"""
    Motivation as defined in the Mimble Wimble (Grin) intro
    Ref:
    https://github.com/mimblewimble/grin/blob/master/doc/intro.md

    "There are a finite number of usable values and one could
    try every single one of them to guess the value of your
    transaction. In addition, knowing v1 (from a previous 
    transaction for example) and the resulting v1*H reveals 
    all outputs with value v1 across the blockchain. For 
    these reasons, we introduce a second elliptic curve G 
    (practically G is just another generator point on the 
    same curve group as H) and a private key r used as a 
    blinding factor."

    An input or output value in a transaction can then be
    expressed as:

        r * G + v * H
    
    Where:
        v = value (such as the value of a UTXO)
        H = generator point
        r = random blinding factor
        G = generator point on same curve as H

    This is called a Pedersen Commitment. Note: neither r
    nor v can be deduced.

    Also note, in elliptic curve cryptography:
        k     = private key, where v is some random positive integer
        k * G = public key, where * denotes elliptic curve multiplication
"""
def generate_commitment(v, r):
    r_G = elliptic_curve.multiplication(a, b, p, G, r)
    v_H = elliptic_curve.multiplication(a, b, p, H, v)
    return elliptic_curve.addition(a,b,p, r_G, v_H)
