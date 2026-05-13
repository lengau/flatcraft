flatcraft.yaml Reference
========================

The ``flatcraft.yaml`` file defines how your application is packaged as a Flatpak.

Top-Level Fields
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - The name of the project
   * - ``app_id``
     - Yes
     - Flatpak application ID in reverse-DNS format (e.g. ``com.example.MyApp``)
   * - ``runtime``
     - Yes
     - The Flatpak runtime to use (e.g. ``org.freedesktop.Platform``)
   * - ``runtime_version``
     - Yes
     - Version of the runtime (e.g. ``"24.08"``)
   * - ``sdk``
     - Yes
     - The SDK to use for building (e.g. ``org.freedesktop.Sdk``)
   * - ``command``
     - Yes
     - The command to run when launching the app
   * - ``modules``
     - Yes
     - List of modules to build (see below)
   * - ``finish_args``
     - No
     - Sandbox permissions (see below)

Modules
-------

Each module defines a component to build:

.. code-block:: yaml

   modules:
     - name: my-lib
       buildsystem: meson
       sources:
         - type: archive
           url: https://example.com/lib-1.0.tar.gz
           sha256: abc123...

     - name: my-app
       buildsystem: simple
       sources:
         - type: git
           url: https://github.com/example/app.git
           tag: v1.0.0
       build_commands:
         - make install PREFIX=/app

Build Systems
~~~~~~~~~~~~~

Supported values for ``buildsystem``:

- ``autotools`` — GNU Autotools (configure/make/make install)
- ``cmake`` — CMake
- ``cmake_ninja`` — CMake with Ninja backend
- ``meson`` — Meson build system
- ``simple`` — Custom build commands only
- ``qmake`` — Qt's qmake

Sources
~~~~~~~

Each source has a ``type`` field:

- ``archive`` — Download and extract a tarball
- ``git`` — Clone a git repository
- ``file`` — Copy a single file
- ``patch`` — Apply a patch file
- ``script`` — Run a script

Common source fields: ``url``, ``sha256``, ``tag``, ``branch``, ``commit``.

Finish Args (Sandbox Permissions)
---------------------------------

.. code-block:: yaml

   finish_args:
     share:
       - network
       - ipc
     socket:
       - x11
       - wayland
       - pulseaudio
     filesystem:
       - home
       - /tmp
     device:
       - dri
       - all

Example
-------

.. code-block:: yaml

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

   finish_args:
     share:
       - network
       - ipc
     socket:
       - x11
       - wayland
     filesystem:
       - home
