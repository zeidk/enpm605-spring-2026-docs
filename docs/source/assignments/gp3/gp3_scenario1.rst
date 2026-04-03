====================================================
Scenario 1: Warehouse Patrol Robot
====================================================


Domain
======

A warehouse facility uses an autonomous patrol robot to perform
periodic security and safety inspections. The robot navigates between
predefined waypoints throughout the warehouse, monitors its
surroundings using lidar to detect unexpected obstacles, and reports
patrol status. The patrol system is managed through lifecycle node
state transitions, allowing operators to configure patrol routes,
activate patrols, pause them during shift changes, and cleanly shut
down at the end of operations.


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
      * - ``patrol_manager`` *(lifecycle)*
        - A lifecycle node that manages the patrol mission. In
          ``on_configure``: loads a list of waypoints from parameters
          (at least 4 waypoints as ``[x, y, yaw]`` triples), creates
          the ``BasicNavigator`` instance, and creates a publisher for
          patrol status. In ``on_activate``: waits for Nav2 to be
          active, sets the initial pose, and begins sending the first
          waypoint goal. In ``on_deactivate``: cancels the current
          navigation goal and pauses the patrol. In ``on_cleanup``:
          destroys the navigator and resets internal state. While active,
          the node iterates through waypoints in a loop (returning to
          the first waypoint after the last). Publishes patrol status on
          ``/patrol/status`` after each waypoint is reached.
      * - ``obstacle_detector``
        - Subscribes to ``/scan`` (``sensor_msgs/LaserScan``). Analyzes
          lidar data to detect obstacles closer than a configurable
          threshold (default 0.5 m). Publishes an
          ``std_msgs/msg/String`` alert on ``/patrol/obstacles`` when
          an obstacle is detected, including the direction (front, left,
          right) and distance. Uses ``self.get_logger().warn()`` for
          obstacle alerts.
      * - ``patrol_reporter``
        - Subscribes to ``/patrol/status`` and ``/patrol/obstacles``.
          Maintains a log of all patrol events (waypoints reached,
          obstacles detected, timestamps). Publishes a
          ``std_msgs/msg/String`` summary on ``/patrol/report`` at
          0.2 Hz containing the total waypoints visited, obstacles
          detected, and current patrol state.
      * - ``rviz_logger`` *(optional, conditional)*
        - Subscribes to ``/patrol/status`` and logs all patrol events
          for debugging. Started only when ``enable_debug`` launch
          argument is ``true``.

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
      * - ``/patrol/status``
        - ``std_msgs/msg/String``
        - JSON-formatted status updates: ``{"waypoint_index": 2,
          "waypoint": [3.0, 1.5, 0.0], "status": "reached",
          "timestamp": "..."}``.
      * - ``/patrol/obstacles``
        - ``std_msgs/msg/String``
        - JSON-formatted obstacle alerts: ``{"direction": "front",
          "distance": 0.35, "timestamp": "..."}``.
      * - ``/patrol/report``
        - ``std_msgs/msg/String``
        - JSON-formatted patrol summary with cumulative statistics.

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
        - Used by ``patrol_manager`` via ``BasicNavigator.goToPose()``
          to send the robot to each waypoint.


.. dropdown:: Simulation Environment
   :open:

   **World description:**

   Create or adapt an SDF world representing a simplified warehouse
   environment. The world must include:

   - A rectangular floor area (at least 10 m x 8 m).
   - At least 4 walls forming the warehouse perimeter.
   - At least 3 interior obstacles representing shelving units or
     storage racks (simple box shapes of varying sizes, e.g.,
     2 m x 0.5 m x 1.5 m).
   - At least 1 narrow passage (approximately 1.0--1.5 m wide)
     between obstacles that tests the robot's navigation capability.
   - A clear patrol path that visits all four quadrants of the
     warehouse.

   **Robot model:**

   Use a differential-drive robot with the following minimum sensors:

   - A 2D lidar with 360-degree coverage and at least 5 m range.
   - A ``DiffDrive`` Gazebo plugin for velocity control.

   You may use TurtleBot3 (Waffle or Burger), a custom SDF model, or
   any differential-drive robot that meets these requirements. Document
   your choice in ``README.md``.


