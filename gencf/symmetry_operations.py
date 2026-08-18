"""Symmetry operations for crystal field calculations.

This module contains functions for performing various symmetry operations.
"""

import numpy as np
import sympy as sp
from typing import Union

from sympy.physics.wigner import wigner_d


def _zero_nonmatching_elements(vector_transformed: sp.Matrix, vector_original: sp.Matrix) -> sp.Matrix:
    """Zero out elements that don't match the original vector.
    
    Args:
        vector_transformed: The transformed vector.
        vector_original: The original vector for comparison.
        
    Returns:
        The transformed vector with non-matching elements set to zero.
    """
    vector_result = vector_transformed.as_mutable()
    k = int((vector_original.shape[0] - 1) / 2)

    for i in range(2 * k + 1):
        if vector_result[i] != vector_original[i]:
            vector_result[i] = 0

    return vector_result


def Cn_rotation(n: int, vector: sp.Matrix) -> sp.Matrix:
    """Cn rotation symmetry operation.
    
    Args:
        n: The rotation order.
        vector: The quantum numbers vector to rotate.
        
    Returns:
        The rotated vector with non-invariant elements zeroed.
    """
    k = int((vector.shape[0] - 1) / 2)
    rot_angle = 2 * sp.pi / n
    rot_matrix = wigner_d(sp.Integer(k), rot_angle, 0, 0)

    vector_rot = rot_matrix @ vector
    return _zero_nonmatching_elements(vector_rot, vector)


def C2_y_rotation(vector: sp.Matrix) -> sp.Matrix:
    """C2 rotation around the y-axis symmetry operation.
    
    Args:
        vector: The quantum numbers vector to rotate.
        
    Returns:
        The rotated vector with non-invariant elements zeroed.
    """
    k = int((vector.shape[0] - 1) / 2)
    rot_matrix = wigner_d(sp.Integer(k), 0, sp.pi, 0)

    vector_rot = rot_matrix @ vector
    return _zero_nonmatching_elements(vector_rot, vector)


def improper_rotation(n: int, vector: sp.Matrix) -> sp.Matrix:
    """Improper rotation (rotation-reflection) symmetry operation.
    
    Args:
        n: The improper rotation order.
        vector: The quantum numbers vector to transform.
        
    Returns:
        The transformed vector with non-invariant elements zeroed.
    """
    k = int((vector.shape[0] - 1) / 2)
    q = sp.Matrix(np.linspace(k, -k, 2 * k + 1, dtype=int))

    rot_angle = 2 * sp.pi / n
    rot_matrix = wigner_d(sp.Integer(k), rot_angle, 0, 0)
    sigma_h = sp.diag(*[(-1) ** (k + i) for i in q])

    vector_rot_refl = sigma_h @ rot_matrix @ vector
    return _zero_nonmatching_elements(vector_rot_refl, vector)


def horizontal_plane_reflection(vector: sp.Matrix) -> sp.Matrix:
    """Horizontal plane reflection symmetry operation.
    
    Args:
        vector: The quantum numbers vector to reflect.
        
    Returns:
        The reflected vector with non-invariant elements zeroed.
    """
    k = int((vector.shape[0] - 1) / 2)
    q = sp.Matrix(np.linspace(k, -k, 2 * k + 1, dtype=int))

    sigma_h = sp.diag(*[(-1) ** (k + i) for i in q])

    vector_refl = sigma_h @ vector
    return _zero_nonmatching_elements(vector_refl, vector)


def vertical_plane_reflection(vector: sp.Matrix) -> sp.Matrix:
    """Vertical plane reflection symmetry operation.
    
    Args:
        vector: The quantum numbers vector to reflect.
        
    Returns:
        The reflected vector with non-invariant elements zeroed.
    """
    k = int((vector.shape[0] - 1) / 2)
    q = sp.Matrix(np.linspace(k, -k, 2 * k + 1, dtype=int))

    sigma_v = sp.diag(*[(-1) ** i for i in q]).rot90(1)

    vector_refl = sigma_v @ vector
    return _zero_nonmatching_elements(vector_refl, vector)


def diagonal_plane_reflection(n: int, vector: sp.Matrix) -> sp.Matrix:
    """Diagonal plane reflection symmetry operation.
    
    Args:
        n: The order parameter.
        vector: The quantum numbers vector to reflect.
        
    Returns:
        The reflected vector with non-invariant elements zeroed.
    """
    k = int((vector.shape[0] - 1) / 2)
    rot_angle = sp.pi / (2 * n) + sp.pi / 2
    rot_matrix = wigner_d(sp.Integer(k), rot_angle, 0, 0)

    vector_rot = rot_matrix @ vector
    vector_refl = vertical_plane_reflection(vector_rot)

    return vector_refl