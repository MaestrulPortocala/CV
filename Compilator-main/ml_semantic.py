

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_ast import *
from typing import Dict, Optional


class SemanticError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"[Eroare Semantica] {msg}")
INT   = 'int'
FLOAT = 'float'
BOOL  = 'bool'


def _numeric(t: str) -> bool:
    return t in (INT, FLOAT)


class SemanticAnalyzer:
    def __init__(self):
        self.env: Dict[str, str] = {}

    def analyze(self, program: Program):
        for stmt in program.statements:
            self._stmt(stmt)

    def _stmt(self, node: Stmt):
        if isinstance(node, AssignStmt):
            val_type = self._expr(node.value)
            existing = self.env.get(node.name)
            if existing and existing != val_type:
                raise SemanticError(
                    f"Variabila '{node.name}' are tipul '{existing}' "
                    f"dar se atribuie '{val_type}'"
                )
            self.env[node.name] = val_type

        elif isinstance(node, VarDeclStmt):
            val_type = self._expr(node.value)
            compatible = (node.declared_type == val_type) or \
                         (node.declared_type == FLOAT and val_type == INT)
            if not compatible:
                raise SemanticError(
                    f"Declaratie '{node.declared_type} {node.name}': "
                    f"valoarea are tipul '{val_type}'"
                )
            self.env[node.name] = node.declared_type

        elif isinstance(node, PrintStmt):
            self._expr(node.expr)

        elif isinstance(node, IfStmt):
            cond_type = self._expr(node.condition)
            if cond_type != BOOL:
                raise SemanticError(
                    f"Condiția 'if' trebuie să fie bool, nu '{cond_type}'"
                )
            for s in node.then_body:
                self._stmt(s)
            if node.else_body:
                for s in node.else_body:
                    self._stmt(s)

        elif isinstance(node, WhileStmt):
            cond_type = self._expr(node.condition)
            if cond_type != BOOL:
                raise SemanticError(
                    f"Condiția 'while' trebuie să fie bool, nu '{cond_type}'"
                )
            for s in node.body:
                self._stmt(s)

        else:
            raise SemanticError(f"Instrucțiune necunoscută: {type(node).__name__}")

    def _expr(self, node: Expr) -> str:
        if isinstance(node, IntLiteral):
            return INT

        if isinstance(node, FloatLiteral):
            return FLOAT

        if isinstance(node, BoolLiteral):
            return BOOL

        if isinstance(node, VarExpr):
            if node.name not in self.env:
                raise SemanticError(f"Variabila '{node.name}' nu a fost declarată")
            return self.env[node.name]

        if isinstance(node, UnaryOp):
            t = self._expr(node.operand)
            if node.op == '!':
                if t != BOOL:
                    raise SemanticError(f"Operatorul '!' se aplică doar pe bool, nu '{t}'")
                return BOOL
            if node.op == '-':
                if not _numeric(t):
                    raise SemanticError(f"Negarea unară '-' necesită tip numeric, nu '{t}'")
                return t

        if isinstance(node, BinOp):
            return self._binop_type(node)

        raise SemanticError(f"Expresie necunoscută: {type(node).__name__}")

    def _binop_type(self, node: BinOp) -> str:
        left_t  = self._expr(node.left)
        right_t = self._expr(node.right)
        op      = node.op
        if op in ('&&', '||'):
            if left_t != BOOL or right_t != BOOL:
                raise SemanticError(
                    f"Operatorul '{op}' necesită ambii operanzi bool, "
                    f"nu '{left_t}' și '{right_t}'"
                )
            return BOOL
        if op in ('==', '!='):
            if left_t != right_t:
                raise SemanticError(
                    f"Compararea '{op}' necesită tipuri identice, "
                    f"nu '{left_t}' și '{right_t}'"
                )
            return BOOL

        if op in ('<', '>', '<=', '>='):
            if not (_numeric(left_t) and _numeric(right_t)):
                raise SemanticError(
                    f"Compararea '{op}' necesită tipuri numerice, "
                    f"nu '{left_t}' și '{right_t}'"
                )
            return BOOL
        if op in ('+', '-', '*', '/'):
            if not (_numeric(left_t) and _numeric(right_t)):
                raise SemanticError(
                    f"Operatorul '{op}' necesită tipuri numerice, "
                    f"nu '{left_t}' și '{right_t}'"
                )

            if op == '/' and isinstance(node.right, (IntLiteral, FloatLiteral)):
                if node.right.value == 0:
                    raise SemanticError("Împărțire la zero detectată!")
         
            if left_t == FLOAT or right_t == FLOAT:
                return FLOAT
            return INT

        if op == '%':
            if left_t != INT or right_t != INT:
                raise SemanticError(
                    f"Operatorul '%' necesită tipul int, nu '{left_t}' și '{right_t}'"
                )
            return INT

        raise SemanticError(f"Operator necunoscut: '{op}'")
