from dataclasses import dataclass

from calc_errors import CalcSyntaxError

_SINGLE_CHARS: dict[str,str] = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "%": "PERCENT",
    "^": "CARET",
    "(": "LPAREN",
    ")": "RPAREN",
    ",": "COMMA",
}


@dataclass(frozen=True)
class Token:
    kind: str
    value: int | float | str
    pos: int


def _read_number(text: str,start: int) -> tuple[Token,int]:
    n=len(text)
    i=start
    has_dot=False
    has_digits=False

    if text[i] == ".":
        has_dot=True
        i += 1
        while i < n and text[i].isdigit():
            has_digits=True
            i += 1
        if not has_digits:
            raise CalcSyntaxError(f"invalid number at position {start}")
    else:
        while i < n and text[i].isdigit():
            has_digits=True
            i += 1
        if i < n and text[i] == ".":
            has_dot=True
            i += 1
            while i < n and text[i].isdigit():
                i += 1

    has_exp=False
    if i < n and text[i] in ("e","E"):
        j=i + 1
        if j < n and text[j] in ("+","-"):
            j += 1
        if j < n and text[j].isdigit():
            has_exp=True
            i=j
            while i < n and text[i].isdigit():
                i += 1

    if i < n and text[i] == ".":
        raise CalcSyntaxError(f"malformed number near position {i}")

    raw=text[start:i]
    if has_dot or has_exp:
        try:
            val: int | float=float(raw)
        except ValueError as exc:
            raise CalcSyntaxError(f"invalid numeric literal '{raw}'") from exc
    else:
        val=int(raw)

    return Token("NUMBER",val,start),i


def _read_ident(text: str,start: int) -> tuple[Token,int]:
    n=len(text)
    i=start
    while i < n and (text[i].isalnum() or text[i] == "_"):
        i += 1
    return Token("IDENT",text[start:i],start),i


def tokenize(text: str) -> list[Token]:
    tokens: list[Token]=[]
    n=len(text)
    i=0

    while i < n:
        ch=text[i]
        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            tok,i=_read_number(text,i)
        elif ch.isalpha() or ch == "_":
            tok,i=_read_ident(text,i)
        elif ch in _SINGLE_CHARS:
            tok=Token(_SINGLE_CHARS[ch],ch,i)
            i += 1
        else:
            raise CalcSyntaxError(f"unexpected character '{ch}' at position {i}")

        if tokens:
            prev=tokens[-1]
            if prev.kind in ("NUMBER","RPAREN") and tok.kind in ("NUMBER","IDENT","LPAREN"):
                raise CalcSyntaxError(f"implied multiplication not allowed near position {tok.pos}")
            if prev.kind == "IDENT" and tok.kind == "NUMBER":
                raise CalcSyntaxError(f"unexpected number '{tok.value}' after identifier '{prev.value}'")

        tokens.append(tok)

    return tokens