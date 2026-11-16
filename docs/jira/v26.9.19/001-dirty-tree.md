# fgn: commit or clean uncommitted changes

- Standing: OPEN
- Created: 2026-09-19 (v26.9.19 gh survey wave)
- Source: working tree dirty at survey time
- Evidence: `git status --porcelain` → 8 path(s) (tracked-modified: 5, untracked: 3); sample:  D __init__.py; M src/typetemp/template/render_mixin.py; M src/typetemp/template/typed_prompt.py;?? hello_module.py;?? sample_module.py;

## Work to complete
- Review the 5 tracked-modified path(s); commit them as atomic pieces on a purpose branch, or revert what is transient.
- For the 3 untracked path(s): add intentional files to git and commit; gitignore or delete build artifacts/temp files.
- Note: this survey's ticket files under docs/jira/v26.9.19/ are intentionally uncommitted; include or exclude them deliberately in the commit plan.

## Acceptance
- `git status --porcelain` is clean (except items deliberately deferred and recorded here).

## History
- 2026-09-19 | OPEN | survey found dirty tree | 8 paths (T5/U3) | commit/clean pending
