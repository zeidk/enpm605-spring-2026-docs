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
building sophisticated robotic systems. All hands-on examples use
dedicated demo packages: ``parameters_demo``, ``custom_interfaces``,
``message_demo``, ``service_demo``, and ``action_demo``, built via
the ``lecture10_demo`` metapackage.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Declare, retrieve, and set ROS 2 parameters, and react to runtime
     changes with a parameter callback.
   - Define custom message, service, and action interfaces in a CMake
     package and use them in Python nodes.
   - Write a service server and client using both asynchronous
     (``call_async``) and synchronous (``call``) patterns.
   - Explain when to use a ``MultiThreadedExecutor`` and a separate
     callback group to avoid deadlocks in a synchronous service client.
   - Write an action server that publishes feedback, handles cancellation
     cooperatively, and returns a terminal result.
   - Write an action client that manages the full asynchronous callback
     chain: goal response, feedback, cancel response, and result.
   - Choose the appropriate communication mechanism (topic, service,
     action, parameter) for a given robotics task.


Contents
--------

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_exercises
   l10_quiz
   l10_references


Next Steps
----------

- In the next lecture, we will cover **L11: Simulation and Mobile Robot
  Control**:

  - Gazebo Harmonic architecture and SDF world files
  - Spawning robots and configuring sensors (LiDAR, camera, IMU)
  - ``ros_gz_bridge`` for Gazebo--ROS 2 communication
  - TF2 coordinate frames, broadcasters, and listeners
  - Mobile robot control with ``cmd_vel`` and differential drive
  - Reading sensor data in Python nodes

- Complete the `exercises
  <https://enpm605-spring-2026-docs.readthedocs.io/en/latest/lectures/lecture10/l10_exercises.html>`_
  from this lecture before the next class.
- Set up the Docker simulation environment (see `Simulation
  <https://enpm605-spring-2026-docs.readthedocs.io/en/latest/simulation/simulation.html>`_
  page).
- Read `Getting Started with Gazebo Harmonic
  <https://gazebosim.org/docs/harmonic/getstarted/>`_.
