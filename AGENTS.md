# AGENTS.md

Guide for AI agents working on **trollsift**. It records the things that are expensive to
rediscover — invariants, deliberate design choices, and workflow traps — not things you can
learn in thirty seconds from the file tree.

## Orientation

- Pure Python, **zero runtime dependencies**, Apache-2.0 (relicensed from GPL in v1.0.0).
- **The entire library is `trollsift/parser.py`** (~730 lines) plus a 20-line `__init__.py`.
  There is no other module. If you are looking for where something lives, it is in `parser.py`.
- `trollsift/version.py` is **generated** by `hatch-vcs` from git tags and is gitignored.
  Never edit or commit it. `pip install -e .` is required before the package imports.
- Public API is exactly seven names: `Parser`, `StringFormatter`, `parse`, `compose`,
  `globify`, `purge`, `validate`.
- Purpose: parse and compose satellite granule filenames using Python format-string syntax.

## Architecture

Four pipelines, all in `parser.py`:

- **Compose** — `compose()` → `_strict_compose()` = `formatter.format()`, where `formatter`
  is the module-level `StringFormatter()` singleton. The `!c !l !u !t !R !h !H` conversions
  are the *only* deviation from stdlib `str.format`.
- **Partial compose** — `_partial_compose()` replaces each undefined `{var:spec}` occurrence
  with a `hex(hash(...))` placeholder token, runs strict compose, then substitutes the
  original `{var:spec}` text back. The result is still a valid format string, so partial
  composes chain.
- **Parse** — `parse()` → `get_convert_dict()` (field → spec) + `extract_values()` →
  `regex_format()` (builds the regex via `RegexFormatter`) → `re.match` → `_convert()`
  coerces each captured group to a Python type.
- **Globify** — `globify()` → `GlobifyFormatter` singleton → the `DT_FMT` table maps
  strftime directives to `?`/`*` runs.

`DT_FMT` is **shared** between globify and parse: `_glob_datetime_directives()` uses its
`?`/`*` values directly, while `_regex_datetime_directives()` derives `\d{N}` from
`count("?")`. Editing `DT_FMT` changes both directions at once. Its `"%%"` entry is
documentation only — every consumer first splits the spec on `%%` via
`_apply_between_percent_escapes()`, so a directive replacement can never straddle a literal
percent. That helper's `join` argument matters: the regex and glob passes rejoin with `%`
because their output is finished, but globify's partial-datetime pass rejoins with `%%`
because its output is still a format spec that gets a second pass.

## Invariants — do not break these

These are load-bearing for downstream projects. Changing any of them is a breaking change.

- **Non-greedy parsing is a contract, not an accident.** `{a}_{b}` against `"abc_def_ghi"`
  yields `abc` / `def_ghi`, not `abc_def` / `ghi`. Documented in `doc/source/usage.rst` and
  the `RegexFormatter` docstring; enforced by `.*?` / `*?` throughout `format_spec_to_regex`.
- **`parse()` and `extract_values()` raise plain `ValueError` on non-match.** Satpy catches
  `ValueError` by name, and `validate()` relies on it. Do not introduce a custom exception.
- **Default keyword values are API**: `parse(..., full_match=True)`,
  `compose(..., allow_partial=False)` (which raises a bare `KeyError` for a missing key),
  `globify(fmt, keyvals=None)`.
- **`globify()` output must stay `fnmatch`-safe** — `*` and `?` only. Downstream feeds it to
  `fnmatch.fnmatch`, `glob.iglob`, *and* `fsspec`'s `fs.glob`. Emitting character classes
  like `[0-9]` would work with `glob` but silently change `fnmatch` and `fsspec` semantics.
- **Type coercion on parse is API**: `:d` → `int`, `:x`/`:X` → base-16 `int`, `:o` → base-8,
  `:b` → base-2, `f`/`e`/`E`/`g` → `float`, and any `%` spec → `datetime.datetime`. `_convert`
  dispatches on the *parsed* type letter (`int_bases`, `fixed_point_types`), never on a
  substring of the whole spec — otherwise a fill character misroutes it (`{foo:d>5s}` is a
  string field, not an int).
- **Padding/fill semantics** (`_strip_padding`, `_get_fill`) back hundreds of real patterns
  such as `{x:_<6s}` and `{x:>04d}`. A width+fill spec deliberately degrades the regex to
  `.{width}` and the fill is stripped afterwards during conversion. That two-step dance is
  intentional — the regex cannot tell fill characters from content. `_strip_padding` takes
  the already-parsed `fmt_spec_regex` groups, not the spec string, so `parse()` matches each
  spec once. `=` alignment puts the padding after the sign (`_strip_sign_padding`), and a
  `0` *flag* means a zero fill (`_get_padding_char`) — but only for `>`/`=` on numbers; see
  the rough edge below.
- **`StringFormatter.CONV_FUNCS`** (`c h H l t u`, plus `R` handled separately) is
  user-facing: `R` removes `-`, `_`, `:` and space; `h` = R+lower, `H` = R+upper. End users
  put these in Satpy `filename=` templates. Entries may be added, never removed or redefined.
- **Names outside `__all__` that are de-facto public**: `get_convert_dict`, `extract_values`,
  `is_one2one`, `regex_format`, and the module-level `formatter` / `globify_formatter`
  singletons. External code imports these from `trollsift.parser`. Narrowing `__all__` in
  v0.6.0 already caused a reported breakage (GH issue 84).

