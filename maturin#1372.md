# Complex Python + Rust layout

At the moment, I have a Python distribution package managed by Poetry, and I'd
like to implement one of its modules in Rust.

On one side, I already had successful and pleasant experience using `maturin`,
but I also like Poetry environment management, development dependencies, and
lock files.

I already had a look into issues and discussions, and found out that the two
things are not incompatible: what I like of Poetry is not the build backend
(i.e. `poetry-core`), but everything else.
Following #1246, I'm willing to switch build backend from `poetry-core` to
`maturin`, while retaining Poetry for development.

Unfortunately, my package is already more complex than the proposed layouts, and
I'd like to also introduce an extended Rust layout.
In the following, I will outline the two levels of support I'm looking for: the
first consist in better integration with pretty standard Python layout (and
possibly Poetry, but I believe this not to be `maturin`'s responsibility), the
second is an extended Rust layout, yet not departing from standard practices.
In order to clarify, I tried to collect the two layouts in a dedicated repo:

https://github.com/AleCandido/atuin

## Multi-package Python

At the moment, my current repository contains a single Python [distribution
package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package),
but multiple [import
packages](https://packaging.python.org/en/latest/glossary/#term-Import-Package).

I tried to follow the advice in #1246, retaining `[tool.poetry]`, but
implementing the [src layout](https://www.maturin.rs/project_layout.html#alternate-python-source-directory-src-layout).
In the repo, this is done in the `alternate` folder.

With this layout, most of the expected workflow works smoothly, i.e.:

- I can install Python import packages with Poetry (declaring them in the
  `[tools.poetry]` section)
- I run `poetry run maturin develop` to recompile the Rust part and install in
  development
- I can package a working wheel by running `poetry run maturin build`

The few places in which this is falling short are:

- `maturin` is currently not packaging the extra Python import packages
- Poetry front-end is not properly working (I'd expect `poetry build` to work similar to
  `pip wheel ...`, but it isn't, since it is not invoking the build backend)
  - this I will raise on Poetry

It seems like nor PEP 517 neither PEP 621 define any way to specify multiple
import packages, so I'd suggest to detect multiple folders in the `src`
directory, and check they contain a top-level `__init__.py` file.

## Rust workspace

One of the reasons to switch to Rust was to release this part with API for a
different language (i.e. make a Rust crate), and possibly provide C bindings as
well.

This is more comfortably developed in distinct crates, and multiple crates might
be useful for further use cases.
I do not ant all of them to be packaged by `maturin`, since a single one will
contain the Python package in the end, but I'd like to develop them altogether
in as single workspace.

So, what I'd like from `maturin`, and it doesn't seem to be currently possible,
is to locate the crate inside a workspace contained in the same `rust` directory
specified in the alternate layout.

In the repo, this is attempted in the `workspace` folder.
In particular, the one presented in this folder is the full layout with two
import packages and two crates:

1. the "main" Python package is `tubul`, depending on `tphon` package resulting
   from the corresponding crate
2. then there is a second package `jerakeen`, providing some further utilities,
   and depending on `tubul`
3. the crate to be recognized by `maturin` is `tphon`, as said before, then on
   its turn depends on
4. `berilia`, that is the crate expected to do the heavy lift, and it has no
   dependence on any other code contained in the package

`berilia` in particular does not have to be known to `maturin`, but it is just
used as a path dependency of `tphon`, that will be resolved by Cargo during
compilation.
I'd like to release `berilia` as a stand-alone crate on https://crates.io, with
no trace of Python packaging.

---

I know I wrote a lengthy issue, and it might be not so straightforward to
implement. However, I expect this not to be incredibly complex: it essentially
boils down to add further import packages on the Python side, and recognize a
nested crate.
If the project makes sense, I'd be happy to provide some help (even a full
proposal) to implement this, if possible with little guidance.
