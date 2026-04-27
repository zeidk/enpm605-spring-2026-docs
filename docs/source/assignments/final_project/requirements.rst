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

6. **Implement 9 behavior tree leaf nodes** (2 conditions + 7
   actions) using ``py_trees.behaviour.Behaviour``.

7. **Assemble the full behavior tree** in an entry point script that
   reads parameters, builds the tree, and runs it with
   ``py_trees_ros.trees.BehaviourTree``.

8. **Write the launch file** that starts the service servers and the
   behavior tree node, loading all parameters from YAML.

9. **Build a map** of the final project world using ``slam_toolbox``
   and save it under ``group<N>_final/maps/`` (see
   :doc:`infrastructure` for the procedure). The saved
   ``.pgm`` and ``.yaml`` files must be included in your submission.

10. **Document contributions** in ``README.md``.

11. **Submit** by zipping the ``~/enpm605_ws/src/final_project/``
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
   |-- maps/
   |   |-- final_project_world.pgm
   |   |-- final_project_world.yaml
   |-- resource/
   |   |-- group<N>_final
   |-- test/
   |-- package.xml
   |-- setup.py
   |-- setup.cfg
   |-- README.md


.. _final-project-build-the-map:

Build the Map
=============

Nav2 needs a pre-built occupancy grid to localize the robot. **No
map is provided** -- each group must build their own with
``slam_toolbox`` and save it with ``nav2_map_server``. The two
output files (``.pgm`` + ``.yaml``) live under
``group<N>_final/maps/`` and ship with your submission.

.. important::

   Build the map yourself by following the same workflow we used in class.

   1. Launch the final project world and ``slam_toolbox`` in mapping
      mode (in two terminals):

   .. list-table::
      :widths: 10 90
      :header-rows: 1
      :class: compact-table

      * -
        - Command
      * - T1
        - ``ros2 launch rosbot_gazebo final_project_world.launch.py rviz:=False``
      * - T2
        - ``ros2 launch nav_demo map_nav.launch.py mode:=mapping``
      * - Gazebo
        - Drive the robot with teleop
      * - RViz
        - Observe the map display

   .. code-block:: console

      # T1
      ros2 launch rosbot_gazebo final_project_world.launch.py rviz:=False
      # T2
      ros2 launch nav_demo map_nav.launch.py mode:=mapping

   2. Save the map under your package's ``maps/`` directory using
      ``nav2_map_server``:

      .. code-block:: console

         mkdir -p ~/enpm605_ws/src/final_project/group<N>_final/maps
         ros2 run nav2_map_server map_saver_cli \
             -f ~/enpm605_ws/src/final_project/group<N>_final/maps/final_project_map

      This produces ``final_project_map.pgm`` and
      ``final_project_map.yaml``.


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
- When called, the server **simulates a command center**: it does
  not forward the message anywhere -- the "report" is simply a
  ROS 2 log entry. Log at minimum:

  - the ``survivor_id``,
  - ``location.header.frame_id`` (so it is obvious that the
    coordinates are in the **map frame**, not the robot body
    frame), and
  - ``location.point.x`` and ``location.point.y``.

- Returns ``acknowledged=True``.

.. note::

   The ``location`` field uses ``geometry_msgs/PointStamped`` --
   not a bare ``Point`` -- specifically so the frame in which the
   coordinates are expressed travels with the data. A receiver
   that gets a stamped point in ``"map"`` can transform it into
   any other frame with ``tf2``. By contract, the BT node sends
   ``frame_id = "map"``; the server should reject (or at least
   warn) if it ever receives a different frame.


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

       def base_pose(self) -> dict:
           """Return the base station pose dict (x, y, yaw)."""
           ...

       def next_survivor_id(self) -> str:
           """Return a unique ID like 'survivor_1', 'survivor_2', etc."""
           ...


Behavior Tree
=============

The full behavior tree must be assembled in
``scripts/main_search_and_rescue.py``. The **static structure** of
the tree (composites, conditions, actions) is shown below.

.. only:: html

   .. figure:: /_static/images/final_project/bt_tree_light.png
      :alt: Search-and-rescue behavior tree structure
      :width: 100%
      :align: center
      :class: only-light

      Behavior tree structure: composites, conditions, and actions.

   .. figure:: /_static/images/final_project/bt_tree_dark.png
      :alt: Search-and-rescue behavior tree structure
      :width: 100%
      :align: center
      :class: only-dark

      Behavior tree structure: composites, conditions, and actions.

The diagram above shows what the tree *looks like*. The diagram
below shows what it *does* at runtime -- the message flow between
your BT node, Nav2, the two simulated service servers, and the
static TF broadcaster. The PlantUML source for the sequence
diagram lives at
``docs/source/_static/images/final_project/final_project.puml``.

.. only:: html

   .. figure:: /_static/images/final_project/final_project_light.png
      :alt: Search-and-rescue mission sequence diagram
      :width: 100%
      :align: center
      :class: only-light

      Runtime message flow during a single mission execution.

   .. figure:: /_static/images/final_project/final_project_dark.png
      :alt: Search-and-rescue mission sequence diagram
      :width: 100%
      :align: center
      :class: only-dark

      Runtime message flow during a single mission execution.

**How the tree works, tick by tick:**

1. The root **Selector** (Mission or ReturnToBase, ``memory=False``)
   tries the **Patrol Sequence** first.

2. The Patrol Sequence (``memory=True``) checks
   ``ZonesRemaining?``. If all zones are visited (FAILURE), the
   Patrol Sequence fails and the root Selector falls back to
   ``NavigateToBase`` (mission complete).

3. If zones remain (SUCCESS), ``NavigateToZone`` sends a
   ``NavigateToPose`` goal to Nav2 for the current zone. It returns
   RUNNING while the goal is in flight and SUCCESS on arrival.

