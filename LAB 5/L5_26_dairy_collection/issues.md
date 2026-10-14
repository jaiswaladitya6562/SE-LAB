| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak MD5 hash (Bandit B324, High) | Security | 16 | `hashlib.md5()` is a weak, broken hash algorithm | Replaced with `hashlib.sha256()` |
| Shell command with user input (Bandit B605, High) | Security | 31 | `os.system("echo ..." + farmer)` starts a shell, so a crafted farmer name could inject commands | Removed `os.system` and used `print()`; deleted the unused `import os` |
| SQL injection (Bandit B608, Medium) | Security | 11 | The INSERT query is built by pasting values into the string with `.format()` | Used parameterized query with `?` placeholders and a values tuple |
| Redefined outer name (Pylint W0621) | Bug / Design | 6, 10, 19, 24, 34 | Global `conn` is shadowed by function parameters named `conn` | Moved database setup into `create_connection()` and created `conn` inside `main()` |
| Comparison to None (Pylint C0121, Flake8 E711) | Style / Bug | 36 | `fat == None` should use identity comparison | Changed to `fat is None` |
| Unused import (Pylint W0611, Flake8 F401) | Code quality | 2 | `import json` is never used | Removed the import |
| Invalid function names (Pylint C0103) | Style | 10, 15, 19, 24, 30, 34 | camelCase names such as `recordMilk` do not follow snake_case | Renamed to `record_milk`, `farmer_token`, `daily_total`, `top_farmer`, `print_slip`, `low_fat` |
| Missing docstrings (Pylint C0114, C0116) | Documentation | 1, 10, 15, 19, 24, 30, 34, 39 | The module and all functions had no docstrings | Added a short docstring to the module and every function |
| Ambiguous variable name (Flake8 E741) | Style | 26 | Variable `l` is easily confused with `1` or `I` | Renamed to `top` |
| Line too long (Pylint C0301, Flake8 E501) | Style | 7, 11, 20, 25 | Lines exceeded the 79-character limit | Split long strings and calls across multiple lines |
| Old-style string formatting (Pylint C0209) | Style | 11, 21 | `.format()` and `%` formatting could be f-strings | Used f-string for the total in `daily_total`; removed the string formatting in the SQL query |
