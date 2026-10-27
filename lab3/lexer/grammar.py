# identifier
#   S -> LA
#   A -> LA | DA | epsilon

# L - letter
# D - digit

IDENTIFIER_GRAMMAR = {
    "start": "S",
    "production_rules": {
        "S": [("L", "A")],
        "A": [("L", "A"), ("D", "A"), (None, None)]
    }
}

# integer
# S -> DB | -B
# B -> DB | epsilon

INTEGER_GRAMMAR = {
    "start": "S",
    "production_rules": {
        "S": [("D", "R"), ("-", "N")],
        "N": [("D", "R")],
        "R": [("D", "R"), (None, None)]
    }
}


# real
# S -> DB | -N | D
# N -> DB
# B -> DB | D | .R
# R -> DR | D

REAL_GRAMMAR = {
    "start": "S",
    "production_rules": {
        "S": [("D", "B"), ("-", "N"), ("D", None)],
        "N": [("D", "B")],
        "B": [("D", "B"), ("D", None), (".", "R")],
        "R": [("D", "R"), ("D", None)]
    }
}