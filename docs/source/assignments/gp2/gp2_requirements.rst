====================================================
Requirements
====================================================

.. |rarr| unicode:: U+2192


.. dropdown:: Package Structure
   :open:

   Your submission must contain **one** ROS 2 Python package. Replace
   ``<N>`` with your group number.

   .. code-block:: text

      group<N>_gp2/
      |-- group<N>_gp2/
      |   |-- __init__.py
      |   |-- marker_navigator.py
      |-- scripts/
      |   |-- __init__.py
      |   |-- main_marker_navigator.py
      |-- launch/
      |   |-- gp2.launch.py
      |-- config/
      |   |-- waypoints.yaml
      |-- resource/
      |   |-- group<N>_gp2
      |-- test/
      |-- package.xml
      |-- setup.py
      |-- setup.cfg
      |-- README.md

   **Package metadata:** ``package.xml`` and ``setup.py`` must include a
   meaningful description, a license (e.g., ``Apache-2.0``), and both
   group members listed as maintainers with their email addresses.


.. dropdown:: Navigator Node (``marker_navigator``)
   :open:

   Implement a node called ``marker_navigator`` that autonomously
   executes the following sequence:

   1. **Read waypoints** from parameters (``waypoint_x``, ``waypoint_y``,
      ``waypoint_yaw``). Validate that all three arrays have equal length.
      Log the number of waypoints loaded.

   2. **For each waypoint** (sequentially):

      a. Convert the waypoint ``(x, y, yaw)`` to a ``PoseStamped``
         message (yaw must be encoded as a quaternion in the orientation
         field).
      b. Publish the ``PoseStamped`` to ``/goal_pose``.
      c. Wait for ``Bool(data=True)`` on ``/goal_reached``.
      d. Once at the waypoint, **wait briefly** (1--2 seconds) for the
         ArUco detector to stabilize its TF broadcast.
      e. **Detect which marker is visible**: query the ``/tf`` topic or
         attempt ``lookup_transform`` for candidate marker IDs. The
         detector logs which markers it sees -- your node must
         determine the correct ``aruco_marker_<id>`` frame
         dynamically.
      f. Use ``tf_buffer.lookup_transform("odom", "aruco_marker_<id>",
         ...)`` to get the marker's position in the ``odom`` frame.
      g. **Store** the marker's ``(x, y)`` position.
      h. **Log** the marker ID and its ``odom``-frame position.

   3. **Compute the centroid** of the three detected marker positions:

      .. math::

         x_c = \frac{x_1 + x_2 + x_3}{3}, \quad
         y_c = \frac{y_1 + y_2 + y_3}{3}

   4. **Log** the centroid coordinates.

   5. **Navigate to the centroid** by publishing a final ``PoseStamped``
      to ``/goal_pose`` (orientation can be ``yaw=0``).

   6. Once the robot reaches the centroid, **log** a completion message
      with a summary: the three marker IDs, their positions, and the
      centroid.

   **Subscriptions and publications:**

   .. list-table::
      :widths: 25 30 45
      :header-rows: 1
      :class: compact-table

      * - Direction
        - Topic / Type
        - Description
      * - **Publishes**
        - ``/goal_pose`` (``PoseStamped``)
        - Goal commands for the proportional controller.
      * - **Subscribes**
        - ``/goal_reached`` (``Bool``)
        - Completion signal from the proportional controller.
      * - **TF2**
        - ``Buffer`` + ``TransformListener``
        - Used to look up ``aruco_marker_<id>`` in the ``odom`` frame.

   **Required parameters** (loaded from ``config/waypoints.yaml``):

   .. list-table::
      :widths: 25 15 60
      :header-rows: 1
      :class: compact-table

      * - Parameter
        - Type
        - Description
      * - ``waypoint_x``
        - ``double[]``
        - X coordinates of the viewing waypoints.
      * - ``waypoint_y``
        - ``double[]``
        - Y coordinates of the viewing waypoints.
      * - ``waypoint_yaw``
        - ``double[]``
        - Yaw orientations at each waypoint (radians).

   **Error handling:**

   - If a TF lookup fails (timeout, frame not found), log a warning and
     **retry up to 3 times** with a 1-second delay between attempts.
   - If a marker cannot be detected after all retries at a waypoint, log
     an error and continue to the next waypoint. Compute the centroid
     using only the markers that were successfully detected.


