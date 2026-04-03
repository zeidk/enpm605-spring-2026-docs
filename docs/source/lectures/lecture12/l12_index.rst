====================================================
L12: Nav2 and Lifecycle Nodes
====================================================

Overview
--------

This lecture introduces **lifecycle (managed) nodes** and the
**Navigation2 (Nav2)** stack in ROS 2. Lifecycle nodes add a
deterministic state machine to the standard ``Node`` class, giving
system integrators precise control over when resources are allocated,
when a node begins processing, and how it shuts down. Nav2 is the
production-grade autonomous navigation framework for ROS 2 and is built
entirely on lifecycle nodes. You will learn how to implement your own
lifecycle nodes in Python, understand the Nav2 architecture and its
plugin-based design, configure Nav2 parameters, launch navigation in
simulation (building on the Gazebo setup from L11), and send navigation
goals programmatically using the ``BasicNavigator`` helper class.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the lifecycle node state machine and its primary and
  transition states.
- Implement a lifecycle node in Python with ``on_configure``,
  ``on_activate``, ``on_deactivate``, ``on_cleanup``, and
  ``on_shutdown`` callbacks.
- Use ``ros2 lifecycle`` CLI tools to inspect and transition managed
  nodes.
- Describe the high-level Nav2 architecture and its core servers.
- Configure Nav2 parameters for planners, controllers, costmaps, and
  AMCL.
- Launch Nav2 in simulation using ``nav2_bringup``.
- Send navigation goals and waypoints programmatically using the
  ``BasicNavigator`` API.
- Generate and save maps using SLAM Toolbox.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l12_lecture
   l12_exercises
   l12_quiz
   l12_references


Next Steps
----------

- In the next lecture, we will cover behavior trees and project
  integration:

  - Behavior tree concepts and terminology (sequence, fallback,
    decorator, condition, action)
  - The ``py_trees`` library for building behavior trees in Python
  - Blackboard data sharing between tree nodes
  - Integrating behavior trees with ROS 2 actions and services
  - Full system integration combining lifecycle nodes, Nav2, and
    behavior trees

- Complete the exercises from this lecture before the next class.
- Read `Nav2 Getting Started
  <https://docs.nav2.org/getting_started/index.html>`_.