4. After reaching a zone, ``DetectSurvivor`` calls the detection
   service and stores the result internally.

5. The **HandleDetection Selector** checks ``IsSurvivorDetected?``:

   - If found (SUCCESS): ``BroadcastSurvivorTF`` publishes a static
     TF frame, then ``NotifyBase`` calls the report service.
   - If not found (FAILURE): ``LogNoDetection`` logs a message and
     returns SUCCESS so the Selector succeeds.

6. ``AdvanceZone`` moves to the next zone, and the Patrol Sequence
   repeats on the next tick.

7. Once every zone has been visited, ``ZonesRemaining?`` returns
   FAILURE, so the Patrol Sequence fails and the Selector ticks
   ``NavigateToBase``. After the robot reaches the base station,
   the mission is complete -- stop the BT node with ``Ctrl-C``.


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
       a ``geometry_msgs/TransformStamped`` and publishes it.
       Field values:

       - ``header.stamp`` = current ROS time
         (``self._node.get_clock().now().to_msg()``).
       - ``header.frame_id = "map"`` -- the **parent** frame. This
         **must** be ``"map"`` because: (1) the survivor coordinates
         returned by ``DetectSurvivor`` are already expressed in
         the map frame (the same frame Nav2 plans in and AMCL
         localizes the robot in -- see REP-105), and (2) ``"map"``
         is the only world-fixed frame in the system, so a static
         transform under it stays valid for the rest of the
         mission even as the robot moves.
       - ``child_frame_id = "survivor_N"`` -- the **new** frame
         being created, named via
         ``zone_manager.next_survivor_id()`` (``"survivor_1"``,
         ``"survivor_2"``, ...).
       - ``transform.translation.{x,y}`` from
         ``detect_node.survivor_pose()``; ``z = 0.0``.
       - ``transform.rotation.w = 1.0`` (identity quaternion --
         we are reporting a position, not an orientation).

       Returns SUCCESS after ``sendTransform()``. Verify with
       ``ros2 run tf2_ros tf2_echo map survivor_1`` -- you should
       see the translation match the coordinates the
       ``DetectSurvivorServer`` returned.

   * - ``NotifyBase``
     - ``name``, ``detect_node``
     - Calls the ``report_survivor`` service with a request whose
       ``survivor_id`` is the same string used as the TF child
       frame (e.g., ``"survivor_1"``) and whose
       ``location`` is a ``geometry_msgs/PointStamped`` carrying
       the survivor's position **in the map frame**:

       - ``location.header.stamp`` = current ROS time.
       - ``location.header.frame_id = "map"`` -- so the receiving
         server (and any downstream consumer) knows the point is
         in the global fixed frame, not in the robot's body frame.
       - ``location.point.{x,y}`` from
         ``detect_node.survivor_pose()``; ``z = 0.0``.

       Returns SUCCESS if the response's ``acknowledged`` field
       is ``True``, FAILURE otherwise.
   * - ``AdvanceZone``
     - ``name``, ``zone_manager``
     - Calls ``zone_manager.advance()``. Returns SUCCESS.
   * - ``LogNoDetection``
     - ``name``
     - Logs an info message that no survivor was found at the
       current zone. Returns SUCCESS.


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

**Launch file requirements:**

1. All nodes must use ``output="screen"`` and ``emulate_tty=True``.
2. Load ``config/mission_params.yaml`` for the behavior tree node
   using ``get_package_share_directory()`` and the ``parameters``
   field.
3. Declare at least one launch argument that the BT node consumes
   (for example, ``tick_rate_hz`` with a sensible default), and
   forward it to the BT node via ``parameters``. The intent is to
   exercise ``DeclareLaunchArgument`` and ``LaunchConfiguration`` --
   not to expose every internal value.
4. The simulation (Gazebo + Nav2) is started **separately** by the
   user in two terminals before launching the mission:

   .. code-block:: console

      ros2 launch rosbot_gazebo final_project_world.launch.py
      ros2 launch rosbot_gazebo navigation.launch.py \
          map:=/path/to/group<N>_final/maps/final_project_world.yaml

   The map file is the one you built and saved with
   ``slam_toolbox`` / ``nav2_map_server`` (see
   :ref:`final-project-build-the-map` above). Your launch file does
   **not** include these.


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
       tick_rate_hz: 2.0

**The** ``/**:`` **wildcard.** The top-level key ``/**`` is a ROS 2
parameter-file glob: a single ``*`` matches one node-name token, and
the doubled ``/**`` matches **any node name in any namespace**.
Because of this, every node started with this YAML loaded will
receive the parameters under ``ros__parameters`` -- you do not have
to hard-code the BT node's name (or its namespace) here.

Why this matters in practice:

- The BT entry point creates an ``rclpy`` node whose name you may
  change later (e.g., when prefixing with the group number). With
  ``/**``, the YAML keeps working without edits.
- If you launch the same node under a namespace
  (``namespace="group3"`` in the launch file), a fully-qualified
  key like ``search_and_rescue:`` would **silently fail to match**
  (the actual node would be ``/group3/search_and_rescue``);
  ``/**`` matches both forms.
- You can be more selective when you need to. For example, scoping
  one parameter to a specific node:

  .. code-block:: yaml

     /**:
       ros__parameters:
         tick_rate_hz: 2.0

     search_and_rescue:
       ros__parameters:
         zones: [...]

  Here ``tick_rate_hz`` is shared by every node, while ``zones``
  only loads into a node literally named ``search_and_rescue``.

For this assignment, the simple ``/**`` block above is enough --
all parameters belong to the BT node, and there is only one
consumer.


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
