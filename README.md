# Pathos de Mathos

This repository contains a small script for finding occurrences of the word
"obviously" in mathematics papers. It was built using a test-driven approach.

## Requirements

The dependencies are listed in `requirements.txt`. They can be installed with
[`uv`](https://github.com/astral-sh/uv), a drop-in replacement for `pip` that
provides faster installs:

```bash
uv pip install -r requirements.txt
```

## Running the tests

The project includes a simple unit test suite. Execute it with:

```bash
python -m unittest -v
```

## Usage

`find_obviously.py` downloads papers from arXiv, extracts their text and prints
any lines containing the word "obviously" (case-insensitive). Example:

```bash
$ python find_obviously.py
An obvious theorem - Alice, Bob
    Obviously the statement follows from ...
```

The actual output will vary depending on the current arXiv results.
