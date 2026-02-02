====================================================
L11: ROS 2 (Advanced Topics)
====================================================

Overview
--------

This lecture covers advanced ROS 2 topics essential for building robust robotic systems. You will learn how Quality of Service (QoS) policies control communication reliability, how executors manage concurrent callback execution, how launch files orchestrate multi-node systems, and how to create custom interfaces for type-safe communication between nodes.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain Quality of Service (QoS) policies and their impact on ROS 2 communication reliability and performance.
- Configure publishers and subscribers with appropriate QoS settings for different use cases (sensor data, reliable delivery, etc.).
- Describe the role of executors in managing callback execution and concurrency.
- Differentiate between single-threaded and multi-threaded executors and their appropriate use cases.
- Use callback groups (mutually exclusive and reentrant) to control concurrent callback execution.
- Create and configure Python launch files to start multiple nodes with various options.
- Define custom message interfaces for type-safe communication between nodes.
- Build and use custom interface packages in your ROS 2 applications.


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

- In the next lecture, we will continue exploring ROS 2 features:
  
  - Parameters and dynamic configuration.
  - Services for request/response communication.
  - Transforms (TF2) for coordinate frame management.

- Final Quiz.