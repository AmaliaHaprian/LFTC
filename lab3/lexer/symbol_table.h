#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    char *symbol;
    int position;
    struct Node *left, *right;
} Node;

typedef struct {
    Node *root;
    int size;
} SymbolTable;

void init(SymbolTable *st);
int search(SymbolTable *st, const char *symbol);
int insert(SymbolTable *st, const char *symbol);
void print(SymbolTable *st);
void destroy(SymbolTable *st);
