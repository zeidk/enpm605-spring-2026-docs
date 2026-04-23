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
       ``has_remaining``, ``advance``, ``skip``, ``base_pose``,
       ``next_survivor_id``). State is managed correctly.
   * - Integration with BT nodes
     - 3
     - ``ZoneManager`` instance is shared via constructor injection.
       BT nodes correctly read and modify zone state.
   * - **Condition Nodes (9 pts)**
     -
     -
   * - ``CheckBattery``
     - 3
     - Subscribes to ``/battery_state`` in ``setup()``. Returns
       SUCCESS when battery is above threshold, FAILURE otherwise.
       Never returns RUNNING.
   * - ``ZonesRemaining``
     - 3
     - Queries ``zone_manager.has_remaining()``. Returns correct
       status.
   * - ``IsSurvivorDetected``
     - 3
     - Reads detection result from the ``DetectSurvivor`` action
       node via direct reference. Returns correct status.
   * - **Action Nodes (30 pts)**
     -
     -
   * - ``NavigateToZone``
     - 6
     - Sends ``NavigateToPose`` goal to Nav2 for the current zone.
       Returns RUNNING while navigating, SUCCESS on arrival,
       FAILURE on Nav2 failure. Publishes zero-velocity on
       ``terminate()``.
   * - ``NavigateToBase``
     - 4
     - Same as ``NavigateToZone`` but targets
       ``zone_manager.base_pose()``.
   * - ``Wait``
     - 3
     - Returns RUNNING for the configured duration, then SUCCESS.
   * - ``DetectSurvivor`` (BT node)
     - 5
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
   * - ``SkipZone``
     - 2
     - Logs a warning. Calls ``zone_manager.skip()``. Returns
       SUCCESS.
   * - ``AdvanceZone`` and ``LogNoDetection``
     - 2
     - ``AdvanceZone`` calls ``zone_manager.advance()``.
       ``LogNoDetection`` logs and returns SUCCESS. Both are
       correct.
   * - **Tree Assembly (10 pts)**
     -
     -
   * - Correct tree structure
     - 5
     - Tree matches the specified structure: root Sequence, Mission
       Selector, Patrol Sequence, NavigateWithRecovery Selector,
       HandleDetection Selector. Correct parent-child relationships.
   * - ``memory`` flags
     - 3
     - Root Sequence uses ``memory=False`` (reactive). Patrol and
       NavigateWithRecovery use ``memory=True`` (resuming).
       Justification provided in README.
   * - Timeout decorators
     - 2
     - Two Timeout decorators correctly wrap the two
       ``NavigateToZone`` instances. Duration loaded from
       parameters.
   * - **Battery Simulation (5 pts)**
     -
     -
   * - Battery simulator node
     - 3
     - Publishes ``sensor_msgs/BatteryState`` on ``/battery_state``
       at 1 Hz. ``percentage`` decreases over time at a
       configurable rate.
   * - Low battery behavior
     - 2
     - When battery drops below threshold, the BT correctly aborts
       the patrol and navigates to base.
   * - **Launch File (8 pts)**
     -
     -
   * - All nodes started
     - 3
     - Launch file starts the BT node, both service servers, and
       the battery simulator. All use ``output="screen"`` and
       ``emulate_tty=True``.
   * - Parameter file loading
     - 3
     - ``config/mission_params.yaml`` is loaded for the BT node
       using ``get_package_share_directory()`` and the
       ``parameters`` field.
   * - Launch arguments
     - 2
     - At least ``battery_threshold`` and ``navigation_timeout``
       declared and passed to the BT node. ``--show-args`` displays
       them correctly.
   * - **Documentation and Code Quality (12 pts)**
     -
     -
   * - README.md contributions
     - 4
     - ``README.md`` contains a contributions section with every
       group member listed and a short, specific summary.
   * - README.md BT design
     - 2
     - Brief explanation of ``memory`` flag choices and tree design
       rationale.
   * - Docstrings and type hints
     - 3
     - Every class and method has a Google-style docstring. All
       method parameters and return types have type annotations.
   * - Logging and code quality
     - 3
     - ROS 2 logger used exclusively (no ``print()``). Correct
       severity levels. Consistent ``snake_case`` naming. No Ruff
       linting errors.
   * - **TOTAL**
     - **100**
     -
