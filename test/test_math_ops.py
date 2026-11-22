import math
import unittest

from calc_errors import CalcDomainError, CalcOverflowError
from maths_op import CONSTANTS, FUNCTIONS


class TestMathOps(unittest.TestCase):
    def test_constants_present_and_case_sensitive(self) -> None:
        self.assertIn("PI",CONSTANTS)
        self.assertIn("e",CONSTANTS)
        self.assertIn("G",CONSTANTS)
        self.assertNotIn("pi",CONSTANTS)
        self.assertNotIn("Pi",CONSTANTS)

    def test_trig_and_hyperbolic(self) -> None:
        _,sin_fn=FUNCTIONS["sin"]
        _,cos_fn=FUNCTIONS["cos"]
        _,tanh_fn=FUNCTIONS["tanh"]
        self.assertAlmostEqual(sin_fn(CONSTANTS["PI"] / 6),0.5,places=12)
        self.assertAlmostEqual(cos_fn(0),1.0,places=12)
        self.assertAlmostEqual(tanh_fn(0),0.0,places=12)

    def test_logs_and_antilog(self) -> None:
        _,log_fn=FUNCTIONS["log"]
        _,log10_fn=FUNCTIONS["log10"]
        _,antilog_fn=FUNCTIONS["antilog"]
        _,exp_fn=FUNCTIONS["exp"]
        self.assertAlmostEqual(log_fn(CONSTANTS["E"]),1.0,places=12)
        self.assertAlmostEqual(log10_fn(1000),3.0,places=12)
        self.assertAlmostEqual(antilog_fn(2),100.0,places=12)
        self.assertAlmostEqual(exp_fn(0),1.0,places=12)
        with self.assertRaises(CalcDomainError):
            log_fn(0)
        with self.assertRaises(CalcDomainError):
            log_fn(-1)
        with self.assertRaises(CalcOverflowError):
            antilog_fn(400)

    def test_combinatorics_and_root(self) -> None:
        _,fact_fn=FUNCTIONS["fact"]
        _,ncr_fn=FUNCTIONS["nCr"]
        _,npr_fn=FUNCTIONS["nPr"]
        _,root_fn=FUNCTIONS["root"]

        f_res=fact_fn(5.0)
        self.assertIs(type(f_res),int)
        self.assertEqual(f_res,120)

        c_res=ncr_fn(5,2)
        self.assertIs(type(c_res),int)
        self.assertEqual(c_res,10)

        p_res=npr_fn(5,2)
        self.assertIs(type(p_res),int)
        self.assertEqual(p_res,20)

        self.assertAlmostEqual(root_fn(-8,3),-2.0,places=12)
        with self.assertRaises(CalcDomainError):
            fact_fn(3.5)
        with self.assertRaises(CalcDomainError):
            ncr_fn(3,5)
        with self.assertRaises(CalcDomainError):
            root_fn(-4,2)
        with self.assertRaises(CalcDomainError):
            root_fn(9,0)

    def test_discrete_and_number_theory(self) -> None:
        _,floor_fn=FUNCTIONS["floor"]
        _,ceil_fn=FUNCTIONS["ceil"]
        _,signum_fn=FUNCTIONS["signum"]
        _,heaviside_fn=FUNCTIONS["heaviside"]
        _,sigmoid_fn=FUNCTIONS["sigmoid"]
        _,gcd_fn=FUNCTIONS["gcd"]
        _,lcm_fn=FUNCTIONS["lcm"]
        _,totient_fn=FUNCTIONS["totient"]
        _,fusc_fn=FUNCTIONS["fusc"]

        self.assertIs(type(floor_fn(3.9)),int)
        self.assertEqual(floor_fn(3.9),3)
        self.assertIs(type(ceil_fn(3.1)),int)
        self.assertEqual(ceil_fn(3.1),4)
        self.assertEqual(signum_fn(-12.5),-1)
        self.assertEqual(signum_fn(0),0)
        self.assertEqual(heaviside_fn(-0.1),0)
        self.assertEqual(heaviside_fn(0),1)
        self.assertAlmostEqual(sigmoid_fn(0),0.5,places=12)
        self.assertAlmostEqual(sigmoid_fn(-1000),0.0,places=12)

        self.assertEqual(gcd_fn(24,18),6)
        self.assertEqual(lcm_fn(4,6),12)
        self.assertEqual(totient_fn(9),6)
        self.assertEqual(fusc_fn(10),3)
        with self.assertRaises(CalcDomainError):
            totient_fn(0)
        with self.assertRaises(CalcDomainError):
            fusc_fn(-1)
        with self.assertRaises(CalcDomainError):
            totient_fn(4.5)


if __name__ == "__main__":
    unittest.main()