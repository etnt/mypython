"""
Shamir's Secret Sharing Algorithm

This implementation demonstrates Shamir's Secret Sharing, a cryptographic algorithm
designed by Adi Shamir. It allows a secret to be divided into n parts (shares),
with a threshold of k parts required to reconstruct the secret.

How it works:
1. Secret Splitting (generate_shares function):
   - Choose a prime number p larger than the secret and the number of shares.
   - Create a polynomial of degree (k-1) where:
     * The constant term is the secret.
     * Other coefficients are random numbers between 1 and p-1.
   - Generate n points on this polynomial to create the shares.
   - All calculations are done in a finite field of integers modulo p.

2. Secret Reconstruction (reconstruct_secret function):
   - Use Lagrange interpolation to reconstruct the polynomial.
   - The constant term of this polynomial is the secret.
   - This works because any k points uniquely determine a polynomial of degree (k-1).

Security:
- With fewer than k shares, the secret cannot be reconstructed.
- The system is information-theoretically secure: fewer than k shares provide
  no information about the secret.

Use cases:
- Distributed key management
- Access control systems
- Secure multi-party computation
"""

import random

def generate_shares(secret, threshold, num_shares, prime):
    """
    Generate shares for Shamir's Secret Sharing.

    Args:
        secret (int): The secret to be shared.
        threshold (int): The minimum number of shares required to reconstruct the secret.
        num_shares (int): The total number of shares to generate.
        prime (int): A prime number larger than the secret and num_shares.

    Returns:
        list: A list of shares, where each share is a tuple of (x, y) coordinates.
    """
    if secret >= prime:
        raise ValueError("Secret must be less than the prime")

    # Generate polynomial coefficients.  The first coefficient is the secret.
    # The remaining coefficients are random numbers between 1 and prime-1.
    coefficients = [secret] + [random.randint(1, prime-1) for _ in range(threshold - 1)]

    # Generate shares using the polynomial.
    shares = []
    for x in range(1, num_shares + 1):
        # Calculate y for each share using polynomial evaluation.
        y = 0
        for degree, coeff in enumerate(coefficients):
            # y = Σ(coeff * x^degree) mod prime
            y += coeff * pow(x, degree, prime)
            y %= prime
        shares.append((x, y))

    return shares

def reconstruct_secret(shares, prime):
    """
    Reconstruct the secret from shares using Lagrange interpolation.

    Args:
        shares (list): A list of shares, where each share is a tuple of (x, y) coordinates.
        prime (int): The prime number used in the finite field.

    Returns:
        int: The reconstructed secret.
    """
    secret = 0
    for i, (x_i, y_i) in enumerate(shares):
        numerator = denominator = 1
        for j, (x_j, _) in enumerate(shares):
            if i != j:
                numerator = (numerator * -x_j) % prime
                denominator = (denominator * (x_i - x_j)) % prime
        lagrange = (y_i * numerator * pow(denominator, prime-2, prime)) % prime
        secret = (secret + lagrange) % prime

    return secret

# Example usage
if __name__ == "__main__":
    secret = 1234567
    threshold = 3
    num_shares = 5
    prime = 2**127 - 1  # A Mersenne prime larger than the secret

    shares = generate_shares(secret, threshold, num_shares, prime)
    print("Shares:")
    for share in shares:
        print(share)

    # Reconstruct with exactly 'threshold' number of shares
    reconstructed_secret = reconstruct_secret(shares[:threshold], prime)
    print(f"Original secret: {secret}")
    print(f"Reconstructed secret: {reconstructed_secret}")

    # Reconstruct with more than 'threshold' number of shares
    reconstructed_secret = reconstruct_secret(shares[:4], prime)
    print(f"Reconstructed secret (with 4 shares): {reconstructed_secret}")

    # Attempt to reconstruct with fewer than 'threshold' number of shares
    try:
        reconstructed_secret = reconstruct_secret(shares[:2], prime)
    except Exception as e:
        print(f"Failed to reconstruct with 2 shares: {e}")

    # --- Example with shuffled shares ---
    shuffled_shares = shares[:]  # Create a copy to avoid modifying the original
    random.shuffle(shuffled_shares)

    print("\nShuffled Shares:")
    for share in shuffled_shares:
        print(share)

    try:
        reconstructed_secret = reconstruct_secret(shuffled_shares[:threshold], prime)
        print(f"Reconstructed secret (from shuffled shares): {reconstructed_secret}")
    except Exception as e:
        print(f"Failed to reconstruct from shuffled shares: {e}")
