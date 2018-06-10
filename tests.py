import unittest
import common
import elliptic_curve
import smile

class CommonTests(unittest.TestCase):
    def test_base_b_digits(self):
        # Base 2
        self.assertEqual(common.base_b_digits(1, 2), [1])
        self.assertEqual(common.base_b_digits(4, 2), [0,0,1])
        self.assertEqual(common.base_b_digits(7, 2), [1,1,1])
        self.assertEqual(common.base_b_digits(12, 2), [0,0,1,1])
        # Base 4
        self.assertEqual(common.base_b_digits(27, 4), [3, 2, 1])
        # Base 12
        self.assertEqual(common.base_b_digits(54, 12), [6, 4])

    def test_gcd(self):
        # Small integers
        self.assertEqual(common.gcd(10, 45), 5)
         # Medium integers
        self.assertEqual(common.gcd(172383, 209399), 1)
         # Large integers
        self.assertEqual(common.gcd(12938183838281, 91827172737173), 1)
    
    def test_extended_eucliden_algorithm(self):
        # Small integers
        self.assertEqual(common.extended_euclidean_algorithm(37, 23),  (5, -8))
         # Medium integers
        self.assertEqual(common.extended_euclidean_algorithm(172383, 209399), (45386, -37363))
         # Large integers
        self.assertEqual(common.extended_euclidean_algorithm(12938183838281, 91827172737173), (40307160997105, -5679162751448))
    
    def test_mod_inverse(self):
        # Small integers
        self.assertEqual(common.mod_inverse(3, 26), 9)
         # Medium integers
        self.assertEqual(common.mod_inverse(323, 26232), 17867)
         # Large integers
        self.assertEqual(common.mod_inverse(32334434, 262323434), False)

class EllipticCurveTests(unittest.TestCase):
    # For these tests, we will use the following parameters:
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
        self.assertEqual(elliptic_curve.addition(2, 3, 97, [3,6], '0'), [3, 6])
        # 2P
        self.assertEqual(elliptic_curve.addition(2, 3, 97, [3,6], [3,6]), [80, 10])
        # 3P
        self.assertEqual(elliptic_curve.addition(2, 3, 97, [3,6], [80,10]), [80, 87])
        # 4P
        self.assertEqual(elliptic_curve.addition(2, 3, 97, [3,6], [80, 87]), [3, 91])
        # 5P
        self.assertEqual(elliptic_curve.addition(2, 3, 97, [3,6], [3,91]), '0')
    
    def test_multiplication(self):
        # 1P
        self.assertEqual(elliptic_curve.multiplication(2, 3, 97, [3,6], 1), [3, 6])
        # 2P
        self.assertEqual(elliptic_curve.multiplication(2, 3, 97, [3,6], 2), [80, 10])
        # 3P
        self.assertEqual(elliptic_curve.multiplication(2, 3, 97, [3,6], 3), [80, 87])
        # 4P
        self.assertEqual(elliptic_curve.multiplication(2, 3, 97, [3,6], 4), [3, 91])
        # 5P
        self.assertEqual(elliptic_curve.multiplication(2, 3, 97, [3,6], 5), '0')

    def test_subtraction(self):
        # Subtracting two equal values equals 0
        self.assertEqual(elliptic_curve.subtraction(2, 3, 97, [3,6], [3,6]), '0')
        # Subtracting zero from P equals P
        self.assertEqual(elliptic_curve.subtraction(2, 3, 97, [3,6], '0'), [3,6])
        # Subtracting P from 0 equals -P
        self.assertEqual(elliptic_curve.subtraction(2, 3, 97, '0', [3,6]), [3,-6])

    def test_is_valid_point(self):
        self.assertEqual(elliptic_curve.is_valid_point(2, 3, 97, [3, 6]), True)
        self.assertEqual(elliptic_curve.is_valid_point(2, 3, 97, [3, 7]), False)

class SmileTests(unittest.TestCase):
    def test_generate_commitment(self):
        v1, v2, v3 = 10, 20, 30
        r1, r2, r3 = 1, 2, 3

        self.assertEqual(smile.generate_commitment(v1, r1), [28.0, 8.0])
        self.assertEqual(smile.generate_commitment(v2, r2), [37.0, 81.0])
        self.assertEqual(smile.generate_commitment(v3, r3), [93.0, 36.0])
    
    # Here we will test whether a full transaction adds up correctly (assume sums to zero, no blinding here).
    # Hence, we are checking that for:
    #   v1 = 10 | r1 = 1 | input1  = (r1 * G + v1 * H )
    #   v2 = 20 | r2 = 2 | input2  = (r2 * G + v2 * H )
    #   v3 = 30 | r1 = 3 | output1 = (r3 * G + v3 * H )
    #
    #   input1 + input2 = output1 = 0
    def test_validate_transaction_is_zero(self):
        v1, v2, v3 = 10, 20, 30
        r1, r2, r3 = 1, 2, 3

        input1 =  smile.generate_commitment(v1, r1)
        input2 =  smile.generate_commitment(v2, r2)
        output1 =  smile.generate_commitment(v3, r3)

        inputs = [input1, input2]
        outputs = [output1]

        self.assertEqual(smile.validate_transaction_is_zero(inputs, outputs), True)


if __name__ == '__main__':
    unittest.main()