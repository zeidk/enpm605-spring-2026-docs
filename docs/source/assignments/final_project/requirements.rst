====================================================
Requirements
====================================================


Your Tasks
==========

At a high level, your group must complete the following tasks. Each
is spelled out in detail in the sections below.

1. **Create two ROS 2 packages** inside the pre-existing
   ``~/enpm605_ws/src/final_project/`` folder:

   a. ``group<N>_final_interfaces`` (CMake) containing the
      ``DetectSurvivor.srv`` and ``ReportSurvivor.srv`` definitions.
   b. ``group<N>_final`` (ament_python) containing the behavior tree
      nodes, service servers, the entry point script, the launch
      file, and the parameter YAML.

2. **Register both packages** as ``<exec_depend>`` entries in
   ``~/enpm605_ws/src/final_project_meta/package.xml`` so that
   ``colcon build --packages-up-to final_project_meta`` picks them up.

3. **Define two custom service interfaces** (``DetectSurvivor.srv``
   and ``ReportSurvivor.srv``) in ``group<N>_final_interfaces``.

4. **Implement two simulated service servers** that respond to
   detection and report requests.

5. **Implement a shared** ``ZoneManager`` **class** (plain Python,
   not a BT node) that manages the list of search zones and tracks
   mission state.

6. **Implement 12 behavior tree leaf nodes** (3 conditions + 9
   actions) using ``py_trees.behaviour.Behaviour``.

7. **Assemble the full behavior tree** in an entry point script that
   reads parameters, builds the tree, and runs it with
   ``py_trees_ros.trees.BehaviourTree``.

8. **Write the launch file** that starts Nav2, the service servers,
   and the behavior tree node, loading all parameters from YAML.

9. **Document contributions** in ``README.md``.

10. **Submit** by zipping the ``~/enpm605_ws/src/final_project/``
    folder and uploading it to Canvas.


Package Structure
=================

Your submission must contain **two** ROS 2 packages, both placed
inside the pre-existing ``~/enpm605_ws/src/final_project/`` folder.

**Package 1. Service interfaces (CMake):**

.. code-block:: text

   group<N>_final_interfaces/
   |-- srv/
   |   |-- DetectSurvivor.srv
   |   |-- ReportSurvivor.srv
   |-- CMakeLists.txt
   |-- package.xml

**Package 2. Nodes, BT, and launch (ament_python):**

.. code-block:: text

   group<N>_final/
   |-- group<N>_final/
   |   |-- __init__.py
   |   |-- zone_manager.py
   |   |-- bt_nodes/
   |   |   |-- __init__.py
   |   |   |-- conditions.py
   |   |   |-- actions.py
   |   |-- service_servers/
   |   |   |-- __init__.py
   |   |   |-- detect_survivor_server.py
   |   |   |-- report_survivor_server.py
   |   |-- scripts/
   |       |-- __init__.py
   |       |-- main_search_and_rescue.py
   |-- launch/
   |   |-- search_and_rescue.launch.py
   |-- config/
   |   |-- mission_params.yaml
   |-- resource/
   |   |-- group<N>_final
   |-- test/
   |-- package.xml
   |-- setup.py
   |-- setup.cfg
   |-- README.md


Service Interfaces
==================

Define two custom services in
``group<N>_final_interfaces/srv/``.

**DetectSurvivor.srv:**

.. code-block:: text

   # Request
   string zone_id
   ---
   # Response
   bool found
   float64 survivor_x
   float64 survivor_y

**ReportSurvivor.srv:**

.. code-block:: text

   # Request
   string survivor_id
   geometry_msgs/PointStamped location
   ---
   # Response
   bool acknowledged

**CMake/package configuration** (follow the template in
``lecture10/custom_interfaces``):

- ``CMakeLists.txt`` must call ``rosidl_generate_interfaces`` on
  both ``.srv`` files and depend on ``geometry_msgs``.
- ``package.xml`` must include
  ``rosidl_default_generators``,
  ``rosidl_default_runtime``,
  ``rosidl_interface_packages``, and
  ``geometry_msgs`` entries.


Simulated Service Servers
=========================

Implement two standalone ROS 2 nodes that act as simulated service
servers. These simulate a perception system and a command center.

