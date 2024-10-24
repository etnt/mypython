"""
A Shift-Reduce Parser for a simple functional programming language.

This parser implements a bottom-up parsing strategy for parsing functional programming
constructs including:
- Integer literals
- Variables
- Lambda abstractions
- Function applications
- Let bindings
- Arithmetic expressions

Grammar Rules:
    Program -> Expr
    Expr    -> INT_LITERAL
             | IDENTIFIER
             | Lambda
             | Apply
             | Let
             | ArithExpr
             | ( Expr )

    Lambda  -> λ IDENTIFIER . Expr
    Apply   -> ( Expr Expr )
    Let     -> let IDENTIFIER = Expr in Expr
    ArithExpr -> Expr + Expr
                | Expr - Expr
                | Expr * Expr
                | Expr / Expr

Example Usage:
    python3 functional_parser.py "let id = λx.x in (id 42)"
    python3 functional_parser.py -v "let id = λx.x in (id 42)"  # verbose mode
"""

import sys
import argparse
from typing import List, Dict, Any
from type_system import (
    Var, Int, Function, Apply, Let, BinOp,
    infer_j, Forall, IntType
)
from core_erlang_generator import generate_core_erlang

class FunctionalParser:
    """
    A shift-reduce parser for functional programming constructs.
    """

    def __init__(self, grammar_rules, terminal_rules, verbose=False):
        self.grammar_rules = grammar_rules
        self.terminal_rules = terminal_rules
        self.stack = []
        self.buffer = []
        self.verbose = verbose

    def debug_print(self, *args, **kwargs):
        """Helper method for conditional printing"""
        if self.verbose:
            print(*args, **kwargs)

    def tokenize(self, input_str: str) -> List[str]:
        """
        Convert input string into tokens.
        Handles special characters and whitespace.
        """
        # Replace special characters with padded spaces
        for char in "()λ.=+*/-":
            input_str = input_str.replace(char, f" {char} ")

        # Split and filter out empty tokens
        return [token for token in input_str.split() if token]

    def try_terminal_reduction(self) -> bool:
        """
        Attempt to reduce terminals (numbers, identifiers, operators).
        """
        if not self.stack:
            return False

        top = self.stack[-1]

        # Try to reduce integer literals
        # Skip if already reduced
        if isinstance(top, tuple):
            return False

        if top.isdigit():
            self.stack.pop()
            self.stack.append(("Expr", Int(int(top))))
            self.debug_print(f"Reduced integer: {top}")
            return True

        # Try to reduce identifiers, but not keywords or special chars
        if top.isalnum() and not top.isdigit() and top not in ["let", "in", "λ"]:
            self.stack.pop()
            self.stack.append(("IDENTIFIER", top))
            self.debug_print(f"Reduced identifier: {top}")
            return True

        return False

    def try_grammar_reduction(self) -> bool:
        """
        Attempt to reduce according to grammar rules.
        """
        if len(self.stack) < 2:
            return False

        # Try to reduce lambda expressions: λ x . e -> Lambda
        if len(self.stack) >= 4:
            if (self.stack[-4] == "λ" and 
                isinstance(self.stack[-3], tuple) and self.stack[-3][0] == "Expr" and
                self.stack[-2] == "." and
                isinstance(self.stack[-1], tuple) and self.stack[-1][0] == "Expr"):

                # Extract the variable from the first Expr (which should be a Var)
                _, var_expr = self.stack[-3]
                if not isinstance(var_expr, Var):
                    return False

                _, body = self.stack[-1]
                self.stack = self.stack[:-4]
                self.stack.append(("Expr", Function(var_expr, body)))
                self.debug_print(f"Reduced lambda: λ{var_expr}.{body}")
                return True

        # Try to reduce function application: ( e1 e2 ) -> Apply
        if len(self.stack) >= 4:
            if (self.stack[-4] == "(" and
                isinstance(self.stack[-3], tuple) and self.stack[-3][0] == "Expr" and
                isinstance(self.stack[-2], tuple) and self.stack[-2][0] == "Expr" and
                self.stack[-1] == ")"):

                _, func = self.stack[-3]
                _, arg = self.stack[-2]
                self.stack = self.stack[:-4]
                self.stack.append(("Expr", Apply(func, arg)))
                self.debug_print(f"Reduced application: ({func} {arg})")
                return True

        # Try to reduce let expressions: let x = e1 in e2 -> Let
        if len(self.stack) >= 6:
            if (self.stack[-6] == "let" and
                isinstance(self.stack[-5], tuple) and self.stack[-5][0] == "Expr" and
                self.stack[-4] == "=" and
                isinstance(self.stack[-3], tuple) and self.stack[-3][0] == "Expr" and
                self.stack[-2] == "in" and
                isinstance(self.stack[-1], tuple) and self.stack[-1][0] == "Expr"):

                # Extract the variable from the first Expr (which should be a Var)
                _, var_expr = self.stack[-5]
                if not isinstance(var_expr, Var):
                    return False

                _, value = self.stack[-3]
                _, body = self.stack[-1]
                self.stack = self.stack[:-6]
                self.stack.append(("Expr", Let(var_expr, value, body)))
                self.debug_print(f"Reduced let: let {var_expr} = {value} in {body}")
                return True

        # Try to reduce parenthesized expressions
        if len(self.stack) >= 3:
            if (self.stack[-3] == "(" and
                isinstance(self.stack[-2], tuple) and self.stack[-2][0] == "Expr" and
                self.stack[-1] == ")"):
                _, expr = self.stack[-2]
                self.stack = self.stack[:-3]
                self.stack.append(("Expr", expr))
                self.debug_print(f"Reduced parenthesized expression: ({expr})")
                return True

        # Try to reduce arithmetic expressions
        if len(self.stack) >= 3:
            if (isinstance(self.stack[-3], tuple) and self.stack[-3][0] == "Expr" and
                self.stack[-2] in ["+", "-", "*", "/"] and
                isinstance(self.stack[-1], tuple) and self.stack[-1][0] == "Expr"):

                _, left = self.stack[-3]
                op = self.stack[-2]
                _, right = self.stack[-1]
                self.stack = self.stack[:-3]
                self.stack.append(("Expr", BinOp(op, left, right)))
                self.debug_print(f"Reduced arithmetic: {left} {op} {right}")
                return True

        # Reduce basic expressions (integers and identifiers)
        if len(self.stack) >= 1:
            top = self.stack[-1]
            if isinstance(top, tuple):
                if top[0] == "INT_LITERAL":
                    self.stack.pop()
                    self.stack.append(("Expr", Int(top[1])))
                    self.debug_print(f"Reduced to Expr: {top[1]}")
                    return True
                elif top[0] == "IDENTIFIER":
                    self.stack.pop()
                    self.stack.append(("Expr", Var(top[1])))
                    self.debug_print(f"Reduced to Expr: {top[1]}")
                    return True
            # Handle raw integers that haven't been converted to INT_LITERAL yet
            elif isinstance(top, str) and top.isdigit():
                self.stack.pop()
                self.stack.append(("Expr", Int(int(top))))
                self.debug_print(f"Reduced integer directly to Expr: {top}")
                return True

        return False

    def parse(self, input_str: str) -> Any:
        """
        Parse an input string and return the AST.
        """
        self.buffer = self.tokenize(input_str)
        self.stack = []
        self.debug_print(f"\nParsing: {input_str}")

        while True:
            self.debug_print(f"\nStack: {self.stack}")
            self.debug_print(f"Buffer: {self.buffer}")

            # Try reductions
            while self.try_terminal_reduction() or self.try_grammar_reduction():
                pass

            # If we can't reduce and have items in buffer, shift
            if self.buffer:
                next_token = self.buffer.pop(0)
                self.stack.append(next_token)
                self.debug_print(f"Shifted: {next_token}")
            else:
                # No more input and no reductions possible
                if len(self.stack) == 1 and isinstance(self.stack[0], tuple) and self.stack[0][0] == "Expr":
                    print("\nSuccessfully parsed!")
                    return self.stack[0][1]
                else:
                    raise ValueError(f"Parsing failed. Final stack: {self.stack}")

