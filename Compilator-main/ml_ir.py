
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_ast import *
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

@dataclass
class TACAssign:
    dest: str
    src: Any  

@dataclass
class TACBinOp:
    dest:  str
    op:    str
    left:  Any
    right: Any

@dataclass
class TACUnaryOp:
    dest:    str
    op:      str
    operand: Any

@dataclass
class TACLabel:
    name: str

@dataclass
class TACJump:
    label: str

@dataclass
class TACJumpIfFalse:
    condition: Any
    label:     str

@dataclass
class TACPrint:
    src: Any


TAC = Union[TACAssign, TACBinOp, TACUnaryOp, TACLabel, TACJump, TACJumpIfFalse, TACPrint]
class IRGenerator:
    def __init__(self):
        self.instructions: List[TAC] = []
        self._temp_count  = 0
        self._label_count = 0

    def _new_temp(self) -> str:
        self._temp_count += 1
        return f"_t{self._temp_count}"

    def _new_label(self) -> str:
        self._label_count += 1
        return f"_L{self._label_count}"

    def emit(self, instr: TAC):
        self.instructions.append(instr)

    def generate(self, program: Program) -> List[TAC]:
        for stmt in program.statements:
            self._gen_stmt(stmt)
        return self.instructions

    def _gen_stmt(self, node: Stmt):
        if isinstance(node, AssignStmt):
            val = self._gen_expr(node.value)
            self.emit(TACAssign(node.name, val))

        elif isinstance(node, VarDeclStmt):
            val = self._gen_expr(node.value)
            self.emit(TACAssign(node.name, val))

        elif isinstance(node, PrintStmt):
            val = self._gen_expr(node.expr)
            self.emit(TACPrint(val))

        elif isinstance(node, IfStmt):
            cond      = self._gen_expr(node.condition)
            end_label = self._new_label()
            self.emit(TACJumpIfFalse(cond, end_label))
            for s in node.then_body:
                self._gen_stmt(s)
            self.emit(TACLabel(end_label))

        elif isinstance(node, WhileStmt):
            start_label = self._new_label()
            end_label   = self._new_label()
            self.emit(TACLabel(start_label))
            cond = self._gen_expr(node.condition)
            self.emit(TACJumpIfFalse(cond, end_label))
            for s in node.body:
                self._gen_stmt(s)
            self.emit(TACJump(start_label))
            self.emit(TACLabel(end_label))

    def _gen_expr(self, node: Expr) -> Any:
        if isinstance(node, IntLiteral):
            return node.value
        if isinstance(node, FloatLiteral):
            return node.value
        if isinstance(node, BoolLiteral):
            return node.value
        if isinstance(node, VarExpr):
            return node.name

        if isinstance(node, UnaryOp):
            operand = self._gen_expr(node.operand)
            dest    = self._new_temp()
            self.emit(TACUnaryOp(dest, node.op, operand))
            return dest

        if isinstance(node, BinOp):
            left  = self._gen_expr(node.left)
            right = self._gen_expr(node.right)
            dest  = self._new_temp()
            self.emit(TACBinOp(dest, node.op, left, right))
            return dest

        raise ValueError(f"Expresie necunoscută în IR: {type(node).__name__}")

def _is_const(v) -> bool:
    return isinstance(v, (int, float, bool))


def _fold_binop(op: str, l, r):
    """Constant folding pentru valori constante cunoscute."""
    if not (_is_const(l) and _is_const(r)):
        return None
    try:
        if op == '+':  return l + r
        if op == '-':  return l - r
        if op == '*':  return l * r
        if op == '/':
            if r == 0: return None 
            return l / r if isinstance(l, float) or isinstance(r, float) else l // r
        if op == '%':  return l % r
        if op == '==': return l == r
        if op == '!=': return l != r
        if op == '<':  return l < r
        if op == '>':  return l > r
        if op == '<=': return l <= r
        if op == '>=': return l >= r
        if op == '&&': return bool(l) and bool(r)
        if op == '||': return bool(l) or bool(r)
    except Exception:
        return None
    return None


def _fold_unary(op: str, v):
    if not _is_const(v):
        return None
    if op == '-':  return -v
    if op == '!':  return not v
    return None


