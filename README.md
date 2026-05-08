# safecatch

Safecatch is a lightweight Python package that provides decorators for streamlined exception handling.

It helps reduce repetitive `try/except` boilerplate while keeping application logic focused and readable.

Safecatch is designed for:

* graceful degradation,
* expected failure handling,
* resilience patterns,
* and cleaner recovery logic.

---

# Philosophy

Safecatch is **not** intended to silently hide unexpected bugs.

The package is built around one principle:

> Catch only expected failures.

Good use cases:

* network timeouts,
* missing optional files,
* API fallbacks,
* transient failures,
* non-critical parsing issues.

Bad use cases:

* catching broad `Exception`,
* suppressing programming bugs,
* hiding production errors,
* ignoring unexpected behavior.

Safecatch should improve resilience without sacrificing debuggability.

---

# Features

* **safecatch_handler**

  * Catch a specific exception
  * Return a fallback value
  * Or execute a fallback function

* **multi_safecatch_handler**

  * Handle multiple exception types
  * Use different recovery strategies per exception

* Lightweight and dependency-free

* Designed for readable recovery logic

---

# Installation

```bash
pip install safecatch
```

---

# Usage

## Single Exception Handling

Use `safecatch_handler` to catch a single expected exception and provide a fallback value or fallback function.

```python
from safecatch.safecatch import safecatch_handler

@safecatch_handler(ZeroDivisionError, 0)
def divide(a, b):
    return a / b

print(divide(10, 2))  # 5.0
print(divide(10, 0))  # 0
```

---

## Using a Fallback Function

Fallback functions allow custom recovery behavior.

```python
from safecatch.safecatch import safecatch_handler

def fallback_division(a, b):
    print("Division by zero occurred")
    return 0

@safecatch_handler(ZeroDivisionError, fallback_division)
def divide(a, b):
    return a / b

print(divide(10, 0))
```

---

## Multiple Exception Handling

Use `multi_safecatch_handler` to define different recovery behavior for different exceptions.

```python
from safecatch.multi_safecatch import multi_safecatch_handler

def handle_value_error(x, y):
    print(f"Invalid value detected: x={x}, y={y}")
    return -1

@multi_safecatch_handler({
    ZeroDivisionError: 0,
    ValueError: handle_value_error
})
def test_func(x, y):
    if y == 0:
        return x / y

    if y < 0:
        raise ValueError("Negative value")

    return x + y

print(test_func(3, 2))   # 5
print(test_func(3, 0))   # 0
print(test_func(3, -1))  # -1
```

---

# Recommended Usage Patterns

Safecatch works best when handling:

* expected operational failures,
* recoverable errors,
* external system instability.

Examples:

* API request timeouts
* Missing cache entries
* Optional file loading
* Temporary database connectivity issues
* User-provided input parsing

Example:

```python
from requests.exceptions import Timeout

@safecatch_handler(Timeout, {})
def fetch_user_data():
    return external_api_call()
```

---

# Anti-Patterns

Avoid broad exception suppression.

## Avoid This

```python
@safecatch_handler(Exception, None)
def process_data():
    ...
```

This can:

* hide programming bugs,
* suppress critical failures,
* make debugging difficult,
* create silent production issues.

## Prefer Specific Exceptions

```python
@safecatch_handler(FileNotFoundError, [])
def load_optional_config():
    ...
```

Specific exception handling is safer and easier to debug.

---

# Debugging and Observability

Safecatch should be used together with:

* proper logging,
* monitoring,
* exception tracking tools.

Even when exceptions are intentionally handled, failures should remain observable.

Recommended tools:

* logging
* Sentry
* OpenTelemetry
* metrics dashboards

---

# How It Works

Safecatch abstracts repetitive exception handling into reusable decorators.

Instead of repeatedly writing:

```python
try:
    ...
except SomeError:
    ...
```

You define reusable recovery behavior once and apply it declaratively.

---

## `safecatch_handler`

Takes:

* an exception type,
* and a fallback value or fallback function.

If the decorated function raises the specified exception:

* the exception is intercepted,
* and the fallback behavior is executed.

---

## `multi_safecatch_handler`

Accepts a dictionary mapping:

* exception types
* to fallback values or fallback functions.

If an exception is raised:

* the matching recovery behavior is executed,
* otherwise the exception propagates normally.

---

# Testing

Safecatch includes tests written with `pytest`.

Run tests locally:

```bash
pip install -e .
pip install -r tests/requirements.txt
pytest tests/
```

---

# Contributing

Contributions are welcome.

Suggested areas for contribution:

* logging support,
* async support,
* retry strategies,
* observability integrations,
* documentation improvements,
* typing enhancements.

Please open an issue or submit a pull request on the GitHub repository.

---

# Future Direction

Safecatch aims to evolve into a lightweight resilience and recovery utility for Python applications.

Planned areas of improvement include:

* retry support,
* async support,
* telemetry and observability,
* structured result objects,
* production-safe exception handling patterns.
