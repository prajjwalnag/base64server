# Contributing to Base64 Server

First off, thanks for taking the time to contribute! 🎉 This project is small, approachable, and a great place to make your first open-source contribution.

## Ways to Contribute

- 🐛 **Report a bug** — Open an [issue](https://github.com/prajjwalnag/base64server/issues) with steps to reproduce
- 💡 **Suggest a feature** — Open an issue describing the use case
- 📝 **Improve docs** — Typos, unclear steps, missing examples — all welcome
- 🔧 **Fix something** — Pick an open issue or submit a PR for something you noticed

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/base64server.git
   cd base64server
   ```
3. **Set up the environment** (see the main [README](README.md#quick-start) for full instructions):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # .venv\Scripts\activate on Windows
   pip install -r base64server/requirements.txt
   ```
4. **Run the app** to confirm it works before making changes:
   ```bash
   cd base64server
   python app.py
   ```

## Making Changes

1. Create a branch for your change:
   ```bash
   git checkout -b feature/short-description
   ```
2. Make your changes. Keep them focused — one logical change per PR is easier to review than a bundle of unrelated edits.
3. Test manually:
   - Run the server and exercise the UI (encode + decode flows)
   - Hit the API endpoints with `curl` or the examples in the README
4. Commit with a clear message describing **why**, not just what:
   ```bash
   git commit -m "Fix rate limit header not resetting after window expiry"
   ```
5. Push and open a Pull Request against `main`.

## Pull Request Guidelines

- Describe **what** changed and **why** in the PR description
- Reference any related issue (`Fixes #12`)
- Keep PRs small and scoped — easier to review, faster to merge
- Update the README if your change affects setup, usage, or the API surface

## Code Style

- Follow existing formatting/conventions in the file you're editing
- Prefer clear, readable code over clever one-liners
- No unrelated refactors bundled into a bug-fix PR

## Reporting Security Issues

Please **do not** open a public issue for security vulnerabilities. Instead, reach out directly via [LinkedIn](https://www.linkedin.com/in/prajjwalnag/) or GitHub's private vulnerability reporting.

## Questions?

Open a [discussion or issue](https://github.com/prajjwalnag/base64server/issues) — happy to help.

Thanks again for contributing! ⭐
