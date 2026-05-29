
import sys
import os
import io
from contextlib import redirect_stdout


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from ml_lexer import Lexer, LexerError
from ml_parser import Parser, ParseError
from ml_semantic import SemanticAnalyzer, SemanticError
from ml_interpreter import Interpreter, RuntimeError_
from ml_ir import IRGenerator, Optimizer, tac_to_str


TESTS = [
    (
        "Aritmetica de baza",
        "x = 10;\ny = x * 2 + 5;\nprint(y);",
        ["25"],
        False
    ),
    (
        "If cu conditie adevarata",
        "x = 10;\ny = x * 2 + 5;\nif (y > 20) {\n    print(y);\n}",
        ["25"],
        False
    ),
    (
        "If cu conditie falsa",
        "x = 5;\nif (x > 10) {\n    print(x);\n}",
        [],
        False
    ),
    (
        "If-else (ramura then)",
        "x = 15;\nif (x > 10) {\n    print(1);\n} else {\n    print(0);\n}",
        ["1"],
        False
    ),
    (
        "If-else (ramura else)",
        "x = 3;\nif (x > 10) {\n    print(1);\n} else {\n    print(0);\n}",
        ["0"],
        False
    ),
    (
        "Bucla while",
        "i = 0;\nwhile (i < 3) {\n    print(i);\n    i = i + 1;\n}",
        ["0", "1", "2"],
        False
    ),
    (
        "Constant folding (2+3=5)",
        "a = 2 + 3;\nprint(a);",
        ["5"],
        False
    ),
    (
        "Operator modulo",
        "a = 10 % 3;\nprint(a);",
        ["1"],
        False
    ),
    (
        "Valori booleene",
        "a = 5;\nb = a > 3;\nif (b) {\n    print(a);\n}",
        ["5"],
        False
    ),
    (
        "Negare unara",
        "a = 5;\nb = -a;\nprint(b);",
        ["-5"],
        False
    ),
    (
        "Declaratie cu tip explicit int",
        "int x = 10;\nprint(x);",
        ["10"],
        False
    ),
    (
        "Declaratie cu tip explicit float",
        "float x = 3.14;\nprint(x);",
        ["3.14"],
        False
    ),
    (
        "Declaratie cu tip explicit bool",
        "bool flag = true;\nif (flag) { print(1); }",
        ["1"],
        False
    ),
    (
        "Eroare: tip incompatibil in declaratie",
        "int x = true;",
        [],
        True
    ),
    (
        "Eroare semantica: variabila nedeclarata",
        "print(x);",
        [],
        True
    ),
    (
        "Eroare semantica: impartire la zero",
        "a = 10 / 0;\nprint(a);",
        [],
        True
    ),
    (
        "Eroare semantica: tip incompatibil in operatie",
        "a = 5 + true;",
        [],
        True
    ),
    (
        "Operatori logici &&",
        "a = 5;\nb = 3;\nif (a > 3 && b < 10) {\n    print(a);\n}",
        ["5"],
        False
    ),
    (
        "Operatori logici ||",
        "a = 1;\nif (a > 10 || a < 5) {\n    print(a);\n}",
        ["1"],
        False
    ),
    (
        "Operator NOT !",
        "a = false;\nif (!a) { print(1); }",
        ["1"],
        False
    ),
    (
        "While cu else nested",
        "i = 0;\nwhile (i < 3) {\n    if (i == 1) {\n        print(99);\n    } else {\n        print(i);\n    }\n    i = i + 1;\n}",
        ["0", "99", "2"],
        False
    ),
    (
        "Nested while",
        "i = 0;\nwhile (i < 2) {\n    j = 0;\n    while (j < 2) {\n        print(j);\n        j = j + 1;\n    }\n    i = i + 1;\n}",
        ["0", "1", "0", "1"],
        False
    ),
    (
        "Expresii cu paranteze",
        "a = (2 + 3) * 4;\nprint(a);",
        ["20"],
        False
    ),
    (
        "Reatribuire variabila",
        "x = 5;\nx = x + 1;\nprint(x);",
        ["6"],
        False
    ),
]


GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def run_test(desc: str, source: str, expected: list, should_fail: bool) -> bool:
    try:
        tokens = Lexer(source).tokenize()
        ast    = Parser(tokens).parse()
        sa     = SemanticAnalyzer()
        sa.analyze(ast)

        if should_fail:
            print(f"  {RED}✗ FAIL{RESET} — {desc}")
            print(f"    Așteptat eroare, dar a trecut analiza semantica")
            return False

    
        buf = io.StringIO()
        with redirect_stdout(buf):
            Interpreter().run(ast)
        output = [line for line in buf.getvalue().splitlines() if line.strip()]

        if output == expected:
            print(f"  {GREEN}✓ PASS{RESET} — {desc}")
            return True
        else:
            print(f"  {RED}✗ FAIL{RESET} — {desc}")
            print(f"    Așteptat: {expected}")
            print(f"    Obtinut:  {output}")
            return False

    except (LexerError, ParseError, SemanticError, Exception) as e:
        if should_fail:
            print(f"  {GREEN}✓ PASS{RESET} — {desc} {YELLOW}(eroare așteptată: {type(e).__name__}){RESET}")
            return True
        else:
            print(f"  {RED}✗ FAIL{RESET} — {desc}")
            print(f"    Eroare neasteptata: {e}")
            return False


def run_optimization_tests():
    """Testează că optimizatorul funcționează corect."""
    print(f"\n{BOLD}─── Teste Optimizator ────────────────────────────{RESET}")

    source = "a = 2 + 3;\nb = a * 4;"
    tokens = Lexer(source).tokenize()
    ast    = Parser(tokens).parse()
    SemanticAnalyzer().analyze(ast)
    ir     = IRGenerator().generate(ast)
    opt_ir = Optimizer().optimize(ir)
    tac_str = tac_to_str(opt_ir)

   
    if "5" in tac_str and "2 + 3" not in tac_str:
        print(f"  {GREEN}✓ PASS{RESET} — Constant folding (2 + 3 → 5)")
    else:
        print(f"  {RED}✗ FAIL{RESET} — Constant folding")
        print(f"    TAC generat:\n{tac_str}")


def main():
    print(f"\n{BOLD}╔══ Suite de Teste MiniLang ═══════════════════╗{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════╝{RESET}\n")
    print(f"{BOLD}─── Teste Interpreter ────────────────────────────{RESET}")

    passed = 0
    total  = len(TESTS)
    for desc, src, exp, fail in TESTS:
        if run_test(desc, src, exp, fail):
            passed += 1

    run_optimization_tests()

    print(f"\n{BOLD}─── Rezultate ────────────────────────────────────{RESET}")
    color = GREEN if passed == total else RED
    print(f"  {color}{passed}/{total} teste trecute{RESET}\n")
    return passed == total


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
