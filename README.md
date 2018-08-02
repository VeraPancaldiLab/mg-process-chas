# mg-process-test for [ChAs](https://github.com/ricolab/Chromatin_Assortativity/)

# Table Of Content

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

# Requirements

- pip and virtualenv
- Python 2.7.X
- Python Modules:
  - pylint
  - pytest
  - mg-tool-api

# Installation

Create the Python environment

```
virtualenv -p /usr/bin/python2 .py2Env
source .py2Env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# Usage

`./process_test.py --config mg_process_test/tests/json/config_test.json --in_metadata mg_process_test/tests/json/input_test.json --out_metadata metadata.txt`
