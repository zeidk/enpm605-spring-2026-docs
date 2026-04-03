====================================================
Scenario 3: Environmental Monitoring Explorer
====================================================


Domain
======

An environmental monitoring robot systematically explores an
environment, collects sensor readings at designated waypoints, and
makes intelligent decisions about where to investigate further based on
the data collected. A behavior tree coordinates the entire system: it
manages lifecycle transitions for data collection and analysis nodes,
navigates between waypoints via Nav2, evaluates sensor readings to
decide whether to revisit anomalous areas or skip clear ones, and
generates a summary report at the end of the exploration mission.


.. dropdown:: System Architecture
   :open:

   Your system must contain the following nodes, topics, services, and
   actions.

   **Nodes**

   .. list-table::
      :widths: 25 15 60
      :header-rows: 1
      :class: compact-table

      * - Node
        - Type
        - Description
      * - ``bt_runner``
        - Regular
        - The behavior tree executor. Constructs the BT, sets up the
          blackboard with the waypoint list and data storage, and
          ticks the tree at 10 Hz. This is the top-level coordinator
          for the entire system.
      * - ``data_collector``
        - Lifecycle
        - Manages sensor data collection at waypoints. In
          ``on_configure()``, creates subscribers to ``/scan`` and
          optionally ``/camera/image_raw``. In ``on_activate()``,
          begins collecting and averaging sensor readings, publishing
          results on ``/exploration/readings``. In
          ``on_deactivate()``, stops collection and publishes a
          final averaged reading for the current waypoint.
      * - ``anomaly_analyzer``
        - Lifecycle
        - Analyzes collected sensor readings for anomalies. In
          ``on_configure()``, loads anomaly thresholds from
          parameters. In ``on_activate()``, subscribes to
          ``/exploration/readings`` and evaluates each reading
          against thresholds. Publishes analysis results on
          ``/exploration/anomalies``. In ``on_deactivate()``, stops
          analysis.
      * - ``exploration_reporter``
        - Regular
        - Subscribes to ``/exploration/readings`` and
          ``/exploration/anomalies``. Maintains a complete log of all
          waypoints visited, readings collected, and anomalies
          detected. On request (via a topic or at mission end),
          publishes a comprehensive exploration report on
          ``/exploration/report``.
      * - ``sensor_processor``
        - Regular
        - Subscribes to ``/scan`` (lidar). Computes environmental
          metrics from the lidar data: average range, minimum range,
          range variance, and open-space ratio (fraction of beams
          exceeding a threshold distance). Publishes processed
          metrics on ``/exploration/environment_metrics``.

   **Behavior Tree Structure**

   The following diagram shows the required high-level structure of
   the behavior tree. You may add additional nodes as needed, but the
   core structure must be present.

   .. code-block:: text

      [Root - Sequence]
      |
      |-- [System Init - Sequence]
      |   |-- ConfigureDataCollector (Action)
      |   |-- ActivateDataCollector (Action)
      |   |-- ConfigureAnomalyAnalyzer (Action)
      |   |-- ActivateAnomalyAnalyzer (Action)
      |   |-- LoadWaypointList (Action - populate blackboard)
      |
      |-- [Exploration Loop - Repeat Decorator]
      |   |
      |   |-- [Process Waypoint - Sequence]
      |   |   |-- WaypointsRemaining? (Condition - check list)
      |   |   |-- GetNextWaypoint (Action - pop from blackboard)
      |   |   |-- NavigateToWaypoint (Action - Nav2 goal)
      |   |   |-- ActivateDataCollector (Action - ensure active)
      |   |   |
      |   |   |-- [Data Collection - Timeout Decorator (15s)]
      |   |   |   |-- CollectReadings (Action - wait while collecting)
      |   |   |
      |   |   |-- DeactivateDataCollector (Action - finalize reading)
      |   |   |-- EvaluateReading (Action - check for anomaly)
      |   |   |
      |   |   |-- [Anomaly Decision - Selector]
      |   |   |   |
      |   |   |   |-- [Investigate Anomaly - Sequence]
      |   |   |   |   |-- AnomalyDetected? (Condition)
      |   |   |   |   |-- LogAnomaly (Action)
      |   |   |   |   |-- [Detailed Scan - Sequence]
      |   |   |   |   |   |-- RotateAndScan (Action - 360 deg scan)
      |   |   |   |   |   |-- ActivateDataCollector (Action)
      |   |   |   |   |   |-- [Extended Collection - Timeout (20s)]
      |   |   |   |   |   |   |-- CollectDetailedReadings (Action)
      |   |   |   |   |   |-- DeactivateDataCollector (Action)
      |   |   |   |   |-- MarkWaypointAnomalous (Action)
      |   |   |   |
      |   |   |   |-- [Normal Waypoint - Sequence]
      |   |   |   |   |-- NOT AnomalyDetected? (Condition w/ Inverter)
      |   |   |   |   |-- MarkWaypointClear (Action)
      |   |   |
      |   |   |-- UpdateExplorationLog (Action)
      |
      |-- [Mission Complete - Sequence]
      |   |-- DeactivateAnomalyAnalyzer (Action)
      |   |-- GenerateReport (Action - publish final report)
      |   |-- LogMissionSummary (Action)

   .. note::

      The BT structure above is a guideline. You are expected to
      refine it based on your implementation. The key requirement is
      that the Anomaly Decision Selector demonstrates
      **data-driven branching** -- the robot performs extended
      investigation at anomalous waypoints and quickly moves on from
      clear ones.

   **Topics**

   .. list-table::
      :widths: 35 30 35
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - Description
      * - ``/scan``
        - ``sensor_msgs/msg/LaserScan``
        - Lidar data from the robot (provided by Gazebo)
      * - ``/exploration/readings``
        - ``std_msgs/msg/String``
        - JSON-encoded sensor readings at a waypoint (waypoint ID,
          average range, min range, range variance, open-space ratio,
          timestamp)
      * - ``/exploration/anomalies``
        - ``std_msgs/msg/String``
        - JSON-encoded anomaly reports (waypoint ID, anomaly type,
          severity, threshold exceeded, details)
      * - ``/exploration/environment_metrics``
        - ``std_msgs/msg/String``
        - JSON-encoded real-time environmental metrics from lidar
          processing
      * - ``/exploration/report``
        - ``std_msgs/msg/String``
        - JSON-encoded final exploration report (all waypoints,
          readings, anomalies, statistics)

   **Services**

   .. list-table::
      :widths: 35 30 35
      :header-rows: 1
      :class: compact-table

      * - Service
        - Type
        - Description
      * - ``/data_collector/change_state``
        - ``lifecycle_msgs/srv/ChangeState``
        - Lifecycle transition service (auto-generated by lifecycle
          node)
      * - ``/anomaly_analyzer/change_state``
        - ``lifecycle_msgs/srv/ChangeState``
        - Lifecycle transition service (auto-generated by lifecycle
          node)

   **Actions**

   .. list-table::
      :widths: 35 30 35
      :header-rows: 1
      :class: compact-table

      * - Action
        - Type
        - Description
      * - ``/navigate_to_pose``
        - ``nav2_msgs/action/NavigateToPose``
        - Nav2 navigation action (send goals, monitor progress)


