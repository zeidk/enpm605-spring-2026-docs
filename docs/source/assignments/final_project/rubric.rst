====================================================
Grading Rubric
====================================================

.. |<=| unicode:: U+2264
.. |rarr| unicode:: U+2192


This rubric details how the 100 points are allocated.

.. list-table::
   :widths: 42 6 52
   :header-rows: 1
   :class: compact-table

   * - Component
     - Pts
     - Criteria
   * - **Service Interfaces (8 pts)**
     -
     -
   * - ``DetectSurvivor.srv`` definition
     - 2
     - Request and response fields match the specification exactly.
   * - ``ReportSurvivor.srv`` definition
     - 2
     - Request and response fields match the specification exactly
       (uses ``geometry_msgs/PointStamped``).
   * - CMake package configuration
     - 4
     - ``CMakeLists.txt`` generates both interfaces via
       ``rosidl_generate_interfaces`` with ``geometry_msgs``
       dependency. ``package.xml`` includes all required entries.
       Package builds cleanly.
   * - **Service Servers (10 pts)**
     -
     -
   * - DetectSurvivorServer
     - 5
     - Advertises ``detect_survivor`` service. Returns correct
       ``found`` status and survivor coordinates based on a
       hardcoded lookup. Logs each request.
   * - ReportSurvivorServer
     - 5
     - Advertises ``report_survivor`` service. Logs the survivor ID
       and location. Returns ``acknowledged=True``.
   * - **ZoneManager (8 pts)**
     -
     -
   * - Class implementation
     - 5
     - All required methods implemented (``current_zone``,
       ``has_remaining``, ``advance``, ``base_pose``,
       ``next_survivor_id``). State is managed correctly.
   * - Integration with BT nodes
     - 3
     - ``ZoneManager`` instance is shared via constructor injection.
       BT nodes correctly read and modify zone state.
   * - **Condition Nodes (6 pts)**
     -
     -
   * - ``ZonesRemaining``
     - 3
     - Queries ``zone_manager.has_remaining()``. Returns correct
       status.
   * - ``IsSurvivorDetected``
     - 3
     - Reads detection result from the ``DetectSurvivor`` action
       node via direct reference. Returns correct status.
   * - **Action Nodes (28 pts)**
     -
     -
   * - ``NavigateToZone``
     - 8
     - Sends ``NavigateToPose`` goal to Nav2 for the current zone.
       Returns RUNNING while navigating, SUCCESS on arrival,
       FAILURE on Nav2 failure. Cancels the goal on
       ``terminate()``.
   * - ``NavigateToBase``
     - 4
     - Same as ``NavigateToZone`` but targets
       ``zone_manager.base_pose()``.
   * - ``DetectSurvivor`` (BT node)
     - 6
     - Calls the ``detect_survivor`` service with the current zone
       ID. Stores result internally. Exposes ``was_found()`` and
       ``survivor_pose()`` methods. Returns SUCCESS after the
       service call completes.
   * - ``BroadcastSurvivorTF``
     - 5
     - Creates a ``StaticTransformBroadcaster``. Publishes a static
       TF frame (``survivor_N``) at the correct pose in the ``map``
       frame. Frame is verifiable via
       ``ros2 run tf2_ros tf2_echo map survivor_N``.
   * - ``NotifyBase``
     - 3
     - Calls the ``report_survivor`` service with the survivor ID
       and location. Returns SUCCESS if acknowledged.
   * - ``AdvanceZone`` and ``LogNoDetection``
     - 2
     - ``AdvanceZone`` calls ``zone_manager.advance()``.
       ``LogNoDetection`` logs and returns SUCCESS. Both are
       correct.
   * - **Tree Assembly (10 pts)**
     -
     -
   * - Correct tree structure
     - 7
     - Tree matches the specified structure: root Selector,
       Patrol Sequence, HandleDetection Selector, SurvivorFound
       Sequence, terminal NavigateToBase. Correct parent-child
       relationships.
   * - ``memory`` flags
     - 3
     - Root Selector uses ``memory=False`` (reactive). Patrol
       Sequence uses ``memory=True`` (resuming).
       HandleDetection Selector uses ``memory=False``.
       SurvivorFound Sequence uses ``memory=False`` (all children
       are synchronous, single-tick). Justification provided in
       README.
   * - **Map (5 pts)**
     -
     -
   * - Saved map files
     - 3
     - ``group<N>_final/maps/`` contains a valid
       ``final_project_map.pgm`` plus matching
       ``final_project_map.yaml``, produced by ``slam_toolbox`` +
       ``nav2_map_server``. Free, occupied, and unknown regions
       look correct.
   * - AMCL localization against the saved map
     - 2
     - ``ros2 launch group<N>_final search_and_rescue.launch.py``
       brings up Nav2 with the saved map and the BT entry point
       auto-seeds AMCL at the spawn pose
       (``BasicNavigator.setInitialPose``) and waits for Nav2 to
       reach ACTIVE
       (``waitUntilNav2Active``) before ticking the tree -- no
       manual ``2D Pose Estimate`` click required.
   * - **Launch File (8 pts)**
     -
     -
   * - All nodes started
     - 3
     - Launch file starts the BT node and both service servers.
       All use ``output="screen"`` and ``emulate_tty=True``.
   * - Parameter file loading
     - 3
     - ``config/mission_params.yaml`` is loaded for the BT node
       via the ``parameters`` field, and
       ``config/nav2_params.yaml`` is forwarded to the Nav2
       bringup include via ``params_file:=``. Both paths are
       resolved with ``get_package_share_directory()``.
   * - Launch arguments
     - 2
     - At least one launch argument declared and forwarded to the
       BT node. ``--show-args`` displays it correctly.
   * - **Documentation and Code Quality (17 pts)**
     -
     -
   * - README.md contributions
     - 5
     - ``README.md`` contains a contributions section with every
       group member listed and a short, specific summary.
   * - README.md BT design
     - 3
     - Brief explanation of ``memory`` flag choices and tree design
       rationale.
   * - Docstrings and type hints
     - 3
     - Every class and method has a Google-style docstring. All
       method parameters and return types have type annotations.
   * - Logging and code quality
     - 6
     - ROS 2 logger used exclusively (no ``print()``). Correct
       severity levels. Consistent ``snake_case`` naming. No Ruff
       linting errors.
   * - **TOTAL**
     - **100**
     -
