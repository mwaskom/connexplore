Connectivity Explorer
=====================

PySurfer extension for interactively exploring connectivity data on a Freesurfer cortex model.

Usage
-----

From the command line:

```
./connexplore.py data/resting_matrix.csv data/yeo17_nodes.csv -a Yeo2011_17Networks_N1000
```

This will launch a PySurfer window. Right-click on the brain to seed the connectivity analysis.

![screenshot](screenshot.png)

Dependencies
------------

- PySurfer
- IPython
- Pandas

License
-------

BSD (3-clause)
