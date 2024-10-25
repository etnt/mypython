# Python Learning Experiments

This repository contains a collection of small Python programs that demonstrate various programming concepts and techniques.
Each program is self-contained and serves as a learning experiment for different aspects of Python programming.

## Programs

### 1. Shamir's Secret Sharing (shared_secrets.py)
An implementation of Shamir's Secret Sharing cryptographic algorithm for securely splitting and reconstructing secrets.

### 2. Minimax Algorithm (minimax.py)
A demonstration of the Minimax algorithm with Alpha-Beta pruning, commonly used in game AI and decision making.

### 3. Pydantic Examples (pydantic.py)
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
