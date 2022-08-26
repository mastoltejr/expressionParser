type PassedData = number | string | boolean | null;
type ExecResponse = (data: Record<string, PassedData>) => PassedData;

type NodeType =
  | 'STRING'
  | 'VARIABLE'
  | 'TOKEN_GROUP'
  | 'OPERATOR'
  | 'COMPARATOR'
  | 'FUNCTION'
  | 'CONSTANT'
  | 'NUMBER';

class ExpressionNode {
  public value: string | null = null;
  public type: NodeType | null = null;
  public node_a: ExpressionNode | null = null;
  public node_b: ExpressionNode | null = null;

  constructor(value: string | null) {
    this.value = value;
  }

  public toString() {
    return `${this.type}: ${this.exec()}`;
  }

  public exec(): ExecResponse {
    throw new Error('Can not execute on an empty node');
  }
}

class StringNode extends ExpressionNode {
  public type: NodeType = 'STRING';

  public exec(): ExecResponse {
    return (...kwargs) => String(this.value);
  }
}

class NuberNode extends ExpressionNode {
  public type: NodeType = 'NUMBER';

  public exec(): ExecResponse {
    return (...kwargs) => Number(this.value);
  }
}

class ConstantNode extends ExpressionNode {
  public type: NodeType = 'CONSTANT';

  public toString() {
    return `Constant ${this.value} = ${this.exec}`;
  }

  public exec(): ExecResponse {
    switch (this.value) {
      case 'pi':
        return (...kwargs) => Math.PI;
      default:
        throw new Error(`${this.value} is not a defined constant`);
    }
  }
}

class VariableNode extends ExpressionNode {
  public type: NodeType = 'VARIABLE';

  public exec(): ExecResponse {
    return (...kwargs) => kwargs[this.value ?? ''];
  }
}

type Operator =
  | 'ADD'
  | 'SUBTRACT'
  | 'MULTIPLY'
  | 'DIVIDE'
  | 'MODULUS'
  | 'INT_DIVIDE'
  | 'FACTORIAL'
  | 'EXPONENTIAL';

const operatorMap: Record<string, Operator> = {
  '+': 'ADD',
  '-': 'SUBTRACT',
  '*': 'MULTIPLY',
  '/': 'DIVIDE',
  '%': 'MODULUS',
  '//': 'INT_DIVIDE',
  '!': 'FACTORIAL',
  '^': 'EXPONENTIAL'
};

const operatorWeightMap: Record<Operator, number> = {
  ADD: 0,
  SUBTRACT: 0,
  MULTIPLY: 1,
  DIVIDE: 1,
  MODULUS: 1,
  INT_DIVIDE: 1,
  FACTORIAL: 3,
  EXPONENTIAL: 2
};

class OperatorNode extends ExpressionNode {
  public type: NodeType = 'OPERATOR';
  public operator: Operator | null = null;
  public weight: number = 0;

  constructor(value) {
    super(value);
    if (operatorMap[value] !== undefined) {
      this.operator = operatorMap[value];
      this.weight = operatorWeightMap[this.operator] ?? 0;
    } else {
      throw new Error(`Invalid Operator: ${value}`);
    }
  }

  public toString() {
    return `${String(this.node_a)} ${this.value} ${String(this.node_b)}`;
  }

  public exec(): ExecResponse {
    if (this.node_a == null && this.node_b == null) {
      throw new Error('Both targers on opperand are null');
    }
    try {
      if (this.operator === 'ADD') {
        if (this.node_a == null)
          return (...kwargs) => this.node_b!.exec()(...kwargs);
        return (...kwargs) =>
          //@ts-ignore
          this.node_a!.exec()(...kwargs) + this.node_b!.exec()(...kwargs);
      }

      if (this.operator === 'SUBTRACT') {
      }
    } catch (err) {
      throw new Error(`Unsupported '${this.value}' operation`);
    }

    throw new Error('Unsupported operator ' + this.value);
  }
}
