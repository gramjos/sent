# Pathos de Mathos

A small demo for scanning mathematics papers for lines that begin with **"Obviously"**.

## Installation

This project uses a `requirements.txt` file. We recommend the [`uv` package manager](https://github.com/astral-sh/uv) for fast installs:

```bash
# install dependencies
uv pip install -r requirements.txt
```

You can also use `pip` directly if you prefer:

```bash
pip install -r requirements.txt
```

## Running the tests

```bash
python -m unittest -v
```

Which should output something like:

```
$ python -m unittest -v
TestScan.test_scan_finds_lines ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

## Example usage

You can invoke the `scan_text_for_obviously` function directly to scan text:

```python
from find_obviously import scan_text_for_obviously
text = "Obviously we start.\nThis is not obvious.\n  Obviously more."
for line in scan_text_for_obviously(text):
    print(line)
```

Example output:

```
Found:
Obviously we start.
  Obviously more.
```

The `search_and_scan` function in `find_obviously.py` demonstrates how to search arXiv for math papers and report lines beginning with "Obviously". It requires network access and the `arxiv`, `requests`, and `pdfminer.six` packages.
