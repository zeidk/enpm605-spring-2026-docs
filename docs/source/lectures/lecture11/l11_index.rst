====================================================
L11: Coordinate Frames, TF2, and Mobile Robot Control
====================================================

Overview
--------

This lecture covers pose representation (position and orientation using
Euler angles and quaternions), coordinate frames and the TF2 transform
library, and mobile robot control. You will learn how orientations are
encoded in ROS 2 using quaternions, why gimbal lock makes Euler angles
unsuitable for continuous rotation tracking, and how TF2 manages
the system-wide tree of coordinate frames that every robotic application
depends on. On the control side, you will drive a differential-drive
robot to a goal pose using a proportional controller on ``cmd_vel``,
subscribe to odometry, and visualize the robot's state in RViz2. All
hands-on examples use the ``robot_control_demo``, ``frame_demo``, and
``tf2_demo`` packages.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Explain how position and orientation are represented in ROS 2 using
     ``geometry_msgs/msg/Pose``, Euler angles, and quaternions.
   - Convert between axis-angle and quaternion representations and
     understand the double-cover property.
   - Describe the gimbal lock problem and explain why quaternions are
     preferred in robotics.
   - Explain coordinate frames and the TF2 transform tree, including the
     standard ROS 2 frames (``world``, ``map``, ``odom``, ``base_link``).
   - Publish static and dynamic transforms, and look them up with
     ``Buffer`` and ``TransformListener``.
   - Inspect the transform tree using ``view_frames``, ``tf2_echo``, and
     ``rqt_tf_tree``.
   - Drive a differential-drive robot to a goal pose using a proportional
     controller on ``cmd_vel``.


Contents
--------

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:


   l11_lecture
   l11_exercises
   l11_quiz
   l11_references


Next Steps
----------

- In the next lecture, we will cover **Mapping and Navigation with
  Nav2**:

  - Occupancy grid maps and the ``map`` frame
  - SLAM with ``slam_toolbox``: building a map from LiDAR + odometry
  - Localization with AMCL against a saved map
  - The Nav2 stack: planner, controller, behavior tree, recovery
  - Sending navigation goals via RViz2 and the ``NavigateToPose`` action

- Complete the exercises from this lecture before the next class.
- Read `Nav2 Getting Started
  <https://docs.nav2.org/getting_started/index.html>`_ and skim
  `Nav2 Concepts
  <https://docs.nav2.org/concepts/index.html>`_.
