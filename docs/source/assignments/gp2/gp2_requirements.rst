====================================================
Requirements
====================================================

.. |rarr| unicode:: U+2192


Your Tasks
==========

At a high level, your group must complete the following tasks. Each
is spelled out in detail in the sections below.

1. **Create two ROS 2 packages** inside the pre-existing
   ``~/enpm605_ws/src/gp2/`` folder:

   a. ``group<N>_gp2_interfaces`` (CMake) containing the
      ``NavigateToGoal.action`` definition.
   b. ``group<N>_gp2`` (ament_python) containing the action server,
      the action client, the launch file, and the goals YAML.

2. **Register both packages** as ``<exec_depend>`` entries in
   ``~/enpm605_ws/src/gp2_meta/package.xml`` so that
   ``colcon build --packages-up-to gp2_meta`` picks them up.

3. **Define the** ``NavigateToGoal`` **action interface** (goal,
   result, feedback) in ``group<N>_gp2_interfaces`` exactly as
   specified.

4. **Implement the action server** (``navigate_to_goal_server``).
   Port the two-phase proportional controller from
   ``robot_control_demo/p_controller_demo.py`` into the
   ``execute_callback``. The server subscribes to
   ``/odometry/filtered``, publishes to ``/cmd_vel``, emits
   feedback during execution, and returns a result on success,
   cancel, or failure.

5. **Implement the action client** (``navigate_to_goal_client``).
   The client's job, in order, is:

   a. **Read the three goals** from ``config/goals.yaml`` (the
      named blocks ``goal1``, ``goal2``, ``goal3``, each with
      fields ``x``, ``y``, and ``final_heading``).
   b. **Validate** that all three goals were loaded successfully.
   c. **Wait** for the action server to become available.
   d. **Task the robot to go to each goal, sequentially**: send
      goal ``i``, wait for its result, log feedback and the
      outcome, and only then send goal ``i+1``. Never queue or
      dispatch in parallel.
   e. **Log a final summary** once all three goals have succeeded.

6. **Write the launch file** (``gp2.launch.py``) that starts the
   server and the client, loads ``goals.yaml`` into the client,
   and exposes ``goal_tolerance`` and ``yaw_tolerance`` as launch
   arguments forwarded to the server.

7. **Document contributions** in ``README.md`` (one short
   paragraph per group member summarizing what they worked on).

8. **Submit** by zipping the ``~/enpm605_ws/src/gp2/`` folder and
   uploading it to Canvas as ``group<N>_gp2.zip`` (see
   :doc:`submission` for the exact command).

The remainder of this page details each of these tasks.


Package Structure
=================

Your submission must contain **two** ROS 2 packages, both placed
inside the pre-existing ``~/enpm605_ws/src/gp2/`` folder. Replace
``<N>`` with your group number.

**Folder layout in the workspace:**

.. code-block:: text

   ~/enpm605_ws/src/gp2/
   |-- group<N>_gp2_interfaces/
   |-- group<N>_gp2/

You will zip and submit the ``gp2/`` folder itself (see
:doc:`submission`).

**Package 1. Action interface (CMake):**

.. code-block:: text

   group<N>_gp2_interfaces/
   |-- action/
   |   |-- NavigateToGoal.action
   |-- CMakeLists.txt
   |-- package.xml

**Package 2. Nodes and launch (ament_python):**

.. code-block:: text

   group<N>_gp2/
   |-- group<N>_gp2/
   |   |-- __init__.py
   |   |-- navigate_to_goal_server.py
   |   |-- navigate_to_goal_client.py
   |-- scripts/
   |   |-- __init__.py
   |   |-- main_navigate_to_goal_server.py
   |   |-- main_navigate_to_goal_client.py
   |-- launch/
   |   |-- gp2.launch.py
   |-- config/
   |   |-- goals.yaml
   |-- resource/
   |   |-- group<N>_gp2
   |-- test/
   |-- package.xml
   |-- setup.py
   |-- setup.cfg
   |-- README.md

**Package metadata:** both ``package.xml`` files and the
``setup.py`` must include a meaningful description, a license
(e.g., ``Apache-2.0``), and all group members listed as
maintainers with their email addresses.

**Update the** ``gp2_meta`` **metapackage** at
``~/enpm605_ws/src/gp2_meta/package.xml``. Two edits are required:

1. **Replace the three placeholder** ``<maintainer>`` **tags** with
   your group members. The file ships with three maintainer slots
   (to accommodate groups of 2 or 3). Fill them with your real
   names and UMD emails, and **delete any extra slots** your group
   does not need.

   .. code-block:: xml

      <!-- For a group of 2, delete the third line. -->
      <maintainer email="alice@umd.edu">Alice Smith</maintainer>
      <maintainer email="bob@umd.edu">Bob Jones</maintainer>
      <maintainer email="carol@umd.edu">Carol Lee</maintainer>

