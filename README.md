# genCF
----------------------

A package to determine non-vanishing crystal field parameters from point group symmetries.

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
The crystal field Hamiltonian can be written as [[1](#1), [2](#2)]

$
\displaystyle H_\text{CF} = \sum_{k=2,4,6}\sum_{q=0}^k \text{Re}\bigl[B^k_q\bigl] \left(C^{(k)}_q + (-1)^q C^{(k)}_{-q} \right) + i\text{Im}\bigl[B^k_q\bigl] \left(C^{(k)}_q - (-1)^q C^{(k)}_{-q}\right).
$

Depending on the site symmetry of the crystal, certain components of the crystal field parameters, or the entire parameter will vanish.

The crystal field parameters for odd $k$ do not contribute to the energy splitting between $4f$ energy levels due to parity of the $4f$ eigenstates, but they are relevant when modelling the electric dipole transition [[3](#3), [4](#4), [5](#5)].
As such, they have been denoted $A_{tp}$, following the notation used by Judd and Ofelt [[4](#4), [5](#5)].

Further reading can be found in the references.


Notes
------------
- The $z$-axis is taken as the axis of highest symmetry.
- The $\sigma_v$ symmetry plane lies along the $xz$-plane to make $\text{Im}(B^k_q)$ vanish [[6](#6)].
- Point groups that do not contain $\sigma_v$ symmetry can be rotated about the $z$-axis to remove the imaginary component of ONE of the $B^k_q$ terms for $q \neq 0$ [[6](#6)].
    - *NOTE: this has not been performed in the code*
- The four cubic point groups $T, T_h, T_d, O, O_h$ were to difficult to calculate and the non-vanishing crystal field parameters have been quoted from [[1](#1), [7](#7)].


References
------------
<a id="1">[1]</a> 
G. Liu, Spectroscopic Properties of Rare Earths in Optical Materials, 1st ed (Springer Berlin / Heidelberg, Berlin, Heidelberg, 2005).

<a id="2">[2]</a>
D. J. Newman and B. Ng, editors , Crystal Field Handbook, Digitally printed version (Cambridge Univ. Press, Cambridge, 2007).

<a id="3">[3]</a>
M. F. Reid and F. S. Richardson, Electric dipole intensity parameters for lanthanide 4 f → 4 f transitions, The Journal of Chemical Physics 79, 5735 (1983).

<a id="4">[4]</a>
G. S. Ofelt, Intensities of Crystal Spectra of Rare-Earth Ions, The Journal of Chemical Physics 37, 511 (1962).

<a id="5">[5]</a>
B. R. Judd, Optical Absorption Intensities of Rare-Earth Ions, Phys. Rev. 127, 750 (1962).

<a id="6">[6]</a>
J. W. Leech and D. J. Newman, How to Use Groups, Repr (Chapman and Hall, London, 1977).

<a id="7">[7]</a>
J.-D. Lizarazo-Ferro, T. O. Puel, M. E. Flatté, and R. Zia, Refining spectroscopic calculations for trivalent lanthanide ions: A revised parametric Hamiltonian and open-source solution, Phys. Rev. B 113, 075127 (2026).


