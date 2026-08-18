"""Generate allowed crystal field terms.

This module combines symmetry operations to determine the allowed terms
in a crystal field based on the symmetry of the system.
"""

import numpy as np
import sympy as sp
from typing import Any, Dict, List, Tuple

from .symmetry_operations import (
    Cn_rotation,
    C2_y_rotation,
    improper_rotation,
    horizontal_plane_reflection,
    vertical_plane_reflection,
    diagonal_plane_reflection,
)


def obtain_operations(symmetry: str) -> Tuple[Any, Any]:
    """Parse symmetry group notation to extract operations and reflection plane.
    
    Args:
        symmetry: Symmetry group notation (e.g., 'C2v', 'D4h').
        
    Returns:
        Tuple of (operations, reflection_plane) where operations is either
        a string (for cubic groups) or a list, and reflection_plane is None
        or a character describing the plane.
        
    Raises:
        KeyError: If symmetry notation is not recognized.
    """
    allowed_symmetries = [
        'C1', 'S2', 'C1h', 'C2', 'C2h', 'C2v', 'D2', 'D2h',
        'C4', 'S4', 'C4h', 'D2d', 'C4v', 'D4', 'D4h',
        'C3', 'S6', 'C3v', 'D3', 'D3d', 'C3h', 'C6', 'C6h', 'D3h', 'C6v', 'D6', 'D6h',
        'T', 'Th', 'Td', 'O', 'Oh',
    ]

    operations = []
    reflection_plane = None
    
    if symmetry not in allowed_symmetries:
        raise KeyError("This symmetry is not recognised. Try an alternative notation.")
    
    if symmetry in ['T', 'Th', 'Td', 'O', 'Oh']:
        return symmetry, reflection_plane
    
    for i in range(len(symmetry)):
        if i == 0:
            operations.append(symmetry[i])
        elif i == 1:
            operations.append(int(symmetry[i]))
        elif i == 2:
            reflection_plane = symmetry[i]

    return operations, reflection_plane


def generate_allowed_terms(symmetry: str) -> Dict[int, Dict[str, List[int]]]:
    """Generate allowed crystal field terms for a given symmetry group.
    
    This function combines symmetry operations to determine which terms
    are allowed for a given crystal field symmetry.
    
    Args:
        symmetry: Symmetry group classification (e.g., 'C2v', 'D4h', 'Oh').
        
    Returns:
        Dictionary with quantum number k as keys and dictionaries of real and
        imaginary allowed terms as values.
    """
    operations, reflection_plane = obtain_operations(symmetry)

    if isinstance(operations, str):
        allowed_terms = {
            2: {'real': [], 'imaginary': []},
            4: {'real': [4, 0, -4], 'imaginary': []},
            6: {'real': [4, 0, -4], 'imaginary': []},
        }
        return allowed_terms

    allowed_terms = {}
    for k in range(1, 8):
        q = sp.Matrix(np.linspace(k, -k, 2 * k + 1, dtype=int))
        real = sp.Matrix([1 if i >= 0 else (-1) ** (k + i) for i in q])
        imaginary = sp.Matrix([1 if i >= 0 else -(-1) ** (k + i) for i in q])
        imaginary[k] = 0

        if operations[0] in ['C', 'D']:
            real_allowed = Cn_rotation(operations[1], real)
            imaginary_allowed = Cn_rotation(operations[1], imaginary)

            if operations[0] == 'D':
                real_allowed = C2_y_rotation(real_allowed)
                imaginary_allowed = C2_y_rotation(imaginary_allowed)
        elif operations[0] == 'S':
            real_allowed = improper_rotation(operations[1], real)
            imaginary_allowed = improper_rotation(operations[1], imaginary)

        if reflection_plane == 'h':
            real_allowed = horizontal_plane_reflection(real_allowed)
            imaginary_allowed = horizontal_plane_reflection(imaginary_allowed)
        elif reflection_plane == 'v':
            real_allowed = vertical_plane_reflection(real_allowed)
            imaginary_allowed = vertical_plane_reflection(imaginary_allowed)
        elif reflection_plane == 'd':
            real_allowed = diagonal_plane_reflection(operations[1], real_allowed)
            imaginary_allowed = diagonal_plane_reflection(operations[1], imaginary_allowed)

        real_allowed_terms = []
        imaginary_allowed_terms = []
        for i in range(2 * k + 1):
            if real_allowed[i] != 0:
                real_allowed_terms.append(q[i])

            if imaginary_allowed[i] != 0:
                imaginary_allowed_terms.append(q[i])

        allowed_terms[k] = {'real': real_allowed_terms, 'imaginary': imaginary_allowed_terms}

    return allowed_terms