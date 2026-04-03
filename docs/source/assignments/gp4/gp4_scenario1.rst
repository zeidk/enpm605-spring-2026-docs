====================================================
Scenario 1: Autonomous Security Patrol
====================================================


Domain
======

A security robot patrols a facility by navigating between checkpoints,
monitoring for intruders using lidar and camera data, and reacting to
detections by investigating suspicious areas. A behavior tree
coordinates the entire system: it manages lifecycle transitions for
patrol and monitoring subsystems, sends navigation goals to Nav2, and
dynamically switches between patrol, investigation, and alert behaviors
based on sensor input.


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
          blackboard, and ticks the tree at 10 Hz. This is the
          top-level coordinator for the entire system.
      * - ``patrol_manager``
        - Lifecycle
        - Manages the patrol mission. In ``on_configure()``, loads
          the list of checkpoint poses from parameters. In
          ``on_activate()``, publishes the current checkpoint goal to
          a topic for the BT to read. In ``on_deactivate()``, stops
          publishing goals. Tracks which checkpoints have been visited.
      * - ``intrusion_detector``
        - Lifecycle
        - Processes sensor data to detect intruders (simulated as
          colored objects in Gazebo). In ``on_configure()``, creates
          subscribers to ``/scan`` (lidar) and ``/camera/image_raw``.
          In ``on_activate()``, begins processing and publishes
          detection results on ``/security/detections``. In
          ``on_deactivate()``, stops processing.
      * - ``alert_manager``
        - Regular
        - Subscribes to ``/security/detections`` and
          ``/security/patrol_status``. Publishes alert messages on
          ``/security/alerts`` when an intrusion is confirmed.
          Maintains an alert log with timestamps and locations.
      * - ``sensor_processor``
        - Regular
        - Subscribes to ``/scan`` (lidar). Performs basic obstacle
          analysis (e.g., detects nearby objects within a configurable
          range). Publishes processed results on
          ``/security/obstacles``. This data is written to the
          blackboard by a BT subscriber node.

   **Behavior Tree Structure**

   The following diagram shows the required high-level structure of
   the behavior tree. You may add additional nodes as needed, but the
   core structure must be present.

   .. code-block:: text

      [Root - Sequence]
      |
      |-- [Setup - Sequence]
      |   |-- ConfigurePatrolManager (Action)
      |   |-- ActivatePatrolManager (Action)
      |   |-- ConfigureIntrusionDetector (Action)
      |   |-- ActivateIntrusionDetector (Action)
      |
      |-- [Main Mission - Repeat Decorator]
      |   |
      |   |-- [Patrol Cycle - Selector]
      |   |   |
      |   |   |-- [Intrusion Response - Sequence]
      |   |   |   |-- IntrusionDetected? (Condition)
      |   |   |   |-- CancelCurrentNav (Action)
      |   |   |   |-- NavigateToDetection (Action - Nav2 goal)
      |   |   |   |-- InvestigateArea (Action - rotate/scan)
      |   |   |   |-- PublishAlert (Action)
      |   |   |   |-- ReturnToPatrol (Action)
      |   |   |
      |   |   |-- [Normal Patrol - Sequence]
      |   |   |   |-- NOT IntrusionDetected? (Condition w/ Inverter)
      |   |   |   |-- GetNextCheckpoint (Action - from blackboard)
      |   |   |   |-- NavigateToCheckpoint (Action - Nav2 goal)
      |   |   |   |-- [Checkpoint Monitoring - Timeout Decorator (10s)]
      |   |   |   |   |-- MonitorArea (Action - wait and scan)
      |   |   |   |-- UpdatePatrolLog (Action)

   .. note::

      The BT structure above is a guideline. You are expected to
      refine it based on your implementation. The key requirement is
      that the tree demonstrates **reactive behavior** -- the
      Intrusion Response branch must preempt Normal Patrol when a
      detection occurs.

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
      * - ``/camera/image_raw``
        - ``sensor_msgs/msg/Image``
        - Camera data from the robot (provided by Gazebo)
      * - ``/security/detections``
        - ``std_msgs/msg/String``
        - JSON-encoded detection results (object type, bearing,
          estimated distance)
      * - ``/security/obstacles``
        - ``std_msgs/msg/String``
        - JSON-encoded obstacle analysis (nearest obstacle distance
          and direction)
      * - ``/security/alerts``
        - ``std_msgs/msg/String``
        - JSON-encoded alert messages (timestamp, location,
          description)
      * - ``/security/patrol_status``
        - ``std_msgs/msg/String``
        - JSON-encoded patrol status (current checkpoint, visited
          count, total count)

   **Services**

   .. list-table::
      :widths: 35 30 35
      :header-rows: 1
      :class: compact-table

      * - Service
        - Type
        - Description
      * - ``/patrol_manager/change_state``
        - ``lifecycle_msgs/srv/ChangeState``
        - Lifecycle transition service (auto-generated by lifecycle
          node)
      * - ``/intrusion_detector/change_state``
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

   In addition to the common BT requirements, Scenario 1 must
   demonstrate:

   1. **Reactive preemption:** The Intrusion Response branch in the
      Selector must take priority over Normal Patrol. When the
      ``IntrusionDetected?`` condition becomes ``SUCCESS`` (i.e., a
      detection is posted to the blackboard), the BT must preempt the
      current patrol navigation and switch to the investigation
      sequence.

   2. **Nav2 goal management:** The BT must be able to:

      - Send a checkpoint navigation goal via ``NavigateToPose``
      - Cancel an in-progress navigation goal when an intrusion is
        detected
      - Send a new goal to navigate to the detection location
      - Resume patrol by sending the next checkpoint goal after
        investigation

   3. **Lifecycle orchestration:** The Setup sequence must configure
      and activate both lifecycle nodes before the main mission begins.
      If configuration or activation fails, the BT must report the
      failure (return ``FAILURE`` to the root).

   4. **Blackboard variables** (minimum):

      - ``checkpoint_poses``: list of patrol checkpoint poses
      - ``current_checkpoint_index``: integer index into the list
      - ``intrusion_detected``: boolean flag
      - ``detection_pose``: the pose of the detected intrusion
      - ``nav_status``: current navigation status (idle, navigating,
        succeeded, failed)
      - ``patrol_manager_state``: lifecycle state of the patrol
        manager
      - ``intrusion_detector_state``: lifecycle state of the detector

   5. **Minimum tree complexity:** The complete BT must have at least
      **15 leaf nodes** (actions + conditions) and at least **3 levels
      of nesting**.


