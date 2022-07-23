# %%
from ast import Pass
from typing import Callable, Union, Any, List, Tuple, TypeVar, Generic, Dict
from enum import Enum
from math import factorial, log, pi
from __future__ import annotations
import re

PassedData = Union[float, int, str, bool, None]
ExecResponse = Callable[[Dict[str, PassedData]],
                        Callable[[Dict[str, PassedData]],float]]


class NodeType(Enum):
    VARIABLE = "VARIABLE"
    TOKEN_GROUP = "TOKEN_GROUP"
    OPERATOR = "OPERATOR"
    FUNCTION = "FUNCTION"
    CONSTANT = "CONSTANT"
    NUMBER = "NUMBER"


class Node():
    value: Union[str, None] = None
    type: Union[NodeType, None] = None
    node_a: Node = None
    node_b: Node = None

    def __init__(self, value: Union[str, None] = None):
        self.value = value

    def __str__(self):
        return self.__str__

    def __str__(self):
        '{type}: {value}'.format(type=str(self.type), value=str(self.exec()))

    def exec(self) -> ExecResponse:
        return self.value


class NumberNode(Node):
    type = NodeType.NUMBER

    def exec(self) -> ExecResponse:
        return lambda **kwargs: float(self.value)


class ConstantNode(Node):
    type = NodeType.CONSTANT

    def __str__(self):
        return 'Constant {value} = {ex}'.format(value=self.value, ex=str(self.exec()))

    def exec(self) -> ExecResponse:
        if self.value == 'pi':
            return lambda **kwargs: pi
        raise Exception(
            '{value} is not a defined constant'.format(value=self.value))


class VariableNode(Node):
    type = NodeType.VARIABLE

    def exec(self) -> ExecResponse:
        return lambda **kwargs: kwargs.get(self.value,None)


operators = [
    ('ADD', '+',0),
    ('SUBTRACT', '-',0),
    ('MULTIPLY', '*',1),
    ('DIVIDE', '/',1),
    ('MODULUS', '%',1),
    ('INT_DIVIDE', '//',1),
    ('FACTORIAL', '!',3),
    ('EXPONENTIAL', '^',2)
]

operatorMap = {o[1]: o[0] for o in operators}
operatorWeightMap = {o[1]: o[2] for o in operators}
OperatorType = Enum('OperatorType', dict(map(lambda x: x[:2],operators)))


class OperatorNode(Node):
    type = NodeType.OPERATOR
    operator: OperatorType

    def __init__(self, value):
        super().__init__(value)
        if operatorMap.get(value, None):
            self.operator = OperatorType(value)
        else:
            raise Exception('Invalid Operator: {op}'.format(op=value))

    def __str__(self):
        '{node_a} {operator} {node_b}'.format(
            node_a=str(self.node_a), operator=self.operator, node_b=str(self.node_b))

    def exec(self) -> ExecResponse:
        if self.node_a is None and self.node_b is None:
            raise Exception("Both targets on opperand are None")

        # Operations where only 1 node needs to be defined
        if self.operator is OperatorType.ADD:
            if self.node_a is None:
                return lambda **kwargs: abs(self.node_b.exec()(**kwargs))
            return lambda **kwargs: self.node_a.exec()(**kwargs) + self.node_b.exec()(**kwargs)

        if self.operator is OperatorType.SUBTRACT:
            if self.node_a is None:
                return lambda **kwargs: -1 * self.node_b.exec()(**kwargs)
            return lambda **kwargs: self.node_a.exec()(**kwargs) - self.node_b.exec()(**kwargs)

        if self.operator is OperatorType.FACTORIAL:
            if self.node_b is None:
                return lambda **kwargs: factorial(self.node_a.exec()(**kwargs))
            raise Exception('Factorial Operand can not have second target')

        if self.node_a is None or self.node_b is None:
            raise Exception("One target on opperand is None")

        # Operations where both nodes need to be defined
        if self.operator is OperatorType.MULTIPLY:
            return lambda **kwargs: self.node_a.exec()(**kwargs) * self.node_b.exec()(**kwargs)

        if self.operator is OperatorType.DIVIDE:
            return lambda **kwargs: self.node_a.exec()(**kwargs) / self.node_b.exec()(**kwargs)

        if self.operator is OperatorType.MODULUS:
            return lambda **kwargs: self.node_a.exec()(**kwargs) % self.node_b.exec()(**kwargs)

        if self.operator is OperatorType.INT_DIVIDE:
            return lambda **kwargs: self.node_a.exec()(**kwargs) // self.node_b.exec()(**kwargs)

        if self.operator is OperatorType.EXPONENTIAL:
            return lambda **kwargs: self.node_a.exec()(**kwargs) ** self.node_b.exec()(**kwargs)


# TODO work out comma spaced argument functions
functions = [
    ('LOG10', 'log10'),
    ('NATURAL_LOG', 'ln'),
    ('SQUARE_ROOT', 'sqrt'),
]

functionMap = {v: k for k, v in functions}
FunctionType = Enum('FunctionType', dict(functions))


