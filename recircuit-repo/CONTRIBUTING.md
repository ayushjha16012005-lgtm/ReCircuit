# Contributing to ReCircuit

Thanks for your interest in ReCircuit! This started as a student project for
Automate India (NIET Chapter), and contributions, suggestions, and issue
reports are welcome.

## Getting set up

1. Fork and clone the repo.
2. For the frontend prototype: open `frontend/index.html` directly in a
   browser — no build step required.
3. For the backend: see [`backend/README.md`](backend/README.md) or the
   root [`README.md`](README.md#backend-getting-started) for setup steps.

## Making changes

- Keep the frontend prototype dependency-free (plain HTML/CSS/JS) so it stays
  easy to run for anyone judging or demoing the project.
- Add or update tests in `backend/tests/` for any change to
  `decision_engine.py` or `database.py`.
- Run the test suite before opening a PR:
  ```bash
  cd backend
  python -m pytest tests/ -v
  ```

## Commit style

Use short, descriptive commit messages, e.g.:
- `feat: add tolerance-based grading for inductors`
- `fix: correct capacitor deviation calculation`
- `docs: update architecture diagram`

## Reporting issues

Please include:
- What you expected to happen
- What actually happened
- Steps to reproduce (browser/OS for frontend issues, Python version for
  backend issues)

## Code of conduct

Be respectful and constructive. This is a learning project — questions and
first-time contributions are especially welcome.
