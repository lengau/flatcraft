Getting Started
===============

Installation
------------

Install flatcraft with pip::

   pip install flatcraft

Or from source::

   git clone https://github.com/lengau/flatcraft.git
   cd flatcraft
   pip install -e .

Prerequisites
-------------

Flatcraft requires:

- Python 3.10 or later
- ``flatpak-builder`` installed on your system
- ``flatpak`` CLI tools

On Ubuntu/Debian::

   sudo apt install flatpak flatpak-builder

Creating Your First Flatpak
---------------------------

1. Create a ``flatcraft.yaml`` in your project directory
2. Run ``flatcraft pack`` to build the flatpak
3. The output ``.flatpak`` bundle will be in the build output directory

See :doc:`flatcraft-yaml` for the full configuration reference.
