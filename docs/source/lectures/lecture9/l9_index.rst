====================================================
L9: Launch Files, Parameters, & Executors
====================================================

Overview
--------

This lecture extends the ROS 2 foundation from Lecture 8 with three
essential topics for building real robotic systems. You will learn how
to start multiple nodes simultaneously using Python launch files,
configure node behavior at runtime with parameters, and manage
concurrent execution with executors and callback groups. The lecture
covers advanced launch features (includes, conditionals, grouping, and
arguments), the full parameter lifecycle (declaration, retrieval, and
dynamic updates via callbacks), and the threading model underlying ROS 2
execution (single-threaded vs. multi-threaded executors, the Python GIL,
and the difference between mutually exclusive and reentrant callback
groups). All hands-on examples use three dedicated demo packages:
``launch_files_demo``, ``parameters_demo``, and ``executors_demo``.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Write Python launch files to start multiple nodes together.
- Use advanced launch features: arguments, conditionals, grouping, and
  includes.
- Understand what ROS 2 parameters are and their supported types.
- Declare and retrieve parameters in a Python node.
- Set parameters from the command line, launch files, and YAML files.
- React to runtime parameter changes with callbacks.
- Explain the difference between single-threaded and multi-threaded
  executors.
- Use callback groups (mutually exclusive and reentrant) for concurrent
  execution.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l9_lecture
   l9_exercises
   l9_quiz
   l9_references


Next Steps
----------

- In the next lecture, we will cover services and actions:

  - Custom interfaces (``.msg``, ``.srv``, ``.action``)
  - Service servers and clients
  - Action servers and clients
  - Synchronous vs. asynchronous patterns

- Complete the exercises from this lecture before the next class.
- Read `Writing a Simple Service and Client (Python)
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html>`_.
