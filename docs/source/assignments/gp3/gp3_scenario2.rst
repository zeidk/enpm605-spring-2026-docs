====================================================
Scenario 2: Search and Rescue Navigator
====================================================


Domain
======

A search and rescue (SAR) team deploys an autonomous robot to
systematically explore a building after a disaster. The robot navigates
through rooms and corridors, uses lidar and camera data to detect
"victims" (represented by colored objects or markers placed in the
simulation), and logs the location and details of each finding. The
search mission is managed through a lifecycle node, allowing the
operations commander to configure the search area, activate the
search, pause it when human responders need to enter, and reset for
a new search zone.


.. dropdown:: System Architecture
   :open:

   Your system must contain the following nodes, topics, services, and
   actions.

   **Nodes**

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Node
        - Description
      * - ``search_manager`` *(lifecycle)*
        - A lifecycle node that manages the search mission. In
          ``on_configure``: loads a list of room waypoints from
          parameters (at least 4 rooms as ``[x, y, yaw]`` triples),
          creates the ``BasicNavigator`` instance, and creates
          publishers for search status and findings. In
          ``on_activate``: waits for Nav2, sets the initial pose,
          and begins navigating to the first room. In
          ``on_deactivate``: cancels the current navigation goal and
          pauses the search. In ``on_cleanup``: destroys the navigator,
          resets internal state (rooms visited, findings list), and
          releases all resources. While active, the node navigates
          sequentially through each room waypoint. After reaching a
          room, it pauses for 5 seconds (simulated dwell time for
          sensor scanning) before proceeding to the next room.
          Publishes status on ``/search/status``.
      * - ``victim_detector``
        - Subscribes to ``/scan`` (``sensor_msgs/LaserScan``). Analyzes
          lidar data to detect objects at close range (1.0--2.0 m) that
          could represent victims. When a potential victim is detected
          (cluster of points at close range in a narrow angular sector),
          publishes a ``std_msgs/msg/String`` detection on
          ``/search/detections`` with the bearing and estimated
          distance. Uses ``self.get_logger().warn()`` to highlight
          detections.
      * - ``findings_logger``
        - Subscribes to ``/search/status`` and ``/search/detections``.
          Maintains a cumulative list of all findings, including which
          room they were detected in and the timestamp. Publishes a
          ``std_msgs/msg/String`` summary on ``/search/report`` at
          0.2 Hz with the total rooms searched, total detections, and
          a list of all findings.
      * - ``scan_visualizer`` *(optional, conditional)*
        - Subscribes to ``/scan`` and ``/search/detections`` and logs
          detailed scan data for offline analysis. Started only when
          ``enable_debug`` launch argument is ``true``.

   **Topics**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - Description
      * - ``/scan``
        - ``sensor_msgs/msg/LaserScan``
        - Lidar scan data bridged from Gazebo via ``ros_gz_bridge``.
      * - ``/cmd_vel``
        - ``geometry_msgs/msg/Twist``
        - Velocity commands sent by Nav2 to the robot.
      * - ``/search/status``
        - ``std_msgs/msg/String``
        - JSON-formatted status: ``{"room_index": 1, "room_waypoint":
          [2.0, 3.0, 1.57], "status": "reached"|"scanning"|"moving",
          "rooms_remaining": 3, "timestamp": "..."}``.
      * - ``/search/detections``
        - ``std_msgs/msg/String``
        - JSON-formatted detection: ``{"room_index": 1, "bearing_deg":
          45.0, "distance": 1.3, "confidence": "high"|"low",
          "timestamp": "..."}``.
      * - ``/search/report``
        - ``std_msgs/msg/String``
        - JSON-formatted cumulative summary of the search mission.

   **Actions (used via BasicNavigator)**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Action
        - Type
        - Description
      * - ``/navigate_to_pose``
        - ``nav2_msgs/NavigateToPose``
        - Used by ``search_manager`` via ``BasicNavigator.goToPose()``
          to navigate the robot to each room waypoint.


.. dropdown:: Simulation Environment
   :open:

   **World description:**

   Create or adapt an SDF world representing a simplified building
   interior with multiple rooms. The world must include:

   - A floor area of at least 12 m x 10 m.
   - At least 4 distinct rooms separated by walls with doorway
     openings (at least 0.8 m wide).
   - A central corridor connecting the rooms.
   - At least 2 "victim" objects placed in different rooms. These can
     be simple colored cylinders or boxes (e.g., red cylinders with
     radius 0.15 m, height 0.5 m) that are detectable by lidar at
     close range.
   - At least 1 piece of debris or furniture (a box or irregular shape)
     in a room that acts as a non-victim obstacle, testing the
     detector's ability to distinguish clutter.

   **Robot model:**

   Use a differential-drive robot with the following minimum sensors:

   - A 2D lidar with 360-degree coverage and at least 8 m range
     (needed for room-scale detection).
   - A ``DiffDrive`` Gazebo plugin for velocity control.

   You may use TurtleBot3 (Waffle or Burger), a custom SDF model, or
   any differential-drive robot that meets these requirements. Document
   your choice in ``README.md``.


