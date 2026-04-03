====================================================
Scenario 3: Delivery Robot System
====================================================


Domain
======

A campus or office building uses an autonomous delivery robot to
transport items between locations. A delivery coordinator receives
delivery requests (pickup and dropoff locations), plans the route,
and commands the robot to navigate to the pickup point, confirm the
item is loaded, then navigate to the dropoff point and confirm
delivery. The coordinator is a lifecycle node, allowing the facility
manager to configure the delivery zones, activate the delivery
service, pause deliveries during off-hours, and cleanly reset the
system for a new shift.


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
      * - ``delivery_coordinator`` *(lifecycle)*
        - A lifecycle node that manages delivery missions. In
          ``on_configure``: loads delivery zones from parameters (at
          least 3 named zones, each with ``[x, y, yaw]`` coordinates),
          creates the ``BasicNavigator`` instance, creates publishers
          for delivery status and a subscriber for delivery requests,
          and initializes the delivery queue. In ``on_activate``: waits
          for Nav2, sets the initial pose, and begins processing the
          delivery queue. In ``on_deactivate``: cancels the current
          navigation goal, pauses delivery processing, and preserves
          the remaining queue. In ``on_cleanup``: destroys the
          navigator, clears the queue, resets delivery statistics, and
          releases all resources. While active, processes deliveries
          one at a time: navigate to pickup, wait 3 seconds (simulated
          loading), navigate to dropoff, wait 3 seconds (simulated
          unloading), then process the next delivery.
      * - ``request_generator``
        - Publishes ``std_msgs/msg/String`` delivery requests on
          ``/delivery/requests`` at 0.1 Hz (one request every 10
          seconds). Each request is a JSON string with fields
          ``request_id`` (incrementing integer), ``pickup_zone``
          (string, e.g., ``"zone_a"``), and ``dropoff_zone`` (string,
          e.g., ``"zone_c"``). Randomly selects different pickup and
          dropoff zones from the configured zone list.
      * - ``proximity_monitor``
        - Subscribes to ``/scan`` (``sensor_msgs/LaserScan``). Monitors
          the robot's surroundings during delivery navigation. If any
          obstacle is detected within a configurable safety radius
          (default 0.3 m), publishes a ``std_msgs/msg/String`` warning
          on ``/delivery/safety`` and logs with
          ``self.get_logger().warn()``. Tracks the number of close-call
          events per delivery.
      * - ``delivery_tracker``
        - Subscribes to ``/delivery/status`` and ``/delivery/safety``.
          Maintains a record of all deliveries: request ID, pickup
          zone, dropoff zone, status (queued / in-transit-pickup /
          loading / in-transit-dropoff / unloading / completed /
          failed), duration, and safety events. Publishes a
          ``std_msgs/msg/String`` summary on ``/delivery/report`` at
          0.2 Hz with cumulative delivery statistics.
      * - ``delivery_logger`` *(optional, conditional)*
        - Subscribes to ``/delivery/status``, ``/delivery/requests``,
          and ``/delivery/safety``, and logs all events for debugging.
          Started only when ``enable_debug`` launch argument is
          ``true``.

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
      * - ``/delivery/requests``
        - ``std_msgs/msg/String``
        - JSON-formatted delivery request: ``{"request_id": 1,
          "pickup_zone": "zone_a", "dropoff_zone": "zone_c"}``.
      * - ``/delivery/status``
        - ``std_msgs/msg/String``
        - JSON-formatted delivery status: ``{"request_id": 1,
          "phase": "in-transit-pickup"|"loading"|"in-transit-dropoff"|
          "unloading"|"completed"|"failed", "current_zone": "zone_a",
          "timestamp": "..."}``.
      * - ``/delivery/safety``
        - ``std_msgs/msg/String``
        - JSON-formatted safety alert: ``{"min_distance": 0.25,
          "direction": "front", "request_id": 1, "timestamp": "..."}``.
      * - ``/delivery/report``
        - ``std_msgs/msg/String``
        - JSON-formatted delivery statistics: total deliveries
          requested, completed, failed, in progress, and total safety
          events.

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
        - Used by ``delivery_coordinator`` via
          ``BasicNavigator.goToPose()`` to navigate to pickup and
          dropoff zones.