.. dropdown:: Detailed Requirements
   :open:

   In addition to the common requirements on the main GP 3 page:

   1. **Lifecycle node -- patrol_manager**:

      - ``on_configure``: Read waypoints from ROS parameters. The node
        must declare a parameter ``waypoints`` as a list of doubles
        (flattened: ``[x1, y1, yaw1, x2, y2, yaw2, ...]``). Parse
        these into a list of ``PoseStamped`` goals. Create the
        ``BasicNavigator`` instance and the ``/patrol/status``
        publisher. Log the number of waypoints loaded.
      - ``on_activate``: Call ``navigator.waitUntilNav2Active()``. Set
        the initial pose using ``navigator.setInitialPose()``. Send
        the first waypoint goal using ``navigator.goToPose()``. Start
        a timer (1 Hz) that checks ``navigator.isTaskComplete()`` and
        advances to the next waypoint when the current goal is reached.
      - ``on_deactivate``: Call ``navigator.cancelTask()`` to stop the
        robot. Cancel the monitoring timer. Log that the patrol is
        paused.
      - ``on_cleanup``: Destroy the navigator and publisher. Reset the
        waypoint index. Log that cleanup is complete.

   2. **Waypoint cycling**: After reaching the last waypoint, the
      patrol robot returns to the first waypoint and continues the
      patrol loop indefinitely (until deactivated).

   3. **Navigation feedback**: During each timer callback (while the
      robot is navigating to a waypoint), retrieve feedback using
      ``navigator.getFeedback()`` and log the estimated distance
      remaining. If navigation fails (``navigator.getResult()``
      returns ``TaskResult.FAILED``), log an error and attempt to
      navigate to the next waypoint.

   4. **Obstacle detector**: The ``obstacle_detector`` node must:

      - Subscribe to ``/scan`` with ``use_sim_time=true``.
      - Divide the lidar scan into three sectors: front
        (approximately -30 to +30 degrees), left (+30 to +90 degrees),
        and right (-90 to -30 degrees).
      - For each sector, compute the minimum distance.
      - If any sector's minimum distance is below the threshold
        (default 0.5 m), publish an alert on ``/patrol/obstacles`` and
        log a warning.
      - The threshold must be configurable via a ROS parameter
        ``obstacle_threshold``.

   5. **Patrol reporter**: The ``patrol_reporter`` node must:

      - Track the total number of waypoints reached.
      - Track the total number of obstacle alerts received.
      - Publish a summary at 0.2 Hz with cumulative statistics.
      - Log each waypoint arrival and each obstacle detection.

   6. **Launch file**:

      - ``system.launch.py``: starts Gazebo, spawns the robot, starts
        ``ros_gz_bridge``, launches Nav2 (using ``nav2_bringup``),
        starts ``patrol_manager``, ``obstacle_detector``, and
        ``patrol_reporter``.
      - ``enable_debug`` argument (default ``false``): conditionally
        starts the ``rviz_logger`` node using ``IfCondition``.
      - ``obstacle_threshold`` argument (default ``0.5``): passed to
        the ``obstacle_detector`` as a ROS parameter override.
      - Custom application nodes (``patrol_manager``,
        ``obstacle_detector``, ``patrol_reporter``) grouped in a
        ``GroupAction``.
      - All custom nodes use ``use_sim_time:=true``.

   7. **Lifecycle management**: After launching, the ``patrol_manager``
      can be controlled via CLI:

      .. code-block:: console

         # Configure the patrol manager (loads waypoints)
         ros2 lifecycle set /patrol_manager configure

         # Activate the patrol (starts navigating)
         ros2 lifecycle set /patrol_manager activate

         # Pause the patrol
         ros2 lifecycle set /patrol_manager deactivate

         # Resume the patrol
         ros2 lifecycle set /patrol_manager activate

         # Clean up and reset
         ros2 lifecycle set /patrol_manager cleanup


.. dropdown:: Scenario 1 Grading Rubric
   :open:

   This rubric details how the 60 points map to Scenario 1 deliverables.

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
        - SDF world loads in Gazebo Harmonic. Contains warehouse walls,
          at least 3 interior obstacles, and a narrow passage. Ground
          plane and lighting configured.
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
        - Loads waypoints from parameters. Creates navigator and
          publisher. Logs waypoint count. Returns SUCCESS or FAILURE
          with appropriate error handling.
      * - ``on_activate``
        - 4
        - Waits for Nav2. Sets initial pose. Sends first waypoint goal.
          Starts monitoring timer. Node begins patrol.
      * - ``on_deactivate``
        - 3
        - Cancels current navigation goal. Stops monitoring timer. Node
          pauses without crashing. Can be re-activated.
      * - ``on_cleanup``
        - 3
        - Destroys navigator, publisher, and timer. Resets waypoint
          index. Node returns to unconfigured state.
      * - **Navigation (14 pts)**
        -
        -
      * - Nav2 configuration
        - 4
        - ``nav2_params.yaml`` correctly configures planner, controller,
          costmaps, and AMCL. Parameters match robot model and world.
      * - Map
        - 2
        - Pre-generated map included in ``maps/`` directory. Map
          accurately represents the warehouse world.
      * - Programmatic goals
        - 4
        - Robot navigates to at least 4 waypoints using
          ``BasicNavigator.goToPose()``. Waypoint cycling works
          (returns to first waypoint after last).
      * - Navigation feedback
        - 2
        - Distance remaining is logged during navigation. Failed
          navigation goals are detected and handled (skip to next
          waypoint).
      * - Goal completion
        - 2
        - Patrol status is published on ``/patrol/status`` after each
          waypoint is reached. Status includes waypoint index and
          coordinates.
      * - **Sensor Processing (8 pts)**
        -
        -
      * - Obstacle detection
        - 4
        - ``obstacle_detector`` correctly analyzes lidar sectors (front,
          left, right). Detects obstacles below threshold. Direction and
          distance included in alerts.
      * - Configurable threshold
        - 2
        - Threshold is a ROS parameter. Can be overridden via launch
          argument.
      * - Alert publishing
        - 2
        - Alerts published on ``/patrol/obstacles``. Warnings logged
          with ``get_logger().warn()``.
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
        - ``enable_debug`` and ``obstacle_threshold`` arguments work.
          Conditional ``rviz_logger`` uses ``IfCondition``.
      * - ``GroupAction``
        - 2
        - Custom application nodes grouped in a ``GroupAction``.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, contributions, scenario summary, system
          architecture diagram, simulation description with screenshot,
          lifecycle design, Nav2 configuration rationale, build/run
          instructions, known issues.
      * - Code quality
        - 3
        - Type hints, Google-style docstrings, ROS 2 logger with
          correct severity levels, consistent naming, lifecycle
          callbacks commented, no linting errors.
      * - **TOTAL**
        - **60**
        -
