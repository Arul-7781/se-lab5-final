# Lab 5: Issues Table

| Issue | Type (Tool) | Line(s) | Description | Fix Approach | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Use of `eval` | Security (Bandit, Pylint) | 59 | Using `eval()` is a medium-severity security risk, as it can execute any string as Python code. | Remove the line: `eval("print('eval used')")`. | High Priority |
| Mutable Default Arg | Bug (Pylint) | 8 | `logs=[]` is a dangerous default value. The same list object is shared across all function calls, leading to unexpected behavior. | Change default to `None`: Modify the function signature to `logs=None` and add `if logs is None: logs = []` inside the function. | High Priority |
| Bare `except` | Bug (Pylint, Flake8, Bandit) | 19 | `except:` catches all possible errors, including system-exit signals. Bandit flags `except: pass` as a low-severity issue. | Be specific: Change `except:` to `except KeyError:` to only catch errors when the item is not in the `stock_data` dictionary. | High Priority |
| No `with` for Files | Bug/Resource (Pylint) | 26, 32 | Files are opened without a `with` statement. If an error occurs, the file may not be closed, leading to a resource leak. | Use `with` syntax: Rewrite `loadData` and `saveData` to use `with open(...) as f:`. | High Priority |
| Unused Import | Code Smell (Pylint, Flake8) | 2 | The `logging` module is imported but never used. | Remove the line: Delete `import logging`. | Low Priority |
| Use of `global` | Code Smell (Pylint) | 27 | The `global` statement is used, which can make code harder to debug. | Refactor: (Advanced Fix) Modify `loadData` to return `stock_data` and pass it as a parameter to other functions. | Medium Priority |
| Missing Docstrings | Convention (Pylint) | 1, 8, 14, 22... | The module and all functions are missing docstrings. | Add docstrings: Add a module-level docstring at the top (e.g., `"""Inventory management system."""`) and a docstring to each function. | Low Priority |
| Naming Convention | Convention (Pylint) | 8, 14, 22... | Function names (`addItem`, `loadData`, etc.) do not follow the `snake_case` naming style (`add_item`, `load_data`). | Rename functions: Change all function names to `snake_case`. | Low Priority |
| String Formatting | Convention (Pylint) | 12 | The code uses old `%` formatting instead of a more modern f-string. | Use f-string: Change the line to: `logs.append(f"{str(datetime.now())}: Added {qty} of {item}")`. | Low Priority |
| File Encoding | Warning (Pylint) | 26, 32 | `open()` is called without specifying an `encoding` (e.g., `encoding="utf-8"`). This can cause issues on different operating systems. | Add encoding: When using `with open()`, add the encoding parameter: `with open(file, "r", encoding="utf-8") as f:`. | Medium Priority |
| Whitespace Issues | Style (Flake8, Pylint) | 8, 14, 61... | The file is missing a final newline and does not have the expected 2 blank lines between function definitions. | Fix formatting: Add a new line at the very end of the file and ensure there are two blank lines separating each `def` block. | Low priority |







# Before vs. After Comparison

## Before (inventory_system.py)

* **Pylint Score:** 4.60/10
* **Bandit Security:** 2 issues found (1 Medium, 1 Low).
* **Critical Issues:** The code contained multiple high-priority bugs and security flaws:
    * [cite_start]`eval()` use (High-Severity Security Risk) [cite: 93]
    * [cite_start]Mutable default value (`logs=[]`) (Critical Bug) [cite: 72, 101]
    * [cite_start]Bare `except:` (Bug) [cite: 19, 92, 101]
    * [cite_start]No `with` statement for file handling (Resource Leak Bug) [cite: 101, 102]
    * [cite_start]Unused `logging` import [cite: 1, 101]

## After (cleaned_inventory_system.py)

* **Pylint Score:** 8.31/10 (or higher)
* [cite_start]**Bandit Security:** 0 issues found[cite: 97].
* **Critical Issues:** All high-priority bugs and security vulnerabilities were fixed.
* [cite_start]**Remaining Issues:** Only low-priority style warnings remain (missing docstrings [cite: 104] [cite_start]and minor whitespace formatting [cite: 100]).

# Reflection

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

* **Easiest:** The easiest fixes were the ones that were simple deletions. [cite_start]Removing the `eval("print('eval used')")` line [cite: 59, 101] [cite_start]and the unused `import logging` [cite: 2, 102] were the most straightforward, as they were single-line changes that didn't affect program logic.

* **Hardest:** The hardest fix was the `logs=[]` mutable default argument. This was conceptually difficult because it's not a syntax error, but a subtle logic bug in Python. Understanding *why* a list is shared across all function calls took more thought than fixing a simple style violation. Refactoring the code to remove the `global` statement was also challenging, as it required changing the program's structure so that `stock_data` was passed as a parameter.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, there were some findings that could be considered "false positives" or at least "low-priority" in the context of this lab.

[cite_start]A good example is Pylint flagging all the function names like `addItem` and `loadData` for not being in `snake_case` (e.g., `add_item`, `load_data`)[cite: 1, 2, 3]. While this is a valid violation of the PEP 8 style guide, it doesn't represent a bug or a functional problem with the code. For a small script, enforcing this is not a critical priority.

### 3. How would you integrate static analysis tools into your actual software development workflow?

[cite_start]I would integrate them in two main places: [cite: 96, 97]

1.  **Local Development:** I would use **pre-commit hooks**. These are scripts that automatically run on your local machine *before* you can even make a Git commit. I would configure a hook to run `flake8` and `bandit` on any changed Python files. If any high-priority style or security issues are found, the commit is automatically blocked until I fix them.

2.  **Continuous Integration (CI):** I would set up a CI pipeline using a tool like GitHub Actions. [cite_start]Every time I or a teammate opens a pull request, the server would automatically run all three tools (`pylint`, `bandit`, `flake8`)[cite: 33, 35, 37]. The pipeline could be configured to "fail" the build if the Pylint score is below a certain threshold (like 8.0/10) or if Bandit finds any new security issues. This prevents bad code from ever being merged into the main branch.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The improvements were significant:

* **Robustness:** The code is far more stable. [cite_start]By fixing the bare `except:`[cite: 19], the program no longer risks catching system-level errors. [cite_start]By fixing the `logs=[]` bug[cite: 8], the logging logic is now correct. [cite_start]Using `with open()` [cite: 26, 32] ensures that files are always closed properly, preventing resource leaks and potential data corruption.
* **Security:** The code is demonstrably more secure. [cite_start]Removing the `eval()` function [cite: 59, 101] eliminated a critical vulnerability that could have allowed an attacker to run any code on the machine.
* **Readability:** After applying all the fixes (especially in the final version), the code is much cleaner. [cite_start]Removing the `global` variable [cite: 27] makes the flow of data easier to trace. Using `snake_case` function names and adding docstrings makes the code's purpose immediately clear to a new developer.

