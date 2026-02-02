====================================================
Exercises
====================================================

This page contains five exercises that reinforce the concepts introduced
in Lecture 10: ROS 2 (Introduction).

Each exercise is designed to be small but concrete, so that you can
practice both the conceptual and hands-on aspects of ROS 2.


Exercise 1 – Conceptual ROS 2 Graph (Nodes, Topics, Messages)
=============================================================

Goal
----

Reinforce your understanding of the ROS 2 computation graph:
nodes, topics, and messages.

Task
----

1. Consider a simple mobile robot with the following functionality:

   - A node that reads wheel encoders and publishes odometry.
   - A node that receives velocity commands and sends low-level motor commands.
   - A node that runs a teleoperation interface (keyboard or joystick).
   - A node that estimates the robot’s pose from odometry and IMU.

2. On paper or using a diagramming tool, draw the ROS 2 graph for this system:

   - Show each node as a box.
   - Show each topic as a named arrow between nodes.
   - Label message types when possible (for example,
     ``nav_msgs/msg/Odometry``, ``geometry_msgs/msg/Twist``).

3. Identify for each topic:

   - Which node(s) publish.
   - Which node(s) subscribe.
   - Whether the data flow is “sensor-like” (one-way streaming) or
     “command-like” (actuation).

Deliverables
------------

- A one-page diagram of your ROS 2 graph (PDF, PNG, or clear photo).
- A short paragraph (4–6 sentences) explaining why ROS 2’s modular
  design is helpful for this system (for example, easier debugging,
  swapping nodes, simulation vs. real robot).


Exercise 2 – Create and Build a ROS 2 Workspace
===============================================

Goal
----

Create a ROS 2 workspace from scratch, add a minimal C++ package, and
build it with ``colcon``.

Task
----

1. Create a workspace:

   .. code-block:: bash

      mkdir -p ~/enpm702_ws/src
      cd ~/enpm702_ws

2. Source your ROS 2 installation (adjust to your distribution):

   .. code-block:: bash

      source /opt/ros/humble/setup.bash

3. In the ``src`` directory, create a new package named
   ``enpm702_l10_demo``:

   .. code-block:: bash

      cd ~/enpm702_ws/src
      ros2 pkg create enpm702_l10_demo --build-type ament_cmake --dependencies rclcpp

4. Return to the workspace root and build:

   .. code-block:: bash

      cd ~/enpm702_ws
      colcon build

5. After a successful build, source the workspace:

   .. code-block:: bash

      source install/setup.bash

6. Use ``ros2 pkg list`` to confirm that your package is visible.

Deliverables
------------

- A short text file (for example, ``exercise2_summary.txt``) that
  includes:

  - The exact commands you used.
  - The output of:

    .. code-block:: bash

       ros2 pkg list | grep enpm702_l10_demo

  - A brief note (2–3 sentences) describing what “overlaying” the
    workspace means and why you must source ``install/setup.bash``.


Exercise 3 – Minimal C++ Node with Logging
==========================================

Goal
----

Write, build, and run a minimal C++ ROS 2 node using ``rclcpp`` and
verify that spinning works.

Task
----

1. In the package ``enpm702_l10_demo``, create a source file
   ``src/minimal_node.cpp`` that:

   - Initializes ROS 2.
   - Creates a node named ``"minimal_node"``.
   - Logs a message at startup.
   - Spins until you stop it.

   Example structure:

   .. code-block:: cpp

      #include "rclcpp/rclcpp.hpp"

      int main(int argc, char * argv[])
      {
        rclcpp::init(argc, argv);

        auto node = std::make_shared<rclcpp::Node>("minimal_node");
        RCLCPP_INFO(node->get_logger(), "Minimal node has started.");

        rclcpp::spin(node);
        rclcpp::shutdown();
        return 0;
      }

