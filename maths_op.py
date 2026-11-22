import math
from typing import Callable
from calc_errors import CalcDomainError, CalcOverflowError


CONSTANTS:dict[str,float]={"PI": 3.141592653589793,"E": 2.718281828459045,"h": 6.62607015e-34,"G": 6.67430e-11,
                            "Na": 6.02214076e23,"e": 1.602176634e-19,"kB": 1.380649e-23,"epsilon0": 8.8541878128e-12,
                            "mu0": 1.25663706212e-6,"c": 299792458.0}


def _to_float(val: int | float) -> float:
    if isinstance(val,bool):
        raise CalcDomainError("boolean value is not allowed")
    f=float(val)
    if not math.isfinite(f):
        raise CalcOverflowError("value is not finite")
    return f

def _to_int(val:int | float,fn_name:str) -> int:
    if isinstance(val,bool):
        raise CalcDomainError(f"{fn_name} expects an integer")
    if isinstance(val,int):
        return val
    if not math.isfinite(val) or not val.is_integer():
        raise CalcDomainError(f"{fn_name} requires a whole number, got {val}")
    return int(val)

def _call_math(fn:Callable[[float],float],x: int | float,name:str) -> float:
    xf=_to_float(x)
    try:
        out=fn(xf)
    except ValueError as exc:
        raise CalcDomainError(f"{name} domain error for {xf}") from exc
    except OverflowError as exc:
        raise CalcOverflowError(f"{name} overflow for {xf}") from exc
    if not math.isfinite(out):
        raise CalcOverflowError(f"{name} overflow for {xf}")
    return out


def _sin(x:int | float) -> float:
    return _call_math(math.sin,x,"sin")
def _cos(x:int | float) -> float:
    return _call_math(math.cos,x,"cos")
def _tan(x: int | float) -> float:
    xf=_to_float(x)
    if abs(math.cos(xf)) < 1e-15:
        raise CalcDomainError(f"tan undefined at {xf}")
    return _call_math(math.tan,xf,"tan")
def _asin(x: int | float) -> float:
    return _call_math(math.asin,x,"asin")
def _acos(x: int | float) -> float:
    return _call_math(math.acos,x,"acos")
def _atan(x: int | float) -> float:
    return _call_math(math.atan,x,"atan")
def _sinh(x: int | float) -> float:
    return _call_math(math.sinh,x,"sinh")
def _cosh(x: int | float) -> float:
    return _call_math(math.cosh,x,"cosh")
def _tanh(x: int | float) -> float:
    return _call_math(math.tanh,x,"tanh")
def _log(x: int | float) -> float:
    xf=_to_float(x)
    if xf <= 0.0:
        raise CalcDomainError("log requires a positive number")
    return _call_math(math.log,xf,"log")

def _log10(x: int | float) -> float:
    xf=_to_float(x)
    if xf <= 0.0:
        raise CalcDomainError("log10 requires a positive number")
    return _call_math(math.log10,xf,"log10")

def _antilog(x: int | float) -> float:
    xf=_to_float(x)
    try:
        out=10.0 ** xf
    except OverflowError as exc:
        raise CalcOverflowError(f"antilog overflow for {xf}") from exc
    if not math.isfinite(out):
        raise CalcOverflowError(f"antilog overflow for {xf}")
    return float(out)


def _exp(x: int | float) -> float:
    return _call_math(math.exp,x,"exp")

def _fact(n: int | float) -> int:
    iv=_to_int(n,"fact")
    if iv < 0:
        raise CalcDomainError("fact requires a non-negative integer")
    try:
        return math.factorial(iv)
    except OverflowError as exc:
        raise CalcOverflowError("factorial overflow") from exc


def _ncr(n: int | float,r: int | float) -> int:
    ni=_to_int(n,"nCr")
    ri=_to_int(r,"nCr")
    if ni < 0 or ri < 0 or ri > ni:
        raise CalcDomainError("nCr requires 0 <= r <= n with non-negative integers")
    return math.comb(ni,ri)


def _npr(n: int | float,r: int | float) -> int:
    ni=_to_int(n,"nPr")
    ri=_to_int(r,"nPr")
    if ni < 0 or ri < 0 or ri > ni:
        raise CalcDomainError("nPr requires 0 <= r <= n with non-negative integers")
    return math.perm(ni,ri)



def _root(x: int | float,n: int | float) -> float:
    xf=_to_float(x)
    ni=_to_int(n,"root")
    if ni == 0:
        raise CalcDomainError("root degree cannot be zero")
    if xf < 0.0 and ni % 2 == 0:
        raise CalcDomainError("even root of a negative number is not real")
    try:
        if xf < 0.0:
            out=-((-xf) ** (1.0 / ni))
        else:
            out=xf ** (1.0 / ni)
    except OverflowError as exc:
        raise CalcOverflowError("root overflow") from exc
    if not math.isfinite(out):
        raise CalcOverflowError("root overflow")
    return float(out)




def _floor(x: int | float) -> int:
    return math.floor(_to_float(x))
def _ceil(x: int | float) -> int:
    return math.ceil(_to_float(x))



def _signum(x: int | float) -> int:
    xf=_to_float(x)
    if xf > 0.0:
        return 1
    if xf < 0.0:
        return -1
    return 0


def _heaviside(x: int | float) -> int:
    xf=_to_float(x)
    return 0 if xf < 0.0 else 1


def _sigmoid(x: int | float) -> float:
    xf=_to_float(x)
    if xf < -700.0:
        return 0.0
    try:
        return 1.0 / (1.0 + math.exp(-xf))
    except OverflowError:
        return 0.0


def _gcd(a: int | float,b: int | float) -> int:
    ai=_to_int(a,"gcd")
    bi=_to_int(b,"gcd")
    return math.gcd(ai,bi)


def _lcm(a: int | float,b: int | float) -> int:
    ai=_to_int(a,"lcm")
    bi=_to_int(b,"lcm")
    if ai == 0 or bi == 0:
        return 0
    return abs(ai * bi) // math.gcd(ai,bi)


def _totient(n: int | float) -> int:
    ni=_to_int(n,"totient")
    if ni < 1:
        raise CalcDomainError("totient requires a positive integer")
    count=0
    for k in range(1,ni + 1):
        if math.gcd(k,ni) == 1:
            count += 1
    return count


def _fusc(n: int | float) -> int:
    ni=_to_int(n,"fusc")
    if ni < 0:
        raise CalcDomainError("fusc requires a non-negative integer")
    if ni == 0:
        return 0
    a,b=0,1
    for bit in bin(ni)[2:]:
        if bit == "0":
            b=a + b
        else:
            a=a + b
    return a


FUNCTIONS: dict[str,tuple[int,Callable[...,int | float]]] = {
    "sin": (1,_sin),
    "cos": (1,_cos),
    "tan": (1,_tan),
    "asin": (1,_asin),
    "acos": (1,_acos),
    "atan": (1,_atan),
    "sinh": (1,_sinh),
    "cosh": (1,_cosh),
    "tanh": (1,_tanh),
    "log": (1,_log),
    "log10": (1,_log10),
    "antilog": (1,_antilog),
    "exp": (1,_exp),
    "fact": (1,_fact),
    "nCr": (2,_ncr),
    "nPr": (2,_npr),
    "root": (2,_root),
    "floor": (1,_floor),
    "ceil": (1,_ceil),
    "signum": (1,_signum),
    "heaviside": (1,_heaviside),
    "sigmoid": (1,_sigmoid),
    "gcd": (2,_gcd),
    "lcm": (2,_lcm),
    "totient": (1,_totient),
    "fusc": (1,_fusc),
}