.. important::

   There is **no camera or computer vision** in this project.
   Detection is entirely simulated via a service call. The
   ``DetectSurvivorServer`` performs a simple dictionary lookup on
   the zone ID string -- it does **not** check whether the robot is
   physically near the zone. The **behavior tree enforces the
   correct sequencing**: the ``DetectSurvivor`` BT action node is
   only ticked after ``NavigateToZone`` succeeds within the Patrol
   Sequence, so the robot must reach the zone before detection runs.
   See :doc:`infrastructure` for a full explanation.

**DetectSurvivorServer** (``detect_survivor_server.py``):

- Advertises a service on ``detect_survivor`` using the
  ``DetectSurvivor`` interface.
- Maintains a hardcoded dictionary mapping zone IDs to survivor
  locations. For example:

  .. code-block:: python

     SURVIVORS = {
         "zone_a": (2.5, 3.2),
         "zone_c": (7.1, 4.5),
     }

- When called, if the ``zone_id`` is in the dictionary, returns
  ``found=True`` with the survivor's ``(x, y)`` coordinates.
  Otherwise returns ``found=False``.
- Logs each detection request and result.

**ReportSurvivorServer** (``report_survivor_server.py``):

- Advertises a service on ``report_survivor`` using the
  ``ReportSurvivor`` interface.
- When called, logs the ``survivor_id`` and ``location``, and
  returns ``acknowledged=True``.
- This simulates a command center acknowledging the report.


ZoneManager
===========

Implement a plain Python class (not a BT node) at
``zone_manager.py`` that manages the mission state. All BT nodes
that need zone information receive a reference to the same
``ZoneManager`` instance via their constructor.

**Required interface:**

.. code-block:: python

   class ZoneManager:
       def __init__(self, zones: list[dict], base_station: dict):
           """Initialize with zone list and base station pose."""
           ...

       def current_zone(self) -> dict:
           """Return the current zone dict (id, x, y, yaw)."""
           ...

       def has_remaining(self) -> bool:
           """True if there are unvisited zones."""
           ...

       def advance(self) -> None:
           """Move to the next zone."""
           ...

       def skip(self) -> None:
           """Skip the current zone and move to the next."""
           ...

       def base_pose(self) -> dict:
           """Return the base station pose dict (x, y, yaw)."""
           ...

       def next_survivor_id(self) -> str:
           """Return a unique ID like 'survivor_1', 'survivor_2', etc."""
           ...


Behavior Tree
=============

The full behavior tree must be assembled in
``scripts/main_search_and_rescue.py``. The tree structure is as
follows:

.. code-block:: text

   Root Sequence (memory=False)
   |-- CheckBattery?                          [condition]
   |-- Selector (Mission or ReturnToBase)
   |   |-- Sequence (Patrol, memory=True)
   |   |   |-- ZonesRemaining?               [condition]
   |   |   |-- Selector (NavigateWithRecovery, memory=True)
   |   |   |   |-- Timeout
   |   |   |   |   |-- NavigateToZone         [action - Nav2]
   |   |   |   |-- Sequence (Recovery)
   |   |   |   |   |-- Wait                   [action - pause]
   |   |   |   |   |-- Timeout
   |   |   |   |       |-- NavigateToZone     [action - Nav2 retry]
   |   |   |   |-- SkipZone                   [action]
   |   |   |-- DetectSurvivor                 [action - service call]
   |   |   |-- Selector (HandleDetection)
   |   |   |   |-- Sequence (SurvivorFound)
   |   |   |   |   |-- IsSurvivorDetected?    [condition]
   |   |   |   |   |-- BroadcastSurvivorTF    [action - TF]
   |   |   |   |   |-- NotifyBase             [action - service call]
   |   |   |   |-- LogNoDetection             [action]
   |   |   |-- AdvanceZone                    [action]
   |   |-- NavigateToBase                     [action - Nav2]
   |-- NavigateToBase                         [action - Nav2, battery low]

**How the tree works, tick by tick:**

1. The root **Sequence** (``memory=False``) first ticks
   ``CheckBattery?``. If the battery is low (FAILURE), the Sequence
   skips to the final child: ``NavigateToBase`` (battery low return).

2. If battery is OK (SUCCESS), the **Selector** (Mission or
   ReturnToBase) tries the **Patrol Sequence** first.

3. The Patrol Sequence (``memory=True``) checks
   ``ZonesRemaining?``. If all zones are visited (FAILURE), the
   Selector falls back to ``NavigateToBase`` (mission complete).