def main():
    """
    Main function that handles command-line input and runs the parser.
    """
    # Set up argument parser
    arg_parser = argparse.ArgumentParser(description='Parse and type-check functional programming expressions.')
    arg_parser.add_argument('expression', nargs='?', help='Expression to parse and type-check')
    arg_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    arg_parser.add_argument('-o', '--output', default="mfl.core", help='Output file name')
    args = arg_parser.parse_args()

    parser = FunctionalParser([], {}, verbose=args.verbose)  # Grammar rules handled in reduction methods

    # If expression is provided as command-line argument, use it
    if args.expression:
        try:
            ast = parser.parse(args.expression)
            print(f"AST: {ast}")
            print(f"AST(raw): {ast.raw_structure()}")

            # Type check the parsed expression
            type_ctx = {}  # Empty typing context
            try:
                expr_type = infer_j(ast, type_ctx)
                print(f"Inferred type: {expr_type}")

                # Generate Core Erlang code
                core_erlang = generate_core_erlang(ast, expr_type)
                if args.verbose:
                    print("\nGenerated Core Erlang code:")
                    print(core_erlang)
                # Write the generated code to file
                with open(args.output, "w") as f:
                    f.write(core_erlang)
                print(f"Output written to: {args.output} ,compile to BEAM as: erlc +from_core {args.output}")
            except Exception as e:
                print(f"Error during type checking/code generation: {str(e)}")

        except ValueError as e:
            print(f"Parse error: {str(e)}")
    else:
        # Default test expressions
        test_exprs = [
            "42",
            "λx.x",
            "(λx.x 42)",
            "let id = λx.x in (id 42)",
            "(2 + 3)",
            "let x = 5 in (x * 3)",
            "let double = λx.(x*2) in (double 21)"
        ]

        print("No expression provided. Running test cases...")
        for expr_str in test_exprs:
            print("\n" + "="*50)
            try:
                ast = parser.parse(expr_str)
                print(f"AST: {ast}")
                print(f"AST(raw): {ast.raw_structure()}")

                # Type check the parsed expression
                type_ctx = {}
                try:
                    expr_type = infer_j(ast, type_ctx)
                    print(f"Inferred type: {expr_type}")
                except Exception as e:
                    print(f"Type error: {str(e)}")

            except ValueError as e:
                print(f"Parse error: {str(e)}")
            print("="*50)

if __name__ == "__main__":
    main()