.. dropdown:: Simulation Environment
   :open:

   **World description:**

   Create or adapt an SDF world representing a simplified office or
   campus building with designated delivery zones. The world must
   include:

   - A floor area of at least 12 m x 10 m.
   - At least 4 walls forming the building perimeter.
   - Interior walls or partitions creating at least 3 distinct zones
     (e.g., ``zone_a``, ``zone_b``, ``zone_c``) connected by
     corridors or doorways.
   - At least 1 narrow corridor (approximately 1.0--1.5 m wide)
     between zones.
   - A designated "home" position where the robot starts and returns
     to when idle.
   - Visual markers (e.g., colored boxes on the floor) at each zone
     location to help identify delivery points in the simulation.

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

   1. **Lifecycle node -- delivery_coordinator**:

      - ``on_configure``: Read delivery zones from ROS parameters. The
        node must declare a parameter ``delivery_zones`` as a list of
        strings (e.g., ``["zone_a", "zone_b", "zone_c"]``) and
        corresponding coordinates as a parameter ``zone_coordinates``
        as a list of doubles (flattened:
        ``[x_a, y_a, yaw_a, x_b, y_b, yaw_b, ...]``). Parse these
        into a dictionary mapping zone names to ``PoseStamped`` goals.
        Create the ``BasicNavigator`` instance, the ``/delivery/status``
        publisher, and a subscriber to ``/delivery/requests``.
        Initialize an empty delivery queue (Python ``deque``). Log the
        configured zones.
      - ``on_activate``: Call ``navigator.waitUntilNav2Active()``. Set
        the initial pose using ``navigator.setInitialPose()``. Start a
        timer (1 Hz) that checks the delivery queue and processes the
        next delivery if the robot is idle. Log that the delivery
        service is active.
      - ``on_deactivate``: Call ``navigator.cancelTask()`` to stop the
        robot mid-delivery if necessary. Cancel the processing timer.
        Preserve the delivery queue (do not clear it). Log the number
        of remaining deliveries in the queue.
      - ``on_cleanup``: Destroy the navigator, publishers, subscribers,
        and timer. Clear the delivery queue. Reset delivery counters
        (completed, failed). Log that cleanup is complete.

   2. **Delivery request handling**: The ``/delivery/requests``
      subscription callback validates incoming requests (both zones
      must exist in the configured zone dictionary and pickup must
      differ from dropoff). Valid requests are added to the delivery
      queue. Invalid requests are logged with
      ``self.get_logger().error()`` and discarded.

   3. **Delivery execution sequence**: For each delivery, the
      coordinator follows this sequence:

      a. Publish ``"in-transit-pickup"`` status. Navigate to the pickup
         zone using ``navigator.goToPose()``.
      b. On arrival, publish ``"loading"`` status. Wait 3 seconds
         (simulated loading).
      c. Publish ``"in-transit-dropoff"`` status. Navigate to the
         dropoff zone.
      d. On arrival, publish ``"unloading"`` status. Wait 3 seconds
         (simulated unloading).
      e. Publish ``"completed"`` status. Increment the completed
         delivery counter. Process the next delivery in the queue.

      If navigation to either the pickup or dropoff zone fails, publish
      ``"failed"`` status, log an error, increment the failed counter,
      and skip to the next delivery.

   4. **Navigation feedback**: During navigation to each zone, retrieve
      feedback using ``navigator.getFeedback()`` and log the estimated
      distance remaining every 2 seconds (not every timer tick -- use a
      counter or time check to throttle feedback logging).

   5. **Proximity monitor**: The ``proximity_monitor`` node must:

      - Subscribe to ``/scan`` with ``use_sim_time=true``.
      - Compute the minimum distance across all lidar rays.
      - If the minimum distance is below the safety radius (default
        0.3 m), publish an alert on ``/delivery/safety`` and log a
        warning.
      - Include the direction of the closest obstacle (divide the scan
        into front, left, right, and rear quadrants).
      - The safety radius must be configurable via a ROS parameter
        ``safety_radius``.
      - Apply a cooldown of 5 seconds between alerts to avoid flooding.

   6. **Delivery tracker**: The ``delivery_tracker`` node must:

      - Track the total number of delivery requests received (from
        ``/delivery/status`` messages with ``"in-transit-pickup"``
        phase).
      - Track the number of completed and failed deliveries.
      - Track the number of safety events from ``/delivery/safety``.
      - Publish a summary at 0.2 Hz with all statistics.

   7. **Request generator**: The ``request_generator`` node must:

      - Publish a new delivery request every 10 seconds.
      - Randomly select pickup and dropoff zones (ensuring they
        differ).
      - Use an incrementing ``request_id`` starting from 1.
      - The zone names must match the zones configured in the
        ``delivery_coordinator``.

   8. **Launch file**:

      - ``system.launch.py``: starts Gazebo, spawns the robot, starts
        ``ros_gz_bridge``, launches Nav2, starts
        ``delivery_coordinator``, ``request_generator``,
        ``proximity_monitor``, and ``delivery_tracker``.
      - ``enable_debug`` argument (default ``false``): conditionally
        starts the ``delivery_logger`` node using ``IfCondition``.
      - ``safety_radius`` argument (default ``0.3``): passed to the
        ``proximity_monitor`` as a ROS parameter override.
      - Custom application nodes (``delivery_coordinator``,
        ``request_generator``, ``proximity_monitor``,
        ``delivery_tracker``) grouped in a ``GroupAction``.
      - All custom nodes use ``use_sim_time:=true``.

   9. **Lifecycle management**: After launching, the
      ``delivery_coordinator`` can be controlled via CLI:

      .. code-block:: console

         # Configure the delivery system (loads zones)
         ros2 lifecycle set /delivery_coordinator configure

         # Activate the delivery service (starts processing requests)
         ros2 lifecycle set /delivery_coordinator activate

         # Pause deliveries (e.g., off-hours)
         ros2 lifecycle set /delivery_coordinator deactivate

         # Resume deliveries (queue is preserved)
         ros2 lifecycle set /delivery_coordinator activate

         # Clean up and reset for a new shift
         ros2 lifecycle set /delivery_coordinator cleanup


