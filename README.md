# SciCalc — Scientific Calculator

A command-line scientific calculator built in Python (using only the standard library). It safely evaluates mathematical expressions using a custom tokenizer, recursive-descent parser, and AST evaluator instead of `eval()`.

## Features

- **Arithmetic & Precedence**: Supports `+`, `-`, `*`, `/`, `%`, and `^` (power with right-associativity).
- **Scientific Constants**: Built-in constants like `PI`, `E`, `c`, `G`, `h`, `Na`, `e`, `kB`, `epsilon0`, and `mu0`.
- **Math Functions**:
  - Trigonometry & Hyperbolic: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`
  - Exponentials & Logs: `log` (ln), `log10`, `antilog`, `exp`
  - Combinatorics: `fact` (n!), `nCr`, `nPr`
  - Roots & Discrete: `root`, `floor`, `ceil`, `signum`, `heaviside`, `sigmoid`
  - Number Theory: `gcd`, `lcm`, `totient`, `fusc`
- **Error Handling**: Clear error messages for syntax errors, division by zero, invalid domains, and overflows without crashing.

## How to Run

Requires Python 3.10+.

```bash
python scicalc.py
```
*(On Windows, you can also use `py scicalc.py`)*

To exit, type `exit` or `quit`.

### Piped / Non-Interactive Mode
You can also pipe expressions directly:

```bash
echo "sin(PI / 6) + nCr(5, 2)" | python scicalc.py
```

## Example Session

```text
SciCalc> 2 ^ 3 ^ 2
512.0
SciCalc> sin(PI / 6) + nCr(5, 2)
10.5
SciCalc> G * (5.972e24) / (6371000 ^ 2)
9.819973446927108
SciCalc> totient(9)
6
SciCalc> 1 / 0
[ERROR] division by zero
SciCalc> exit
```

## Project Structure

- `scicalc.py` — Main entry point and CLI loop.
- `tokenizer.py` — Breaks expressions into tokens (numbers, operators, identifiers).
- `parser.py` — Builds the AST according to operator precedence and associativity.
- `evaluator.py` — Walks the AST to calculate results and enforce integer vs float types.
- `maths_op.py` — Contains all supported mathematical functions and constants.
- `calc_errors.py` — Custom error classes for clean error reporting.
- `test/` — Unit test suite for CLI, math operations, and parser.

## Running Tests

To run all unit tests:

```bash
python -m unittest discover -s test -v
```
*(Or `py -m unittest discover -s test -v` on Windows)*
