#!/usr/bin/env python3
"""
MFL (Mini Functional Language) Parser and Type Checker

This script provides a command-line interface for parsing, type checking,
and compiling functional programming expressions into Core Erlang.

Example Usage:
    python3 mfl.py "let id = λx.x in (id 42)"
    python3 mfl.py -v "let id = λx.x in (id 42)"  # verbose mode
"""

import argparse
import subprocess
import shlex  # For safe shell command construction
from mfl_parser import FunctionalParser
from mfl_type_checker import infer_j
from mfl_core_erlang_generator import generate_core_erlang

def main():
    """
    Main function that handles command-line input and runs the parser.
    """
    # Set up argument parser
    arg_parser = argparse.ArgumentParser(description='Parse and type-check functional programming expressions.')
    arg_parser.add_argument('expression', nargs='?', help='Expression to parse and type-check')
    arg_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    arg_parser.add_argument('-o', '--output', default="mfl.core", help='Output file name')
    arg_parser.add_argument('-s', '--secd', action='store_true', help='Execute using SECD machine instead of generating Core Erlang')
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

                if args.secd:
                    try:
                        # Execute using SECD machine
                        from mfl_secd import execute_ast
                        result = execute_ast(ast, args.verbose)
                        print(f"SECD machine result: {result}")
                    except Exception as e:
                        print(f"Error executing with SECD machine: {e}")
                else:
                    try:
                        # Generate Core Erlang code
                        core_erlang = generate_core_erlang(ast, expr_type)
                        if args.verbose:
                            print("\nGenerated Core Erlang code:")
                            print(core_erlang)
                        # Write the generated code to file
                        with open(args.output, "w") as f:
                            f.write(core_erlang)
                        print(f"Output written to: {args.output} ,compiling to BEAM as: erlc +from_core {args.output}")
                        try:
                            # Use shlex.quote to safely handle filenames with spaces or special characters
                            command = shlex.split(f"erlc +from_core {shlex.quote(args.output)}")
                            result = subprocess.run(command, capture_output=True, text=True, check=True)
                            print("Compilation successful!")
                            print(result.stdout)  # Print compilation output (if any)
                        except subprocess.CalledProcessError as e:
                            print(f"Error compiling with erlc: {e}")
                            print(f"Return code: {e.returncode}")
                            print(f"Stdout: {e.stdout}")
                            print(f"Stderr: {e.stderr}")
                        except FileNotFoundError:
                            print("Error: erlc command not found. Make sure it's in your PATH.")
                    except Exception as e:
                        print(f"Error during code generation: {str(e)}")

            except Exception as e:
                print(f"Error during type checking: {str(e)}")

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
            "let double = λx.(x*2) in (double 21)",
            "(!True)",
            "(!False)",
            "(True & True)",
            "(False | False)",
            "(True | True)",
            "(False & False)",
            "let x = True in (x & False)",
            "let y = False in (!y)"
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
