import ctypes
import re
from pathlib import Path

library_name = "st.dll"
library_path = Path(__file__).resolve().parent / library_name
st = ctypes.CDLL(str(library_path))
st.connect_init.argtypes= []
st.connect_init.restype = None

st.connect_insert.argtypes = [ctypes.c_char_p]
st.connect_insert.restype = ctypes.c_int

st.connect_search.argtypes = [ctypes.c_char_p]
st.connect_search.restype = ctypes.c_int

st.connect_print.argtypes = []
st.connect_print.restype = None

st.connect_destroy.argtypes = []
st.connect_destroy.restype = None

st.connect_init()

identifier_pattern = re.compile(r"[a-zA-Z]|([a-zA-z]*[0-9]*)*")
digit_pattern = re.compile(r"[0-9]")
letter_pattern = re.compile(r"[a-zA-Z]")
unsigned_integer_pattern = re.compile(r"[1-9]|[1-9][0-9]+")
integer_pattern = re.compile(r"-?[0-9]+")
real_pattern = re.compile(r"-?[0-9]+\.[0-9]+")
string_pattern = re.compile(r'"[^"]*"')
KEYWORDS = {"if", "input", "output", "distance", "point", "line", "triangle", "rectangle", "circle", "end if", "end for", "translate", "by", "rotate", "scale", "area", "perimeter", "else"}
OPERATORS = {"+", "-", "*", "/", "=", "==", "and", "or", "<=", "<", ">=", ">"}
SEPARATORS = {"(", ")", ",", ";", "[", "]"}

# TOKEN_PATTERN = re.compile(
#     r'(?P<STRING>"[^"]*")'
#     r'(?P<REAL>[+-]?[0-9]+\.[0-9]+)'
#     r'(?P<OPERATOR>==|<=|>=|[+\-*/=<>])?'
#     r'(?P<SEPARATOR>[(),;])'
#     r'(?P<INTEGER>0|[+-]?[0-9]+)'
#     r'(?P<IDENTIFIER>[a-zA-Z]|([a-zA-z]*[0-9]*)*)'
#     r'(?P<KEYWORD>\b(?:if|input|output|distance|point|line|triangle|rectangle|circle|area|perimeter|translate|scale|rotate|by)\b)'
# )

TOKEN_PATTERN = re.compile(
    r'(?P<STRING>"[^"]*")'
    r'|(?P<REAL>-?[0-9]+\.[0-9]+)'
    r'|(?P<INTEGER>-?[0-9]+)'
    r'|(?P<OPERATOR>==|<=|>=|[+\-*/=<>])'
    r'|(?P<SEPARATOR>[(),;\[\]])'
    r'|(?P<KEYWORD>\b(?:if|for|input|output|distance|point|line|triangle|rectangle|circle|area|perimeter|translate|scale|rotate|by|else|->)\b)'
    r'|(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z_0-9]*)'
)

def get_symbol_position(symbol):
    encoded = symbol.encode("utf-8")
    position = st.connect_search(encoded)
    if position == -1:
        position = st.connect_insert(encoded)
    if position == -1:
        raise Exception("Could not find symbol position")

    return position

def process_token(token, pif):
    if token[1] in KEYWORDS:
        pif.append((token[1], 0))
    elif token[1] in OPERATORS:
        pif.append((token[1], 0))
    elif token[1] in SEPARATORS:
        pif.append((token[1], 0))
    elif string_pattern.match(token[1]):
        position = get_symbol_position(token[1])
        pif.append((token[1], position))
    elif identifier_pattern.fullmatch(token[1]):
        position = get_symbol_position(token[1])
        pif.append(("IDENTIFIER", position))
    elif real_pattern.fullmatch(token[1]):
        position = get_symbol_position(token[1])
        pif.append(("CONSTANT", position))
    # elif unsigned_integer_pattern.fullmatch(token[1]):
    #     position = get_symbol_position(token[1])
    #     pif.append(("CONSTANT", position))
    elif integer_pattern.fullmatch(token[1]):
        position = get_symbol_position(token[1])
        pif.append(("CONSTANT", position))

    else:
        print(f"{token} is not a valid token")

def recognize_token(token):
    if token[1] in KEYWORDS:
        return "keyword"
    elif token[1] in OPERATORS:
        return "operator"
    elif token[1] in SEPARATORS:
        return "separator"
    elif real_pattern.fullmatch(token[1]):
        return "real_constant"
    elif unsigned_integer_pattern.fullmatch(token[1]):
        return "unsigned_integer_constant"
    elif integer_pattern.fullmatch(token[1]):
        return "integer_constant"
    elif identifier_pattern.fullmatch(token[1]):
        return "identifier"

def tokenize_line(line):
    tokens = []
    pos = 0
    while pos < len(line):
        if line[pos].isspace():
            pos += 1
            continue

        match = TOKEN_PATTERN.match(line, pos)
        if match:
            token_type = match.lastgroup
            token_value = match.group()

            tokens.append((token_type, token_value))
            pos = match.end()
        else:
            print(f"Lexical error at position {pos}: {line[pos]!r}")
            pos +=1
    return tokens

if __name__ ==  "__main__":
    pif = []
    with open("program1.txt") as f:
        line = f.readline()
        while line:
            tokens = tokenize_line(line)
            # tokens = line.split()
            for token in tokens:
                print(token)
                process_token(token, pif)
            line = f.readline()

    print("PIF:")
    for entry in pif:
        print(entry)
    print("ST:")
    st.connect_print()
    st.connect_destroy()