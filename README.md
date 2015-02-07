Connectivity Explorer
=====================

[PySurfer](http://pysurfer.github.io/) extension for interactively exploring connectivity data on a Freesurfer cortex model.

The tool is intended to be used with a dataset that describes edge weights between regional nodes defined on a Freesurfer surface. It's most geared towards functional connectivity analyses, but it's implemented generally and any kind of data that can be described this way will work.

To use it, you input two data structures:

- `matrix`: A square, symmetric matrix where each cell is the weight of the connection between the row and column nodes. This should be a Pandas DataFrame object with region names as the index and columns. The only constraint on the region names is that they have to start with either `"lh"` or `"rh"` to identify the hemisphere they lie in.

- `names:` A Pandas DataFrame with the region name corresponding to each vertex in the left and right hemisphere meshes. There must be a name for every vertex, but the names can be a superset of `matrix` index and column names (i.e., you can have a dataset that is missing data for some regions).

See the example data for an idea of how the input data should be structured.

Usage
-----

From the command line, using data stored in csv format:

```
./connexplore.py data/resting_matrix.csv data/yeo17_nodes.csv \
                 -annot Yeo2011_17Networks_N1000
```

From an interactive IPython session (make sure to run with `%gui qt` or similar), using data stored in Pandas objects:

```python
c = ConnectivityExplorer(resting_matrix, vertex_names,
                         annot="Yeo2011_17Networks_N1000")
```

Either way will launch a PySurfer window. Right-click on the brain to seed the connectivity analysis. You should see something that looks like this:

![screenshot](screenshot.png)

There are a few other options for controlling what anatomy is used and how the colormap is scaled.

Dependencies
------------

- PySurfer ([installation instructions](http://pysurfer.github.io/install.html))
- Pandas

The tool does not depend on Freesurfer, but you do need to have used Freesurfer to process the anatomy you want to visualize. `$SUBJECTS_DIR` must be defined and have the required files.

If you don't have Freesufer but want to play around with the sample data, you can download the minimal (~20MB) [fsaverage dataset](http://faculty.washington.edu/larsoner/fsaverage_min.zip) that we use for testing PySurfer.

Development
-----------

This is intended mostly as a proof of concept and will probably remain fairly narrowly focused. It's BSD licensed, so feel free to build on it.

Known Issues
------------

There is a memory leak in PySurfer/Mayavi that will cause memory usage to grow over time as you explore different seeds.

License
-------

Copyright (c) 2015, Michael Waskom All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