.. dropdown:: Scenario 3 Grading Rubric
   :open:

   This rubric details how the 60 points map to Scenario 3 deliverables.

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
        - SDF world loads in Gazebo Harmonic. Contains building walls,
          at least 3 distinct zones connected by corridors or doorways,
          and visual markers at zone locations. Ground plane and
          lighting configured.
      * - Robot spawn
        - 3
        - Robot model spawns at the designated home position via the
          launch file. Differential-drive plugin is functional (robot
          responds to ``/cmd_vel``).
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
        - Loads delivery zones from parameters. Creates navigator,
          publishers, subscriber, and delivery queue. Logs configured
          zones. Returns SUCCESS or FAILURE with appropriate error
          handling.
      * - ``on_activate``
        - 4
        - Waits for Nav2. Sets initial pose. Starts queue processing
          timer. Begins processing deliveries. Logs activation.
      * - ``on_deactivate``
        - 3
        - Cancels current navigation goal. Stops timer. Preserves
          delivery queue (does not clear it). Logs remaining queue
          size. Can be re-activated to resume.
      * - ``on_cleanup``
        - 3
        - Destroys navigator, publishers, subscriber, timer. Clears
          delivery queue. Resets counters. Node returns to unconfigured
          state.
      * - **Navigation (14 pts)**
        -
        -
      * - Nav2 configuration
        - 4
        - ``nav2_params.yaml`` correctly configures planner, controller,
          costmaps, and AMCL. Parameters suitable for indoor navigation
          through corridors and doorways.
      * - Map
        - 2
        - Pre-generated map included in ``maps/`` directory. Map
          accurately represents the building with zones and corridors.
      * - Delivery navigation sequence
        - 4
        - Robot navigates to pickup zone, waits 3 s, navigates to
          dropoff zone, waits 3 s. Full pickup-to-dropoff cycle works.
          At least 3 zones used as destinations.
      * - Navigation feedback
        - 2
        - Distance remaining is logged during navigation (throttled to
          every 2 seconds). Failed navigation goals are detected and
          handled (delivery marked as failed, skip to next).
      * - Request handling
        - 2
        - Delivery requests are validated (zones exist, pickup differs
          from dropoff). Valid requests added to queue. Invalid requests
          logged as errors and discarded.
      * - **Sensor Processing (8 pts)**
        -
        -
      * - Proximity monitoring
        - 4
        - ``proximity_monitor`` computes minimum lidar distance.
          Detects obstacles below safety radius. Direction (front,
          left, right, rear) included in alerts.
      * - Configurable radius
        - 2
        - Safety radius is a ROS parameter. Can be overridden via
          launch argument.
      * - Alert cooldown
        - 2
        - Alerts are suppressed for 5 seconds after each alert to
          prevent flooding.
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
        - ``enable_debug`` and ``safety_radius`` arguments work.
          Conditional ``delivery_logger`` uses ``IfCondition``.
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
          (including zone markers), lifecycle design (especially queue
          preservation on deactivate), Nav2 configuration rationale,
          build/run instructions, known issues.
      * - Code quality
        - 3
        - Type hints, Google-style docstrings, ROS 2 logger with
          correct severity levels, consistent naming, lifecycle
          callbacks commented, delivery state machine commented, no
          linting errors.
      * - **TOTAL**
        - **60**
        -