2. Update ``CMakeLists.txt`` to:

   - Add an executable target called ``minimal_node``.
   - Link it with ``rclcpp``.
   - Install the target to ``lib/${PROJECT_NAME}``.

3. Rebuild your workspace and source it.

4. Run the node:

   .. code-block:: bash

      ros2 run enpm702_l10_demo minimal_node

5. In a separate terminal, list running nodes:

   .. code-block:: bash

      ros2 node list

   Confirm that ``/minimal_node`` appears.

Deliverables
------------

- The ``minimal_node.cpp`` file.
- The relevant snippet from ``CMakeLists.txt`` that shows how you
  added and installed the executable.
- A brief note (2–3 sentences) explaining what happens if you omit
  ``rclcpp::spin(node);`` from ``main``.


Exercise 4 – String Publisher and Subscriber Pair
=================================================

Goal
----

Create a pair of nodes: a publisher that periodically publishes a
string message, and a subscriber that prints whatever it receives.

Task
----

1. In ``enpm702_l10_demo``, add two C++ source files:

   - ``src/minimal_publisher.cpp``
   - ``src/minimal_subscriber.cpp``

2. Implement the publisher:

   - Node name: ``"minimal_publisher"``.
   - Topic name: ``"chatter"``.
   - Message type: ``std_msgs/msg/String``.
   - Use a timer to publish a message every 0.5 seconds, for example
     ``"Hello from ENPM702 L10"``.

3. Implement the subscriber:

   - Node name: ``"minimal_subscriber"``.
   - Topic name: ``"chatter"``.
   - Message type: ``std_msgs/msg/String``.
   - In the callback, print the received string using
     ``RCLCPP_INFO``.

4. Update ``CMakeLists.txt`` to:

   - Add executables for both nodes.
   - Link them with ``rclcpp`` and ``std_msgs``.
   - Install the executables.

5. Rebuild the workspace and source it.

6. Run the nodes in two terminals:

   .. code-block:: bash

      # Terminal 1
      ros2 run enpm702_l10_demo minimal_publisher

      # Terminal 2
      ros2 run enpm702_l10_demo minimal_subscriber

7. Use ROS 2 CLI tools to inspect the system:

   - ``ros2 node list``
   - ``ros2 topic list``
   - ``ros2 topic info /chatter``

Deliverables
------------

- The two C++ source files for publisher and subscriber.
- The updated ``CMakeLists.txt`` snippet.
- A short text note:

  - Describe what happens if the subscriber uses topic name
    ``"chatter2"`` instead of ``"chatter"``.
  - Describe what happens if you change the message type in the
    subscriber to ``geometry_msgs/msg/Twist`` while leaving the
    publisher unchanged.


Exercise 5 – Debugging and Introspection Scenario
=================================================

Goal
----

Practice using ROS 2 introspection tools to debug a small system.

Scenario
--------

Assume the following:

- You start your publisher node  
  (from Exercise 4: ``minimal_publisher``).
- You start your subscriber node  
  (from Exercise 4: ``minimal_subscriber``).
- The subscriber prints nothing, and you see no log output.

Task
----

1. Using only ROS 2 CLI tools (do not modify the code at this stage),
   list and record the outputs of:

   - ``ros2 node list``
   - ``ros2 topic list``
   - ``ros2 topic info /chatter``

2. Consider the following possible causes and explain how you would
   detect each one:

   - The publisher and subscriber are using different topic names.
   - The publisher and subscriber are using different message types.
   - One of the nodes did not start or crashed immediately.
   - You forgot to source the workspace after building.

3. Propose a systematic checklist (4–6 steps) that you would follow
   whenever “I see no messages on my subscriber” happens in ROS 2.

Deliverables
------------

- A short report (about half a page) that includes:

  - The CLI commands you would run and what information you expect.
  - A numbered checklist for debugging publisher–subscriber issues.
  - A final paragraph connecting this process back to the concepts
    from Lecture 10 (nodes, topics, the ROS 2 daemon, overlays).

