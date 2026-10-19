#include "symbol_table.h"

static SymbolTable st;
void connect_init(void) {
    init(&st);
}

int connect_insert(const char *symbol) {
    return insert(&st, symbol);
}

int connect_search(const char *symbol) {
    return search(&st, symbol);
}

void connect_print(void) {
    print(&st);
}

void connect_destroy(void) {
    destroy(&st);
}