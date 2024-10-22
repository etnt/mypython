"""
A Shift-Reduce Parser implementation for parsing simple English sentences.

This parser implements a bottom-up parsing strategy that recognizes the right-hand side
of grammar productions and reduces them to their corresponding left-hand side symbol.
It uses two main operations:
- Shift: moves the next input token to the top of the stack
- Reduce: replaces symbols on top of the stack that match a grammar rule's RHS with the rule's LHS

Example Usage:
    # Parse a custom sentence:
    python3 shift_reduce_parser.py the cat chases the dog

    # Run default test cases:
    python3 shift_reduce_parser.py

Grammar Rules:
    S  -> NP VP     (Sentence = Noun Phrase + Verb Phrase)
    NP -> Det Noun  (Noun Phrase = Determiner + Noun)
    VP -> Verb NP   (Verb Phrase = Verb + Noun Phrase)

Terminal Rules:
    Det  -> the, a, an
    Noun -> cat, dog
    Verb -> chases, eats
"""

import sys

class ShiftReduceParser:
    """
    A shift-reduce parser that processes sentences according to a predefined grammar.

    The parser maintains two main data structures:
    - A stack that holds grammar symbols (both terminals and non-terminals)
    - A buffer that holds the remaining input tokens

    The parsing process alternates between shifting tokens from the buffer to the stack
    and reducing sequences of symbols on the stack according to grammar rules.

    Attributes:
        grammar_rules (list): List of tuples (LHS, RHS) for non-terminal productions
        terminal_rules (dict): Dictionary mapping terminal categories to their possible values
        stack (list): The parsing stack
        buffer (list): The remaining input tokens
    """

    def __init__(self, grammar_rules, terminal_rules):
        """
        Initialize the parser with grammar rules.

        Args:
            grammar_rules (list): List of tuples (LHS, RHS) representing grammar productions
            terminal_rules (dict): Dictionary mapping terminal categories to possible values
        """
        self.grammar_rules = grammar_rules
        self.terminal_rules = terminal_rules
        self.stack = []
        self.buffer = []

    def try_terminal_reduction(self):
        """
        Attempt to reduce the top of stack using terminal rules.

        This method checks if the top stack symbol matches any terminal rule
        and performs the reduction if possible.

        Returns:
            bool: True if a reduction was performed, False otherwise
        """
        if not self.stack:
            return False

        # Look at the top of stack
        top = self.stack[-1]
        for lhs, rhs_list in self.terminal_rules.items():
            if top in rhs_list:
                self.stack.pop()
                self.stack.append(lhs)
                print(f"Terminal reduction: {top} -> {lhs}")
                return True
        return False

    def try_grammar_reduction(self):
        """
        Attempt to reduce the top of stack using grammar rules.

        This method checks if the symbols at the top of the stack match
        the right-hand side of any grammar rule and performs the reduction if possible.

        Returns:
            bool: True if a reduction was performed, False otherwise
        """
        if len(self.stack) < 2:
            return False

        for lhs, rhs in self.grammar_rules:
            if len(rhs) <= len(self.stack):
                stack_top = self.stack[-len(rhs):]
                if stack_top == list(rhs):
                    old_top = self.stack[-len(rhs):]
                    self.stack = self.stack[:-len(rhs)]
                    self.stack.append(lhs)
                    print(f"Grammar reduction: {' '.join(old_top)} -> {lhs}")
                    return True
        return False

    def parse(self, input_sentence):
        """
        Parse an input sentence using shift-reduce parsing.

        The parsing process follows these steps:
        1. Initialize the buffer with input tokens
        2. While there are tokens in buffer or symbols on stack:
           a. Try to perform reductions using existing stack symbols
           b. If no reduction is possible, shift next input token to stack
        3. The parse succeeds if the only symbol left on stack is 'S'

        Args:
            input_sentence (str): The sentence to parse

        Returns:
            list: The final stack containing the parse result

        Raises:
            ValueError: If the sentence cannot be parsed using the grammar
        """
        self.buffer = input_sentence.split()
        self.stack = []
        print(f"\nParsing sentence: {input_sentence}")

        while True:
            print(f"\nStack: {self.stack}")
            print(f"Buffer: {self.buffer}")

            # Try reductions as much as possible
            while self.try_terminal_reduction() or self.try_grammar_reduction():
                pass

            # If we can't reduce and have items in buffer, shift
            if self.buffer:
                next_token = self.buffer.pop(0)
                self.stack.append(next_token)
                print(f"Shifted: {next_token}")
            else:
                # No more input and no reductions possible
                if len(self.stack) == 1 and self.stack[0] == "S":
                    print("\nSuccessfully parsed!")
                    return self.stack
                else:
                    raise ValueError(f"Parsing failed. Final stack: {self.stack}")

# Define grammar rules (non-terminal productions)
grammar_rules = [
    ("S", ["NP", "VP"]),    # Sentence -> Noun Phrase + Verb Phrase
    ("NP", ["Det", "Noun"]), # Noun Phrase -> Determiner + Noun
    ("VP", ["Verb", "NP"])   # Verb Phrase -> Verb + Noun Phrase
]

# Define terminal rules (terminal productions)
terminal_rules = {
    "Det": ["the", "a", "an"],     # Determiners
    "Noun": ["cat", "dog"],        # Nouns
    "Verb": ["chases", "eats"]     # Verbs
}

def main():
    """
    Main function that handles command-line input and runs the parser.

    If a sentence is provided as command-line arguments, it parses that sentence.
    Otherwise, it runs the parser on predefined test sentences.
    """
    parser = ShiftReduceParser(grammar_rules, terminal_rules)

    # If a sentence is provided as command-line argument, use it
    if len(sys.argv) > 1:
        sentence = ' '.join(sys.argv[1:])
        try:
            parsed_tree = parser.parse(sentence)
            print(f"Final parse tree: {parsed_tree}\n")
        except ValueError as e:
            print(f"Error: {str(e)}\n")
    else:
        # Default test sentences
        test_sentences = [
            "the cat chases the dog",
            "a dog eats the cat",
        ]

        print("No sentence provided. Running default test sentences...")
        for sentence in test_sentences:
            try:
                parsed_tree = parser.parse(sentence)
                print(f"Final parse tree: {parsed_tree}\n")
                print("-" * 50)
            except ValueError as e:
                print(f"Error: {str(e)}\n")
                print("-" * 50)

if __name__ == "__main__":
    main()