.. dropdown:: Detailed Requirements
   :open:

   In addition to the common requirements on the main GP 3 page:

   1. **Lifecycle node -- search_manager**:

      - ``on_configure``: Read room waypoints from ROS parameters. The
        node must declare a parameter ``room_waypoints`` as a list of
        doubles (flattened: ``[x1, y1, yaw1, x2, y2, yaw2, ...]``).
        Parse these into a list of ``PoseStamped`` goals. Create the
        ``BasicNavigator`` instance, the ``/search/status`` publisher,
        and an internal findings list. Log the number of rooms to
        search.
      - ``on_activate``: Call ``navigator.waitUntilNav2Active()``. Set
        the initial pose using ``navigator.setInitialPose()``. Begin
        navigating to the first room. Start a timer (1 Hz) that
        monitors navigation progress and manages the room-by-room
        search sequence.
      - ``on_deactivate``: Call ``navigator.cancelTask()`` to stop the
        robot. Cancel the monitoring timer. Publish a status update
        indicating the search is paused. Log the current room index and
        total rooms visited.
      - ``on_cleanup``: Destroy the navigator, publishers, and timer.
        Reset the room index, rooms visited count, and findings list.
        Log that cleanup is complete.

   2. **Room dwell time**: After the robot reaches a room waypoint, the
      ``search_manager`` publishes a ``"scanning"`` status and waits
      for 5 seconds (using a one-shot timer or a counter in the
      periodic timer) before navigating to the next room. This dwell
      time simulates the robot scanning the room for victims.

   3. **Sequential room search**: The robot visits rooms in order
      (room 1, room 2, ..., room N). Unlike Scenario 1, the search
      does **not** loop -- after visiting the last room, the node
      publishes a ``"search_complete"`` status and remains active
      (waiting for deactivation by the operator).

   4. **Navigation feedback**: During navigation to each room, retrieve
      feedback using ``navigator.getFeedback()`` and log the estimated
      distance remaining. If navigation to a room fails, log an error,
      publish a ``"failed"`` status for that room, and skip to the next
      room.

   5. **Victim detector**: The ``victim_detector`` node must:

      - Subscribe to ``/scan`` with ``use_sim_time=true``.
      - Analyze the lidar scan for clusters of points at close range
        (between ``min_detect_range`` and ``max_detect_range``
        parameters, defaults 1.0 m and 2.0 m).
      - A "detection" is defined as 3 or more consecutive lidar rays
        returning distances within the detection range in a narrow
        angular sector (less than 15 degrees).
      - For each detection, compute the average bearing and distance.
      - Assign a confidence level: ``"high"`` if the cluster has 5+
        consecutive rays, ``"low"`` if 3--4 rays.
      - Publish the detection on ``/search/detections``.
      - Apply a cooldown: do not re-publish the same detection
        (same bearing within +/- 10 degrees) for at least 10 seconds.

   6. **Findings logger**: The ``findings_logger`` node must:

      - Track the number of rooms the robot has entered (from
        ``/search/status`` messages with ``"reached"`` status).
      - Track all detections from ``/search/detections``.
      - Associate each detection with the current room (based on the
        most recent ``"reached"`` or ``"scanning"`` status).
      - Publish a summary at 0.2 Hz with rooms searched, total
        detections, and a list of ``{room, bearing, distance,
        confidence}`` entries.

   7. **Launch file**:

      - ``system.launch.py``: starts Gazebo, spawns the robot, starts
        ``ros_gz_bridge``, launches Nav2, starts ``search_manager``,
        ``victim_detector``, and ``findings_logger``.
      - ``enable_debug`` argument (default ``false``): conditionally
        starts the ``scan_visualizer`` node using ``IfCondition``.
      - ``min_detect_range`` argument (default ``1.0``): passed to
        the ``victim_detector`` as a ROS parameter override.
      - Custom application nodes (``search_manager``,
        ``victim_detector``, ``findings_logger``) grouped in a
        ``GroupAction``.
      - All custom nodes use ``use_sim_time:=true``.

   8. **Lifecycle management**: After launching, the ``search_manager``
      can be controlled via CLI:

      .. code-block:: console

         # Configure the search manager (loads room waypoints)
         ros2 lifecycle set /search_manager configure

         # Activate the search (starts navigating to rooms)
         ros2 lifecycle set /search_manager activate

         # Pause the search (e.g., human responders entering)
         ros2 lifecycle set /search_manager deactivate

         # Resume the search from where it left off
         ros2 lifecycle set /search_manager activate

         # Clean up and prepare for a new search zone
         ros2 lifecycle set /search_manager cleanup


