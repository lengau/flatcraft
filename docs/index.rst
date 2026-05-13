Flatcraft Documentation
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   flatcraft-yaml
   api/index

Introduction
============

Flatcraft is a craft tool for creating `Flatpak <https://flatpak.org/>`_ packages, following the
patterns established by `snapcraft <https://github.com/canonical/snapcraft>`_,
`rockcraft <https://github.com/canonical/rockcraft>`_, and other \*craft tools.

It uses a declarative ``flatcraft.yaml`` file to define your application's Flatpak manifest,
then builds and bundles it into a distributable ``.flatpak`` file.

Quick Start
===========

Install flatcraft::

   pip install flatcraft

Create a ``flatcraft.yaml`` in your project::

   name: my-app
   app_id: com.example.MyApp
   runtime: org.freedesktop.Platform
   runtime_version: "24.08"
   sdk: org.freedesktop.Sdk
   command: my-app
   modules:
     - name: my-app
       buildsystem: meson
       sources:
         - type: git
           url: https://github.com/example/my-app.git
           tag: v1.0.0

Build your flatpak::

   flatcraft pack

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
