from fractions import Fraction
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from typing import Optional, Tuple
import math

# Increase decimal precision for intermediate calculations
getcontext().prec = 50

def percentage_to_rounding_interval(percentage: float) -> Tuple[Fraction, Fraction, int]:
    """
    Convert a reported percentage (e.g. 18.6) into the exact open/closed
    interval of true proportions that round to it under standard half-even
    (banker's) rounding to the given number of decimal places.

    Returns
    -------
    lower : Fraction
        Inclusive lower bound of the true proportion p = x/N.
    upper : Fraction
        Exclusive upper bound of the true proportion.
    decimals : int
        Number of decimal places used in the reported percentage.
    """
    # Represent the percentage exactly as a Decimal to avoid binary float noise
    pct_dec = Decimal(str(percentage))
    decimals = max(0, -pct_dec.as_tuple().exponent)

    # Half-unit in the last decimal place, expressed as a percentage
    half_unit = Decimal('0.5') * (Decimal(10) ** -decimals)

    # Convert to proportion [0,1]
    p = pct_dec / Decimal(100)
    half = half_unit / Decimal(100)

    # Rounding interval: [p - half, p + half)
    # (standard half-even is slightly more subtle at exact midpoints,
    #  but the interval still contains all values that round to the target)
    lower = Fraction(p - half)
    upper = Fraction(p + half)

    return lower, upper, decimals


def find_smallest_sample(
    percentage: float,
    max_N: int = 1_000_000,
) -> Optional[Tuple[int, int, Fraction, int]]:
    """
    Find the smallest positive integer N (sample size) and corresponding
    non-negative integer x (0 ≤ x ≤ N) such that

        round(100 * x / N, decimals) == percentage

    under IEEE-754 / Python round-half-even semantics.

    The search is exhaustive over N = 1, 2, …, max_N and is therefore
    guaranteed to return the minimal N if one exists inside the limit.

    Parameters
    ----------
    percentage : float
        The reported percentage (e.g. 18.6, 9.22, 45.463).
    max_N : int
        Upper bound on the search (default 1 000 000).

    Returns
    -------
    (N, x, exact_fraction, decimals) or None
        N           – minimal sample size
        x           – number of “successes” / “against”
        exact_fraction – Fraction(x, N)
        decimals    – decimal places of the original percentage
    """
    if not (0 <= percentage <= 100):
        raise ValueError("percentage must lie in [0, 100]")

    lower, upper, decimals = percentage_to_rounding_interval(percentage)

    # Special-case exact 0 % and 100 %
    if percentage == 0:
        return 1, 0, Fraction(0, 1), decimals
    if percentage == 100:
        return 1, 1, Fraction(1, 1), decimals

    # Exhaustive search for the smallest N
    for N in range(1, max_N + 1):
        # The integers x that satisfy lower ≤ x/N < upper are
        #   ceil(lower * N) ≤ x ≤ floor((upper * N) - ε)
        x_min = math.ceil(float(lower * N))
        x_max = math.floor(float(upper * N) - 1e-15)  # guard against float noise

        for x in range(max(0, x_min), min(N, x_max) + 1):
            # Exact verification with Fraction
            frac = Fraction(x, N)
            # Convert to percentage with high-precision Decimal and apply
            # the same rounding mode Python’s round() uses (half-even)
            pct_exact = Decimal(x) / Decimal(N) * 100
            rounded = pct_exact.quantize(
                Decimal(10) ** -decimals,
                rounding=ROUND_HALF_EVEN
            )
            if rounded == Decimal(str(percentage)):
                return N, x, frac, decimals

    return None


def format_result(percentage: float, max_N: int = 1_000_000) -> None:
    """Pretty-print a scientifically verified result."""
    result = find_smallest_sample(percentage, max_N=max_N)

    if result is None:
        print(f"No solution found for {percentage}% with N ≤ {max_N:,}. "
              "Increase max_N or check the percentage.")
        return

    N, x, frac, decimals = result
    actual = float(frac) * 100

    print(f"\n{'='*70}")
    print(f"Target percentage          : {percentage}%  ({decimals} decimal place(s))")
    print(f"{'='*70}")
    print(f"Minimal sample size N      : {N:,}")
    print(f"Corresponding count x      : {x:,}")
    print(f"Exact fraction             : {frac}  (= {x}/{N})")
    print(f"Exact percentage           : {actual:.{decimals+6}f} %")
    print(f"Rounds to (half-even)      : {round(actual, decimals)} %")
    print(f"Verification (Decimal)     : "
          f"{Decimal(x)/Decimal(N)*100:.{decimals+8}f} → "
          f"{Decimal(str(percentage))}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    # Scientific test suite covering integers, one decimal, two decimals, etc.
    test_cases = [
        0.0, 100.0,          # extremes
        50, 25, 33,          # integers
        18.6, 13.6, 5.2,     # one decimal
        9.22, 11.1, 9.9,     # two decimals
        45.463,              # three decimals
        0.1, 99.9,           # near boundaries
        33.333, 66.667,      # classic repeating
    ]

    print("=== Scientific verification of minimal sample sizes ===\n")
    for pct in test_cases:
        format_result(pct)

    # Interactive mode
    print("\n" + "="*70)
    print("Enter a percentage (or press Enter to exit).")
    print("You may also supply a second number as max_N, e.g.  18.6 500000")
    while True:
        try:
            line = input("\nPercentage [max_N]: ").strip()
            if not line:
                break
            parts = line.split()
            pct = float(parts[0])
            max_N = int(parts[1]) if len(parts) > 1 else 1_000_000
            format_result(pct, max_N=max_N)
        except ValueError:
            print("Please enter a number (e.g. 18.6 or 9.22 2000000)")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