2. **Uncomment the two** ``<exec_depend>`` **lines** near the
   bottom of the file, replacing ``<N>`` with your group number:

   .. code-block:: xml

      <exec_depend>group<N>_gp2_interfaces</exec_depend>
      <exec_depend>group<N>_gp2</exec_depend>

Together these edits let ``colcon build --packages-up-to gp2_meta``
pick up your packages, and make ``gp2_meta`` a valid package
attributed to your group.


Action Interface
================

Define the custom action at
``group<N>_gp2_interfaces/action/NavigateToGoal.action`` exactly as
follows:

.. code-block:: text

   # Goal
   geometry_msgs/Point goal_position
   float64 final_heading
   ---
   # Result
   bool success
   float64 total_distance
   float64 elapsed_time
   ---
   # Feedback
   geometry_msgs/Pose current_pose
   float64 distance_remaining

**Semantics:**

- ``goal_position.x`` / ``goal_position.y`` are the target position
  in the ``odom`` frame (meters). ``goal_position.z`` is ignored.
- ``final_heading`` is the desired yaw at the goal (radians).
- ``success`` is ``True`` if both position and orientation
  tolerances are satisfied, ``False`` on cancellation or abort.
- ``total_distance`` is the cumulative path length traveled during
  execution (meters).
- ``elapsed_time`` is the wall-clock duration of the goal (seconds).
- ``distance_remaining`` is the straight-line distance from the
  current pose to the goal position (meters).

**CMake/package configuration** (follow the template in
``lecture10/custom_interfaces``):

- ``CMakeLists.txt`` must call ``rosidl_generate_interfaces`` on
  ``action/NavigateToGoal.action`` and depend on ``geometry_msgs``.
- ``package.xml`` must include the
  ``<buildtool_depend>rosidl_default_generators</buildtool_depend>``,
  ``<exec_depend>rosidl_default_runtime</exec_depend>``,
  ``<member_of_group>rosidl_interface_packages</member_of_group>``,
  and ``<depend>geometry_msgs</depend>`` entries.


Action Server
=============

Implement a node called ``navigate_to_goal_server`` that exposes an
``ActionServer`` on the action name ``navigate_to_goal`` using the
``NavigateToGoal`` interface. **The server itself drives the
robot.** Do not delegate to any other controller node.

**The execute callback must:**

1. **Accept** a goal in ``goal_callback`` only if the goal position
   is reachable (e.g., accept all for this assignment, or reject on
   obviously invalid inputs such as NaNs). Log the decision.

2. **Subscribe** to ``/odometry/filtered`` and maintain the current
   ``(x, y, yaw)`` as internal state, independent of the action
   lifecycle.

3. **Publish** to ``/cmd_vel`` (``geometry_msgs/TwistStamped``)
   inside a 20 Hz control loop (driven by the execute callback or
   by a timer that runs during execution).

4. **Implement the two-phase P-controller** (phase 1 = position,
   phase 2 = orientation) ported from
   ``robot_control_demo/p_controller_demo.py``. Use the gains and
   tolerances as parameters (see below).

5. **Publish feedback** at a regular rate (no faster than 5 Hz, no
   slower than 1 Hz) containing:

   - ``current_pose`` (the latest pose from odometry),
   - ``distance_remaining`` (``sqrt(dx^2 + dy^2)`` to the goal
     position).

6. **Check for cancellation** each control iteration. On
   cancellation, send a zero-velocity stop command, call
   ``goal_handle.canceled()``, and return a result with
   ``success=False`` populated with the partial totals.

7. **Succeed** when both position and orientation tolerances are
   satisfied: send a zero-velocity stop command, call
   ``goal_handle.succeed()``, and return a result with
   ``success=True`` and the final ``total_distance`` /
   ``elapsed_time``.

**Server parameters** (declared in ``__init__``):

.. list-table::
   :widths: 25 15 60
   :header-rows: 1
   :class: compact-table

   * - Parameter
     - Default
     - Description
   * - ``k_rho``
     - 0.4
     - Proportional gain on distance (linear velocity).
   * - ``k_alpha``
     - 0.8
     - Proportional gain on heading error (phase 1).
   * - ``k_yaw``
     - 0.8
     - Proportional gain on yaw error (phase 2).
   * - ``goal_tolerance``
     - 0.10
     - Position tolerance (meters).
   * - ``yaw_tolerance``
     - 0.05
     - Yaw tolerance (radians).

**Subscriptions and publications:**

.. list-table::
   :widths: 25 30 45
   :header-rows: 1
   :class: compact-table

   * - Direction
     - Topic / Type
     - Description
   * - **Subscribes**
     - ``/odometry/filtered`` (``nav_msgs/Odometry``)
     - Robot pose feedback.
   * - **Publishes**
     - ``/cmd_vel`` (``geometry_msgs/TwistStamped``)
     - Velocity commands.
   * - **Action server**
     - ``navigate_to_goal`` (``group<N>_gp2_interfaces/NavigateToGoal``)
     - Receives goals, publishes feedback, returns the result.


Action Client
=============

Implement a node called ``navigate_to_goal_client`` that owns an
``ActionClient`` on ``navigate_to_goal`` and **sends three goals
sequentially**.

