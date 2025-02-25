mindm documentation
===================

Python library for interacting with local installed MindManager(tm) on Windows and MacOS platform.

Getting Started
===============

Installation
------------

Install using ``pip``:

.. code-block:: bash

   pip install mindm

Basic Usage
-----------

Example for loading a mindmap from an open mindmap document and cloning it to a new document:

.. code-block:: python

   import mindm.mindmap_helper as mm

   document = mm.MindmapDocument()
   if not document.get_mindmap():
       print("No mindmap found.")
   else:
       document.create_mindmap()

Platform Specific Functionality
-------------------------------

Windows
~~~~~~~

Supported:

* topics (central topic + subtopics)
* notes
* icons
* images
* tags
* links (external and topic links)
* relationships
* rtf

Not supported:

* floating topics
* callouts
* colors, lines, boundaries

MacOS
~~~~~

Supported:

* topics (central topic + subtopics)
* notes
* relationships

Not supported:

* icons
* images
* tags
* links
* rtf
* floating topics
* callouts
* colors, lines, boundaries

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   development
