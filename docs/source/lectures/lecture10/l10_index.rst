=======================================================
L10: Parameters, Custom Interfaces, Services & Actions
=======================================================

Overview
--------

This lecture covers four interconnected pillars of ROS 2 communication
beyond publish/subscribe. You will learn how to configure nodes at
runtime using **parameters**, define domain-specific data types with
**custom interfaces** (``.msg``, ``.srv``, ``.action``), implement
request/response communication with **services**, and build
goal-oriented long-running tasks with **actions**. Together these
mechanisms form the complete ROS 2 communication toolkit required for
building sophisticated robotic systems. All hands-on examples use four
dedicated demo packages: ``param_demo``, ``custom_interfaces``,
``service_demo``, and ``action_demo``.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Declare, read, and set parameters on ROS 2 nodes using Python.
- Write YAML parameter files and pass parameters from the command line
  and launch files.
- Create custom ``.msg``, ``.srv``, and ``.action`` interface
  definitions and build them with CMake.
- Write service servers and service clients (synchronous and
  asynchronous).
- Write action servers and action clients with feedback and
  cancellation support.
- Choose the appropriate communication pattern (topic, service, action)
  for a given robotic task.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_exercises
   l10_quiz
   l10_references


Next Steps
----------

- In the next lecture, we will cover simulation and mobile robot control:

  - Gazebo Harmonic simulation environment
  - TF2 coordinate transforms
  - Commanding mobile robots with ``cmd_vel``
  - Sensor integration (LiDAR, camera, IMU)

- Complete the `exercises
  <https://enpm605-spring-2026-docs.readthedocs.io/en/latest/lectures/lecture10/l10_exercises.html>`_
  from this lecture before the next class.
- Read `Understanding Actions
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html>`_.
