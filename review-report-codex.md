# Code review report

Status: **complete**

Static test-gap analysis only; tests were not executed and coverage was not measured.

critical: 0 | high: 3 | medium: 1 | low: 0 | info: 0

## 1. [HIGH] Expression evaluation permits arbitrary code execution

Location: `vulnerable.py:5` · Agents: quality

If an untrusted caller controls expression, they can execute arbitrary Python code with the process's permissions, including importing modules and invoking filesystem or system operations.

Fix: Replace eval with a restricted arithmetic parser that explicitly allows only required operators and numeric literals.

Suggested test: Verify ordinary arithmetic evaluates correctly and expressions containing function calls, imports, or attribute access are rejected without executing them.

Evidence:

````
    return eval(expression)
````

## 2. [HIGH] Unrestricted eval permits arbitrary code execution

Location: `vulnerable.py:5` · Agents: security

If an attacker can control expression passed to calculate(), they can execute arbitrary Python code with the process's privileges. eval() exposes built-ins by default, allowing imports and operating-system commands.

Fix: Replace eval() with a restricted arithmetic parser that explicitly allows only required numeric literals and operators.

Suggested test: Pass an expression containing a function call or import attempt and assert that it is rejected without executing it; verify supported arithmetic still works.

Evidence:

````
    return eval(expression)
````

## 3. [HIGH] Unrestricted expression evaluation permits arbitrary code execution

Location: `vulnerable.py:5` · Agents: tests

calculate evaluates arbitrary Python with access to builtins. If an untrusted caller controls expression, they can execute code with the process's privileges instead of only performing arithmetic. No tests are supplied to check rejection of non-arithmetic expressions.

Fix: Replace eval with an arithmetic parser that explicitly allows only supported numeric literals and operators.

Suggested test: Assert calculate('2 + 3 * 4') returns 14. Assert calculate("__import__('builtins')") raises a validation error without evaluating the expression.

Evidence:

````
    return eval(expression)
````

## 4. [MEDIUM] Empty input causes division by zero

Location: `vulnerable.py:9` · Agents: quality

Calling average([]) raises ZeroDivisionError because the denominator is zero. The function does not explicitly handle an input for which an average is undefined.

Fix: Check for empty input and raise a descriptive ValueError, or implement an explicitly documented empty-input result.

Suggested test: Call average([]) and assert the documented empty-input behavior; also assert average([2, 4]) equals 3.

Evidence:

````
    return sum(values) / len(values)
````

## Review limitations

- quality: ok
  - Only the supplied snapshot was reviewed; caller trust boundaries and intended input contracts are unknown.
  - No code was executed.
- security: ok
  - Only the supplied snapshot was reviewed. No callers are shown, so attacker control of expression and deployment exposure cannot be established.
- tests: ok
  - Only the supplied snapshot was reviewed; no tests were supplied or executed.
  - Caller trust boundaries and intended behavior for empty inputs to average are unspecified.
