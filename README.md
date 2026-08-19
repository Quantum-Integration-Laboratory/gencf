# genCF
----------------------

A package to determine nonzero crystal field parameters from point group symmetries.

Installation
------------

To install genCF using PyPI, run the following command:

```shell
pip install gencf
```

Example Usage
------------

```pycon
>>> from gencf import generate_allowed_terms, print_allowed_terms

>>> C3v = generate_allowed_terms('C3v')
>>> print_allowed_terms(C3v)
+-----+---------------+-------------------+
|   k | Real Terms    | Imaginary Terms   |
+=====+===============+===================+
|   1 | A10           | —                 |
+-----+---------------+-------------------+
|   2 | B20           | —                 |
+-----+---------------+-------------------+
|   3 | A33, A30      | —                 |
+-----+---------------+-------------------+
|   4 | B43, B40      | —                 |
+-----+---------------+-------------------+
|   5 | A53, A50      | —                 |
+-----+---------------+-------------------+
|   6 | B66, B63, B60 | —                 |
+-----+---------------+-------------------+
|   7 | A76, A73, A70 | —                 |
+-----+---------------+-------------------+

```

Theory
------------
The crystal field Hamiltonian can be written as

$$
H_\text{CF} = \sum_{k=2,4,6}\sum_{q=0}^k \text{Re}\bigl[B^k_q\bigl] \left(C^{(k)}_q + (-1)^q C^{(k)}_{-q} +\right) + i\,\text{Im}\bigl[B^k_q\bigl] \left(C^{(k)}_q - (-1)^q C^{(k)}_{-q}\right).
$$

Depending on the site symmetry of the crystal, certain components of the crystal field parameters, or the entire parameter will vanish.

The crystal field parameters for odd $k$ do not contribute to the energy splitting between $4f$ energy levels due to parity of the $4f$ eigenstates, but they are relevant when modelling the electric dipole transition.
As such, they have been denoted $A_{tp}$, following the notation used by Judd and Ofelt.

References
------------