.. dropdown:: Simulation Environment
   :open:

   Create a Gazebo world that represents a facility or building floor
   with the following elements:

   1. **Walls and corridors:** The environment must have walls forming
      rooms or corridors that require Nav2 path planning (not an open
      field).

   2. **Patrol checkpoints:** At least **4 checkpoint locations**
      spread across the environment. These should be positions the
      robot navigates to during patrol.

   3. **Intruder objects:** Place at least **2 colored objects** (e.g.,
      red cylinders or boxes) in the environment to simulate intruders.
      The ``intrusion_detector`` node should detect these based on
      lidar proximity (object within a threshold distance while at or
      near a checkpoint) or camera color detection.

   4. **Obstacles:** Include static obstacles (furniture, barriers)
      that the robot must navigate around.

   5. **Robot:** TurtleBot3 Waffle (preferred, as it includes both
      lidar and camera) or TurtleBot4.


.. dropdown:: Detailed Requirements
   :open:

   In addition to the common requirements in the main GP 4 page:

   1. **Patrol behavior:** The robot must autonomously navigate through
      at least 4 checkpoints in sequence. At each checkpoint, the
      robot must pause for a configurable duration (default 10 seconds)
      to "monitor" the area. The ``patrol_manager`` lifecycle node
      tracks which checkpoints have been visited and provides the next
      goal to the BT via a topic or the blackboard.

   2. **Intrusion detection:** The ``intrusion_detector`` lifecycle
      node must process sensor data and publish detection messages when
      a simulated intruder is identified. Detection can be based on:

      - **Lidar-based:** An unexpected object within a threshold
        distance (e.g., < 1.0 m) at a checkpoint location
      - **Camera-based:** A colored object detected in the camera
        image (e.g., red blob detection using simple thresholding)
      - You must implement at least one of these methods.

   3. **Investigation behavior:** When an intrusion is detected, the
      BT must:

      - Cancel any in-progress navigation goal
      - Navigate to the detection location
      - Perform an investigation action (e.g., rotate 360 degrees to
        scan the area)
      - Publish an alert message with the location and timestamp
      - Resume normal patrol from the next unvisited checkpoint

   4. **Navigation failure recovery:** If a Nav2 goal fails (e.g., the
      goal is unreachable), the BT must handle the failure gracefully
      by:

      - Logging a warning
      - Skipping the failed waypoint and proceeding to the next one
      - Or attempting an alternative route

   5. **Lifecycle transitions during mission:** Demonstrate that the
      BT can deactivate and reactivate the ``intrusion_detector``
      during runtime. For example, deactivate it during navigation
      between checkpoints (to save computation) and reactivate it upon
      arriving at a checkpoint.

   6. **Logging:** All major events must be logged with appropriate
      severity levels:

      - ``INFO``: checkpoint reached, patrol started/completed,
        investigation complete
      - ``WARN``: navigation failure, sensor timeout, detection
        uncertain
      - ``ERROR``: lifecycle transition failure, Nav2 unavailable


