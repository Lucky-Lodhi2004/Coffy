# ☕ Contributing to Coffy

Thanks for your interest in improving Coffy! We welcome contributions of all kinds — bug fixes, tests, features, or documentation. Follow the guidelines below to get started.

---

## 🔧 Development Setup

1. **Fork from the `dev` branch** (not `main`)
2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/my-feature
   ```
   ❗ Do **not** include `dev` or `main` in your branch name.

3. **Install dependencies** and test locally:
   ```bash
   pip install -e .
   python run_tests.py
   ```

4. **Format your code with [Black](https://black.readthedocs.io/en/stable/)**:
   ```bash
   black coffy/
   ```
   Black enforces [PEP8](https://peps.python.org/pep-0008/) style automatically.

5. **Lint your code using [Ruff](https://docs.astral.sh/ruff/)**:
   ```bash
   ruff check coffy/
   ```

6. **Commit and push to your fork**, then open a pull request **to the `dev` branch**.

---
### gitignore
Refer [Discussion 57](https://github.com/nsarathy/Coffy/discussions/57)

---

## 🚦 Pull Request Guidelines

- Target **`dev`**, not `main`.
- Keep PRs small and focused — split large changes if necessary.
- Add or update tests for any new behavior.
- Update documentation if your changes affect usage.
- Use clear and descriptive commit messages.
- All tests must pass before merging.

---

## 📦 Publishing to PyPI

Publishing is done from the `main` branch. When ready for release:

- Open a pull request **from `dev` to `main`**
- The maintainer will review, version, and publish the package

**Note**: Only maintainers can merge to `main` or publish.

---

## 🧪 Running Tests

Use the provided runner to install and test:

```bash
python run_tests.py
```

This will install Coffy in editable mode and run all unit tests in `tests/`.

---

## 🙋‍♀️ Where to Start

See [Open Issues](https://github.com/nsarathy/Coffy/issues) for good first tasks:

- 🟢 Label: [`good first issue`](https://github.com/nsarathy/Coffy/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

---

## 📣 Communication

- For questions or ideas, open a [GitHub Discussion](https://github.com/nsarathy/Coffy/discussions)
- To report bugs or request features, [file an issue](https://github.com/nsarathy/Coffy/issues)

---

## 📜 Code of Conduct

All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md).

Let's keep Coffy a friendly and inclusive space for everyone ☕✨
