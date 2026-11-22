import sys

from calc_errors import CalcError
from evaluator import evaluate
from parser import parse
from tokenizer import tokenize


def eval_line(line: str) -> int | float:
    tokens=tokenize(line)
    ast=parse(tokens)
    return evaluate(ast)


def main() -> int:
    is_tty=sys.stdin.isatty()

    while True:
        if is_tty:
            sys.stdout.write("SciCalc> ")
            sys.stdout.flush()

        raw=sys.stdin.readline()
        if raw == "":
            if is_tty:
                sys.stdout.write("\n")
                sys.stdout.flush()
            break

        expr=raw.strip()
        if not expr:
            continue

        if expr.lower() in ("exit","quit"):
            break

        try:
            result=eval_line(expr)
        except CalcError as exc:
            print(f"[ERROR] {exc}")
            continue
        except Exception as exc:
            print(f"[ERROR] unexpected error: {exc}")
            continue

        if type(result) is int:
            print(result)
        else:
            print(repr(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())