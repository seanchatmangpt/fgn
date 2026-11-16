# fgn migration plan v26.11.16

Standing: UNVERIFIED

## Identity
- Path: /Users/sac/fgn
- Remote: https://github.com/seanchatmangpt/fgn.git (upstream origin/main)
- Branch@sha: main@ae4156d
- Last commit: 2023-10-16; commits: 19; size: 4 MB
- Languages/build: Python (pyproject.toml, setup.py, tox.ini, requirements.txt, uv.lock)
- Nested repos: none

## Observed state
- Dirty: 5 — D __init__.py; M src/typetemp/template/{render_mixin,typed_prompt,typed_template}.py,
  tests/conftest.py
- Untracked: 5 — docs/jira/, hello_module.py, sample_module.py, uv.lock (+ __pycache__)
- Ahead/behind origin/main: 0/20 (remote has 20 newer commits than this checkout)
- Stash: 0; unpushed branches: 0. src.zip present at root.
- Submodules: none

## What it is
fgn: a typed-template / typed-prompt Python library (src/typetemp) from 2023. README.rst
is a boilerplate stub; purpose beyond typetemp is unclear.

## Classification
DORMANT — last commit 2023-10-16, remote is 20 commits ahead of local.

## Migration risk
LOW. Local edits are small 2023-era tweaks to typetemp and two sample modules; the remote
already holds newer work. No secrets.

## Recommended action
CLONE-FRESH
1. DECISION: are the 3 modified typetemp files worth keeping? If yes:
   `cd /Users/sac/fgn && git switch -c wip/2023-typetemp-edits && git add -A && git commit -m "wip: 2023 local edits" && git push -u origin HEAD`
2. Otherwise discard: no copy needed; delete after the archive volume is verified.
3. `rm -rf __pycache__ src.zip` before any copy.

## First commands on the new machine
`git clone https://github.com/seanchatmangpt/fgn.git && cd fgn && uv sync && uv run pytest -q`

## See Also
- ../v26.9.19/
- /Users/sac/docs/jira/v26.11.16/README.md
