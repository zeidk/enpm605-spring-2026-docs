====================================================
L10: ROS 2 (Introduction)
====================================================

Overview
--------

This lecture introduces the Robot Operating System 2 (ROS 2). You will learn how ROS 2 structures robot software into nodes that communicate via topics, services, and other middleware abstractions, and how to build and run simple ROS 2 packages in your own workspace.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the motivation for ROS 2 and its role in modern robotics.
- Describe the core ROS 2 concepts: nodes, topics, messages, services, and the ROS 2 daemon.
- Set up and build a ROS 2 workspace using ``colcon``.
- Create a minimal C++ node using ``rclcpp``.
- Implement simple publisher and subscriber nodes and run them from the command line.
- Use basic ROS 2 CLI tools to introspect nodes, topics, and messages.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   lecture
   exercises
   references

Next Steps
----------

- In the next lecture, we will deepen the ROS 2 programming model:
  
  - Launch files and multi-node systems.
  - Parameters and configuration.
  - Timers, rate control, and basic debugging tools.

- Start thinking about how to migrate small OOP examples from earlier lectures into ROS 2 nodes to prepare for future assignments.
