#! /usr/bin/env python3

from tatsu.ast import AST
from pygame.event import Event
from pygame import QUIT
from pygame import KEYDOWN
from pygame import KEYUP
class HALLang:
    def terminate (self, ast): return Event (QUIT)
	
	
    def number (self, ast): return int (ast)
    def term (self, ast):
        if not isinstance(ast, AST): return ast
        elif ast.op == '*':
            return ast.left * ast.right
        elif ast.op == '/':
            return ast.left / ast.right
        else:
            raise Exception('Unknown operator', ast.op)

    def expression (self, ast):
        if not isinstance(ast, AST): return ast
        elif ast.op == '+':
            return ast.left + ast.right
        elif ast.op == '-':
            return ast.left - ast.right
        else:
            raise Exception('Unknown operator', ast.op)	
					
if __name__ == "__main__":
	# TODO
	quit ()
	
