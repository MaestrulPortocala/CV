
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import List, Optional
from ml_lexer import Token, TokenType
from ml_ast import *


class ParseError(Exception):
    def __init__(self, msg: str, token: Token):
        super().__init__(
            f"[Eroare Sintactica] Linia {token.line}, Coloana {token.col}: {msg} (got {token.type.name} {token.value!r})"
        )
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos    = 0
    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        if tok.type != TokenType.EOF:
            self.pos += 1
        return tok

    def _check(self, *types: TokenType) -> bool:
        return self._peek().type in types

    def _match(self, *types: TokenType) -> Optional[Token]:
        if self._check(*types):
            return self._advance()
        return None

    def _expect(self, typ: TokenType, msg: str = "") -> Token:
        if self._check(typ):
            return self._advance()
        raise ParseError(msg or f"Așteptat {typ.name}", self._peek())
    def parse(self) -> Program:
        stmts = []
        while not self._check(TokenType.EOF):
            stmts.append(self._parse_stmt())
        return Program(stmts)
    def _parse_stmt(self) -> Stmt:
        tok = self._peek()
        if tok.type == TokenType.IF:
            return self._parse_if()
        if tok.type == TokenType.WHILE:
            return self._parse_while()
        if tok.type == TokenType.PRINT:
            return self._parse_print()
        if tok.type in (TokenType.INT_TYPE, TokenType.FLOAT_TYPE, TokenType.BOOL_TYPE):
            return self._parse_typed_decl()
        if tok.type == TokenType.IDENTIFIER:
            next_tok = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_tok and next_tok.type == TokenType.ASSIGN:
                return self._parse_assign()
        raise ParseError("Instrucțiune necunoscută", tok)

    def _parse_typed_decl(self) -> 'VarDeclStmt':
        """int x = expr;  /  float x = expr;  /  bool x = expr;"""
        type_map = {
            TokenType.INT_TYPE:   'int',
            TokenType.FLOAT_TYPE: 'float',
            TokenType.BOOL_TYPE:  'bool',
        }
        declared_type = type_map[self._advance().type]
        name = self._expect(TokenType.IDENTIFIER, "Așteptat identificator după tip").value
        self._expect(TokenType.ASSIGN, "Așteptat '=' după identificator")
        val  = self._parse_expr()
        self._expect(TokenType.SEMICOLON, "Așteptat ';' după declarație")
        from ml_ast import VarDeclStmt
        return VarDeclStmt(declared_type, name, val)

    def _parse_assign(self) -> AssignStmt:
        name = self._expect(TokenType.IDENTIFIER, "Așteptat identificator").value
        self._expect(TokenType.ASSIGN, "Așteptat '='")
        val  = self._parse_expr()
        self._expect(TokenType.SEMICOLON, "Așteptat ';' după atribuire")
        return AssignStmt(name, val)

    def _parse_if(self) -> IfStmt:
        self._expect(TokenType.IF)
        self._expect(TokenType.LPAREN, "Așteptat '(' după 'if'")
        cond = self._parse_expr()
        self._expect(TokenType.RPAREN, "Așteptat ')' după condiție")
        self._expect(TokenType.LBRACE, "Așteptat '{' după condiție if")
        then_body = self._parse_block()
        self._expect(TokenType.RBRACE, "Așteptat '}' la finalul blocului if")
        else_body = None
        if self._match(TokenType.ELSE):
            self._expect(TokenType.LBRACE, "Așteptat '{' după 'else'")
            else_body = self._parse_block()
            self._expect(TokenType.RBRACE, "Așteptat '}' la finalul blocului else")
        return IfStmt(cond, then_body, else_body)

    def _parse_while(self) -> WhileStmt:
        self._expect(TokenType.WHILE)
        self._expect(TokenType.LPAREN, "Așteptat '(' după 'while'")
        cond = self._parse_expr()
        self._expect(TokenType.RPAREN, "Așteptat ')' după condiție")
        self._expect(TokenType.LBRACE, "Așteptat '{' după condiție while")
        body = self._parse_block()
        self._expect(TokenType.RBRACE, "Așteptat '}' la finalul blocului while")
        return WhileStmt(cond, body)

    def _parse_print(self) -> PrintStmt:
        self._expect(TokenType.PRINT)
        self._expect(TokenType.LPAREN, "Așteptat '(' după 'print'")
        expr = self._parse_expr()
        self._expect(TokenType.RPAREN, "Așteptat ')' după expresia print")
        self._expect(TokenType.SEMICOLON, "Așteptat ';' după print")
        return PrintStmt(expr)

    def _parse_block(self) -> List[Stmt]:
        stmts = []
        while not self._check(TokenType.RBRACE, TokenType.EOF):
            stmts.append(self._parse_stmt())
        return stmts

    def _parse_expr(self) -> Expr:
        return self._parse_or()

    def _parse_or(self) -> Expr:
        left = self._parse_and()
        while self._match(TokenType.OR):
            right = self._parse_and()
            left  = BinOp('||', left, right)
        return left

    def _parse_and(self) -> Expr:
        left = self._parse_not()
        while self._match(TokenType.AND):
            right = self._parse_not()
            left  = BinOp('&&', left, right)
        return left

    def _parse_not(self) -> Expr:
        if self._match(TokenType.NOT):
            operand = self._parse_not()
            return UnaryOp('!', operand)
        return self._parse_comparison()

    def _parse_comparison(self) -> Expr:
        left = self._parse_addition()
        CMP = {
            TokenType.EQ: '==', TokenType.NEQ: '!=',
            TokenType.LT: '<',  TokenType.GT: '>',
            TokenType.LTE: '<=', TokenType.GTE: '>=',
        }
        if self._check(*CMP.keys()):
            op_tok = self._advance()
            right  = self._parse_addition()
            left   = BinOp(CMP[op_tok.type], left, right)
        return left

    def _parse_addition(self) -> Expr:
        left = self._parse_multiplication()
        while self._check(TokenType.PLUS, TokenType.MINUS):
            op   = self._advance().value
            right = self._parse_multiplication()
            left  = BinOp(op, left, right)
        return left

    def _parse_multiplication(self) -> Expr:
        left = self._parse_unary()
        while self._check(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op    = self._advance().value
            right = self._parse_unary()
            left  = BinOp(op, left, right)
        return left

    def _parse_unary(self) -> Expr:
        if self._match(TokenType.MINUS):
            operand = self._parse_unary()
            return UnaryOp('-', operand)
        return self._parse_primary()

    def _parse_primary(self) -> Expr:
        tok = self._peek()

        if tok.type == TokenType.INT_LITERAL:
            self._advance()
            return IntLiteral(int(tok.value))

        if tok.type == TokenType.FLOAT_LITERAL:
            self._advance()
            return FloatLiteral(float(tok.value))

        if tok.type == TokenType.BOOL_LITERAL:
            self._advance()
            return BoolLiteral(tok.value == 'true')

        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return VarExpr(tok.value)

        if tok.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expr()
            self._expect(TokenType.RPAREN, "Așteptat ')' după expresie")
            return expr

        raise ParseError("Expresie așteptată", tok)
