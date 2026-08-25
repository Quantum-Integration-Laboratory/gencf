import pytest

from gencf.terms import generate_allowed_terms, Symmetry

@pytest.mark.parametrize(
    ("symmetry", "expected"),
    [
        ("C2v", Symmetry(symbol="C", order=2, reflection_plane="v", is_cubic=False)),
        ("D4h", Symmetry(symbol="D", order=4, reflection_plane="h", is_cubic=False)),
        ("S6", Symmetry(symbol="S", order=6, reflection_plane=None, is_cubic=False)),
        ("Oh", Symmetry(symbol="Oh", order=None, reflection_plane=None, is_cubic=True)),
    ],
)
def test_symmetry_parse_valid(symmetry, expected):
    assert Symmetry.parse(symmetry) == expected


@pytest.mark.parametrize(
    ("symmetry", "expected_real", "expected_imaginary"),
    [
        (
            "C2",
            {1: (0,), 2: (2, 0), 3 : (2, 0), 4: (4, 2, 0), 5: (4, 2, 0), 6 : (6, 4, 2, 0), 7: (6, 4, 2, 0)},
            {1: tuple(), 2: (2,), 3 : (2,), 4: (4, 2), 5: (4, 2), 6 : (6, 4, 2), 7: (6, 4, 2)}
        ),
        (
            "D2d",
            {1: tuple(), 2: (0,), 3 : tuple(), 4: (4, 0), 5: tuple(), 6 : (4, 0), 7: tuple()},
            {1: tuple(), 2: tuple(), 3 : (2,), 4: tuple(), 5: (2,), 6 : tuple(), 7: (6, 2)}
        ),
        (
            "C3v",
            {1: (0,), 2: (0,), 3 : (3, 0), 4: (3, 0), 5: (3, 0), 6 : (6, 3, 0), 7: (6, 3, 0)},
            {1: tuple(), 2: tuple(), 3 : tuple(), 4: tuple(), 5: tuple(), 6 : tuple(), 7: tuple()}
        ),
        (
            "S4",
            {1: tuple(), 2: (0,), 3 : (2,), 4: (4, 0), 5: (2,), 6 : (4, 0), 7: (6, 2)},
            {1: tuple(), 2: tuple(), 3 : (2,), 4: (4,), 5: (2,), 6 : (4,), 7: (6, 2)}
        ),
        (
            "D3",
            {1: tuple(), 2: (0,), 3 : tuple(), 4: (3, 0), 5: tuple(), 6 : (6, 3, 0), 7: tuple()},
            {1: tuple(), 2: tuple(), 3 : (3,), 4: tuple(), 5: (3,), 6 : tuple(), 7: (6, 3)}
        ),
    ],
)
def test_generate_allowed_terms_smoke(symmetry, expected_real, expected_imaginary):
    terms = generate_allowed_terms(symmetry)

    assert 1 in terms
    assert 2 in terms
    assert 3 in terms
    assert 4 in terms
    assert 5 in terms
    assert 6 in terms
    assert 7 in terms

    assert terms[1]["real"] == expected_real[1]
    assert terms[2]["real"] == expected_real[2]
    assert terms[3]["real"] == expected_real[3]
    assert terms[4]["real"] == expected_real[4]
    assert terms[5]["real"] == expected_real[5]
    assert terms[6]["real"] == expected_real[6]
    assert terms[7]["real"] == expected_real[7]

    assert terms[1]["imaginary"] == expected_imaginary[1]
    assert terms[2]["imaginary"] == expected_imaginary[2]
    assert terms[3]["imaginary"] == expected_imaginary[3]
    assert terms[4]["imaginary"] == expected_imaginary[4]
    assert terms[5]["imaginary"] == expected_imaginary[5]
    assert terms[6]["imaginary"] == expected_imaginary[6]
    assert terms[7]["imaginary"] == expected_imaginary[7]


@pytest.mark.parametrize(
    "symmetry",
    ["Z9", "C", "C99", "D", "D4x", "", "invalid"],
)
def test_symmetry_parse_invalid_raises_value_error(symmetry):
    with pytest.raises(ValueError):
        Symmetry.parse(symmetry)


def test_symmetry_parse_cubic_group_short_circuits():
    parsed = Symmetry.parse("Td")

    assert parsed.symbol == "Td"
    assert parsed.is_cubic is True
    assert parsed.order is None
    assert parsed.reflection_plane is None
