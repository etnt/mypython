import random

class Node:
    """
    Represents a node in the game tree.

    Attributes:
        value (int): The value associated with this node.
        children (list): A list of child nodes.
    """

    def __init__(self, value, children=None):
        """
        Initialize a Node object.

        Args:
            value (int): The value associated with this node.
            children (list, optional): A list of child nodes. Defaults to None.
        """
        self.value = value
        self.children = children if children else []


def minimax(node, depth, alpha, beta, is_maximizing):
    """
    Implement the Minimax algorithm with Alpha-Beta Pruning.

    Args:
        node (Node): The current node in the game tree.
        depth (int): The current depth in the game tree.
        alpha (float): The best value that the maximizer can guarantee at this level or above.
        beta (float): The best value that the minimizer can guarantee at this level or above.
        is_maximizing (bool): True if it's the maximizing player's turn, False otherwise.

    Returns:
        tuple: A tuple containing the best score for the current player and the best child node.
    """
    if depth == 0 or len(node.children) == 0:
        return node.value, None

    best_child = None

    if is_maximizing:
        value = float('-inf')
        for child in node.children:
            child_value, _ = minimax(child, depth - 1, alpha, beta, False)
            if child_value > value:
                value = child_value
                best_child = child
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cut-off
        return value, best_child
    else:
        value = float('inf')
        for child in node.children:
            child_value, _ = minimax(child, depth - 1, alpha, beta, True)
            if child_value < value:
                value = child_value
                best_child = child
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cut-off
        return value, best_child


def create_sample_tree():
    """
    Create a larger sample game tree for testing.

    Returns:
        Node: The root node of the sample game tree.
    """
    root = Node(0)
    
    # Level 1
    root.children = [Node(0), Node(0), Node(0)]
    
    # Level 2
    root.children[0].children = [Node(3), Node(5), Node(2)]
    root.children[1].children = [Node(9), Node(1), Node(2)]
    root.children[2].children = [Node(1), Node(2), Node(3)]
    
    # Level 3
    root.children[0].children[0].children = [Node(1), Node(5)]
    root.children[0].children[1].children = [Node(8), Node(2)]
    root.children[0].children[2].children = [Node(3), Node(7)]
    
    root.children[1].children[0].children = [Node(2), Node(6)]
    root.children[1].children[1].children = [Node(4), Node(3)]
    root.children[1].children[2].children = [Node(1), Node(9)]
    
    root.children[2].children[0].children = [Node(5), Node(4)]
    root.children[2].children[1].children = [Node(7), Node(2)]
    root.children[2].children[2].children = [Node(6), Node(1)]
    
    return root


def print_path_to_best_move(node, depth, is_maximizing):
    score, best_child = minimax(node, depth, float('-inf'), float('inf'), is_maximizing)
    print(f"Depth {depth}: Score = {score}, Node value = {node.value}")
    if best_child and depth > 0:
        print_path_to_best_move(best_child, depth - 1, not is_maximizing)


def pretty_print_tree(node, prefix="", is_last=True):
    """
    Pretty print the game tree.

    Args:
        node (Node): The current node in the game tree.
        prefix (str): The prefix to use for the current line (for indentation).
        is_last (bool): Whether the current node is the last child of its parent.
    """
    # Print the current node
    print(prefix, end="")
    print("└── " if is_last else "├── ", end="")
    print(node.value)

    # Prepare the prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Print children
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        is_last_child = i == child_count - 1
        pretty_print_tree(child, child_prefix, is_last_child)


# Create a larger sample game tree
root = create_sample_tree()

print("Sample Game Tree:")
pretty_print_tree(root)
print("\n")

# Run the Minimax algorithm with Alpha-Beta Pruning
best_score, best_move = minimax(root, 3, float('-inf'), float('inf'), True)
print("Best score:", best_score)
print("Best move value:", best_move.value if best_move else "No move available")

# Additional test: run minimax on a subtree
subtree_root = root.children[1]
subtree_score, subtree_move = minimax(subtree_root, 2, float('-inf'), float('inf'), False)
print("Subtree best score:", subtree_score)
print("Subtree best move value:", subtree_move.value if subtree_move else "No move available")

print("\nPath to the best move:")
print_path_to_best_move(root, 3, True)
