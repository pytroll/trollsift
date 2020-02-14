
.. .. sectnum::
..   :depth: 4
..   :start: 1
..   :suffix: .

Installation
------------

Trollsift is available from PyPI::

  $ pip install trollsift

Alternatively, you can install it into a conda environment by using the
conda-forge channel::

  $ conda install -c conda-forge trollsift

Or you can install it directly from the GitHub repository::

  $ pip install git+https://github.com/pytroll/trollsift.git

Developer Installation
++++++++++++++++++++++

You can download the trollsift source code from github::

  $ git clone https://github.com/pytroll/trollsift.git

and then run::

  $ pip install -e .

Testing
++++++++

To check if your python setup is compatible with trollsift,
you can run the test suite using pytest::

  $ pytest trollsift/tests

