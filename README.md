# mg-process-chas for [ChAs](https://github.com/ricolab/Chromatin_Assortativity/)

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
1. Update all VM file paths in mug_generated_metadata to local paths
```
test_0_ComputeChromatineassortativityfromPChiCdata.sh:14:TOOL_EXECUTABLE=/home/pmes/mg-process-chas/process_chas.py
test_1_ComputeChromatineassortativityfromChicagodata.sh:14:TOOL_EXECUTABLE=/home/pmes/mg-process-chas/process_chas.py
json/0_ComputeChromatineassortativityfromPChiCdata/in_metadata.json:4:        "file_path": "/home/pmes/mg-process-chas/testing_data/PCHiC_interaction_map.txt",
json/0_ComputeChromatineassortativityfromPChiCdata/in_metadata.json:33:        "file_path": "/home/pmes/mg-process-chas/testing_data/Features_mESC.txt",
json/1_ComputeChromatineassortativityfromChicagodata/in_metadata.json:4:        "file_path": "/home/pmes/mg-process-chas/testing_data/PCHiC_interaction_map_BAD.txt",
json/1_ComputeChromatineassortativityfromChicagodata/
```

2. Run
`./mug_generated_metadata/test_0_ComputeChromatineassortativityfromPChiCdata.sh`

