

from dataclasses import dataclass, field
from typing import List, Optional, Any

class ASTNode:
    pass

class Stmt(ASTNode):
    pass
class Expr(ASTNode):
    pass
@dataclass
class IntLiteral(Expr):
    value: int

@dataclass
class FloatLiteral(Expr):
    value: float

@dataclass
class BoolLiteral(Expr):
    value: bool

@dataclass
class VarExpr(Expr):
    name: str

@dataclass
class BinOp(Expr):
    op: str       
    left: Expr
    right: Expr

@dataclass
class UnaryOp(Expr):
    op: str         
    operand: Expr

@dataclass
class AssignStmt(Stmt):
    name: str
    value: Expr

@dataclass
class VarDeclStmt(Stmt):
    declared_type: str  
    name: str
    value: Expr

@dataclass
class PrintStmt(Stmt):
    expr: Expr

@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_body: List[Stmt]
    else_body: Optional[List[Stmt]] = None

@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: List[Stmt]

@dataclass
class Program(ASTNode):
    statements: List[Stmt] = field(default_factory=list)
