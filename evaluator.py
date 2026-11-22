import math

from calc_errors import CalcDomainError, CalcOverflowError
from maths_op import CONSTANTS, FUNCTIONS
from parser import BinaryNode, CallNode, ConstNode, ExprNode, NumberNode, UnaryNode


def _is_pure_int(val: int | float) -> bool:
    return type(val) is int


def _check_finite(val: int | float,label: str) -> int | float:
    if isinstance(val,float) and not math.isfinite(val):
        raise CalcOverflowError(f"overflow in {label}")
    return val


def _eval_binary(op: str,left: int | float,right: int | float) -> int | float:
    both_int=_is_pure_int(left) and _is_pure_int(right)

    if op == "+":
        if both_int:
            return _check_finite(int(left) + int(right),"addition")
        try:
            return _check_finite(float(left) + float(right),"addition")
        except OverflowError as exc:
            raise CalcOverflowError("overflow in addition") from exc

    if op == "-":
        if both_int:
            return _check_finite(int(left) - int(right),"subtraction")
        try:
            return _check_finite(float(left) - float(right),"subtraction")
        except OverflowError as exc:
            raise CalcOverflowError("overflow in subtraction") from exc

    if op == "*":
        if both_int:
            return _check_finite(int(left) * int(right),"multiplication")
        try:
            return _check_finite(float(left) * float(right),"multiplication")
        except OverflowError as exc:
            raise CalcOverflowError("overflow in multiplication") from exc

    if op == "/":
        if float(right) == 0.0:
            raise CalcDomainError("division by zero")
        try:
            return _check_finite(float(left) / float(right),"division")
        except OverflowError as exc:
            raise CalcOverflowError("overflow in division") from exc

    if op == "%":
        if float(right) == 0.0:
            raise CalcDomainError("modulo by zero")
        if both_int:
            return int(left) % int(right)
        try:
            return _check_finite(float(left) % float(right),"modulo")
        except OverflowError as exc:
            raise CalcOverflowError("overflow in modulo") from exc

    if op == "^":
        base=float(left)
        exp=float(right)
        if base == 0.0 and exp < 0.0:
            raise CalcDomainError("zero raised to a negative power")
        if base < 0.0 and not exp.is_integer():
            raise CalcDomainError("negative base with non-integer exponent")
        try:
            res=base ** exp
        except ZeroDivisionError as exc:
            raise CalcDomainError("zero raised to a negative power") from exc
        except ValueError as exc:
            raise CalcDomainError("invalid power operation") from exc
        except OverflowError as exc:
            raise CalcOverflowError("overflow in exponentiation") from exc
        return float(_check_finite(res,"exponentiation"))

    raise CalcDomainError(f"unknown operator '{op}'")


def evaluate(node: ExprNode) -> int | float:
    if isinstance(node,NumberNode):
        return _check_finite(node.value,"number")

    if isinstance(node,ConstNode):
        if node.name not in CONSTANTS:
            raise CalcDomainError(f"unknown constant or function '{node.name}'")
        return CONSTANTS[node.name]

    if isinstance(node,UnaryNode):
        val=evaluate(node.operand)
        if node.op == "+":
            return _check_finite(val,"unary plus")
        if node.op == "-":
            try:
                neg=-val
            except OverflowError as exc:
                raise CalcOverflowError("overflow in unary minus") from exc
            return _check_finite(neg,"unary minus")
        raise CalcDomainError(f"unknown unary operator '{node.op}'")

    if isinstance(node,BinaryNode):
        left_val=evaluate(node.left)
        right_val=evaluate(node.right)
        return _eval_binary(node.op,left_val,right_val)

    if isinstance(node,CallNode):
        if node.name not in FUNCTIONS:
            raise CalcDomainError(f"unknown function '{node.name}'")
        arity,fn=FUNCTIONS[node.name]
        if len(node.args) != arity:
            raise CalcDomainError(
                f"function '{node.name}' expects {arity} argument(s), got {len(node.args)}"
            )
        eval_args=[evaluate(arg) for arg in node.args]
        return fn(*eval_args)

    raise CalcDomainError("invalid expression node")