import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_ir import *
from typing import List, Dict, Set


class CodeGenerator:

    def __init__(self):
        self.output:    List[str]      = []
        self.var_map:   Dict[str, int] = {}  
        self.stack_off: int            = 0
        self._float_consts: Dict[str, str] = {}  
        self._fc_count: int = 0

   

    def _emit(self, line: str = ""):
        self.output.append(line)

    def _emiti(self, line: str):    
        self.output.append(f"    {line}")

    def _var_offset(self, name: str) -> int:
        if name not in self.var_map:
            self.stack_off += 8
            self.var_map[name] = self.stack_off
        return self.var_map[name]

    def _var_addr(self, name: str) -> str:
        off = self._var_offset(name)
        return f"[rbp - {off}]"

    def _load(self, val, reg="rax"):
        if isinstance(val, bool):
            self._emiti(f"mov {reg}, {1 if val else 0}")
        elif isinstance(val, int):
            self._emiti(f"mov {reg}, {val}")
        elif isinstance(val, float):
            label = self._float_label(val)
            self._emiti(f"movsd xmm0, [{label}]")
        elif isinstance(val, str):
            # variabilă / temporar
            addr = self._var_addr(val)
            self._emiti(f"mov {reg}, {addr}")

    def _float_label(self, v: float) -> str:
        key = str(v)
        if key not in self._float_consts:
            self._fc_count += 1
            label = f"__fc{self._fc_count}"
            self._float_consts[key] = label
        return self._float_consts[key]

    def generate(self, instructions: List[TAC]) -> str:
        all_vars: Set[str] = set()
        for instr in instructions:
            for attr in ('dest', 'src', 'left', 'right', 'operand', 'src', 'condition'):
                v = getattr(instr, attr, None)
                if isinstance(v, str):
                    all_vars.add(v)
        for v in all_vars:
            self._var_offset(v)

        stack_size = (self.stack_off + 15) & ~15  

        self._emit("section .data")
        self._emit('    fmt_int   db "%lld", 10, 0')
        self._emit('    fmt_float db "%g", 10, 0')
        self._emit('    fmt_bool_t db "true", 10, 0')
        self._emit('    fmt_bool_f db "false", 10, 0')
        self._emit("")
        self._emit("section .text")
        self._emit("    global main")
        self._emit("    extern printf")
        self._emit("")
        self._emit("main:")
        self._emiti("push rbp")
        self._emiti("mov rbp, rsp")
        self._emiti(f"sub rsp, {stack_size}")
        self._emit("")

        for instr in instructions:
            self._gen_instr(instr)   
        self._emit("")
        self._emiti("mov rax, 0")
        self._emiti("leave")
        self._emiti("ret")
        if self._float_consts:
            self._emit("")
            self._emit("section .data")
            for val_str, label in self._float_consts.items():
                self._emit(f"    {label} dq {val_str}")

        return "\n".join(self.output)

    def _gen_instr(self, instr: TAC):
        if isinstance(instr, TACLabel):
            self._emit(f"{instr.name}:")

        elif isinstance(instr, TACAssign):
            self._emit(f"    ; {instr.dest} = {instr.src}")
            if isinstance(instr.src, float):
                label = self._float_label(instr.src)
                self._emiti(f"movsd xmm0, [{label}]")
                self._emiti(f"movsd {self._var_addr(instr.dest)}, xmm0")
            else:
                self._load(instr.src, "rax")
                self._emiti(f"mov {self._var_addr(instr.dest)}, rax")

        elif isinstance(instr, TACBinOp):
            self._emit(f"    ; {instr.dest} = {instr.left} {instr.op} {instr.right}")
            self._gen_binop(instr)

        elif isinstance(instr, TACUnaryOp):
            self._emit(f"    ; {instr.dest} = {instr.op}{instr.operand}")
            self._load(instr.operand, "rax")
            if instr.op == '-':
                self._emiti("neg rax")
            elif instr.op == '!':
                self._emiti("cmp rax, 0")
                self._emiti("sete al")
                self._emiti("movzx rax, al")
            self._emiti(f"mov {self._var_addr(instr.dest)}, rax")

        elif isinstance(instr, TACJump):
            self._emiti(f"jmp {instr.label}")

        elif isinstance(instr, TACJumpIfFalse):
            self._load(instr.condition, "rax")
            self._emiti("cmp rax, 0")
            self._emiti(f"je {instr.label}")

        elif isinstance(instr, TACPrint):
            self._gen_print(instr)

    def _gen_binop(self, instr: TACBinOp):
        op = instr.op
        self._load(instr.left,  "rax")
        self._load(instr.right, "rbx")

        if op == '+':
            self._emiti("add rax, rbx")
        elif op == '-':
            self._emiti("sub rax, rbx")
        elif op == '*':
            self._emiti("imul rax, rbx")
        elif op == '/':
            self._emiti("cqo")
            self._emiti("idiv rbx")
        elif op == '%':
            self._emiti("cqo")
            self._emiti("idiv rbx")
            self._emiti("mov rax, rdx")
        elif op in ('==', '!=', '<', '>', '<=', '>='):
            self._emiti("cmp rax, rbx")
            cc = {'==': 'sete', '!=': 'setne', '<': 'setl',
                  '>': 'setg', '<=': 'setle', '>=': 'setge'}[op]
            self._emiti(f"{cc} al")
            self._emiti("movzx rax, al")
        elif op == '&&':
            self._emiti("and rax, rbx")
        elif op == '||':
            self._emiti("or rax, rbx")

        self._emiti(f"mov {self._var_addr(instr.dest)}, rax")

    def _gen_print(self, instr: TACPrint):
        src = instr.src
        self._emit("    ; print")
        if isinstance(src, float):
            label = self._float_label(src)
            self._emiti(f"movsd xmm0, [{label}]")
            self._emiti("lea rdi, [rel fmt_float]")
            self._emiti("mov rax, 1")     # 1 xmm arg
            self._emiti("call printf")
        elif isinstance(src, bool):
            lbl = "fmt_bool_t" if src else "fmt_bool_f"
            self._emiti(f"lea rdi, [rel {lbl}]")
            self._emiti("mov rax, 0")
            self._emiti("call printf")
        elif isinstance(src, int):
            self._emiti(f"mov rsi, {src}")
            self._emiti("lea rdi, [rel fmt_int]")
            self._emiti("mov rax, 0")
            self._emiti("call printf")
        else:
            self._load(src, "rsi")
            self._emiti("lea rdi, [rel fmt_int]")
            self._emiti("mov rax, 0")
            self._emiti("call printf")
