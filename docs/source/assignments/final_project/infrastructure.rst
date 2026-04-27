====================================================
Simulation and Provided Code
====================================================


Simulation Setup
================

This project uses the **final project world** (``final_project.sdf``)
from ``husarion_gz_worlds`` and the differential-drive ``rosbot``. The
world is a 12 m x 10 m disaster zone with four rooms separated by
walls and doorways. Four color-coded floor markers indicate the search
zones, and a white marker with a red cross marks the base station at
the origin. Debris obstacles are scattered inside the rooms.

.. important::

   The floor markers are **visual-only** (no collision geometry).
   The robot does **not** use them for perception. They exist purely
   as a visual cue for you and the instructor to confirm the zone
   poses at a glance.


   .. only:: html

      .. figure:: /_static/images/final_project/final_project_world.png
         :alt: Simulation environment for the Final Project
         :width: 90%
         :align: center
         :class: only-light

         Simulation environment for the Final Project.

      .. figure:: /_static/images/final_project/final_project_world.png
         :alt: Simulation environment for the Final Project
         :width: 90%
         :align: center
         :class: only-dark

         Simulation environment for the Final Project.

You will use **Nav2** for autonomous navigation, which requires a
pre-built occupancy grid map. **Each group must build their own map**
of the final project world using ``slam_toolbox`` and save it with
``nav2_map_server``. No map is provided. The full map-building
procedure is documented in :ref:`final-project-build-the-map` under
:doc:`requirements`.


Build and Launch
----------------

Follow these steps from a terminal opened in ``~/enpm605_ws``.

**1. Pull the latest code.**

.. code-block:: console

   cd ~/enpm605_ws && git pull

**2. Install system dependencies.**

.. code-block:: console

   sudo apt update && rosdep install --from-paths src --ignore-src -y \
       --skip-keys "micro_ros_agent python3-ftdi"

**3. Build the full stack.**

.. code-block:: console

   colcon build --symlink-install \
       --cmake-args -DCMAKE_BUILD_TYPE=Release \
       --packages-up-to final_project_meta

.. important::

   **Edit** ``~/enpm605_ws/src/final_project_meta/package.xml``
   **before your first full build**:

   - Replace the three placeholder ``<maintainer>`` tags with your
     group members' names and UMD emails. If your group has 2
     members, delete the extra slot.
   - Uncomment the two ``<exec_depend>`` lines near the bottom,
     replacing ``N`` with your group number:

     .. code-block:: xml

        <exec_depend>groupN_final_interfaces</exec_depend>
        <exec_depend>groupN_final</exec_depend>

   Without the ``<exec_depend>`` edits, ``colcon build
   --packages-up-to final_project_meta`` will build the simulation
   stack but skip your own code.

**4. Source the workspace.**

.. code-block:: console

   source ~/enpm605_ws/install/setup.bash

**5. Launch the simulation.**

.. code-block:: console

   ros2 launch rosbot_gazebo final_project_world.launch.py

The rosbot starts at the origin ``(0, 0, 0)`` with yaw ``0``. You
should see the four color-coded zone markers (red, green, blue,
yellow) in the four rooms and a white base station marker with a
red cross at the center.

**6. Launch Nav2** (in a second terminal). Pass the path to the map
your group built and saved under ``group<N>_final/maps/``:

.. code-block:: console

   ros2 launch rosbot_gazebo navigation.launch.py \
       map:=/path/to/group<N>_final/maps/final_project_world.yaml

**7. Launch the search and rescue mission** (in a third terminal):

.. code-block:: console

   ros2 launch group<N>_final search_and_rescue.launch.py


How Detection Works
===================

This project uses **simulated detection** -- there is no camera or
computer vision involved. Survivor detection is implemented entirely
as a ROS 2 service call.

**The flow:**

1. The robot navigates to a search zone using Nav2.
2. Once the robot arrives, the ``DetectSurvivor`` BT action node
   calls the ``detect_survivor`` service, passing the current zone
   ID (e.g., ``"zone_a"``).
3. The ``DetectSurvivorServer`` (a separate node you write) maintains
   a **hardcoded dictionary** mapping zone IDs to survivor locations.
   If the zone has a survivor, it returns ``found=True`` with the
   survivor's ``(x, y)`` coordinates. Otherwise it returns
   ``found=False``.
4. If a survivor is found, the ``BroadcastSurvivorTF`` BT action
   uses ``tf2_ros.StaticTransformBroadcaster`` to publish a static
   TF frame (e.g., ``survivor_1``) at the reported coordinates,
   relative to the ``map`` frame.

.. note::

   The detection service is a simple dictionary lookup -- it does
   **not** check whether the robot is physically near the zone. A
   student could call the service manually from any location:

   .. code-block:: console

      ros2 service call /detect_survivor \
          group<N>_final_interfaces/srv/DetectSurvivor \
          "{zone_id: 'zone_a'}"

   and receive ``found=True`` regardless of the robot's position.
   This is intentional: the service is a simulation stand-in for a
   real perception system. **The behavior tree enforces the correct
   sequencing** -- the ``DetectSurvivor`` node is only ticked
   *after* ``NavigateToZone`` succeeds within the Patrol Sequence,
   so the robot must physically reach the zone before detection runs.


Zone Layout
===========

The four search zones and the base station are positioned as follows:

