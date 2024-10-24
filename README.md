# Python Learning Experiments

This repository contains a collection of small Python programs that demonstrate various programming concepts and techniques.
Each program is self-contained and serves as a learning experiment for different aspects of Python programming.

## Programs

### 1. Shamir's Secret Sharing (shared_secrets.py)
An implementation of Shamir's Secret Sharing cryptographic algorithm for securely splitting and reconstructing secrets.

### 2. Minimax Algorithm (minimax.py)
A demonstration of the Minimax algorithm with Alpha-Beta pruning, commonly used in game AI and decision making.

### 3. Pydantic Examples (xpydantic.py)
Examples showing how to use Pydantic for data validation and settings management.

### 4. Dynamic Attributes (dynattr.py)
Exploration of Python's dynamic attribute handling using __getattr__ and __dict__.

### 5. Shift-Reduce Parser (shift_reduce_parser.py)
Implementation of a shift-reduce parser for processing simple English sentences.

### 6. Python Decorators (decorators.py)
Various examples of Python decorators including timing, logging, and function repetition.

### 7. FastAPI Server (api_server.py)
A simple REST API server implementation using FastAPI framework.

### 8. Python Dataclasses (using_dataclasses.py)
A comprehensive guide to Python's dataclasses, demonstrating how to use the @dataclasses.dataclass decorator for simplified class creation with automatic method generation, customization options, and best practices.

### 9. MFL - Type Inference System (mfl_type_checker.py)
An educational implementation of the Hindley-Milner type inference system, demonstrating how programming language type systems work. Includes polymorphic type inference, unification, and type checking with detailed documentation explaining core concepts.

### 10. MFL - Parser (mfl_parser.py)
A shift-reduce parser for a simple functional programming language that supports lambda abstractions, function applications, let bindings, and arithmetic expressions. Integrates with the type inference system to provide static typing for parsed expressions.

### 11. MFL - SECD Machine (mfl_secd.py)
An implementation of the SECD (Stack, Environment, Control, Dump) virtual machine for evaluating lambda calculus expressions.
The SECD machine serves as one of the execution backends for the MFL language, allowing direct interpretation of MFL expressions without compilation via Erlang Core.

### 12. MFL - Core Erlang Generator (mfl_core_erlang_generator.py)
A code generator that translates parsed and type-checked expressions into Erlang Core language code. Supports lambda abstractions, function applications, let bindings, and arithmetic expressions.

## Requirements

The programs may require various Python packages. Install them using:

```bash
make
```

Then setup the virtual environment:

```bash
source ./venv/bin/activate
```

## Usage

Each program can be run independently. Most programs include example usage in their source code or can be run directly:

```bash
python3 <program_name>.py
```

The `mfl.py` can be run with an argument or without, where in the latter case it will run the default test cases for the parser and type checker.
It also takes a `-v`/`--verbose` flag to print the parsing steps.

Example, generating BEAM code:

```bash
❯ ./venv/bin/python3 mfl.py "let double = λx.(x*2) in (double 21)"
Successfully parsed!
AST: let double = λx.(x * 2) in (double 21)
AST(raw): Let(Var("double"), Function(Var("x"), BinOp("*", Var("x"), Int(2))), Apply(Var("double"), Int(21)))
Inferred type: int
Output written to: mfl.core ,compiling to BEAM as: erlc +from_core mfl.core
Compilation successful!

❯ erl
1> mfl:main().
42
```

Another example, this time running our code in the SECD machine:

```bash
❯ ./venv/bin/python3 mfl.py -s "let add = λx.λy.(x+y) in (add 3 4)"
Successfully parsed!
AST: let add = λx.λy.(x + y) in ((add 3) 4)
AST(raw): Let(Var("add"), Function(Var("x"), Function(Var("y"), BinOp("+", Var("x"), Var("y")))), Apply(Apply(Var("add"), Int(3)), Int(4)))
Inferred type: int
SECD instructions: [('LDF', [('LDF', [('LD', (1, 0)), ('LD', (0, 0)), 'ADD', 'RET']), 'RET']), ('LET', 0), 'NIL', ('LDC', 4), 'CONS', 'NIL', ('LDC', 3), 'CONS', ('LD', (0, 0)), 'AP', 'AP']
SECD machine result: 7
```

Testing the type checker:

```bash
❯ ./venv/bin/python3 mfl.py -s "let add = λx.λy.(x+y) in (add 3 4)"
Successfully parsed!
AST: let add = λx.λy.(x + y) in ((add 3) True)
AST(raw): Let(Var("add"), Function(Var("x"), Function(Var("y"), BinOp("+", Var("x"), Var("y")))), Apply(Apply(Var("add"), Int(3)), Bool(True))) 
Error during type checking: Type mismatch: int and bool
 ```