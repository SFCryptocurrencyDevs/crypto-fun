import unittest
import common
import elliptic_curve

class CommonTests(unittest.TestCase):
    def test_base_b_digits(self):
        # Base 2
        self.failUnlessEqual(common.base_b_digits(1, 2), [1])
        self.failUnlessEqual(common.base_b_digits(4, 2), [0,0,1])
        self.failUnlessEqual(common.base_b_digits(7, 2), [1,1,1])
        self.failUnlessEqual(common.base_b_digits(12, 2), [0,0,1,1])
        # Base 4
        self.failUnlessEqual(common.base_b_digits(27, 4), [3, 2, 1])
        # Base 12
        self.failUnlessEqual(common.base_b_digits(54, 12), [6, 4])

    def test_gcd(self):
        # Small integers
        self.failUnlessEqual(common.gcd(10, 45), 5)
         # Medium integers
        self.failUnlessEqual(common.gcd(172383, 209399), 1)
         # Large integers
        self.failUnlessEqual(common.gcd(12938183838281, 91827172737173), 1)
    
    def test_extended_eucliden_algorithm(self):
        # Small integers
        self.failUnlessEqual(common.extended_euclidean_algorithm(37, 23),  (5, -8))
         # Medium integers
        self.failUnlessEqual(common.extended_euclidean_algorithm(172383, 209399), (45386, -37363))
         # Large integers
        self.failUnlessEqual(common.extended_euclidean_algorithm(12938183838281, 91827172737173), (40307160997105, -5679162751448))
    
    def test_mod_inverse(self):
        # Small integers
        self.failUnlessEqual(common.mod_inverse(3, 26), 9)
         # Medium integers
        self.failUnlessEqual(common.mod_inverse(323, 26232), 17867)
         # Large integers
        self.failUnlessEqual(common.mod_inverse(32334434, 262323434), False)

class EllipticCurveTests(unittest.TestCase):
    # For the next two tests, we will use the following parameters:
    #   a = 2
    #   b = 3
    #   p = 97
    #
    # This curve has a generator point at [3,6] with an order of 5:
    #   0P = '0'
    #   1P = [3,6]
    #   2P = [80, 10]
    #   3P = [80, 87]
    #   4P = [3, 91]
    
    def test_addition(self):
        # 1P
        self.failUnlessEqual(elliptic_curve.addition(2, 3, 97, [3,6], '0'), [3, 6])
        # 2P
        self.failUnlessEqual(elliptic_curve.addition(2, 3, 97, [3,6], [3,6]), [80, 10])
        # 3P
        self.failUnlessEqual(elliptic_curve.addition(2, 3, 97, [3,6], [80,10]), [80, 87])
        # 4P
        self.failUnlessEqual(elliptic_curve.addition(2, 3, 97, [3,6], [80, 87]), [3, 91])
        # 5P
        self.failUnlessEqual(elliptic_curve.addition(2, 3, 97, [3,6], [3,91]), '0')
    
    def test_multiplication(self):
        # 1P
        self.failUnlessEqual(elliptic_curve.multipliction(2, 3, 97, [3,6], 1), [3, 6])
        # 2P
        self.failUnlessEqual(elliptic_curve.multipliction(2, 3, 97, [3,6], 2), [80, 10])
        # 3P
        self.failUnlessEqual(elliptic_curve.multipliction(2, 3, 97, [3,6], 3), [80, 87])
        # 4P
        self.failUnlessEqual(elliptic_curve.multipliction(2, 3, 97, [3,6], 4), [3, 91])
        # 5P
        self.failUnlessEqual(elliptic_curve.multipliction(2, 3, 97, [3,6], 5), '0')

if __name__ == '__main__':
    unittest.main()