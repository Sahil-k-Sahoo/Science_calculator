Markdown
# SciCalc — Scientific Calculator (Problem B3)

Command-line scientific calculator implemented in Python using only the standard library, with a custom tokenizer, recursive-descent parser, and AST evaluator (no `eval`, `exec`, or `compile`).

## How to Run

Requires Python 3.10+.

```bash
python scicalc.py
Use py scicalc.py or python3 scicalc.py depending on your environment.

Interactive mode: Displays SciCalc>  when stdin is attached to a terminal (isatty() is true).

Piped / non-interactive mode: Prints no prompt; reads one expression per line from stdin until exit, quit (case-insensitive), or EOF. Blank lines are skipped.

Sample Session
Plaintext
SciCalc> G * (5.972e24) / (6371000 ^ 2)
9.819973446927108
SciCalc> sin(PI / 6) + nCr(5, 2)
10.5
SciCalc> totient(9)
6
SciCalc> fusc(10)
3
SciCalc> sigmoid(0)
0.5
SciCalc> 2 ^ 3 ^ 2
512.0
SciCalc> 1 / 0
[ERROR] division by zero
SciCalc> exit
Design & Architecture
Plaintext
line (stdin)
  -> tokenizer.py   (tokens: numbers, identifiers, operators, parentheses, commas)
  -> parser.py      (recursive-descent AST respecting precedence and associativity)
  -> evaluator.py   (evaluates AST using maths_op.py; raises calc_errors.py errors)
  -> scicalc.py     (CLI loop, TTY vs. piped handling, result & [ERROR] output)
Modules
calc_errors.py: Defines the error hierarchy (CalcError, CalcSyntaxError, CalcDomainError, CalcOverflowError).

maths_op.py: Stores case-sensitive CONSTANTS (PI, E, h, G, Na, e, kB, epsilon0, mu0, c) and FUNCTIONS covering trigonometry, hyperbolic functions, logs/exponents, combinatorics, roots, discrete/step functions, and number theory.

tokenizer.py: Converts input text into tokens, handles numbers (including .5 and 1.5e-3 / 6.022e23 while distinguishing 2e3 from 2*e), and rejects implied multiplication (2e, 2(3), 2 PI).

parser.py: Builds an AST with precedence from lowest to highest: +/- (left) -> *///% (left) -> unary +/- -> ^ (right-associative, allowing unary signs in exponents) -> literals, constants, parenthesized expressions, and comma-separated function calls.

evaluator.py: Walks the AST, enforces integer vs. float result types, checks division/modulo by zero, and catches numeric overflow.

scicalc.py: Manages stdin/stdout, exit/quit, and [ERROR] <message> output without exposing raw tracebacks.

Assumptions & Choices
Case sensitivity: Constant and function names are case-sensitive (PI and e work; pi and Pi raise an error).

Integer vs. float outputs: / and ^ return floats; +, -, *, and % preserve integers when both operands are integers; integer-valued functions (fact, nCr, nPr, gcd, lcm, totient, fusc, floor, ceil, signum, heaviside) return integers (6, not 6.0).

Modulo semantics: % follows Python's modulo behavior (for example, -7 % 3 evaluates to 2).

Function conventions:

antilog(x) computes 10.0 ** x and raises an overflow error if outside float limits.

heaviside(x) returns 0 for x < 0 and 1 otherwise (including 0).

tan(x) rejects values where cos(x) is effectively zero to catch asymptotes cleanly.

root(x, n) requires a non-zero integer n and allows negative x only when n is odd.

Integer-only functions reject non-whole numbers like 3.5 while accepting whole-valued floats like 5.0.

Running Tests
Bash
python -m unittest discover -s test -v
(Or py -m unittest discover -s test -v on Windows.)