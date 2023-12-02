# Advent of Code Challenges for 2023

## To Prep Debian Linux Environment

First, clone repo and **change into cloned repo directory.**

```
git clone https://github.com/0xc0c0/aoc-2023.git
cd aoc-2023/
```

Best practices are to utilize local virtual environments for python development, so...
Then run:

```
sudo apt-get install python3 python-is-python3
python -m pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

And any time a new python package is required for a project/puzzle, add the package to `requirements.txt` and rerun:

```
python -m pip install -r requirements.txt
```

## To Activate the Virtual Python Environment

This needs to happen everytime you develop to make sure you're using the local virtual python instance instead of the machine-wide one.

From with the `aoc-2023/` folder:

```
source venv/bin/activate
```

## Test-Driven Development (TDD) Approach

There are really great test cases typically described in detail with representative input and solutions. Perfect for unit testing and TDD.

### Logging and showing it in test runs

The template code has a quick `logger` setup. Inserting print statements or quick logging statements like `logger.info("value was %s", val)` works great, but you need to run `pytest` correctly to show the output elegantly for each test run.

```
pytest -o log_cli=true -o log_cli_level="INFO" -v
```

OR, if there are problems in the code, add debug statements with

```
logger.debug("at point xyz the value of val is %s", val)
```

and upgrade your output level to DEBUG from INFO:

```
pytest -o log_cli=true -o log_cli_level="DEBUG" -v
```

They're a little awkward to remember, so I use command line aliases:

```
alias pytest_debug='pytest -o log_cli=true -o log_cli_level="DEBUG" -v'
alias pytest_info='pytest -o log_cli=true -o log_cli_level="INFO" -v'
```

## Recommendation for Jupyter Notebook

When utilizing the `pandas` and `numpy` packages, it was often useful to have a dynamic environment to play around with data outside of the Test Driven Development construct

I excluded the `jupyter` notebooks from git commits, but generally setup ones per Day where it was useful.

From inside a day's folder, in a dedicated terminal

```
mkdir -p ./nb
cd ./nb
jupyter notebook
```

Then inside the notebook in first two cells, copied and ran:

Cell 1:

```
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
```

Cell 2:

```
import solve
import importlib
importlib.reload(solve)
from solve import *
```