.. list-table::
   :widths: 15 15 15 20 35
   :header-rows: 1
   :class: compact-table

   * - Zone
     - X (m)
     - Y (m)
     - Color
     - Room
   * - ``zone_a``
     - -3.0
     - 3.0
     - Red
     - Northwest
   * - ``zone_b``
     - 3.5
     - 3.0
     - Green
     - Northeast
   * - ``zone_c``
     - 4.0
     - -3.0
     - Blue
     - Southeast
   * - ``zone_d``
     - -3.5
     - -3.0
     - Yellow
     - Southwest
   * - **Base**
     - 0.0
     - 0.0
     - White + red cross
     - Center (origin)

The simulated detection server should be configured so that
**zones A and C** contain survivors and **zones B and D** do not.
You are free to change the survivor locations, but your submitted
``DetectSurvivorServer`` must have **at least two** zones with
survivors.


Topics and Frames
=================

.. dropdown:: Topics You Will Use
   :open:

   .. list-table::
      :widths: 25 30 45
      :header-rows: 1
      :class: compact-table

      * - Direction
        - Topic / Type
        - Description
      * - **Action client**
        - ``navigate_to_pose`` (``nav2_msgs/NavigateToPose``)
        - Nav2 action for autonomous navigation to a goal pose.
      * - **Service client**
        - ``/detect_survivor`` (``DetectSurvivor``)
        - Simulated survivor detection at a zone.
      * - **Service client**
        - ``/report_survivor`` (``ReportSurvivor``)
        - Report a found survivor to the simulated command center.

.. dropdown:: TF Frames
   :open:

   .. list-table::
      :widths: 20 80
      :header-rows: 1
      :class: compact-table

      * - Frame
        - Description
      * - ``map``
        - The global fixed frame. All zone coordinates and survivor
          positions are expressed in this frame.
      * - ``odom``
        - The odometry frame, child of ``map`` (corrected by AMCL).
      * - ``base_link``
        - The robot's body frame.
      * - ``survivor_N``
        - Static frames broadcast by your BT when survivors are
          found. Each is a child of ``map``. Broadcast using
          ``tf2_ros.StaticTransformBroadcaster``.


Provided Reference Code
========================

The following packages from the lecture series are relevant
reference material. You will **not** submit or depend on them
directly.

.. dropdown:: Reference Files to Study
   :open:

   .. list-table::
      :widths: 45 55
      :header-rows: 1
      :class: compact-table

      * - File
        - What to learn from it
      * - ``lecture13/mapping_navigation_demo/mapping_navigation_demo/navigation_demo_interface.py``
        - **Primary Nav2 reference.** Shows how to use
          ``BasicNavigator`` from ``nav2_simple_commander`` to send
          ``NavigateToPose`` goals, handle feedback and results
          (``TaskResult.SUCCEEDED / CANCELED / FAILED``), and
          follow waypoints. Also demonstrates setting the initial
          pose using TF lookups and ``setInitialPose()``.
      * - ``lecture13/mapping_navigation_demo/mapping_navigation_demo/scripts/main_navigation_demo.py``
        - Entry point pattern: creating the node with a
          ``MultiThreadedExecutor``.
      * - ``lecture13/mapping_navigation_demo/launch/navigation.launch.py``
        - Launch file that starts Nav2 localization, navigation
          stack, RViz, and an optional demo node with
          ``IfCondition``. Shows how to pass parameters and
          launch arguments.
      * - ``lecture13/mapping_navigation_demo/config/nav2_params.yaml``
        - Nav2 parameter configuration. Note the
          ``enable_stamped_cmd_vel: True`` setting required for
          the ROSbot (the robot uses ``TwistStamped``, not
          ``Twist``).
      * - ``lecture12/bt_demo/bt_demo/drive_forward.py``
        - Custom BT action node pattern: ``setup(**kwargs)`` to
          get the ROS 2 node, ``update()`` returning
          ``Status.RUNNING/SUCCESS/FAILURE``, ``terminate()``
          for cleanup.
      * - ``lecture12/bt_demo/bt_demo/goal_not_reached.py``
        - Custom BT condition node pattern: subscribes to a topic
          in ``setup()``, returns ``SUCCESS`` or ``FAILURE`` in
          ``update()`` (never ``RUNNING``).
      * - ``lecture12/bt_demo/bt_demo/scripts/main_drive_to_goal.py``
        - Entry point that reads parameters, builds the BT,
          wraps it in ``py_trees_ros.trees.BehaviourTree``, and
          runs ``tick_tock()`` + ``rclpy.spin()``.
      * - ``lecture12/bt_demo/launch/drive_to_goal.py``
        - Launch file with ``DeclareLaunchArgument``,
          ``LaunchConfiguration``, parameter forwarding, and
          ``emulate_tty=True``.
      * - ``lecture10/custom_interfaces/``
        - Template for a CMake package that generates service
          interfaces via ``rosidl_generate_interfaces``.
      * - ``lecture10/parameters_demo/launch/demo3.launch.py``
        - Loading a YAML parameter file in a launch file using
          ``get_package_share_directory()`` and the
          ``parameters`` field.
      * - ``lecture11/frame_demo/``
        - TF2 frame broadcasting examples using
          ``tf2_ros.StaticTransformBroadcaster`` and
          ``TransformStamped`` messages.


Starter Packages
================

Your workspace contains two directories for this project:

- ``~/enpm605_ws/src/final_project/`` -- empty folder where you
  create your two packages (``group<N>_final_interfaces`` and
  ``group<N>_final``).
- ``~/enpm605_ws/src/final_project_meta/`` -- metapackage that you
  edit to register your packages (see above).

The metapackage already includes dependencies on ``py_trees``,
``py_trees_ros``, ``tf2_ros``, ``sensor_msgs``, ``geometry_msgs``,
``nav_msgs``, and ``nav2_simple_commander``.
