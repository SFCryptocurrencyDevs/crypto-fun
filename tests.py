import unittest
import common

class CommonTests(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()