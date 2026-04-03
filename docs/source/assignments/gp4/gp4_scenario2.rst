====================================================
Scenario 2: Hospital Delivery Robot
====================================================


Domain
======

A hospital delivery robot transports supplies between stations --
pharmacy, patient rooms, and nurse stations -- using a behavior tree to
coordinate its mission. The BT manages lifecycle transitions for
delivery management and sensor subsystems, navigates between stations
via Nav2, maintains a delivery queue through the blackboard, and reacts
to blocked paths and delivery priorities. The system must handle
multiple deliveries in sequence and adapt to dynamic conditions such as
obstacles blocking corridors.


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
          blackboard with the delivery queue, and ticks the tree at
          10 Hz. This is the top-level coordinator for the entire
          system.
      * - ``delivery_manager``
        - Lifecycle
        - Manages the delivery mission. In ``on_configure()``, loads
          station locations and initializes the delivery queue from
          parameters. In ``on_activate()``, begins publishing the
          current delivery task to ``/hospital/current_task``. In
          ``on_deactivate()``, pauses task publishing. Tracks delivery
          completions and maintains statistics.
      * - ``corridor_monitor``
        - Lifecycle
        - Monitors corridor conditions using lidar data. In
          ``on_configure()``, creates a subscriber to ``/scan``. In
          ``on_activate()``, begins processing lidar data and
          publishes corridor status on ``/hospital/corridor_status``
          (clear, partially blocked, fully blocked). In
          ``on_deactivate()``, stops monitoring.
      * - ``delivery_status_reporter``
        - Regular
        - Subscribes to ``/hospital/delivery_events`` and maintains
          a delivery log. Publishes periodic summary reports on
          ``/hospital/delivery_report`` at 0.5 Hz. Tracks delivery
          times, success/failure counts, and current queue depth.
      * - ``sensor_processor``
        - Regular
        - Subscribes to ``/scan`` (lidar). Detects nearby objects and
          classifies corridor conditions (clear path vs. obstacle).
          Publishes processed results on ``/hospital/obstacles``.
          This data feeds into the BT through blackboard subscribers.

   **Behavior Tree Structure**

   The following diagram shows the required high-level structure of
   the behavior tree. You may add additional nodes as needed, but the
   core structure must be present.

   .. code-block:: text

      [Root - Sequence]
      |
      |-- [System Init - Sequence]
      |   |-- ConfigureDeliveryManager (Action)
      |   |-- ActivateDeliveryManager (Action)
      |   |-- ConfigureCorridorMonitor (Action)
      |   |-- ActivateCorridorMonitor (Action)
      |   |-- LoadDeliveryQueue (Action - populate blackboard)
      |
      |-- [Delivery Loop - Repeat Decorator]
      |   |
      |   |-- [Process Delivery - Sequence]
      |   |   |-- DeliveriesRemaining? (Condition - check queue)
      |   |   |-- GetNextDelivery (Action - pop from blackboard queue)
      |   |   |
      |   |   |-- [Pickup Phase - Sequence]
      |   |   |   |-- NavigateToPickup (Action - Nav2 goal to source)
      |   |   |   |-- ConfirmPickup (Action - log + update blackboard)
      |   |   |
      |   |   |-- [Delivery Phase - Selector]
      |   |   |   |
      |   |   |   |-- [Direct Delivery - Sequence]
      |   |   |   |   |-- CorridorClear? (Condition)
      |   |   |   |   |-- NavigateToDestination (Action - Nav2 goal)
      |   |   |   |   |-- ConfirmDelivery (Action - log + update)
      |   |   |   |
      |   |   |   |-- [Blocked Path Recovery - Sequence]
      |   |   |   |   |-- NOT CorridorClear? (Condition w/ Inverter)
      |   |   |   |   |-- LogBlockedPath (Action)
      |   |   |   |   |-- [Retry with Timeout - Timeout Decorator (30s)]
      |   |   |   |   |   |-- [Wait and Retry - Sequence]
      |   |   |   |   |   |   |-- WaitForClearance (Action - 5s pause)
      |   |   |   |   |   |   |-- NavigateToDestination (Action)
      |   |   |   |   |   |   |-- ConfirmDelivery (Action)
      |   |   |   |
      |   |   |   |-- [Skip Delivery - Sequence]
      |   |   |   |   |-- LogDeliverySkipped (Action)
      |   |   |   |   |-- RequeueDelivery (Action - push to back)
      |   |   |
      |   |   |-- PublishDeliveryEvent (Action)

   .. note::

      The BT structure above is a guideline. You are expected to
      refine it based on your implementation. The key requirement is
      that the Delivery Phase Selector demonstrates **fallback
      behavior** -- the robot tries direct delivery first, then
      waits and retries if the corridor is blocked, and finally
      skips the delivery as a last resort.

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
      * - ``/hospital/current_task``
        - ``std_msgs/msg/String``
        - JSON-encoded current delivery task (source station,
          destination station, item type, priority)
      * - ``/hospital/corridor_status``
        - ``std_msgs/msg/String``
        - JSON-encoded corridor condition (clear, partially_blocked,
          fully_blocked, direction, distance_to_obstacle)
      * - ``/hospital/delivery_events``
        - ``std_msgs/msg/String``
        - JSON-encoded delivery events (pickup_complete,
          delivery_complete, delivery_skipped, with timestamps)
      * - ``/hospital/delivery_report``
        - ``std_msgs/msg/String``
        - JSON-encoded summary (total deliveries, completed,
          skipped, average delivery time, queue depth)
      * - ``/hospital/obstacles``
        - ``std_msgs/msg/String``
        - JSON-encoded obstacle data (nearest obstacle distance,
          direction, severity)

   **Services**

   .. list-table::
      :widths: 35 30 35
      :header-rows: 1
      :class: compact-table

      * - Service
        - Type
        - Description
      * - ``/delivery_manager/change_state``
        - ``lifecycle_msgs/srv/ChangeState``
        - Lifecycle transition service (auto-generated by lifecycle
          node)
      * - ``/corridor_monitor/change_state``
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

   In addition to the common BT requirements, Scenario 2 must
   demonstrate:

   1. **Delivery queue management:** The blackboard must maintain a
      delivery queue (list of delivery tasks). Each delivery task is a
      dictionary with at least: ``source`` (pickup station name),
      ``destination`` (drop-off station name), ``item`` (what is being
      delivered), and ``priority`` (normal or urgent). The BT must
      process deliveries in queue order.

   2. **Three-tier fallback:** The Delivery Phase Selector must
      implement a three-tier fallback strategy:

      - **Tier 1:** Direct delivery if the corridor is clear
      - **Tier 2:** Wait for clearance with a timeout, then retry
      - **Tier 3:** Skip the delivery and requeue it at the back of
        the queue

      This demonstrates the power of Selector (Fallback) nodes for
      graceful degradation.

   3. **Lifecycle orchestration:** The System Init sequence must
      configure and activate both lifecycle nodes. Additionally, the
      BT should demonstrate deactivating the ``corridor_monitor``
      when the robot is stationary at a station (to save resources)
      and reactivating it before navigating.

   4. **Blackboard variables** (minimum):

      - ``delivery_queue``: list of pending delivery tasks
      - ``current_delivery``: the delivery task currently in progress
      - ``corridor_status``: current corridor condition (from
        ``corridor_monitor``)
      - ``nav_status``: navigation status (idle, navigating,
        succeeded, failed)
      - ``deliveries_completed``: count of successful deliveries
      - ``deliveries_skipped``: count of skipped deliveries
      - ``delivery_manager_state``: lifecycle state
      - ``corridor_monitor_state``: lifecycle state
      - ``station_poses``: dictionary mapping station names to poses

   5. **Minimum tree complexity:** The complete BT must have at least
      **15 leaf nodes** (actions + conditions) and at least **3 levels
      of nesting**.


