# rad routes

making routes rad!

* Stitch together multiple activities into a single map that can be viewed in any HTML client
* Annotate segments with titles and media
* Mouseover highlighting of each segment on the map

# Installation
If you are using Codespaces, simply launch the Codespace and it will be provisioned correctly (recommended).

To install locally:
1. clone this repository
2. `python -m pip install -r requirements.txt` (note: this was developed in a Python 3.10 environment with
dependencies at the pinned versions in `requirements.txt`, so you may need to update based on your
environment)

# Use
After installation, run `python radoutes.py <path_to_config_file> --out_file_path <path_to_output_file>`.
To try the provided example: `python radroutes.py examples/activities.yml --out_file_path examples`.

# Testing

In this project we use [pytest](https://docs.pytest.org/en/7.2.x/). 
To use, first ensure that it is installed and then run `pytest -v`
from the top-level directory.

We also use the [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) plugin to measure code coverage.
To use, run `pytest --cov src/ test/` from the top-level directory.
