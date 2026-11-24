# Bell-type Riordan inertia

**Extending Mwafise's cycle example to answer Cheon–Jung–Kitaev–Mojallal's Bell-type Riordan inertia question**

Haobo Ma — ChronoAI Pte Ltd, Singapore.  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

## Mathematical coverage

Problem 6.11 in Cheon, Jung, Kitaev and Mojallal,
*Riordan graphs II: Spectral properties*,
[arXiv:1801.07021v1](https://arxiv.org/abs/1801.07021v1), p. 25,
has a negative answer: the proper Bell-type graph with g=1+z^3 at
order five is C_5 with inertia (3,2,0).

Arnauld Mesinga Mwafise's earlier five-cycle example is credited:
*riordan-graph-enumerator*, v1.0.0 (26 October 2026), README §4.4,
[version DOI](https://doi.org/10.5281/zenodo.23676629) and
[pinned example](https://github.com/arnauldmwafise/riordan-graph-enumerator/blob/adef2ec6b5ab78a878911eb514e49188e3eca388/README.md#44-self-complementary-riordan-graphs).
It gives G_5(1+z^3,z), with edges 12,15,23,34,45. Since z(1+z^3)
and z agree modulo z^4, this is the same labelled Bell-type graph.
The note derives its inertia and extends the construction to all cycle orders.

The written proofs establish the following statements.

- Every labelled cycle C_n, n>=3, is G_n(1+z^(n-2), z(1+z^(n-2))).
  Its binary generator prefix is uniquely forced by its first column.
- The complete cycle inertia formula gives counterexamples at all orders
  4q+1>=5. The generator depends on the selected order.
- Every simple graph on at most four vertices has positive index at most
  its negative index. The proof uses trace(A)=0 and trace(A^3)>=0.
- For proper Bell-type graphs at fixed order n, bipartiteness is equivalent
  to vanishing modulo two of odd-degree coefficients through degree n-2.
  This extends the source's even-series observation, which is credited there.
- The source's bound max(n+,n-)<=ceil(n/2) is re-established and is sharp
  at every order n>=2, using cycles at odd orders and paths at even orders.
- G_4(1+z,z(1+z)) has a triangle and inertia (2,2,0), distinguishing equal
  inertia indices from bipartiteness. This converse was not posed in the source.

The cycle spectrum is credited to Brouwer and Haemers, *Spectra of Graphs*,
Section 1.4.3. Jung's 2019 diameter counterexample is credited separately
in the coverage table; it concerns the source's Conjecture 5.1, not Problem 6.11.
The other listed degree, nullity and Catalan-determinant conjectures are not covered.

## Build the PDF

The sole typesetting input is `note.tex`; its bibliography is included.
Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, with the LaTeX packages named in the source:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
```

No BibTeX invocation or external bibliography file is needed.

## Exact finite checks

Python 3.9 or newer, standard library only:

```sh
python3 verify.py > checks.json
```

The deterministic output has SHA-256
`b476ef087e0bd7d2669461fe24c099009a4b1ad8ec6d05aaa7c33cc1b45e28d3`.

The checker constructs adjacency entries by integer polynomial multiplication
and reduction modulo two. Inertia is computed independently by rational
Schur complements: nonzero scalar pivots contribute their sign; a two-by-two
zero-diagonal pivot contributes one of each strict sign; a remaining zero
block contributes nullity. No floating-point rounding or tolerance is used.

The checks comprise:

- The five-vertex matrix, det(A)=2, det(B)=4 and
  B^T A B=diag(2,-2,2,-2,2).
- Every cycle order 3 through 49 and its full inertia triple.
- All 255 binary prefixes at orders 1 through 8, the absolute bound,
  even-label independence, and the nonsingular even-order consequence.
- The finite-prefix bipartiteness equivalence on all 128 proper cases
  in that range, and labelled-cycle prefix uniqueness.
- All 75 labelled simple graphs on 1 through 4 vertices for minimality.
- Sharpness examples at every order 2 through 49.
- The four-vertex triangle-with-pendant-vertex example, determinant 1,
  inertia (2,2,0), and failure of bipartiteness.

At fixed order n>=2 only the first n-1 binary coefficients matter;
order one has zero adjacency independently of g. These finite ranges
supplement the written proofs and do not replace their all-order conclusions.

## Lean coverage

The [pinned Lean file](https://github.com/the-omega-institute/trureturing/blob/79dfe4f731baccd42dd3c56cf6331a0ddd3cafdb/D5/S3/Combinatorics/SpectralGraph/RiordanBellInertiaRefutation.lean)
contains the namespace ending `RiordanBellInertiaRefutation`.
Its public `result` proves the negation of `claim`, the universal strict-index
inequality over all positive orders and integer formal series.
The private lemmas `adjacency_witness`, `B_det`, `congruence` and
`witness_inertia` give the five-vertex coefficient matrix, determinant,
congruence and strict indices (3,2). The other results listed above are
written proofs, separate from that declaration's scope.

## Files and license

The source archive contains `note.tex`, `metadata.json`, `verify.py`,
`checks.json` and this guide. The matching `note.pdf` and deterministic
`checks.json` are also supplied separately. All authored material is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
(`cc-by-4.0`); linked sources retain their own terms.
