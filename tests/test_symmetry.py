import sympy as sp

from gencf.symmetry_operations import (
    C2_y_rotation,
    Cn_rotation,
    diagonal_plane_reflection,
    horizontal_plane_reflection,
    improper_rotation,
    vertical_plane_reflection,
)


def test_cn_rotation_reduces_to_allowed_component_for_real_components():
    vector = sp.Matrix([1, 1, 1, -1, 1])
    result = Cn_rotation(2, vector)

    assert result == sp.Matrix([1, 0, 1, 0, 1])

def test_cn_rotation_reduces_to_allowed_component_for_imaginary_components():
    vector = sp.Matrix([1, 1, 1, 1, -1])
    result = Cn_rotation(2, vector)

    assert result == sp.Matrix([1, 0, 1, 0, -1])


def test_c2_y_rotation_zeroes_nonmatching_entries():
    vector = sp.Matrix([1, 1, -1])
    result = C2_y_rotation(vector)

    assert result == sp.Matrix([0, 0, 0])

def test_c2_y_rotation_for_k_3_imaginary_terms():
    vector = sp.Matrix([1, 1, 1, 1, 1, -1, 1])
    result = C2_y_rotation(vector)

    assert result == sp.Matrix([1, 1, 1, 0, 1, -1, 1])


def test_improper_rotation_matches_expected_matrix_real_components():
    vector = sp.Matrix([1, 1, 1, -1, 1])
    result = improper_rotation(2, vector)

    assert result == sp.Matrix([1, 1, 1, -1, 1])


def test_improper_rotation_matches_expected_matrix_imaginary_components():
    vector = sp.Matrix([1, 1, 1, 1, -1])
    result = improper_rotation(2, vector)

    assert result == sp.Matrix([1, 1, 1, 1, -1])


def test_horizontal_plane_reflection_matches_expected_matrix():
    vector = sp.Matrix([1, 1, 1, -1, 1])
    result = horizontal_plane_reflection(vector)

    assert result == sp.Matrix([1, 0, 1, 0, 1])


def test_vertical_plane_reflection_leaves_input_unchanged_for_this_case():
    vector = sp.Matrix([1, 1, 1, -1, 1])
    result = vertical_plane_reflection(vector)

    assert result == vector


def test_vertical_plane_reflection_sets_imaginary_terms_to_zero():
    vector = sp.Matrix([1, 1, 1, 1, 1, -1, 1])
    result = vertical_plane_reflection(vector)

    assert result == sp.Matrix([0, 0, 0, 1, 0, 0, 0])


def test_diagonal_plane_reflection_works_for_D2d_real_components():
    vector = sp.Matrix([1, 1, 1, -1, 1])
    result = diagonal_plane_reflection(2, vector)

    assert result == sp.Matrix([0, 0, 1, 0, 0])


def test_diagonal_plane_reflection_works_for_D2d_imaginary_components():
    vector = sp.Matrix([1, 1, 1, 1, -1])
    result = diagonal_plane_reflection(2, vector)

    assert result == sp.Matrix([-sp.I, 0, 1, 0, -sp.I])

def test_diagonal_plane_reflection_works_for_D3d_real_components():
    vector = sp.Matrix([1, 1, 1, -1, 1])
    result = diagonal_plane_reflection(3, vector)

    assert result == sp.Matrix([0, 0, 1, 0, 0])


def test_diagonal_plane_reflection_works_for_D3d_imaginary_components():
    vector = sp.Matrix([1, 1, 1, 1, -1])
    result = diagonal_plane_reflection(3, vector)

    assert result == sp.Matrix([0, 0, 1, 0, 0])

