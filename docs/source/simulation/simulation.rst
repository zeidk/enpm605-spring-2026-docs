====================================================
Simulation
====================================================

Overview
--------

This page provides instructions for setting up the simulation
environment used in this course. The simulation stack consists of:

- **ROS 2 Jazzy** desktop installation
- **Gazebo Harmonic** simulator
- **Husarion ROSbot** simulation packages (robot model with LiDAR,
  camera, and IMU sensors)

.. note::

   These instructions are for **simulation only**. No physical robot
   hardware is required.

Choosing an Installation Method
-------------------------------

There are two ways to set up the simulation environment:

.. list-table::
   :widths: 15 42 43
   :header-rows: 1
   :class: compact-table

   * - Method
     - When to use
     - Trade-off
   * - :doc:`docker`
     - You need **Gazebo Classic** or you need to use **ROS Humble** for another course
     - Gazebo Harmonic runs inside a Docker container, isolated from
       Gazebo Classic on the host.
   * - :doc:`native`
     - You do **not** need Gazebo Classic and you can use **ROS Jazzy**.
     - Gazebo Harmonic is installed directly on your system. Simpler
       workflow, but cannot coexist with Gazebo Classic.

.. warning::

   Gazebo Harmonic and Gazebo Classic cannot
   coexist on the same system -- they share library names and the
   ``gazebo`` command, leading to symbol collisions. Pick the method
   that matches your situation.

.. toctree::
   :hidden:
   :maxdepth: 2

   docker
   native

.. _simulation-launch:

Launching the Simulation
====================================================

Once your environment is set up (via either method), launch the
simulation.

.. dropdown:: Launch Gazebo with ROSbot
   :open:
   :animate: fade-in-slide-down

   .. code-block:: console

      ros2 launch rosbot_gazebo simulation.yaml robot_model:=<rosbot/rosbot_xl>

   - ``ros2 launch`` starts a launch file that brings up multiple nodes.
   - ``rosbot_gazebo`` is the package containing the simulation launch
     files.
   - ``simulation.yaml`` is the launch file that starts Gazebo with the
     ROSbot model and RViz.
   - ``robot_model:=`` selects the robot model -- use ``rosbot`` or
     ``rosbot_xl``.


.. dropdown:: Launch Arguments
   :animate: fade-in-slide-down

   You can customize the simulation by passing arguments to the launch
   file using the ``argument:=value`` syntax.

   .. list-table::
      :widths: 22 50 28
      :header-rows: 1
      :class: compact-table

      * - Argument
        - Description
        - Default
      * - ``robot_model``
        - Robot model (``rosbot`` or ``rosbot_xl``)
        - ``rosbot``
      * - ``gz_gui``
        - GUI layout configuration file
        - ``teleop.config``
      * - ``gz_headless_mode``
        - Run Gazebo without the GUI
        - ``False``
      * - ``gz_log_level``
        - Console output verbosity (0--4)
        - ``1``
      * - ``gz_world``
        - Path to SDF world file
        - ``husarion_world.sdf``
      * - ``rviz``
        - Launch RViz alongside the simulation
        - ``True``
      * - ``x``, ``y``, ``z``
        - Initial robot position
        - ``0.0``, ``2.0``, ``0.0``
      * - ``roll``, ``pitch``, ``yaw``
        - Initial robot orientation
        - ``0.0``, ``0.0``, ``0.0``

   **Example:** launch without RViz and with the robot at position
   (1, 3, 0):

   .. code-block:: console

      ros2 launch rosbot_gazebo simulation.yaml rviz:=False x:=1.0 y:=3.0


.. _simulation-verify:

Verifying the Setup
====================================================

.. dropdown:: Quick Smoke Test
   :open:
   :animate: fade-in-slide-down

   Open a terminal in your simulation environment and verify the robot
   is publishing data:

   .. code-block:: console

      # List all active topics -- you should see /scan, /odom,
      # /camera/color/image_raw, etc.
      ros2 topic list

      # Print one LiDAR scan message and exit
      ros2 topic echo /scan --once

      # Measure the camera publishing rate (Ctrl+C to stop)
      ros2 topic hz /camera/color/image_raw

      # Print one odometry message and exit
      ros2 topic echo /odom --once

      # Generate a PDF of the TF tree (saved to frames.pdf)
      ros2 run tf2_tools view_frames

   You should see topics for the LiDAR (``/scan``), camera, IMU
   (``/imu_broadcaster/imu``), and odometry (``/odom``).

   **Drive the robot manually:**

   .. code-block:: console

      ros2 run teleop_twist_keyboard teleop_twist_keyboard

   - This node reads your keyboard input and publishes velocity
     commands on ``/cmd_vel``.
   - Use the keys shown on screen (``i`` = forward, ``j`` = turn left,
     ``l`` = turn right, ``k`` = stop, ``,`` = backward).
