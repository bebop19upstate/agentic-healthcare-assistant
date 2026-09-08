Completed Phase 0: venv, deps, folder skeleton, gitignore. Hit a pip/truststore bug with a non-standard Python 3.14 build, fixed by reinstalling Python 3.13 from python.org.
# Day 0 — Environment & Project Scaffold

## What I did
- Set up Python virtual environment and installed dependencies
- Created the full folder skeleton (src/, app/, tests/, data/, docs/)
- Set up .gitignore and .env for secrets
- Verified all packages import correctly

## What I learned
- What a virtual environment actually does and why it isolates dependencies
- Why .gitignore matters for keeping secrets out of GitHub

## Snags hit
- Initial Python install (3.14, non-standard Clang build) had a broken pip —
  ensurepip failed with a truststore/mac_ver() SSL bug specific to that build.
  Fixed by installing Python 3.13 from python.org and recreating the venv.

## Status
Phase 0 complete. Next: Phase 1 (planner), starting at step 1.1 — need
real Anthropic API key in .env before that step.
