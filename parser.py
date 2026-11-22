from dataclasses import dataclass

from calc_errors import CalcSyntaxError
from tokenizer import Token


@dataclass(frozen=True)
class NumberNode:
    value: int | float
@dataclass(frozen=True)
class ConstNode:
    name: str
@dataclass(frozen=True)
class UnaryNode:
    op: str
    operand: "ExprNode"
@dataclass(frozen=True)
class BinaryNode:
    op: str
    left: "ExprNode"
    right: "ExprNode"
@dataclass(frozen=True)
class CallNode:
    name: str
    args: tuple["ExprNode", ...]
    
ExprNode = NumberNode | ConstNode | UnaryNode | BinaryNode | CallNode


class _Parser:
    def __init__(self,tokens: list[Token]) -> None:
        self.tokens=tokens
        self.pos=0

    def _peek(self) -> Token | None:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _consume(self,kind: str,msg: str) -> Token:
        tok=self._peek()
        if tok is None or tok.kind != kind:
            raise CalcSyntaxError(msg)
        self.pos += 1
        return tok

    def parse_expr(self) -> ExprNode:
        if not self.tokens:
            raise CalcSyntaxError("empty expression")
        node=self._parse_add_sub()
        if self._peek() is not None:
            raise CalcSyntaxError(f"unexpected token '{self._peek().value}'")
        return node

    def _parse_add_sub(self) -> ExprNode:
        node=self._parse_mul_div()
        while (tok := self._peek()) is not None and tok.kind in ("PLUS","MINUS"):
            self.pos += 1
            right=self._parse_mul_div()
            node=BinaryNode(str(tok.value),node,right)
        return node

    def _parse_mul_div(self) -> ExprNode:
        node=self._parse_unary()
        while (tok := self._peek()) is not None and tok.kind in ("STAR","SLASH","PERCENT"):
            self.pos += 1
            right=self._parse_unary()
            node=BinaryNode(str(tok.value),node,right)
        return node

    def _parse_unary(self) -> ExprNode:
        tok=self._peek()
        if tok is not None and tok.kind in ("PLUS","MINUS"):
            self.pos += 1
            operand=self._parse_unary()
            return UnaryNode(str(tok.value),operand)
        return self._parse_power()

    def _parse_power(self) -> ExprNode:
        base=self._parse_primary()
        tok=self._peek()
        if tok is not None and tok.kind == "CARET":
            self.pos += 1
            # Right-associative; allows unary +/- in exponent (e.g. 2 ^ -1)
            exp=self._parse_unary()
            return BinaryNode("^",base,exp)
        return base

    def _parse_primary(self) -> ExprNode:
        tok=self._peek()
        if tok is None:
            raise CalcSyntaxError("unexpected end of expression")

        if tok.kind == "NUMBER":
            self.pos += 1
            assert isinstance(tok.value,(int,float))
            return NumberNode(tok.value)

        if tok.kind == "LPAREN":
            self.pos += 1
            inner=self._parse_add_sub()
            self._consume("RPAREN","missing closing ')'")
            return inner

        if tok.kind == "IDENT":
            self.pos += 1
            name=str(tok.value)
            nxt=self._peek()
            if nxt is not None and nxt.kind == "LPAREN":
                self.pos += 1
                args: list[ExprNode]=[]
                if (after := self._peek()) is not None and after.kind == "RPAREN":
                    self.pos += 1
                    return CallNode(name,tuple(args))
                while True:
                    args.append(self._parse_add_sub())
                    sep=self._peek()
                    if sep is not None and sep.kind == "COMMA":
                        self.pos += 1
                        continue
                    if sep is not None and sep.kind == "RPAREN":
                        self.pos += 1
                        break
                    raise CalcSyntaxError(f"expected ',' or ')' in call to '{name}'")
                return CallNode(name,tuple(args))
            return ConstNode(name)

        raise CalcSyntaxError(f"unexpected token '{tok.value}' at position {tok.pos}")


def parse(tokens: list[Token])->ExprNode:
    return _Parser(tokens).parse_expr()