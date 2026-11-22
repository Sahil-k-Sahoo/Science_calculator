import unittest

from calc_errors import CalcDomainError, CalcOverflowError, CalcSyntaxError
from scicalc import eval_line


class TestParserAndEval(unittest.TestCase):
    def test_precedence_and_associativity(self) -> None:
        self.assertEqual(eval_line("2 ^ 3 ^ 2"),512.0)
        self.assertEqual(eval_line("-2 ^ 2"),-4.0)
        self.assertEqual(eval_line("2 ^ -1"),0.5)
        self.assertEqual(eval_line("2 * -4"),-8)
        self.assertEqual(eval_line("2 - -3"),5)

    def test_numbers_and_e_constant(self) -> None:
        self.assertEqual(eval_line("2e3"),2000.0)
        self.assertEqual(eval_line(".5"),0.5)
        self.assertAlmostEqual(eval_line("2 * e"),3.204353268e-19,places=28)
        with self.assertRaises(CalcSyntaxError):
            eval_line("2e")
        with self.assertRaises(CalcSyntaxError):
            eval_line("2(3)")
        with self.assertRaises(CalcSyntaxError):
            eval_line("2 PI")

    def test_gravity_and_sample_expressions(self) -> None:
        g_val=eval_line("G * (5.972e24) / (6371000 ^ 2)")
        self.assertAlmostEqual(g_val,9.8199734,delta=1e-6)
        self.assertAlmostEqual(eval_line("sin(PI / 6) + nCr(5, 2)"),10.5,places=12)
        self.assertEqual(eval_line("totient(9)"),6)
        self.assertEqual(eval_line("fusc(10)"),3)
        self.assertEqual(eval_line("sigmoid(0)"),0.5)

    def test_int_vs_float_and_modulo(self) -> None:
        res_int=eval_line("3 + 3")
        self.assertIs(type(res_int),int)
        self.assertEqual(res_int,6)

        mod_res=eval_line("-7 % 3")
        self.assertIs(type(mod_res),int)
        self.assertEqual(mod_res,2)

        div_res=eval_line("6 / 2")
        self.assertIs(type(div_res),float)
        self.assertEqual(div_res,3.0)

    def test_errors(self) -> None:
        with self.assertRaises(CalcDomainError):
            eval_line("1 / 0")
        with self.assertRaises(CalcDomainError):
            eval_line("5 % 0")
        with self.assertRaises(CalcDomainError):
            eval_line("asin(2)")
        with self.assertRaises(CalcDomainError):
            eval_line("pi")
        with self.assertRaises(CalcDomainError):
            eval_line("sin(1, 2)")
        with self.assertRaises(CalcSyntaxError):
            eval_line("1.2.3")
        with self.assertRaises(CalcSyntaxError):
            eval_line("$")
        with self.assertRaises(CalcSyntaxError):
            eval_line("(1 + 2")
        with self.assertRaises(CalcSyntaxError):
            eval_line("1 +")
        with self.assertRaises(CalcOverflowError):
            eval_line("10 ^ 400")


if __name__ == "__main__":
    unittest.main()