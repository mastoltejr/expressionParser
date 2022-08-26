# mathExpressionParser

Math Expression Parser that works with [ + - * / ^ // ! ] operators, constants [ pi ], functions [ exp, log, ln ], strings ["testString"], and [variables] out of the box and can be expanded to cover more use cases!

## Motivation

A lot of the math expression parsers I found online didn't quite cover all the use cases I needed as well as were hard to expand upon. With that, I created my own!

## How To Install

```
pip install expressionParser
```

## How To Use

Regardless of the language, you'll primarily use 2 lines of code in order.

1. createExpressionTree - This function takes the list of nodes from extractNodes and creates a binary tree. Each parent node is an operator or a function, and each child node is a number, constant, or token group. This function returns the base node of the tree which you can call exec() on to prepare the tree.
2. The result of the base Node's exec() function is a function that takes in an optional dictionary argument. If any variables are defined in the expression, the variables will be replaced with the dictionary key-value where the key is the variable's name.

What's great about this approach is say you have a table represented as a list of dictionaries. If you'd want to add a calculated column that is some expression based on other row values, you can create the new column easily.

**Example in python**

```python
from expressionParser import createExpressionTree

tbl = [{'a': 1, 'b': 2},{'a': 3, 'b': 4},{'a': 5, 'b': 6}]
expression = '[a]+2*[b]'
func = createExpressionTree(expression=expression).exec()
tbl = [{**r, 'c': func(**r)} for r in tbl]
print(tbl) # [{'a': 1, 'b': 2, 'c': 5.0},{'a': 3, 'b': 4, 'c': 11.0},{'a': 5, 'b': 6, 'c': 17.0}]
```
