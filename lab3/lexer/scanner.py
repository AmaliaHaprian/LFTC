import re
from fa import is_identifier, is_integer_constant, is_real_constant
import main as main

KEYWORDS = {"if", "input", "output", "distance", "point", "line", "triangle", "rectangle", "circle", "end if", "end for", "translate", "by", "rotate", "scale", "area", "perimeter", "else"}
OPERATORS = {"+", "-", "*", "/", "=", "==", "and", "or", "<=", "<", ">=", ">"}
SEPARATORS = {"(", ")", ",", ";", "[", "]"}

def classify(token):
    if is_identifier(token):
        return "IDENTIFIER"
    elif is_integer_constant(token):
        return "INTEGER"
    elif is_real_constant(token):
        return "REAL"
    else:
        return "OTHER"

def process_token(token, pif):
    if token[1] == "STRING":
        position = main.get_symbol_position(token[1])
        pif.append(("STRING", position))
    elif token[1] in KEYWORDS or token[1] in OPERATORS or token[1] in SEPARATORS:
        pif.append((token[1], 0))
    else:
        classification = classify(token[1])
        if classification != "OTHER":
            position = main.get_symbol_position(token[1])
            pif.append((classification, position))
        else:
            print("Lexical error for: ", token[1])

TOKEN_PATTERN = re.compile(
    r'(?P<STRING>"[^"]*")'
    # r'|(?P<REAL>-?[0-9]+\.[0-9]+)'
    # r'|(?P<INTEGER>-?[0-9]+)'
    r'|(?P<OPERATOR>==|<=|>=|->|[+*/=<>])'
    r'|(?P<SEPARATOR>[(),;\[\]])'
    r'|(?P<KEYWORD>\b(?:if|for|input|output|distance|point|line|triangle|rectangle|circle|area|perimeter|translate|scale|rotate|by|else|->)\b)'
    # r'|(?P<ELSE>-?[a-zA-Z0-9]+)'
    # r'|(?P<ELSE>\S+)'
    r'|(?P<WORD>[^ \t\n+*/=<>(),;\[\]]+)'
)

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
            for token in tokens:
                print(token)
                process_token(token, pif)
            line = f.readline()

    print("PIF:")
    for entry in pif:
        print(entry)
    print("ST:")
    main.st.connect_print()
    main.st.connect_destroy()