class FunctionNode(Node):
    type: NodeType = NodeType.FUNCTION
    function: FunctionType
    arguments: List[TokenGroupNode] = []

    def __init__(self, value):
        super().__init__(value)
        if functionMap.get(value, None):
            self.function = FunctionType(value)
        else:
            raise Exception(
                'Invalid Function: {function}'.format(function=value))

    def __str__(self):
        '{function}({node_a})'.format(
            node_a=str(self.node_a), function=self.function)

    def exec(self) -> ExecResponse:
        if len(self.arguments) == 0:
            raise Exception("Function argument is None")

        if self.function is FunctionType.LOG10:
            return lambda **kwargs: log(self.arguments[0].exec()(**kwargs), 10)

        if self.function is FunctionType.NATURAL_LOG:
            return lambda **kwargs: log(self.arguments[0].exec()(**kwargs))

        if self.function is FunctionType.SQUARE_ROOT:
            return lambda **kwargs: self.arguments[0].exec()(**kwargs) ** 0.5

class TokenGroupNode(Node):
    type: NodeType = NodeType.TOKEN_GROUP
    tokens: List[Tuple[NodeType, str]] = []

    def __init__(self, value):
        super().__init__(value)
        self.tokens = tokenizeExpression(value)
    
    def exec(self) -> ExecResponse:
        tree = createExpressionTree(self.tokens)
        return lambda **kwargs: tree.exec()(**kwargs)

tokenRegex = ("((?<=\[)[a-z_]+(?=\]))"
              + "|(\((?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*\))"
              + "|([^a-z0-9\[\]\(\)]+)"
              + "|([a-z][a-z_0-9]+(?=\())"
              + "|([a-z][a-z_0-9]+)"
              + "|([0-9.]+)")

nodeTypes = {
    1: NodeType.VARIABLE,
    2: NodeType.TOKEN_GROUP,
    3: NodeType.OPERATOR,
    4: NodeType.FUNCTION,
    5: NodeType.CONSTANT,
    6: NodeType.NUMBER
}


def tokenizeExpression(expression: str) -> List[Tuple[NodeType, str]]:
    expression = expression.replace(' ', '')
    matches = re.finditer(tokenRegex, expression, re.MULTILINE | re.IGNORECASE)
    tokens = []
    for match in matches:
        # print(match.groups())
        for groupNum, group in enumerate(match.groups(), start=1):
            if group:
                tokens.append((nodeTypes[groupNum], expression[match.start(
                    groupNum):match.end(groupNum)].lower()))
    return tokens

def orderOfOperations(tokens):
    weights = sorted(set(operatorWeightMap.values()),reverse=True)[:-1]
    for w in weights:
        i = 1
        while i < len(tokens):
            t, v = tokens[i]
            if t is NodeType.OPERATOR and operatorWeightMap[v] == w:
                isSingleOperator = int(v in ['!'])
                tokenGroup = '(' + ''.join([t[1] for t in tokens[(i-1):(i+2-isSingleOperator)]]) + ')'
                tokens[i-1] = (NodeType.TOKEN_GROUP, tokenGroup)
                tokens = tokens[:i] + tokens[(i+2-isSingleOperator):]
                i-=1
            i+=1
    return tokens

def createExpressionTree(tokens: List[Tuple[NodeType, str]]) -> Node:
    base = Node()
    for t, v in tokens:
        if t is NodeType.OPERATOR:
            newBase = OperatorNode(v)
            if base.value is None:
                newBase.node_a = base.node_a
                newBase.node_b = base.node_b
            else:
                newBase = OperatorNode(v)
                newBase.node_a = base
            base = newBase
        elif t.value is NodeType.TOKEN_GROUP.value:
            v = v[1:-1]
            if base.node_a and base.node_a.type is NodeType.FUNCTION:
                funcArgumentNodes = [TokenGroupNode(arg) for arg in v.split(r",\s*(?![^()]*\))")] # split by commas not in parentheses
                base.node_a.arguments.extend(funcArgumentNodes)
            elif base.node_b and base.node_b.type is NodeType.FUNCTION:
                funcArgumentNodes = [TokenGroupNode(arg) for arg in v.split(r",\s*(?![^()]*\))")] # split by commas not in parentheses
                base.node_b.arguments.extend(funcArgumentNodes)
            elif base.node_a is None:
                base.node_a = TokenGroupNode(v)
            elif base.node_b is None:
                base.node_b = TokenGroupNode(v)
            else:
                raise Exception('Operator can not have more than 2 children')
        else: # Number Function Constant Variable 
            nodeClass = NumberNode
            if t is NodeType.FUNCTION: nodeClass = FunctionNode
            elif t is NodeType.VARIABLE: nodeClass = VariableNode
            elif t is NodeType.CONSTANT: nodeClass = ConstantNode
            
            if base.value is None:
                base = nodeClass(v)
            elif base.node_a is None:
                base.node_a = nodeClass(v)
            elif base.node_b is None:
                base.node_b = nodeClass(v)
            else:
                raise Exception('Operator can not have more than 2 children')

    return base




# %%
expression = '5+9*3^3!'
tokens = tokenizeExpression(expression)
# print(tokens)
tokens = orderOfOperations(tokens)
print(tokens)
tree = createExpressionTree(tokens)
tree.exec()()
# %%