.. dropdown:: Scenario 2 Grading Rubric
   :open:

   This rubric details how the 60 points map to Scenario 2 deliverables.

   .. list-table::
      :widths: 40 8 52
      :header-rows: 1
      :class: compact-table

      * - Component
        - Pts
        - Criteria
      * - **Simulation Setup (10 pts)**
        -
        -
      * - Gazebo world
        - 3
        - SDF world loads in Gazebo Harmonic. Contains at least 4 rooms
          with doorways, a corridor, victim objects, and debris.
          Ground plane and lighting configured.
      * - Robot spawn
        - 3
        - Robot model spawns at a specified pose via the launch file.
          Differential-drive plugin is functional (robot responds to
          ``/cmd_vel``).
      * - Sensor bridging
        - 4
        - ``ros_gz_bridge`` correctly relays ``/cmd_vel``, ``/scan``,
          and ``/clock``. Lidar data is visible in RViz. Bridge
          configuration is documented.
      * - **Lifecycle Node (14 pts)**
        -
        -
      * - ``on_configure``
        - 4
        - Loads room waypoints from parameters. Creates navigator,
          publishers, and findings list. Logs room count. Returns
          SUCCESS or FAILURE with appropriate error handling.
      * - ``on_activate``
        - 4
        - Waits for Nav2. Sets initial pose. Begins navigating to
          first room. Starts monitoring timer. Node enters search mode.
      * - ``on_deactivate``
        - 3
        - Cancels current navigation goal. Stops timer. Publishes
          paused status. Node pauses without crashing. Can be
          re-activated to resume from the current room.
      * - ``on_cleanup``
        - 3
        - Destroys navigator, publishers, timer. Resets room index,
          visit count, and findings list. Node returns to unconfigured
          state.
      * - **Navigation (14 pts)**
        -
        -
      * - Nav2 configuration
        - 4
        - ``nav2_params.yaml`` correctly configures planner, controller,
          costmaps, and AMCL. Parameters suitable for indoor
          room-to-room navigation through doorways.
      * - Map
        - 2
        - Pre-generated map included in ``maps/`` directory. Map
          accurately represents the building with rooms and doorways.
      * - Sequential room navigation
        - 4
        - Robot navigates to at least 4 room waypoints sequentially
          using ``BasicNavigator.goToPose()``. Publishes
          ``"search_complete"`` after the last room. Does not loop.
      * - Room dwell time
        - 2
        - Robot pauses for 5 seconds at each room (``"scanning"``
          status published). Proceeds to next room after dwell.
      * - Navigation feedback
        - 2
        - Distance remaining is logged during navigation. Failed room
          navigation is detected, logged as error, and skipped.
      * - **Sensor Processing (8 pts)**
        -
        -
      * - Victim detection algorithm
        - 4
        - ``victim_detector`` correctly identifies clusters of close-
          range lidar points. Detections include bearing, distance, and
          confidence level. Consecutive-ray threshold (3+ rays) is
          implemented.
      * - Detection cooldown
        - 2
        - Same-bearing detections are suppressed for 10 seconds.
          Prevents duplicate alerts for the same object.
      * - Configurable range
        - 2
        - Detection range is configurable via ROS parameters. Can be
          overridden via launch argument.
      * - **Launch and Integration (8 pts)**
        -
        -
      * - ``system.launch.py``
        - 4
        - Single command launches Gazebo, robot, bridge, Nav2, and all
          custom nodes. All nodes use ``use_sim_time``,
          ``output="screen"``, and ``emulate_tty=True``.
      * - Launch arguments
        - 2
        - ``enable_debug`` and ``min_detect_range`` arguments work.
          Conditional ``scan_visualizer`` uses ``IfCondition``.
      * - ``GroupAction``
        - 2
        - Custom application nodes grouped in a ``GroupAction``.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, contributions, scenario summary, system
          architecture diagram, simulation description with screenshot
          (including victim placement), lifecycle design, Nav2
          configuration rationale, build/run instructions, known issues.
      * - Code quality
        - 3
        - Type hints, Google-style docstrings, ROS 2 logger with
          correct severity levels, consistent naming, lifecycle
          callbacks commented, detection algorithm commented, no
          linting errors.
      * - **TOTAL**
        - **60**
        -
