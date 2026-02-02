====================================================
Exercises
====================================================

This page contains exercises that reinforce the concepts introduced
in Lecture 11: ROS 2 (Advanced Topics).

Each exercise is designed to be practical and hands-on, covering
QoS, Executors, Launch Files, and Custom Interfaces.


Exercise 1 – QoS Compatibility Analysis
=======================================

Goal
----

Understand QoS compatibility rules and their impact on publisher-subscriber communication.

Task
----

1. Consider the following QoS configurations:

   **Publisher A:**
   
   - Reliability: BEST_EFFORT
   - Durability: VOLATILE
   - History: KEEP_LAST(5)

   **Publisher B:**
   
   - Reliability: RELIABLE
   - Durability: TRANSIENT_LOCAL
   - History: KEEP_LAST(10)

2. For each of the following subscriber configurations, determine if they can successfully receive messages from Publisher A, Publisher B, or both:

   **Subscriber 1:**
   
   - Reliability: RELIABLE
   - Durability: VOLATILE

   **Subscriber 2:**
   
   - Reliability: BEST_EFFORT
   - Durability: VOLATILE

   **Subscriber 3:**
   
   - Reliability: BEST_EFFORT
   - Durability: TRANSIENT_LOCAL

3. Explain the reasoning behind each compatibility result.

Deliverables
------------

- A table showing which publisher-subscriber pairs are compatible.
- A short explanation (3–4 sentences) of why QoS compatibility matters in real robotic systems.


Exercise 2 – Executor Behavior Experiment
=========================================

Goal
----

Observe the difference between single-threaded and multi-threaded executor behavior.

Task
----

1. Create a ROS 2 package named ``executor_experiment``.

2. Implement a node with two timer callbacks:

   - ``slow_callback``: Sleeps for 2 seconds, then logs a message.
   - ``fast_callback``: Logs a message immediately (runs every 500ms).

3. Test the node with:

   a. ``rclcpp::spin(node)`` (single-threaded)
   b. ``MultiThreadedExecutor`` with default thread count

4. Observe and document:

   - How does the slow callback affect the fast callback in each case?
   - What happens when you use different callback groups?

Deliverables
------------

- The C++ source file for your node.
- A short report (half page) documenting your observations with timestamps from the logs.
- An explanation of when you would choose multi-threaded over single-threaded execution.


Exercise 3 – Launch File Development
====================================

Goal
----

Create a comprehensive launch file that demonstrates multiple advanced features.

Task
----

1. Create a package named ``launch_exercise`` with a ``launch`` directory.

2. Create a launch file ``system.launch.py`` that:

   a. Launches the ``talker`` and ``listener`` nodes from ``demo_nodes_cpp``.
   b. Accepts a launch argument ``enable_talker`` (default: ``true``).
   c. Conditionally launches the talker based on the argument.
   d. Groups both nodes under a namespace ``/demo``.

3. Create a second launch file ``full_system.launch.py`` that:

   a. Includes ``system.launch.py``.
   b. Passes the ``enable_talker`` argument through.

4. Test your launch files:

   .. code-block:: bash

      ros2 launch launch_exercise system.launch.py
      ros2 launch launch_exercise system.launch.py enable_talker:=false
      ros2 launch launch_exercise full_system.launch.py enable_talker:=true

Deliverables
------------

- Both launch files with comments explaining each section.
- The ``CMakeLists.txt`` snippet showing how to install launch files.
- Screenshots or terminal output showing the different launch configurations.


Exercise 4 – Custom Message Interface
=====================================

Goal
----

Design and implement a custom message interface for a specific robotics scenario.

Task
----

1. **Scenario**: You are developing a warehouse robot that needs to report its current task status.

2. Create an interface package named ``warehouse_interfaces`` with a message ``TaskStatus.msg`` containing:

   - Constants for task states: ``IDLE``, ``NAVIGATING``, ``PICKING``, ``PLACING``, ``CHARGING``, ``ERROR``
   - A ``std_msgs/Header`` for timestamp
   - A ``string`` for robot ID
   - A ``uint8`` for current state (using the constants)
   - A ``string`` for current task description
   - A ``float32`` for task completion percentage (0.0 to 100.0)
   - A ``geometry_msgs/Pose`` for current position

3. Build the interface package and verify the message structure:

   .. code-block:: bash

      ros2 interface show warehouse_interfaces/msg/TaskStatus

4. Create a simple publisher node that publishes ``TaskStatus`` messages.

Deliverables
------------

- The ``TaskStatus.msg`` file.
- The ``package.xml`` and ``CMakeLists.txt`` for the interface package.
- A simple publisher node that demonstrates using the custom message.
- Terminal output showing the message structure from ``ros2 interface show``.


Exercise 5 – Integrated System Design
=====================================

Goal
----

Design a complete ROS 2 system architecture incorporating QoS, executors, launch files, and custom interfaces.

Scenario
--------

You are designing a multi-robot monitoring system with the following requirements:

- Multiple robots publish their status at 10 Hz.
- A central monitor subscribes to all robot statuses.
- Status messages must be delivered reliably for safety-critical information.
- Sensor data (camera, lidar) uses best-effort delivery for performance.
- The system should be launchable with a single command.

Task
----

1. Design the system architecture:

   - Identify all nodes needed.
   - Define the topics and their QoS requirements.
   - Specify which executor type each node should use and why.

2. Define the custom interfaces needed.

3. Create a launch file structure that:

   - Launches a configurable number of robot simulators.
   - Launches the central monitor.
   - Allows enabling/disabling specific sensor streams via arguments.

4. Document your design decisions.

Deliverables
------------

- A system architecture diagram showing nodes, topics, and QoS settings.
- Interface definitions for your custom messages.
- Launch file(s) with comments.
- A design document (1 page) explaining:

  - Why you chose specific QoS settings for each topic.
  - Why you chose specific executor types for each node.
  - How the launch file structure supports system configuration.