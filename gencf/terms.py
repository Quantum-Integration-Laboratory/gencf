"""Generate allowed crystal field terms.

This module provides functions to generate allowed crystal field terms from an input point-group symmetry.
It also provides a function to print the allowed terms in a tabular format.
"""

import sympy as sp
from dataclasses import dataclass
from typing import Dict, Tuple

from tabulate import tabulate

from .symmetry_operations import (
    Cn_rotation,
    C2_y_rotation,
    improper_rotation,
    horizontal_plane_reflection,
    vertical_plane_reflection,
    diagonal_plane_reflection,
)

# Define the minimum and maximum ranks for crystal field terms
MIN_RANK = 1
MAX_RANK = 7

@dataclass(frozen=True)
class Symmetry:
    """Class to represent a point-group symmetry.
    
    Args:
        symbol: The symmetry symbol (e.g., 'C', 'D', 'S').
        order: The order of the symmetry operation (e.g., 2 for C2).
        reflection_plane: The type of reflection plane ('h', 'v', 'd') if applicable.
        is_cubic: Boolean indicating if the symmetry is cubic.
        
    Returns:
        An instance of the Symmetry class with parsed attributes.
    """
    symbol: str
    order: int | None = None
    reflection_plane: str | None = None
    is_cubic: bool = False

    SUPPORTED_SYMMETRIES = frozenset({
        "C1", "S2", "C1h", "C2", "C2h", "C2v", "D2", "D2h",
        "C4", "S4", "C4h", "D2d", "C4v", "D4", "D4h",
        "C3", "S6", "C3v", "D3", "D3d", "C3h",
        "C6", "C6h", "D3h", "C6v", "D6", "D6h",
        "T", "Th", "Td", "O", "Oh",
    })

    CUBIC_SYMMETRIES = frozenset({"T", "Th", "Td", "O", "Oh",})

    @classmethod
    def parse(cls, symmetry: str):
        """Parse and validate a point-group symmetry string into a Symmetry object.
        
        Args:
            symmetry: Symmetry group classification (e.g., 'C2v', 'D4h', 'Oh').
            
        Returns:
            An instance of the Symmetry class with parsed attributes.
        """
        if symmetry not in cls.SUPPORTED_SYMMETRIES:
            # Raise an error for unsupported symmetries
            raise ValueError(
                f"Unsupported symmetry {symmetry!r}. "
                f"Supported symmetries are: {', '.join(sorted(cls.SUPPORTED_SYMMETRIES))}"
            )

        if symmetry in cls.CUBIC_SYMMETRIES:
            # Return a Symmetry instance for cubic symmetries
            return cls(symbol=symmetry, is_cubic=True)

        # Parse the symmetry string for remaining symmetries
        symbol = symmetry[0]
        order = int(symmetry[1])
        reflection = symmetry[2] if len(symmetry) == 3 else None

        return cls(symbol = symbol, order = order, reflection_plane = reflection, is_cubic = False)


def generate_allowed_terms(symmetry: str) -> Dict[int, Dict[str, Tuple[int, ...]]]:
    """Generate allowed crystal field terms for a given symmetry group.
    
    This function combines symmetry operations to determine which terms
    are allowed for a given crystal field symmetry.
    
    Args:
        symmetry: Symmetry group classification (e.g., 'C2v', 'D4h', 'Oh').
        
    Returns:
        Dictionary with quantum number k as keys and dictionaries of real and
        imaginary allowed terms as values.
    """
    # Parse the symmetry string into a Symmetry object
    symmetry_info = Symmetry.parse(symmetry)

    if symmetry_info.is_cubic:
        # For cubic symmetries, return predefined allowed terms
        return {
            2: {'real': tuple(), 'imaginary': tuple()},
            4: {'real': (4, 0), 'imaginary': tuple()},
            6: {'real': (4, 0), 'imaginary': tuple()},
        }
    
    allowed_terms = {}
    for k in range(MIN_RANK, MAX_RANK + 1):
        q = sp.Matrix(range(k, -k - 1, -1))
        real_vector = sp.Matrix([1 if i >= 0 else (-1) ** i for i in q])
        imaginary_vector = sp.Matrix([1 if i >= 0 else -(-1) ** i for i in q])
        imaginary_vector[k] = 0

        if symmetry_info.symbol in ['C', 'D']:
            # Apply Cn rotation operations for Cyclic and Dihedral groups
            real_allowed = Cn_rotation(symmetry_info.order, real_vector)
            imaginary_allowed = Cn_rotation(symmetry_info.order, imaginary_vector)

            if symmetry_info.symbol == 'D':
                # Apply C2 rotation about the y-axis for Dihedral groups
                real_allowed = C2_y_rotation(real_allowed)
                imaginary_allowed = C2_y_rotation(imaginary_allowed)

        elif symmetry_info.symbol == 'S':
            real_allowed = improper_rotation(symmetry_info.order, real_vector)
            imaginary_allowed = improper_rotation(symmetry_info.order, imaginary_vector)

        # Apply reflection plane operations
        if symmetry_info.reflection_plane == 'h':
            # horizontal plane reflection (xy plane)
            real_allowed = horizontal_plane_reflection(real_allowed)
            imaginary_allowed = horizontal_plane_reflection(imaginary_allowed)
        elif symmetry_info.reflection_plane == 'v':
            # vertical plane reflection (xz plane)
            real_allowed = vertical_plane_reflection(real_allowed)
            imaginary_allowed = vertical_plane_reflection(imaginary_allowed)
        elif symmetry_info.reflection_plane == 'd':
            # diagonal plane reflection (xz plane)
            real_allowed = diagonal_plane_reflection(symmetry_info.order, real_allowed)
            imaginary_allowed = diagonal_plane_reflection(symmetry_info.order, imaginary_allowed)

        # Collect the allowed values of q for q >= 0
        real_allowed_terms = []
        imaginary_allowed_terms = []
        for i in range(k + 1):
            if int(real_allowed[i]) != 0:
                real_allowed_terms.append(int(q[i]))

            if int(imaginary_allowed[i]) != 0:
                imaginary_allowed_terms.append(int(q[i]))

        # Store the allowed terms for the current rank k
        allowed_terms[k] = {'real': tuple(real_allowed_terms), 'imaginary': tuple(imaginary_allowed_terms)}

    return allowed_terms

def print_allowed_terms(allowed_terms: dict[int, dict[str, list[int]]], fmt = "grid") -> None:
    """ Print the allowed crystal field terms in a tabular format.
    
    Args:
        allowed_terms: Dictionary with quantum number k as keys and dictionaries of real and
                       imaginary allowed terms as values.
        fmt: Table format for printing (e.g., "grid", "github").
    """
    header = ["k", "Real Terms", "Imaginary Terms"]
    letter = ('A', 'B')

    rows = []
    for k, terms in allowed_terms.items():
        # Format lists of allowed q-values into readable strings.
        real = ", ".join(f"{letter[k % 2 - 1]}{k}{q}" for q in terms["real"]  ) or "—"
        imaginary = ", ".join( f"{letter[k % 2 - 1]}{k}{q}" for q in terms["imaginary"] ) or "—"

        rows.append([k, real, imaginary])

    # print table
    print(tabulate(rows, headers = header, tablefmt = fmt))