## Format-spec behavior worth knowing before touching the regex code

- Empty spec is equivalent to `s`; `s` maps to `\S`, so string fields never match whitespace.
  A width+fill spec degrades to `.{width}`, which *does* match spaces.
- Duplicate field names: identical specs emit a backreference `(?P=name)`; differing specs
  raise `ValueError`.
- Fixed-point width is a **minimum** (via a `(?=.{width})` lookahead); the decimal count is
  **exact**. So `{foo:5.2f}` matches `"123.45"` and `" 1.23"` but not `"1.23"` or `"1.234"`.
- Every character in `string.punctuation` is escaped in literal text **except `%`**, so
  datetime directives survive. `format_spec_to_regex` strips backslashes before matching a
  spec, because literal text has already been escaped by then.
- Partial datetime globs: pass a `(value, "Ymd")` tuple to substitute only some directives
  and leave the rest as `?`.
- Parsing a time-only spec yields `datetime(1900, 1, 1, ...)` — plain `strptime` defaults.
- **Caching**: module-level `lru_cache` on `regex_format` and `get_convert_dict`; `purge()`
  clears both. `regex_format` constructs a **fresh** `RegexFormatter` on every cache miss on
  purpose — the class holds mutable `_cached_fields` state and a shared instance broke under
  concurrent use. Do not reintroduce a global `RegexFormatter` singleton.

## Development workflow

- **Install**: `pip install -e .` (required — `trollsift/version.py` is generated at build).
- **Test**: `pytest` (testpaths is configured). CI runs `pytest --cov=trollsift trollsift/tests`.
- **`filterwarnings = ["error"]`** — any warning fails a test. `--strict-markers` and
  `--strict-config` are on, so never use a pytest marker without registering it.
- **`mypy trollsift` runs in CI and there is no mypy config anywhere** — it runs on defaults.
  This is easy to forget; run it locally before pushing.
- **Lint**: `pre-commit run -a` (ruff + ruff-format, line length 120, Google-style
  docstrings, **mccabe max-complexity 10**). `format_spec_to_regex` sits closest to the
  complexity ceiling (9); past commits exist purely to get back under it. pre-commit.ci
  runs on PRs but does **not** autofix them.
- **Test layout**: `trollsift/tests/{unittests,integrationtests,regressiontests}/test_parser.py`.
  No `conftest.py`. Older classes subclass `unittest.TestCase`; write new tests in plain
  pytest style with `@pytest.mark.parametrize`, matching `TestCompose` / `TestParserFixedPoint`.
- **CI matrix**: Windows/macOS/Linux × Python 3.10, 3.11, 3.13. Avoid path-separator
  assumptions. Note `requires-python = ">=3.9"` is broader than what CI actually exercises.
- **Docs**: `doc/source/usage.rst` is written entirely as doctests, but **nothing runs them in
  CI**. After changing documented behavior, run `make doctest` in `doc/` by hand. Read the
  Docs builds with `fail_on_warning: true`.
- **Release**: see `RELEASING.md`. `CHANGELOG.md` is generated by `loghub` from GitHub PR
  labels (`bug`, `enhancement`, `documentation`, `backwards-incompatibility`) — do not
  hand-edit it. Tags are `vX.Y.Z`; PyPI publishing uses a trusted publisher on GitHub release.
- **Commit style**: short imperative one-liners, no conventional-commit prefixes — e.g.
  "Add mypy to CI", "Fix overly complex functions". Contributors add themselves to `AUTHORS.md`.

## Downstream consumers (why compatibility matters)

- **satpy** — the dominant consumer. `globify` + `parse` drive file discovery in
  `satpy/readers/core/yaml_reader.py`; `Parser.compose` backs every writer's `filename=`;
  `StringFormatter` renders NetCDF attribute templates in the AWIPS tiled writer; and a
  `Parser` parses CF wavelength metadata. Roughly 130 reader YAML configs carry
  `file_patterns` that trollsift both parses and globifies, exercising string widths, many
  datetime layouts, `_<6s`-style fill/align, and zero-padded ints.
- **trollflow2** — uses `compose`, including `compose("", ...)` on an empty pattern, and
  installs trollsift from **git main** in its CI, so main-branch breakage surfaces there fast.
- **uwsift** — uses `get_convert_dict`, `validate`, `parse`, the module-level `formatter`
  singleton (iterating its `.parse()` tuples directly), and two-argument `globify(fmt, keyvals)`.
- **pyspectral** — optional extra, uses `compose`.

Rule of thumb: any behavior change to parsing or globifying deserves a Satpy sanity check and
a `backwards-incompatibility` label on the PR.

## Known rough edges

Already known. Don't rediscover them, and don't "fix" them as a drive-by in an unrelated PR.

- **Trailing zero padding is ambiguous and is deliberately not stripped.** `{foo:<05d}`
  formats both `-12` and `-1200` as `"-1200"`; `{foo:^05d}` formats both `12` and `120` as
  `"01200"`. There is no correct parse, so `_get_padding_char` infers a `"0"` pad from the
  `0` flag only for the alignments that pad *before* the value (`>`, `=`), where leading
  zeros are never significant. Note the *explicit* `0` fill spelling (`{foo:0<5d}`) does
  strip, and so returns `-12` for `"-1200"` — long-standing behavior, left alone, and
  inconsistent with the flag spelling on purpose. `is_one2one()` detects none of this: its
  generated data fills the field width, so padding is never exercised.