4. If zones remain (SUCCESS), the **NavigateWithRecovery Selector**
   (``memory=True``) attempts navigation:

   - First child: ``NavigateToZone`` wrapped in a ``Timeout``.
   - If timeout expires (FAILURE), try the **Recovery Sequence**:
     ``Wait`` (pause), then retry ``NavigateToZone`` with a second
     ``Timeout``.
   - If the retry also fails, ``SkipZone`` is ticked (always
     SUCCESS), which logs a warning and advances past the zone.

5. After reaching a zone, ``DetectSurvivor`` calls the detection
   service and stores the result internally.

6. The **HandleDetection Selector** checks ``IsSurvivorDetected?``:

   - If found (SUCCESS): ``BroadcastSurvivorTF`` publishes a static
     TF frame, then ``NotifyBase`` calls the report service.
   - If not found (FAILURE): ``LogNoDetection`` logs a message and
     returns SUCCESS so the Selector succeeds.

7. ``AdvanceZone`` moves to the next zone, and the Patrol Sequence
   repeats on the next tick.


Condition Nodes
---------------

All condition nodes must inherit from
``py_trees.behaviour.Behaviour`` and return only ``SUCCESS`` or
``FAILURE`` (never ``RUNNING``).

.. list-table::
   :widths: 25 25 50
   :header-rows: 1
   :class: compact-table

   * - Node
     - Constructor args
     - Behavior
   * - ``CheckBattery``
     - ``name``, ``battery_threshold``
     - Subscribes to ``/battery_state``
       (``sensor_msgs/BatteryState``) in ``setup()``. Returns
       SUCCESS if ``percentage > battery_threshold``, FAILURE
       otherwise.
   * - ``ZonesRemaining``
     - ``name``, ``zone_manager``
     - Returns SUCCESS if ``zone_manager.has_remaining()`` is True,
       FAILURE otherwise.
   * - ``IsSurvivorDetected``
     - ``name``, ``detect_node``
     - Holds a reference to the ``DetectSurvivor`` action node.
       Returns SUCCESS if ``detect_node.was_found()`` is True,
       FAILURE otherwise.


Action Nodes
------------

All action nodes must inherit from
``py_trees.behaviour.Behaviour``. Each creates its ROS 2 resources
(publishers, subscribers, service clients, action clients) in
``setup(**kwargs)`` using ``kwargs['node']``.

.. list-table::
   :widths: 22 22 56
   :header-rows: 1
   :class: compact-table

   * - Node
     - Constructor args
     - Behavior
   * - ``NavigateToZone``
     - ``name``, ``zone_manager``
     - Sends a ``NavigateToPose`` goal to Nav2 for the current zone
       from ``zone_manager``. Uses ``ActionClient`` from
       ``rclpy.action`` (see
       ``lecture13/mapping_navigation_demo/navigation_demo_interface.py``
       for the ``BasicNavigator`` pattern, but here you use
       the raw action client inside a BT node). Returns RUNNING
       while navigating, SUCCESS when Nav2 reports success,
       FAILURE if Nav2 fails. Cancels the goal on ``terminate()``.
   * - ``NavigateToBase``
     - ``name``, ``zone_manager``
     - Same as ``NavigateToZone`` but uses
       ``zone_manager.base_pose()`` as the target.
   * - ``Wait``
     - ``name``, ``duration``
     - Returns RUNNING for ``duration`` seconds, then SUCCESS.
       Provides a pause before retrying navigation.
   * - ``DetectSurvivor``
     - ``name``, ``zone_manager``
     - Calls the ``detect_survivor`` service with the current zone
       ID. Stores the result internally. Exposes
       ``was_found()`` and ``survivor_pose()`` methods. Returns
       SUCCESS when the service call completes (regardless of
       whether a survivor was found).
   * - ``IsSurvivorDetected``
     - (listed above as condition)
     -
   * - ``BroadcastSurvivorTF``
     - ``name``, ``detect_node``, ``zone_manager``
     - Creates a ``tf2_ros.StaticTransformBroadcaster`` in
       ``setup()`` using ``kwargs['node']``. In ``update()``, builds
       a ``geometry_msgs/TransformStamped`` with
       ``header.frame_id = "map"``,
       ``child_frame_id = "survivor_N"`` (from
       ``zone_manager.next_survivor_id()``), and translation from
       ``detect_node.survivor_pose()``. Publishes the static
       transform and returns SUCCESS. Verify with
       ``ros2 run tf2_ros tf2_echo map survivor_1``.
   * - ``NotifyBase``
     - ``name``, ``detect_node``
     - Calls the ``report_survivor`` service with the survivor ID
       and location from ``detect_node``. Returns SUCCESS if
       acknowledged, FAILURE otherwise.
   * - ``SkipZone``
     - ``name``, ``zone_manager``
     - Logs a warning that the current zone is being skipped. Calls
       ``zone_manager.skip()``. Returns SUCCESS.
   * - ``AdvanceZone``
     - ``name``, ``zone_manager``
     - Calls ``zone_manager.advance()``. Returns SUCCESS.
   * - ``LogNoDetection``
     - ``name``
     - Logs an info message that no survivor was found at the
       current zone. Returns SUCCESS.


