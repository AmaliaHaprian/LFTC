from grammar import IDENTIFIER_GRAMMAR, INTEGER_GRAMMAR, REAL_GRAMMAR

FINAL = "FINAL"

def matches(symbol, char):
    if symbol == "D":
        return char in "0123456789"

    if symbol == "-":
        return True
    if symbol == "L":
        return char.isascii() and char.isalpha()

    return char == symbol

def rg_to_fa(grammar):
    productions = grammar["production_rules"]
    start_state = grammar["start"]

    states = set(productions.keys())
    states.add(FINAL)

    transitions = {state: [] for state in states}
    accepting_states = {FINAL}
    for nonterminal, rules in productions.items():
        for terminal, next_nonterminal in rules:

            if terminal is None:
                accepting_states.add(nonterminal)
                continue

            if next_nonterminal is None:
                transitions[nonterminal].append((terminal, FINAL))
            else:
                transitions[nonterminal].append((terminal, next_nonterminal))

    return {
        "states": states,
        "start": start_state,
        "transitions": transitions,
        "accepting_states": accepting_states,
    }

def accepts(automaton, token):
    current_states = {automaton["start"]}

    for char in token:
        next_states = set()

        for state in current_states:
            transitions_for_state = automaton["transitions"][state]
            #transitions_for_state = automaton["transitions"].get(state, [])
            for symbol, destination in transitions_for_state:
                if matches(symbol, char):
                    next_states.add(destination)

        current_states = next_states

        if not current_states:
            return False

    return bool (current_states & automaton["accepting_states"])


identifier_fa = rg_to_fa(IDENTIFIER_GRAMMAR)
integer_fa = rg_to_fa(INTEGER_GRAMMAR)
real_fa = rg_to_fa(REAL_GRAMMAR)

def is_identifier(token):
    return accepts(identifier_fa, token)


def is_integer_constant(token):
    return accepts(integer_fa, token)

def is_real_constant(token):
    return accepts(real_fa, token)

if __name__ == "__main__":
    print("IDENTIFIER TESTS")

    for token in ["A", "triangle1", "nr", "pointA",
                  "1point", ""]:
        print(f"{token}: {is_identifier(token)}")

    print("\nINTEGER CONSTANT TESTS")

    for token in ["0", "10", "-1", "-25", "-", "12a", ""]:
        print(f"{token}: {is_integer_constant(token)}")

    print("\nREAL CONSTANT TESTS")

    for token in ["0", "10", "-1.45", "-25.23", "234.432", "12a", ""]:
        print(f"{token }: {is_real_constant(token)}")