.. dropdown:: Behavior Tree Requirements
   :open:

   In addition to the common BT requirements, Scenario 3 must
   demonstrate:

   1. **Data-driven decision making:** The Anomaly Decision Selector
      must branch based on actual sensor data analysis. The
      ``AnomalyDetected?`` condition node reads the analysis result
      from the blackboard and returns ``SUCCESS`` if the reading
      exceeds defined thresholds, triggering the investigation branch.
      This is not scripted -- the decision depends on the environment.

   2. **Lifecycle cycling during mission:** The ``data_collector``
      lifecycle node must be activated and deactivated **at each
      waypoint** as part of the normal BT execution. This demonstrates
      fine-grained lifecycle management:

      - Activate upon arriving at a waypoint to begin collection
      - Deactivate after collection to finalize and publish the
        averaged reading
      - Reactivate for detailed collection if an anomaly is detected

   3. **Mission phases:** The BT must clearly separate three mission
      phases:

      - **Initialization:** configure and activate all lifecycle nodes
      - **Exploration:** iterate through waypoints, collect data, and
        make decisions
      - **Completion:** deactivate nodes and generate the final report

   4. **Blackboard variables** (minimum):

      - ``waypoint_list``: list of waypoint poses to explore
      - ``current_waypoint_index``: integer index into the list
      - ``current_waypoint_id``: string identifier for the current
        waypoint
      - ``latest_reading``: most recent sensor reading at the current
        waypoint
      - ``anomaly_detected``: boolean flag from the anomaly analyzer
      - ``anomaly_details``: details of the detected anomaly
      - ``exploration_log``: list of dicts recording each waypoint's
        result (waypoint ID, status, readings, anomaly info)
      - ``nav_status``: navigation status
      - ``data_collector_state``: lifecycle state
      - ``anomaly_analyzer_state``: lifecycle state
      - ``waypoints_visited``: count of waypoints visited
      - ``anomalies_found``: count of anomalies detected

   5. **Minimum tree complexity:** The complete BT must have at least
      **18 leaf nodes** (actions + conditions) and at least **3 levels
      of nesting**.