.. dropdown:: Simulation Environment
   :open:

   Create a Gazebo world that represents a simplified hospital floor
   with the following elements:

   1. **Hospital layout:** The environment must include walls forming
      corridors connecting at least 4 distinct stations. The layout
      should require Nav2 path planning (not a straight-line path
      between all stations).

   2. **Stations:** At least **4 named stations** positioned at
      identifiable locations:

      - **Pharmacy** -- the primary pickup location for deliveries
      - **Room 101** -- a patient room (delivery destination)
      - **Room 102** -- a second patient room (delivery destination)
      - **Nurse Station** -- a drop-off/pickup point for supplies

   3. **Corridor obstacles:** Place at least **1 movable or static
      obstacle** in a corridor to simulate a blocked path. The
      ``corridor_monitor`` should detect this obstacle using lidar
      data and report the corridor as blocked, triggering the fallback
      behavior in the BT.

   4. **Station markers:** Place colored or distinctive objects at each
      station location to visually identify them in the simulation
      (e.g., colored boxes or signs).

   5. **Robot:** TurtleBot3 Waffle (preferred) or TurtleBot4. The
      robot must have a lidar sensor.


.. dropdown:: Detailed Requirements
   :open:

   In addition to the common requirements in the main GP 4 page:

   1. **Delivery queue:** Initialize the delivery queue with at least
      **4 delivery tasks** that cover different source-destination
      pairs. For example:

      - Pharmacy to Room 101 (medication, normal priority)
      - Pharmacy to Room 102 (medication, urgent priority)
      - Nurse Station to Room 101 (supplies, normal priority)
      - Pharmacy to Nurse Station (equipment, normal priority)

      The queue must be stored on the blackboard and managed by BT
      action nodes (``GetNextDelivery`` pops the front of the queue,
      ``RequeueDelivery`` pushes a skipped delivery to the back).

   2. **Pickup and delivery confirmation:** At each station, the robot
      must:

      - Log arrival at the station (``INFO`` level)
      - Pause briefly (2--3 seconds) to simulate loading/unloading
      - Publish a delivery event (pickup or delivery) to
        ``/hospital/delivery_events``
      - Update the blackboard with the delivery status

   3. **Corridor monitoring and blocked path handling:** The
      ``corridor_monitor`` lifecycle node must:

      - Process lidar data to detect obstacles in the forward path
      - Classify the corridor as ``clear`` (no obstacles within 2 m),
        ``partially_blocked`` (obstacles within 2 m but a path exists),
        or ``fully_blocked`` (obstacle directly ahead within 0.5 m)
      - Publish the status on ``/hospital/corridor_status``
      - The BT ``CorridorClear?`` condition node must read this status
        from the blackboard

   4. **Navigation between stations:** The robot must navigate to at
      least **3 distinct stations** during a single mission run using
      Nav2 ``NavigateToPose``. Station poses must be loaded from
      parameters or a configuration file, not hardcoded in the BT
      nodes.

   5. **Delivery status reporting:** The ``delivery_status_reporter``
      node must publish periodic reports including:

      - Total deliveries attempted
      - Successful deliveries
      - Skipped deliveries (due to blocked paths)
      - Current queue depth
      - Average time per delivery

   6. **Navigation failure recovery:** If Nav2 fails to reach a
      station, the BT must:

      - Log a warning
      - Mark the delivery as skipped
      - Requeue the delivery at the back of the queue
      - Proceed to the next delivery

   7. **Logging:** All major events must be logged with appropriate
      severity levels:

      - ``INFO``: arrived at station, pickup/delivery complete,
        delivery report published
      - ``WARN``: corridor blocked, delivery requeued, navigation
        taking longer than expected
      - ``ERROR``: lifecycle transition failure, Nav2 unavailable,
        delivery queue empty unexpectedly


