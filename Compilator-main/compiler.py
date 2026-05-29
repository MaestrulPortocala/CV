
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sys
import os
import argparse

from ml_lexer import Lexer,    LexerError
from ml_parser import Parser,   ParseError
from ml_semantic import SemanticAnalyzer, SemanticError
from ml_ir import IRGenerator, Optimizer, tac_to_str
from ml_codegen import CodeGenerator
from ml_interpreter import Interpreter



def compile_source(source: str, options: dict):
    print("[ 1/6 ] Analiza lexicala...", end="")
    try:
        lexer  = Lexer(source)
        tokens = lexer.tokenize()
        print(f" OK ({len(tokens)-1} tokeni)")
    except LexerError as e:
        print(f"\n{e}")
        return False

    if options.get('tokens'):
        print("\n─── TOKENI ───────────────────────────────────")
        for tok in tokens[:-1]:  
            print(f"  {tok}")
        print()

    print("[ 2/6 ] Analiza sintactica...", end="")
    try:
        parser = Parser(tokens)
        ast    = parser.parse()
        print(f" OK ({len(ast.statements)} instructiuni)")
    except ParseError as e:
        print(f"\n{e}")
        return False

    if options.get('ast'):
        print("\n─── AST ──────────────────────────────────────")
        _print_ast(ast)
        print()

    print("[ 3/6 ] Analiza semantica...", end="")
    try:
        sa = SemanticAnalyzer()
        sa.analyze(ast)
        print(f" OK ({len(sa.env)} variabile)")
    except SemanticError as e:
        print(f"\n{e}")
        return False

    print("[ 4/6 ] Generare cod intermediar (TAC)...", end="")
    ir_gen = IRGenerator()
    tac    = ir_gen.generate(ast)
    print(f" OK ({len(tac)} instructiuni TAC)")

    print("[ 5/6 ] Optimizare...", end="")
    opt     = Optimizer()
    tac_opt = opt.optimize(tac)
    removed = len(tac) - len(tac_opt)
    print(f" OK ({removed} instructiuni eliminate)")

    if options.get('ir'):
        print("\n─── COD INTERMEDIAR (TAC) — dupa optimizare ──")
        print(tac_to_str(tac_opt))
        print()

    print("[ 6/6 ] Generare Assembly (x86-64)...", end="")
    cg  = CodeGenerator()
    asm = cg.generate(tac_opt)
    print(" OK")

    if options.get('asm'):
        print("\n─── ASSEMBLY (NASM x86-64) ───────────────────")
        print(asm)
        print()

    base     = options.get('output', 'out')
    asm_path = base + ".asm"
    with open(asm_path, 'w') as f:
        f.write(asm)
    print(f"\n✔ Assembly scris in: {asm_path}")
    print(f"  (compilare cu NASM: nasm -f elf64 {asm_path} -o out.o && gcc out.o -o {base} -no-pie)")
    return True

def run_source(source: str):
    try:
        tokens = Lexer(source).tokenize()
        ast    = Parser(tokens).parse()
        sa     = SemanticAnalyzer()
        sa.analyze(ast)
        interp = Interpreter()
        interp.run(ast)
    except (LexerError, ParseError, SemanticError) as e:
        print(e)

def _print_ast(node, indent=0):
    prefix = "  " * indent
    name   = type(node).__name__

    from ml_ast import (Program, AssignStmt, PrintStmt, IfStmt, WhileStmt,
                           BinOp, UnaryOp, VarExpr, IntLiteral, FloatLiteral, BoolLiteral)

    if isinstance(node, Program):
        print(f"{prefix}Program")
        for s in node.statements:
            _print_ast(s, indent + 1)

    elif isinstance(node, AssignStmt):
        print(f"{prefix}Assign: {node.name}")
        _print_ast(node.value, indent + 1)

    elif isinstance(node, PrintStmt):
        print(f"{prefix}Print")
        _print_ast(node.expr, indent + 1)

    elif isinstance(node, IfStmt):
        print(f"{prefix}If")
        print(f"{prefix}  Condition:")
        _print_ast(node.condition, indent + 2)
        print(f"{prefix}  Then:")
        for s in node.then_body:
            _print_ast(s, indent + 2)

    elif isinstance(node, WhileStmt):
        print(f"{prefix}While")
        print(f"{prefix}  Condition:")
        _print_ast(node.condition, indent + 2)
        print(f"{prefix}  Body:")
        for s in node.body:
            _print_ast(s, indent + 2)

    elif isinstance(node, BinOp):
        print(f"{prefix}BinOp: {node.op!r}")
        _print_ast(node.left,  indent + 1)
        _print_ast(node.right, indent + 1)

    elif isinstance(node, UnaryOp):
        print(f"{prefix}UnaryOp: {node.op!r}")
        _print_ast(node.operand, indent + 1)

    elif isinstance(node, VarExpr):
        print(f"{prefix}Var: {node.name}")

    elif isinstance(node, IntLiteral):
        print(f"{prefix}Int: {node.value}")

    elif isinstance(node, FloatLiteral):
        print(f"{prefix}Float: {node.value}")

    elif isinstance(node, BoolLiteral):
        print(f"{prefix}Bool: {node.value}")

    else:
        print(f"{prefix}{name}")

def main():
    ap = argparse.ArgumentParser(
        description="Compilator MiniLang",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Exemple:
  python compiler.py prog.ml              # compilare + generare .asm
  python compiler.py prog.ml --run        # interpretare directa
  python compiler.py prog.ml --tokens     # afiseaza tokenii
  python compiler.py prog.ml --ast        # afiseaza AST-ul
  python compiler.py prog.ml --ir         # afiseaza IR-ul (TAC)
  python compiler.py prog.ml --asm        # afiseaza Assembly-ul
  python compiler.py prog.ml -o myapp     # scrie myapp.asm
"""
    )
    ap.add_argument("file",      help="Fisierul sursa .ml")
    ap.add_argument("--run",     action="store_true", help="Interpreteaza direct (fara NASM)")
    ap.add_argument("--tokens",  action="store_true", help="Afiseaza tokenii")
    ap.add_argument("--ast",     action="store_true", help="Afiseaza AST-ul")
    ap.add_argument("--ir",      action="store_true", help="Afiseaza codul intermediar (TAC)")
    ap.add_argument("--asm",     action="store_true", help="Afiseaza Assembly-ul generat")
    ap.add_argument("-o", "--output", default="out", help="Prefixul fisierului de iesire (default: out)")
    args = ap.parse_args()

    if not os.path.exists(args.file):
        print(f"Eroare: fisierul '{args.file}' nu exista.")
        sys.exit(1)

    with open(args.file, 'r', encoding='utf-8') as f:
        source = f.read()

    print(f"Compilator MiniLang")
    print(f"Fisier: {args.file:<36}")
    print(f"\n")

    if args.run:
        print("──Rezultate─────────────────")
        run_source(source)
        return

    options = {
        'tokens': args.tokens,
        'ast':    args.ast,
        'ir':     args.ir,
        'asm':    args.asm,
        'output': args.output,
    }
    success = compile_source(source, options)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