.. dropdown:: Simulation Environment
   :open:

   Create a Gazebo world that represents an environment to be explored
   and monitored, with the following elements:

   1. **Environment layout:** The environment must include walls and
      structures creating distinct areas or rooms connected by
      passages. The layout should require Nav2 path planning and
      prevent direct line-of-sight between all waypoints.

   2. **Exploration waypoints:** At least **5 waypoint locations**
      spread across the environment. These should be positioned in
      different areas to require significant navigation.

   3. **Anomaly sources:** Place at least **2 anomaly-inducing
      objects** in the environment near certain waypoints. These are
      objects that alter the lidar readings in detectable ways:

      - A cluster of small objects close to a waypoint (causes low
        minimum range and high range variance)
      - A narrow passage or enclosed area near a waypoint (causes
        lower-than-average open-space ratio)
      - Alternatively, use colored objects detectable by camera

   4. **Varied terrain:** Include areas with different characteristics
      -- open spaces, narrow corridors, cluttered areas -- so that
      sensor readings vary meaningfully between waypoints.

   5. **Robot:** TurtleBot3 Waffle (preferred, includes lidar and
      camera) or TurtleBot4.


.. dropdown:: Detailed Requirements
   :open:

   In addition to the common requirements in the main GP 4 page:

   1. **Waypoint exploration:** The robot must systematically visit at
      least **5 waypoints**. At each waypoint, the robot:

      - Navigates to the waypoint using Nav2
      - Activates the ``data_collector`` lifecycle node
      - Collects sensor readings for a configurable duration (default
        15 seconds)
      - Deactivates the ``data_collector`` to finalize the reading
      - Evaluates the reading for anomalies

   2. **Data collection:** The ``data_collector`` lifecycle node must:

      - Subscribe to ``/scan`` and compute averaged metrics over the
        collection period: mean range, minimum range, range variance,
        and open-space ratio
      - Publish the averaged reading on ``/exploration/readings``
        when deactivated (i.e., the deactivation transition triggers
        publishing the finalized reading)
      - Reset its internal accumulators each time it is activated

   3. **Anomaly detection:** The ``anomaly_analyzer`` lifecycle node
      must evaluate readings against configurable thresholds:

      - **Low minimum range** anomaly: minimum range below a threshold
        (e.g., < 0.3 m) indicates unexpected nearby objects
      - **High range variance** anomaly: variance above a threshold
        (e.g., > 2.0 m^2) indicates an irregular environment
      - **Low open-space ratio** anomaly: ratio below a threshold
        (e.g., < 0.3) indicates a cluttered or enclosed area

      When an anomaly is detected, it must publish the anomaly details
      on ``/exploration/anomalies`` and update the blackboard.

   4. **Anomaly investigation:** When an anomaly is detected at a
      waypoint, the BT must:

      - Log the anomaly with details (type, severity, waypoint ID)
      - Perform a detailed scan: rotate the robot 360 degrees to
        capture a complete lidar sweep
      - Reactivate the ``data_collector`` for an extended collection
        period (20 seconds)
      - Record the detailed readings in the exploration log
      - Mark the waypoint as anomalous in the blackboard

   5. **Exploration report:** At the end of the mission (all waypoints
      visited), the ``exploration_reporter`` must publish a
      comprehensive report including:

      - Total waypoints visited
      - Number of waypoints with anomalies
      - Number of clear waypoints
      - Summary of each waypoint (ID, status, key readings)
      - List of all detected anomalies with details
      - Total mission duration

   6. **Navigation failure handling:** If Nav2 fails to reach a
      waypoint, the BT must:

      - Log a warning with the waypoint ID
      - Mark the waypoint as ``unreachable`` in the exploration log
      - Proceed to the next waypoint

   7. **Dynamic waypoint ordering** (bonus complexity): If an anomaly
      is detected, the BT should check whether any neighboring
      waypoints (within a configurable radius) have already been
      visited. If not, it should prioritize them by moving them to the
      front of the remaining waypoint list. This demonstrates dynamic
      replanning based on collected data.

   8. **Logging:** All major events must be logged with appropriate
      severity levels:

      - ``INFO``: waypoint reached, data collection started/completed,
        waypoint classified as clear, report generated
      - ``WARN``: anomaly detected, navigation taking longer than
        expected, waypoint unreachable
      - ``ERROR``: lifecycle transition failure, Nav2 unavailable,
        data collection failure


