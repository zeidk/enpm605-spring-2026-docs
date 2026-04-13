====================================================
GP 2: Coordinate Frames and Autonomous Navigation
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - April 27, 2026, 11:59 PM EST
   * - **Total Points**
     - 50 points
   * - **Submission**
     - Canvas (ZIP file: ``group<N>_gp2.zip`` containing the ROS 2 package)
   * - **Collaboration**
     - Groups of 2.
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.
   * - **Peer Review**
     - Final grade: 60% assignment grade + 40% peer review score.


.. dropdown:: Description
   :open:

   This is a **group project** (2 students per group). You will build a
   ROS 2 system that autonomously navigates a simulated rosbot_xl to three
   waypoints, detects an ArUco marker at each location using TF2 frame
   lookups, computes the centroid of the three marker positions in the
   ``odom`` frame, and finally drives the robot to that centroid.

   You will create **one** ROS 2 Python package inside ``~/enpm605_ws/src/``:

   - ``group<N>_gp2`` -- contains a **marker navigator** node, a launch
     file, a parameter configuration file, and a ``README.md``.

   Two infrastructure packages are **provided** and must not be modified:

   - ``robot_control_demo`` -- provides the **proportional controller**
     node (``p_controller``) that accepts goals on the ``/goal_pose``
     topic (``PoseStamped``) and publishes ``Bool`` on ``/goal_reached``
     when the robot reaches the goal position and orientation.
   - ``frame_demo`` -- provides the **ArUco detector** node
     (``aruco_detector``) that detects ArUco markers from the robot's
     camera and broadcasts each marker's pose as a TF frame named
     ``aruco_marker_<id>``.


.. dropdown:: Learning Objectives
   :open:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: TF2 Frame Lookups
           :class-card: sd-border-info

           Use ``tf2_ros.Buffer`` and ``TransformListener`` to look up
           transforms between coordinate frames. Understand how to
           query the pose of a detected ArUco marker relative to the
           ``odom`` frame rather than the camera frame.

       .. grid-item-card:: Frame Chains
           :class-card: sd-border-info

           Understand how ROS 2 builds a transform tree
           (``odom`` |rarr| ``base_link`` |rarr| ``camera_link`` |rarr|
           ``camera_optical_frame`` |rarr| ``aruco_marker_<id>``) and
           how ``lookup_transform`` traverses that tree automatically.

       .. grid-item-card:: Goal-Based Navigation
           :class-card: sd-border-info

           Publish ``PoseStamped`` goals and subscribe to a ``Bool``
           completion signal to sequence multi-waypoint missions. Convert
           a desired yaw angle to a quaternion for the goal orientation.

       .. grid-item-card:: Parameter Configuration
           :class-card: sd-border-info

           Declare and use ROS 2 parameters in nodes. Load waypoint
           coordinates from a YAML configuration file at launch time.

       .. grid-item-card:: Launch File Integration
           :class-card: sd-border-info

           Write a Python launch file that starts multiple nodes from
           different packages, loads a parameter file, and exposes
           launch arguments.

       .. grid-item-card:: Autonomous State Sequencing
           :class-card: sd-border-info

           Implement a state machine that sequences navigation goals,
           marker detection, data collection, centroid computation,
           and final navigation.

   .. |rarr| unicode:: U+2192


.. dropdown:: Suggested Timeline
   :open:

   .. list-table::
      :widths: 18 12 70
      :header-rows: 1
      :class: compact-table

      * - Period
        - Duration
        - Tasks
      * - **Days 1--2**
        - 2 days
        - Read the assignment carefully. Set up the workspace: verify
          ``robot_control_demo`` and ``frame_demo`` are built and
          functional. Launch the simulation with
          ``aruco_triangle_world.sdf`` and confirm the ArUco detector
          sees markers. Test the P-controller by publishing a
          ``PoseStamped`` manually. Understand how TF frames are
          organized (``ros2 run tf2_tools view_frames``). Create the
          package skeleton. Divide work between teammates.
      * - **Days 3--4**
        - 2 days
        - Implement the navigator node state machine: read waypoints
          from parameters, publish goals to ``/goal_pose``, subscribe to
          ``/goal_reached``, sequence through waypoints. Test that the
          robot physically drives to each waypoint.
      * - **Days 5--6**
        - 2 days
        - Add TF2 frame lookups at each waypoint: initialize Buffer and
          TransformListener, call ``lookup_transform`` for detected
          markers, extract and store each marker's ``(x, y)`` in the
          ``odom`` frame. Compute the centroid and navigate to it.
      * - **Day 7**
        - 1 day
        - Write the launch file. Test the full autonomous pipeline end
          to end. Write ``README.md``. Code quality pass (docstrings,
          type hints, comments). Package and submit.

   .. tip::

      Start by testing each piece in isolation before wiring them
      together. Use ``ros2 run tf2_ros tf2_echo odom aruco_marker_2``
      to verify TF data is flowing before writing lookup code. Publish
      test goals manually with ``ros2 topic pub`` before automating
      the sequencer.


----


Assignment Details
==================

.. toctree::
   :maxdepth: 1
   :titlesonly:

   gp2_infrastructure
   gp2_requirements
   gp2_rubric