.. dropdown:: Scenario 1 Grading Rubric
   :open:

   This rubric details how the 100 points map to Scenario 1
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
          least 15 leaf nodes and 3 levels of nesting.
      * - Reactive preemption
        - 7
        - Intrusion Response branch correctly preempts Normal Patrol
          when a detection occurs. The Selector prioritizes the
          intrusion branch.
      * - Blackboard usage
        - 5
        - Blackboard stores all required variables. BT nodes read and
          write blackboard state correctly. Shared state enables
          coordination between branches.
      * - BT ticking and lifecycle
        - 5
        - BT ticks at the configured rate. Tree starts, runs, and
          shuts down cleanly. ``py_trees`` / ``py_trees_ros`` used
          correctly.
      * - **Lifecycle Management (15 pts)**
        -
        -
      * - Lifecycle node implementation
        - 5
        - ``patrol_manager`` and ``intrusion_detector`` correctly
          implement ``on_configure()``, ``on_activate()``,
          ``on_deactivate()``, and ``on_cleanup()``. State-dependent
          behavior demonstrated.
      * - BT-driven transitions
        - 5
        - BT action nodes call lifecycle transition services.
          Configure and activate during setup. Demonstrate at least
          one deactivate/reactivate cycle during the mission.
      * - Transition error handling
        - 5
        - BT handles failed transitions gracefully (returns FAILURE
          up the tree). Transition timeouts handled.
      * - **Nav2 Integration (20 pts)**
        -
        -
      * - Checkpoint navigation
        - 8
        - Robot navigates to at least 4 checkpoints via
          ``NavigateToPose``. Goals sent correctly with proper pose
          format. Navigation monitored for completion.
      * - Dynamic goal (intrusion)
        - 5
        - Robot navigates to a detection location determined at
          runtime. Goal pose derived from sensor data, not hardcoded.
      * - Goal cancellation
        - 4
        - In-progress navigation goal cancelled when intrusion
          detected. New goal sent after cancellation completes.
      * - Failure recovery
        - 3
        - Navigation failure handled gracefully (skip waypoint or
          attempt alternative).
      * - **Sensor Integration (15 pts)**
        -
        -
      * - Sensor processing
        - 5
        - At least one sensor (lidar or camera) processed by a ROS 2
          node. Detection logic implemented (proximity or color
          detection).
      * - BT condition nodes
        - 5
        - At least two condition nodes check sensor data or system
          state. Conditions correctly return SUCCESS or FAILURE based
          on blackboard values.
      * - Reactive behavior
        - 5
        - Robot demonstrably changes behavior based on sensor input
          during runtime. Investigation triggered by detection, not
          scripted.
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
          Major events logged (checkpoints, detections, transitions).
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
          descriptions, design decision rationale.
      * - **Demo Video (5 pts)**
        -
        -
      * - Video content
        - 3
        - Video shows complete patrol cycle, intrusion detection and
          investigation, lifecycle transitions in logs, Nav2
          navigation.
      * - Video quality
        - 2
        - 2--3 minutes, narrated or captioned, clearly shows all
          required behaviors.
      * - **TOTAL**
        - **100**
        -