class Optimizer:

    def optimize(self, instructions: List[TAC]) -> List[TAC]:
        instructions = self._constant_folding(instructions)
        instructions = self._copy_propagation(instructions)
        instructions = self._dead_code_elimination(instructions)
        return instructions

    def _constant_folding(self, instrs: List[TAC]) -> List[TAC]:
        result = []
        for instr in instrs:
            if isinstance(instr, TACBinOp):
                folded = _fold_binop(instr.op, instr.left, instr.right)
                if folded is not None:
                    result.append(TACAssign(instr.dest, folded))
                    continue
            elif isinstance(instr, TACUnaryOp):
                folded = _fold_unary(instr.op, instr.operand)
                if folded is not None:
                    result.append(TACAssign(instr.dest, folded))
                    continue
            result.append(instr)
        return result

    def _copy_propagation(self, instrs: List[TAC]) -> List[TAC]:
        const_map: Dict[str, Any] = {}

        def resolve(v):
            if isinstance(v, str) and v in const_map:
                return const_map[v]
            return v

        result = []
        for instr in instrs:
            if isinstance(instr, TACAssign):
                src = resolve(instr.src)
                if _is_const(src) and instr.dest.startswith('_t'):
                    const_map[instr.dest] = src
                else:
                    const_map.pop(instr.dest, None)
                result.append(TACAssign(instr.dest, src))

            elif isinstance(instr, TACBinOp):
                left  = resolve(instr.left)
                right = resolve(instr.right)
                result.append(TACBinOp(instr.dest, instr.op, left, right))

            elif isinstance(instr, TACUnaryOp):
                operand = resolve(instr.operand)
                result.append(TACUnaryOp(instr.dest, instr.op, operand))

            elif isinstance(instr, TACJumpIfFalse):
                result.append(TACJumpIfFalse(resolve(instr.condition), instr.label))

            elif isinstance(instr, TACPrint):
                result.append(TACPrint(resolve(instr.src)))

            else:
                result.append(instr)

        return result

    def _dead_code_elimination(self, instrs: List[TAC]) -> List[TAC]:
    
        def _uses(instr) -> List[str]:
          
            vals = []
            if isinstance(instr, TACAssign):
                if isinstance(instr.src, str): vals.append(instr.src)
            elif isinstance(instr, TACBinOp):
                if isinstance(instr.left,  str): vals.append(instr.left)
                if isinstance(instr.right, str): vals.append(instr.right)
            elif isinstance(instr, TACUnaryOp):
                if isinstance(instr.operand, str): vals.append(instr.operand)
            elif isinstance(instr, TACJumpIfFalse):
                if isinstance(instr.condition, str): vals.append(instr.condition)
            elif isinstance(instr, TACPrint):
                if isinstance(instr.src, str): vals.append(instr.src)
            return vals

        def _defines(instr) -> Optional[str]:
            if isinstance(instr, (TACAssign, TACBinOp, TACUnaryOp)):
                return instr.dest
            return None

        used = set()
        for instr in instrs:
            for v in _uses(instr):
                used.add(v)

        result = []
        for instr in instrs:
            dest = _defines(instr)
         
            if dest and dest.startswith('_t') and dest not in used:
                continue
            result.append(instr)

        return result


def tac_to_str(instructions: List[TAC]) -> str:
    lines = []
    for instr in instructions:
        if isinstance(instr, TACLabel):
            lines.append(f"{instr.name}:")
        elif isinstance(instr, TACAssign):
            lines.append(f"    {instr.dest} = {instr.src}")
        elif isinstance(instr, TACBinOp):
            lines.append(f"    {instr.dest} = {instr.left} {instr.op} {instr.right}")
        elif isinstance(instr, TACUnaryOp):
            lines.append(f"    {instr.dest} = {instr.op}{instr.operand}")
        elif isinstance(instr, TACJump):
            lines.append(f"    goto {instr.label}")
        elif isinstance(instr, TACJumpIfFalse):
            lines.append(f"    if not {instr.condition} goto {instr.label}")
        elif isinstance(instr, TACPrint):
            lines.append(f"    print {instr.src}")
    return "\n".join(lines)