Battery Simulation
------------------

The battery is simulated by a simple publisher node (provided or
written by the student) that publishes
``sensor_msgs/BatteryState`` on ``/battery_state`` at 1 Hz. The
``percentage`` field starts at ``100.0`` and decreases by a
configurable rate per second (e.g., ``0.5`` per second). The
``CheckBattery`` condition reads this topic.

.. note::

   You must write a simple ``battery_simulator`` node that publishes
   ``BatteryState`` messages. This node is started by your launch
   file.


Decorators
----------

Two ``py_trees.decorators.Timeout`` decorators are used:

1. **Primary navigation timeout**: wraps the first
   ``NavigateToZone``. If Nav2 does not reach the zone within the
   configured timeout, returns FAILURE.
2. **Retry navigation timeout**: wraps the second
   ``NavigateToZone`` (inside the Recovery Sequence). Same timeout
   duration.

The timeout duration is loaded from the parameter file.


Launch File
===========

Write a Python launch file at
``launch/search_and_rescue.launch.py`` that starts all required
nodes and loads the parameter file.

**Required nodes:**

.. list-table::
   :widths: 30 30 40
   :header-rows: 1
   :class: compact-table

   * - Executable
     - Package
     - Notes
   * - ``search_and_rescue_exe``
     - ``group<N>_final``
     - The behavior tree entry point.
   * - ``detect_survivor_server_exe``
     - ``group<N>_final``
     - Simulated detection service server.
   * - ``report_survivor_server_exe``
     - ``group<N>_final``
     - Simulated report service server.
   * - ``battery_simulator_exe``
     - ``group<N>_final``
     - Simulated battery publisher.

**Launch file requirements:**

1. All nodes must use ``output="screen"`` and ``emulate_tty=True``.
2. Load ``config/mission_params.yaml`` for the behavior tree node
   using ``get_package_share_directory()`` and the ``parameters``
   field.
3. Declare at least the following launch arguments:

   - ``battery_threshold`` (default ``20.0``)
   - ``navigation_timeout`` (default ``30.0``)

4. The simulation (Gazebo + Nav2) is started **separately** by the
   user in two terminals before launching the mission:

   .. code-block:: console

      ros2 launch rosbot_gazebo final_project_world.launch.py
      ros2 launch rosbot_gazebo navigation.launch.py map:=/path/to/map.yaml

   Your launch file does **not** include these.


Parameter File
==============

Create ``config/mission_params.yaml`` with the following structure:

.. code-block:: yaml

   /**:
     ros__parameters:
       zones:
         - {id: "zone_a", x: -3.0, y: 3.0, yaw: 0.0}
         - {id: "zone_b", x: 3.5, y: 3.0, yaw: 1.57}
         - {id: "zone_c", x: 4.0, y: -3.0, yaw: 3.14}
         - {id: "zone_d", x: -3.5, y: -3.0, yaw: -1.57}
       base_station:
         x: 0.0
         y: 0.0
         yaw: 0.0
       battery_threshold: 20.0
       navigation_timeout: 30.0
       wait_duration: 5.0
       battery_drain_rate: 0.5

You are free to adjust the zone coordinates for your map, but your
submitted file must contain **at least four zones**.


README.md
=========

Your ``README.md`` must contain:

1. A **contributions section** listing each group member and a short
   (2 to 4 sentence) summary of what they personally wrote,
   debugged, tested, or documented.
2. A **brief description** of your behavior tree design (which
   composites use ``memory=True`` vs ``memory=False`` and why).

No other sections are required.


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
  logic (e.g., Nav2 goal construction, TF frame broadcasting,
  service call handling).
- **Naming conventions:** ``snake_case`` for topics, services,
  methods, and variables. ``CamelCase`` for class names.
- **Logging:** Use the ROS 2 logger exclusively. Never use
  ``print()``. Use the appropriate severity level.
- **Linting:** Ensure Ruff is enabled and no errors appear.
