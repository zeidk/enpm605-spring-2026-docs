====================================================
L11: Simulation and Mobile Robot Control
====================================================

Overview
--------

This lecture introduces simulation with Gazebo Harmonic and covers the
fundamentals of mobile robot control in ROS 2. You will learn how to
define simulation worlds and robot models using SDF, bridge Gazebo
topics into ROS 2 with ``ros_gz_bridge``, and spawn robots into a
running simulation. The lecture then covers TF2, the ROS 2 coordinate
frame system that every robotic application depends on, including
static and dynamic transforms, transform listeners, and broadcasters.
Finally, you will drive a differential-drive robot using
``geometry_msgs/Twist`` messages and read sensor data (lidar, camera,
IMU) from Python nodes. All hands-on examples use the
``gazebo_demo``, ``tf2_demo``, and ``robot_control_demo`` packages.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the Gazebo Harmonic architecture and how it differs from
  Gazebo Classic.
- Define simulation worlds and robot models using SDF files.
- Configure ``ros_gz_bridge`` to bridge Gazebo topics into ROS 2.
- Spawn a robot model into a running Gazebo simulation.
- Describe the TF2 coordinate frame system and the difference between
  static and dynamic transforms.
- Write a TF2 transform listener and a transform broadcaster in Python.
- Control a differential-drive mobile robot using ``cmd_vel`` and
  ``Twist`` messages.
- Read and process lidar, camera, and IMU sensor data in a ROS 2
  Python node.
- Launch a complete simulation pipeline: Gazebo, bridge, spawn, and
  control nodes.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l11_lecture
   l11_exercises
   l11_quiz
   l11_references


Next Steps
----------

- In the next lecture, we will cover Nav2 and Lifecycle Nodes:

  - Managed node concept and state transitions
  - Nav2 architecture and components
  - Sending navigation goals programmatically
  - Waypoint following

- Complete the exercises from this lecture before the next class.
- Read `Nav2 Documentation
  <https://docs.nav2.org/>`_.
