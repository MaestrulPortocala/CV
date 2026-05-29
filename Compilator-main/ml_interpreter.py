

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_ast import *
from typing import Dict, Any


class RuntimeError_(Exception):
    def __init__(self, msg: str):
        super().__init__(f"[Eroare Runtime] {msg}")


class Interpreter:
    def __init__(self):
        self.env: Dict[str, Any] = {}

    def run(self, program: Program):
        for stmt in program.statements:
            self._exec(stmt)
    def _exec(self, node: Stmt):
        if isinstance(node, AssignStmt):
            self.env[node.name] = self._eval(node.value)

        elif isinstance(node, VarDeclStmt):
            self.env[node.name] = self._eval(node.value)

        elif isinstance(node, PrintStmt):
            val = self._eval(node.expr)
            if isinstance(val, bool):
                print("true" if val else "false")
            elif isinstance(val, float):
                # Afișare fără trailing zeros
                s = f"{val:g}"
                print(s)
            else:
                print(val)

        elif isinstance(node, IfStmt):
            if self._eval(node.condition):
                for s in node.then_body:
                    self._exec(s)
            elif node.else_body:
                for s in node.else_body:
                    self._exec(s)

        elif isinstance(node, WhileStmt):
            limit = 100_000   
            count = 0
            while self._eval(node.condition):
                for s in node.body:
                    self._exec(s)
                count += 1
                if count >= limit:
                    raise RuntimeError_(f"Bucla while a depasit {limit} iteratii")

        else:
            raise RuntimeError_(f"Instrucțiune necunoscută: {type(node).__name__}")

    def _eval(self, node: Expr) -> Any:
        if isinstance(node, IntLiteral):   return node.value
        if isinstance(node, FloatLiteral): return node.value
        if isinstance(node, BoolLiteral):  return node.value

        if isinstance(node, VarExpr):
            if node.name not in self.env:
                raise RuntimeError_(f"Variabila '{node.name}' nu a fost initializata")
            return self.env[node.name]

        if isinstance(node, UnaryOp):
            v = self._eval(node.operand)
            if node.op == '-': return -v
            if node.op == '!': return not v

        if isinstance(node, BinOp):
            return self._eval_binop(node)

        raise RuntimeError_(f"Expresie necunoscută: {type(node).__name__}")

    def _eval_binop(self, node: BinOp) -> Any:
        op = node.op
        if op == '&&':
            return bool(self._eval(node.left)) and bool(self._eval(node.right))
        if op == '||':
            return bool(self._eval(node.left)) or bool(self._eval(node.right))

        l = self._eval(node.left)
        r = self._eval(node.right)

        if op == '+':  return l + r
        if op == '-':  return l - r
        if op == '*':  return l * r
        if op == '/':
            if r == 0:
                raise RuntimeError_("Împărțire la zero!")
            return l // r if (isinstance(l, int) and isinstance(r, int)) else l / r
        if op == '%':
            if r == 0:
                raise RuntimeError_("Modulo zero!")
            return l % r
        if op == '==': return l == r
        if op == '!=': return l != r
        if op == '<':  return l < r
        if op == '>':  return l > r
        if op == '<=': return l <= r
        if op == '>=': return l >= r

        raise RuntimeError_(f"Operator necunoscut: '{op}'")