.. dropdown:: Scenario 2 Grading Rubric
   :open:

   This rubric details how the 100 points map to Scenario 2
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
      * - Three-tier fallback
        - 7
        - Delivery Phase Selector implements direct delivery,
          wait-and-retry, and skip-and-requeue tiers. Fallback
          behavior demonstrated with a blocked corridor.
      * - Blackboard usage
        - 5
        - Blackboard stores delivery queue, current delivery,
          corridor status, nav status, station poses, and lifecycle
          states. Queue operations (pop, push) work correctly.
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
        - ``delivery_manager`` and ``corridor_monitor`` correctly
          implement ``on_configure()``, ``on_activate()``,
          ``on_deactivate()``, and ``on_cleanup()``. State-dependent
          behavior demonstrated (e.g., corridor monitoring only when
          active).
      * - BT-driven transitions
        - 5
        - BT action nodes call lifecycle transition services.
          Configure and activate during setup. Demonstrate at least
          one deactivate/reactivate cycle during the mission (e.g.,
          corridor monitor toggled during station stops).
      * - Transition error handling
        - 5
        - BT handles failed transitions gracefully (returns FAILURE
          up the tree). Transition timeouts handled.
      * - **Nav2 Integration (20 pts)**
        -
        -
      * - Station navigation
        - 8
        - Robot navigates to at least 3 distinct stations via
          ``NavigateToPose``. Goals sent correctly with proper pose
          format. Navigation monitored for completion.
      * - Dynamic goal selection
        - 5
        - At least one navigation goal determined at runtime from
          the delivery queue (destination varies by delivery task).
          Not all goals hardcoded.
      * - Pickup-delivery sequence
        - 4
        - Robot navigates to source station, then to destination
          station. Both pickup and delivery confirmed with logs and
          events.
      * - Failure recovery
        - 3
        - Navigation failure handled gracefully (delivery skipped
          and requeued, next delivery attempted).
      * - **Sensor Integration (15 pts)**
        -
        -
      * - Corridor monitoring
        - 5
        - Lidar data processed to classify corridor conditions
          (clear, partially blocked, fully blocked). Published on
          topic and available on blackboard.
      * - BT condition nodes
        - 5
        - ``CorridorClear?`` and ``DeliveriesRemaining?`` condition
          nodes correctly check blackboard values. Return
          SUCCESS/FAILURE appropriately.
      * - Reactive behavior
        - 5
        - Robot demonstrably changes behavior when corridor is
          blocked (waits, retries, or skips). Not scripted -- reacts
          to actual sensor data.
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
          Major events logged (station arrivals, deliveries, corridor
          status changes).
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
          blackboard variable documentation (especially delivery
          queue structure), lifecycle state descriptions, design
          decision rationale.
      * - **Demo Video (5 pts)**
        -
        -
      * - Video content
        - 3
        - Video shows at least 2 complete deliveries, blocked
          corridor handling, lifecycle transitions in logs, Nav2
          navigation between stations.
      * - Video quality
        - 2
        - 2--3 minutes, narrated or captioned, clearly shows all
          required behaviors.
      * - **TOTAL**
        - **100**
        -