**The client must:**

1. **Declare and read** the three goals from the YAML file (see
   :doc:`gp2_infrastructure`). Each goal is a named block
   (``goal1``, ``goal2``, ``goal3``) with three fields
   (``x``, ``y``, ``final_heading``), so the client declares nine
   parameters in total using dot-namespaced names such as
   ``goal1.x`` and ``goal1.final_heading``. Validate that all three
   goals were loaded successfully and log them at startup.

2. **Wait** for the action server to become available using
   ``self._action_client.wait_for_server()``.

3. **Send goals one at a time.** The client sends goal ``i+1``
   **only after** the result for goal ``i`` has been received
   (i.e., never sends in parallel and never queues ahead).

4. **Log each feedback message** at ``info`` level with the current
   pose and distance remaining, throttled to at most once per
   second (``throttle_duration_sec=1.0``).

5. **Log each result** with ``success``, ``total_distance``, and
   ``elapsed_time``. If the result is ``success=False``, abort the
   sequence: log an error and **do not** send the remaining goals.

6. When all three goals have completed successfully, log a
   **mission-complete summary** that lists each goal and its
   ``total_distance`` / ``elapsed_time``.

**Client parameters** (loaded from ``config/goals.yaml``):

.. list-table::
   :widths: 25 15 60
   :header-rows: 1
   :class: compact-table

   * - Parameter
     - Type
     - Description
   * - ``goalN.x``
     - ``double``
     - X coordinate of goal ``N`` in the odom frame (meters),
       for ``N`` in ``{1, 2, 3}``.
   * - ``goalN.y``
     - ``double``
     - Y coordinate of goal ``N`` in the odom frame (meters).
   * - ``goalN.final_heading``
     - ``double``
     - Desired yaw at goal ``N`` (radians).


Launch File
===========

Write a Python launch file at ``launch/gp2.launch.py`` that starts
**both** your nodes and loads the parameter file.

**Required nodes:**

.. list-table::
   :widths: 30 30 40
   :header-rows: 1
   :class: compact-table

   * - Executable
     - Package
     - Notes
   * - ``navigate_to_goal_server``
     - ``group<N>_gp2``
     - Controller gains and tolerances come from launch arguments.
   * - ``navigate_to_goal_client``
     - ``group<N>_gp2``
     - Loads ``config/goals.yaml`` via the ``parameters`` field.

**Launch file requirements:**

1. Both nodes must use ``output="screen"`` and ``emulate_tty=True``.
2. Load ``config/goals.yaml`` for the **client** node using
   ``get_package_share_directory()`` and the ``parameters`` field.
3. Declare at least **two** launch arguments:

   - ``goal_tolerance`` (default ``0.10``), passed to the server.
   - ``yaw_tolerance`` (default ``0.05``), passed to the server.

4. The simulation launch
   (``ros2 launch rosbot_gazebo gp2_world.launch.py``) is **not**
   included in your launch file; the user starts it in a separate
   terminal.

**What your launch file should do, in order:**

1. Resolve the path to ``config/goals.yaml`` inside the installed
   share directory of ``group<N>_gp2`` (so it is found at runtime
   regardless of where the user launched from).
2. Declare the two launch arguments ``goal_tolerance`` and
   ``yaw_tolerance`` with their default values and short
   descriptions.
3. Build a ``Node`` action for the action server, forwarding the
   two launch arguments into its ``parameters``.
4. Build a ``Node`` action for the action client, passing the
   resolved ``goals.yaml`` path into its ``parameters``.
5. Assemble a ``LaunchDescription`` that registers the two launch
   arguments and both ``Node`` actions, and return it from
   ``generate_launch_description()``.

Lecture 8 and Lecture 10 launch files (e.g.,
``parameters_demo/launch/demo3.launch.py``) show each of these
pieces in isolation; use them as reference material rather than
as copy-paste templates.


README.md
=========

Your ``README.md`` must contain a single section describing **each
group member's contributions** to the project. For every member,
list their name and a short (2 to 4 sentence) summary of what they
personally wrote, debugged, tested, or documented.

No other sections are required. Do **not** include system
architecture diagrams, design write-ups, or build instructions in
the README; keep it focused on who did what.


Code Quality
============

.. warning::

   The following are mandatory and will result in point deductions
   if missing.

- **Docstrings:** Every class and every method must have a
  Google-style docstring.
- **Type hints:** All method parameters and return types must have
  type annotations.
- **Inline comments:** Include comments that explain non-obvious
  logic (e.g., quaternion conversion, two-phase transition,
  cancellation handling).
- **Naming conventions:** ``snake_case`` for topics, services,
  actions, methods, and variables. ``CamelCase`` for class names.
- **Logging:** Use the ROS 2 logger exclusively. Never use
  ``print()``. Use the appropriate severity level: ``info()`` for
  normal operation, ``warn()`` for recoverable issues, ``error()``
  for failures.
- **Linting:** Ensure Ruff is enabled and no errors appear.