.. dropdown:: Launch File (``gp2.launch.py``)
   :open:

   Write a launch file that starts **all three nodes** and loads the
   parameter file.

   **Required nodes:**

   .. list-table::
      :widths: 25 25 50
      :header-rows: 1
      :class: compact-table

      * - Executable
        - Package
        - Notes
      * - ``p_controller``
        - ``robot_control_demo``
        - No parameters needed (uses defaults; goals come via topic).
      * - ``aruco_detector``
        - ``frame_demo``
        - No parameters needed (defaults target the rosbot_xl OAK-D camera).
      * - ``marker_navigator``
        - ``group<N>_gp2``
        - Load ``config/waypoints.yaml`` using the ``parameters`` field.

   **Launch file requirements:**

   1. All nodes must use ``output="screen"`` and ``emulate_tty=True``.
   2. Load ``config/waypoints.yaml`` for the ``marker_navigator`` node
      using ``get_package_share_directory()`` and the ``parameters``
      field.
   3. Declare at least **two** launch arguments:

      - ``goal_tolerance`` (default ``0.10``) -- passed to the
        ``p_controller`` node.
      - ``yaw_tolerance`` (default ``0.05``) -- passed to the
        ``p_controller`` node.

   4. Group the **infrastructure nodes** (``p_controller`` and
      ``aruco_detector``) in a ``GroupAction``.

   **Example launch file skeleton:**

   .. code-block:: python

      from launch import LaunchDescription
      from launch_ros.actions import Node
      from launch.actions import DeclareLaunchArgument, GroupAction
      from launch.substitutions import LaunchConfiguration
      from ament_index_python.packages import get_package_share_directory
      import os


      def generate_launch_description():
          # Get the path to the waypoints config
          pkg_dir = get_package_share_directory("group<N>_gp2")
          waypoints_file = os.path.join(pkg_dir, "config", "waypoints.yaml")

          # Launch arguments
          goal_tolerance_arg = DeclareLaunchArgument(
              "goal_tolerance", default_value="0.10",
              description="Position tolerance for the P-controller (meters)",
          )
          yaw_tolerance_arg = DeclareLaunchArgument(
              "yaw_tolerance", default_value="0.05",
              description="Yaw tolerance for the P-controller (radians)",
          )

          # Infrastructure nodes (grouped)
          infrastructure = GroupAction([
              Node(
                  package="robot_control_demo",
                  executable="p_controller",
                  output="screen",
                  emulate_tty=True,
                  parameters=[{
                      "goal_tolerance": LaunchConfiguration("goal_tolerance"),
                      "yaw_tolerance": LaunchConfiguration("yaw_tolerance"),
                  }],
              ),
              Node(
                  package="frame_demo",
                  executable="aruco_detector",
                  output="screen",
                  emulate_tty=True,
              ),
          ])

          # Student's navigator node
          navigator = Node(
              package="group<N>_gp2",
              executable="marker_navigator",
              output="screen",
              emulate_tty=True,
              parameters=[waypoints_file],
          )

          ld = LaunchDescription()
          ld.add_action(goal_tolerance_arg)
          ld.add_action(yaw_tolerance_arg)
          ld.add_action(infrastructure)
          ld.add_action(navigator)
          return ld


.. dropdown:: README.md Requirements
   :open:

   Your ``README.md`` must include:

   1. **Group members**: names and UIDs.
   2. **Contributions**: a brief description of each team member's
      contributions.
   3. **System architecture**: a text or diagram showing all three nodes,
      topics (``/goal_pose``, ``/goal_reached``, ``/cmd_vel``), TF frames,
      and how they interact. You may use
      `Mermaid <https://mermaid.js.org/>`_ or a screenshot of
      ``rqt_graph``.
   4. **TF tree**: include the output of ``ros2 run tf2_tools
      view_frames`` (the generated ``frames.pdf``) and annotate which
      frames your node uses for lookups.
   5. **Design decisions**: explain how you detect which marker ID is
      visible at each waypoint, how you handle detection failures, and
      any timing/sequencing choices you made.
   6. **Build and run instructions**: exact commands to build, source,
      launch the simulation, and launch your system.
   7. **Known issues**: any limitations or incomplete features.


.. dropdown:: Code Quality Requirements
   :open:

   .. warning::

      The following are mandatory and will result in point deductions if
      missing.

   - **Docstrings:** Every class and every method must have a
     Google-style docstring.
   - **Type hints:** All method parameters and return types must have
     type annotations.
   - **Inline comments:** Include comments that explain non-obvious logic
     (e.g., TF lookup strategy, quaternion conversion, centroid
     computation).
   - **Naming conventions:** ``snake_case`` for topics, services,
     methods, and variables. ``CamelCase`` for class names.
   - **Logging:** Use the ROS 2 logger exclusively -- never ``print()``.
     Use the appropriate severity level: ``info()`` for normal
     operation, ``warn()`` for retries or recoverable issues,
     ``error()`` for failures.
   - **Linting:** Ensure Ruff is enabled and no errors appear.
