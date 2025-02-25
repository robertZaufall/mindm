Development
===========

This section covers information for developers who want to contribute to mindm.

Installation
------------

For development, you can clone and install the package locally:

.. code-block:: bash

   git clone https://github.com/robertZaufall/mindm
   pip install -e .

Building
--------

To build the package:

.. code-block:: bash

   python -m build

Testing
-------

Run the test script to verify functionality:

.. code-block:: bash

   python ./tests/clone_map_by_dom.py

Documentation
-------------

Generate documentation using Sphinx:

.. code-block:: bash

   cd docs
   make html

View the documentation in your browser:

.. code-block:: bash

   open _build/html/index.html