.. dropdown:: Scenario 3 Grading Rubric
   :open:

   This rubric details how the 100 points map to Scenario 3
   deliverables.

   .. list-table::
      :widths: 40 8 52
      :header-rows: 1
      :class: compact-table

      * - Component
        - Pts
        - Criteria
      * - **Behavior Tree Design (25 pts)**
        -
        -
      * - Tree structure
        - 8
        - BT contains at least two Sequences, one Selector, two
          Conditions, three Actions, and one Decorator. Tree has at
          least 18 leaf nodes and 3 levels of nesting. Three mission
          phases (init, exploration, completion) clearly separated.
      * - Data-driven branching
        - 7
        - Anomaly Decision Selector correctly branches based on
          sensor data analysis. Investigation triggered by actual
          anomaly detection, not scripted. Clear waypoints handled
          efficiently.
      * - Blackboard usage
        - 5
        - Blackboard stores waypoint list, current waypoint, readings,
          anomaly flags, exploration log, nav status, and lifecycle
          states. Exploration log accumulates data across waypoints.
      * - BT ticking and lifecycle
        - 5
        - BT ticks at the configured rate. Tree starts, runs through
          all waypoints, completes the mission, and shuts down cleanly.
          ``py_trees`` / ``py_trees_ros`` used correctly.
      * - **Lifecycle Management (15 pts)**
        -
        -
      * - Lifecycle node implementation
        - 5
        - ``data_collector`` and ``anomaly_analyzer`` correctly
          implement ``on_configure()``, ``on_activate()``,
          ``on_deactivate()``, and ``on_cleanup()``. State-dependent
          behavior demonstrated. ``data_collector`` resets on
          activation and finalizes on deactivation.
      * - BT-driven transitions
        - 5
        - BT action nodes call lifecycle transition services.
          ``data_collector`` activated/deactivated at each waypoint.
          Multiple activate/deactivate cycles demonstrated per
          mission.
      * - Transition error handling
        - 5
        - BT handles failed transitions gracefully (returns FAILURE
          up the tree). Transition timeouts handled.
      * - **Nav2 Integration (20 pts)**
        -
        -
      * - Waypoint navigation
        - 8
        - Robot navigates to at least 5 waypoints via
          ``NavigateToPose``. Goals sent correctly with proper pose
          format. Navigation monitored for completion.
      * - Dynamic goal selection
        - 5
        - At least one navigation goal determined at runtime (e.g.,
          waypoint order adjusted based on anomaly detection or
          waypoint selected from the list dynamically). Not all goals
          in a fixed sequence.
      * - Complete exploration path
        - 4
        - Robot visits all reachable waypoints, collecting data at
          each. Navigation path covers the entire environment.
      * - Failure recovery
        - 3
        - Navigation failure handled gracefully (waypoint marked
          unreachable, next waypoint attempted).
      * - **Sensor Integration (15 pts)**
        -
        -
      * - Data collection
        - 5
        - Lidar data processed into meaningful metrics (mean range,
          min range, variance, open-space ratio). Readings averaged
          over collection period. Published correctly.
      * - Anomaly detection
        - 5
        - Anomaly analyzer evaluates readings against configurable
          thresholds. Detects at least one anomaly during the mission.
          Anomaly details published and written to blackboard.
      * - Reactive behavior
        - 5
        - Robot demonstrably performs extended investigation at
          anomalous waypoints and quickly proceeds at clear ones.
          Behavior difference visible in demo.
      * - **Code Quality (10 pts)**
        -
        -
      * - Type hints and docstrings
        - 4
        - All methods have type annotations. All classes and methods
          have Google-style docstrings.
      * - Logging
        - 3
        - ROS 2 logger used exclusively with correct severity levels.
          Major events logged (waypoint arrivals, readings, anomalies,
          report generation).
      * - Style and linting
        - 3
        - ``snake_case`` / ``CamelCase`` conventions followed. No Ruff
          errors. Clean, readable code.
      * - **Documentation (10 pts)**
        -
        -
      * - README.md
        - 5
        - Group members, contributions, scenario summary, build/run
          instructions, known issues.
      * - Architecture documentation
        - 5
        - BT diagram, node descriptions, topic/service/action list,
          blackboard variable documentation, lifecycle state
          descriptions (especially ``data_collector`` cycling),
          anomaly threshold explanations, design decision rationale.
      * - **Demo Video (5 pts)**
        -
        -
      * - Video content
        - 3
        - Video shows exploration of at least 3 waypoints, data
          collection process, anomaly detection and investigation,
          lifecycle transitions in logs, Nav2 navigation, and final
          report generation.
      * - Video quality
        - 2
        - 2--3 minutes, narrated or captioned, clearly shows all
          required behaviors including the difference between
          anomalous and clear waypoints.
      * - **TOTAL**
        - **100**
        -
