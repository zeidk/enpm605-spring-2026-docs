====================================================
L9: Launch Files & Executors
====================================================

Overview
--------

This lecture extends the ROS 2 foundation from Lecture 8 with two
essential topics for building real robotic systems. You will learn how
to start multiple nodes simultaneously using Python launch files and
manage concurrent execution with executors and callback groups. The
lecture covers advanced launch features (includes, conditionals,
grouping, and arguments) and the threading model underlying ROS 2
execution (single-threaded vs. multi-threaded executors, the Python GIL,
and the difference between mutually exclusive and reentrant callback
groups). All hands-on examples use two dedicated demo packages:
``launch_demo`` and ``executor_demo``.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Write Python launch files to start multiple nodes together.
   - Use advanced launch features: arguments, conditionals, grouping, and
     includes.
   - Explain the difference between single-threaded and multi-threaded
     executors.
   - Use callback groups (mutually exclusive and reentrant) for concurrent
     execution.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :hidden:

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
  - Parameters

- Complete the `exercises
  <https://enpm605-spring-2026-docs.readthedocs.io/en/latest/lectures/lecture9/l9_exercises.html>`_
  from this lecture before the next class.
- Read `Writing a Simple Service and Client (Python)
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html>`_.
