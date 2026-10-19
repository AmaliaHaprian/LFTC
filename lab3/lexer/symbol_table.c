#include "symbol_table.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

static char *copy_string(const char *s) {
    size_t len = strlen(s) + 1;
    char *copy = malloc(len);

    if (copy != NULL) {
        memcpy(copy, s, len);
    }

    return copy;
}


void init(SymbolTable *st) {
    st->root = NULL;
    st->size = 0;
}

static Node *searchNode(Node *root, const char *symbol) {
    while (root != NULL) {
        int cmp = strcmp(symbol, root->symbol);

        if (cmp == 0) {
            return root;
        }

        if (cmp < 0) {
            root = root->left;
        } else {
            root = root->right;
        }
    }

    return NULL;
}
int search(SymbolTable *st, const char *symbol) {
    Node *node = searchNode(st->root, symbol);

    if (node == NULL) {
        return -1;
    }

    return node->position;
}

static Node *createNode(const char *symbol, int position) {
    Node *node = malloc(sizeof(Node));
    if (node == NULL)
        return NULL;

    node->symbol=copy_string(symbol);

    if (node->symbol == NULL) {
        free(node);
        return NULL;
    }

    node->position=position;
    node->left=NULL;
    node->right=NULL;

    return node;
}

static Node *insertNode(Node *root, const char *symbol, int position, int *success) {
    if (root == NULL) {
        Node *node = createNode(symbol, position);

        if (node == NULL) {
            *success = 0;
        }

        return node;
    }

    int cmp = strcmp(symbol, root->symbol);

    if (cmp == 0) {
        return root;  // Already exists
    }

    if (cmp < 0) {
        Node *child = insertNode(
            root->left, symbol, position, success
        );

        if (*success) {
            root->left = child;
        }
    } else {
        Node *child = insertNode(
            root->right, symbol, position, success
        );

        if (*success) {
            root->right = child;
        }
    }

    return root;
}
int insert(SymbolTable *st, const char *symbol) {
    Node *existing = searchNode(st->root, symbol);
    if (existing != NULL) {
        return existing->position;
    }

    int position = st->size+1;
    int success = 1;

    Node *new_root = insertNode(
        st->root, symbol, position, &success
    );

    if (!success) {
        return -1;  // Allocation failed
    }

    st->root = new_root;
    st->size++;

    return position;
}


static void print_inorder(Node *root) {
    if (root == NULL)
        return;
    
    print_inorder(root->left);

    printf("%d\t%s\n", root->position, root->symbol);

    print_inorder(root->right);
}

void print(SymbolTable *st) {
    printf("Position\tSymbol\n");
    print_inorder(st->root);
}

static void destroy_nodes(Node *root) {
    if (root == NULL) {
        return;
    }

    destroy_nodes(root->left);
    destroy_nodes(root->right);

    free(root->symbol);
    free(root);
}

void destroy(SymbolTable *st) {
    destroy_nodes(st->root);
    st->root = NULL;
    st->size = 0;
}