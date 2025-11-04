# Static Code Analysis Lab

## Summary of Findings

The following table highlights the most critical and representative issues discovered by the analysis tools.

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Use of `eval`** | **Security / Bug** | `59` | **(Bandit: B307, Pylint: W0123)**. `eval()` can execute arbitrary code from a string, creating a severe injection vulnerability. | Remove the line entirely. If string-based evaluation is ever needed, use the much safer `ast.literal_eval`. |
| **Bare `except`** | **Bug / Style** | `19` | **(Flake8: E722, Pylint: W0702, Bandit: B110)**. Using `except:` or `except: pass` catches *all* errors (including `SystemExit`), silently hiding bugs. | Specify the exact exception to catch, such as `except KeyError:`, to only handle expected errors. |
| **Mutable Default Arg** | **Bug** | `8` | **(Pylint: W0102)**. The `logs=[]` list is created once and shared across all calls, leading to unexpected, shared log data. | Change the default to `logs=None` and initialize a new list inside the function with `if logs is None: logs = []`. |
| **File I/O without `with`** | **Bug / Resource Leak**| `26`, `32` | **(Pylint: R1732)**. Files are opened with `f = open(...)` but not closed in a `finally` block, which can leak file handles if an error occurs. | Use the `with open(...) as f:` context manager, which guarantees the file is closed automatically. |
| **Unused Import** | **Style / Clutter** | `2` | **(Flake8: F401, Pylint: W0611)**. The `logging` module was imported but never used in the code. | Remove the `import logging` line to clean up the code and reduce the program's footprint. |
| **PEP 8 Naming** | **Style / Convention** | `8`, `14`, ... | **(Pylint: C0103)**. Functions like `addItem` use `camelCase`, which violates the standard Python `snake_case` convention. | Rename functions to `add_item`, `remove_item`, `load_data`, etc., for consistency and readability. |

## Lab Reflection

### Which issues were the easiest to fix, and which were the hardest? Why?

* **Easiest:** The easiest issues to fix were the simple, single-line style errors. These included:
    * **`F401: 'logging' imported but unused`** (found by Flake8/Pylint): This was trivial, requiring only the deletion of one line.
    * **`C0103: Naming convention`** (found by Pylint): While tedious, renaming functions from `camelCase` to `snake_case` (e.g., `addItem` to `add_item`) was a straightforward mechanical find-and-replace.

* **Hardest:** The most difficult issues were those that required refactoring the code's logic, not just changing a single line.
    * **`W0603: Using the global statement`** (found by Pylint): Fixing this was the hardest because it required fundamentally changing the program's structure. The `stock_data` global variable had to be removed, `main()` had to be updated to initialize it, and *every single function* had to be modified to accept `stock_data` as a parameter.
    * **`W0102: Dangerous default value []`** (found by Pylint): This was conceptually harder. It required understanding *why* a mutable default is bad (it's shared across all calls) and implementing the correct `logs=None` pattern to fix it.

### Did the static analysis tools report any false positives? If so, describe one example.

A potential false positive was found in the original Pylint report:

* **`C0103: Constant name "stock_data" doesn't conform to UPPER_CASE naming style (invalid-name)`**

Pylint flagged the `stock_data` global variable as a "constant" because it was defined at the module's top level. It expected the name to be `STOCK_DATA`. However, this was a false positive because the program's *intent* was for `stock_data` to be a global *variable*, not a constant, as it was modified by functions like `addItem` and `loadData`. The true issue wasn't the naming (a symptom) but the use of a global variable in the first place (the disease).

### How would you integrate static analysis tools into your actual software development workflow?

Static analysis tools can be integrated at two key points to ensure code quality:

1.  **Local Development (Pre-Commit):** The most effective local practice is using **Git hooks**. A `pre-commit` hook can be configured to automatically run `flake8`, `bandit`, and `pylint` on any changed files *before* the commit is allowed to be created. If any tool reports an error, the commit is blocked, forcing the developer to fix the issues. This prevents bad code from ever entering the repository. 

2.  **Continuous Integration (CI) Pipeline:** For a team workflow, static analysis should be a required step in the CI pipeline (e.g., using GitHub Actions). On every `push` or `pull request` to the `main` branch, a server-side job would automatically:
    * Check out the code.
    * Install all dependencies.
    * Run the full `pylint`, `bandit`, and `flake8` test suites.
    * If any check fails, the pipeline "fails" (shows a red X), which can be configured to automatically block the pull request from being merged until the issues are fixed. 

### What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The improvements were significant across the board:

* **Robustness:** This saw the biggest improvement.
    * Fixing the bare `except:` to `except KeyError:` means the program no longer silently hides unrelated bugs (like a `TypeError`).
    * Fixing the `W0102` mutable default bug (`logs=[]`) prevents a confusing logical error where all calls to `add_item` would share the same log.
    * Replacing `f = open()` with `with open(...)` prevents resource leaks, making file I/O much safer.

* **Security:** The most critical change was removing the `eval()` call (Bandit `B307`), which eliminated a major code injection vulnerability.

* **Readability:** The code is much cleaner. Using standard `snake_case` naming and adding docstrings (to fix Pylint's `C0116` error) makes the code's purpose immediately clear. Removing the global variable also makes the functions easier to understand, as their behavior now depends only on their inputs, not on a hidden shared state.