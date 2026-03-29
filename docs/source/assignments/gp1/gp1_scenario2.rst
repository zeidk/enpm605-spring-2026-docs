====================================================
Scenario 2: Robot Fleet Dispatcher
====================================================


Domain
======

A warehouse management system dispatches tasks to a fleet of mobile
robots. A central dispatcher node publishes task assignments, each
robot node receives its tasks and reports status updates, and a
monitor node tracks fleet throughput and detects stalled robots.


.. dropdown:: System Architecture
   :open:

   Your system must contain the following nodes and topics.

   **Nodes**

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Node
        - Description
      * - ``dispatcher``
        - Publishes ``std_msgs/msg/String`` task assignments on
          ``/fleet/tasks`` at 1 Hz. Each message contains a JSON-formatted
          string with fields ``robot_id`` (string) and ``task``
          (string, e.g., ``"pick_shelf_A3"``, ``"deliver_dock_2"``).
          Cycles through robot IDs ``"robot_1"``, ``"robot_2"``,
          ``"robot_3"`` in round-robin order.
      * - ``robot_1``
        - Subscribes to ``/fleet/tasks``. Filters messages where
          ``robot_id == "robot_1"``. Simulates task execution with a
          short sleep (0.5 s). Publishes status on
          ``/fleet/status`` as ``std_msgs/msg/String`` with fields
          ``robot_id``, ``status`` (``"busy"``/``"done"``), and
          ``task``.
      * - ``robot_2``
        - Same as ``robot_1`` but filters for ``"robot_2"``. Simulates
          a **slow** robot with a 2 s sleep to demonstrate queue
          buildup.
      * - ``robot_3``
        - Same as ``robot_1`` but filters for ``"robot_3"``. Uses a
          0.3 s sleep (fast robot).
      * - ``monitor``
        - Subscribes to ``/fleet/status``. Tracks the number of
          completed tasks per robot and the last status timestamp.
          Publishes a ``std_msgs/msg/String`` summary on
          ``/fleet/report`` at 0.5 Hz. Uses ``self.get_logger().warn()``
          if any robot has not reported in 5 seconds.
      * - ``debug_logger`` *(optional, conditional)*
        - Subscribes to ``/fleet/tasks`` and ``/fleet/status`` and
          logs all messages. Started only when ``enable_debug`` is
          ``true``.

   **Topics**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - QoS
      * - ``/fleet/tasks``
        - ``std_msgs/msg/String``
        - ``RELIABLE``, ``TRANSIENT_LOCAL``, depth 5
      * - ``/fleet/status``
        - ``std_msgs/msg/String``
        - ``BEST_EFFORT``, ``VOLATILE``, depth 3
      * - ``/fleet/report``
        - ``std_msgs/msg/String``
        - ``RELIABLE``, ``VOLATILE``


.. dropdown:: Specific Requirements
   :open:

   In addition to the common requirements in the main GP 1 page:

   1. **QoS -- TRANSIENT_LOCAL**: The ``dispatcher`` publishes on
      ``/fleet/tasks`` with ``TRANSIENT_LOCAL`` and depth 5. If a robot
      node starts late, it immediately receives the last 5 task messages.
      Demonstrate this by starting ``robot_3`` 5 seconds after the
      dispatcher and verifying it receives backlogged tasks.

   2. **QoS -- Intentional mismatch**: Create a test subscriber (can be
      in the ``monitor`` node or a separate debug node) that subscribes
      to ``/fleet/status`` using ``RELIABLE`` reliability. The
      ``/fleet/status`` publisher uses ``BEST_EFFORT``. A ``RELIABLE``
      subscriber cannot connect to a ``BEST_EFFORT`` publisher -- this is
      incompatible and will receive no data. Add comments in the code
      documenting the mismatch and how to diagnose it with
      ``ros2 topic info /fleet/status -v``.

   3. **Slow robot and queue overflow**: ``robot_2`` sleeps for 2 s per
      task but receives tasks every 3 s (round-robin with 3 robots at
      1 Hz = one task per robot every 3 s). This is manageable. To
      demonstrate overflow, temporarily increase the dispatch rate or
      decrease the queue depth and document the observation in
      ``README.md``.

   4. **Monitor callback groups**: The ``monitor`` node must use a
      ``MultiThreadedExecutor``. The ``/fleet/status`` subscription
      callback must be in a ``MutuallyExclusiveCallbackGroup`` (it
      updates shared dictionaries tracking per-robot counts and
      timestamps). The report-publishing timer must be in a
      ``ReentrantCallbackGroup``.

   5. **Robot node callback groups**: Each robot node has two callbacks
      (task subscription and status publishing timer). These must be in
      a ``MutuallyExclusiveCallbackGroup`` because the subscription
      callback writes to shared state (current task) that the status
      publisher reads.

   6. **Launch files**:

      - ``system.launch.py``: starts the dispatcher, all three robot
        nodes, and the monitor.
      - ``enable_debug`` argument (default ``false``): conditionally
        starts the ``debug_logger`` node.
      - Robot nodes grouped in a ``GroupAction``.


.. dropdown:: Expected Behavior
   :open:

   **Normal operation:**

   .. code-block:: text

      [INFO] [<timestamp>] [dispatcher]: Assigned task pick_shelf_A3 to robot_1
      [INFO] [<timestamp>] [robot_1]: Received task pick_shelf_A3 -- executing...
      [INFO] [<timestamp>] [robot_1]: Task pick_shelf_A3 complete
      [INFO] [<timestamp>] [dispatcher]: Assigned task deliver_dock_2 to robot_2
      [INFO] [<timestamp>] [robot_2]: Received task deliver_dock_2 -- executing...
      [INFO] [<timestamp>] [monitor]: Fleet report -- robot_1: 3 tasks, robot_2: 1 tasks, robot_3: 4 tasks

   **Robot stalled** -- to test this, run ``robot_2`` separately with
   ``ros2 run`` in its own terminal instead of the launch file, then
   stop it with Ctrl-C:

   .. code-block:: console

      # Terminal 1: launch the system without robot_2
      ros2 launch group<N>_gp1 system.launch.py start_robot_2:=false

      # Terminal 2: start robot_2 manually
      ros2 run group<N>_gp1 robot_2

      # Press Ctrl-C in Terminal 2 to simulate a stalled robot

   The monitor should detect the silence and log:

   .. code-block:: text

      [WARNING] [<timestamp>] [monitor]: robot_2 has not reported in 5.0 s

   .. note::

      To support this testing workflow, add a ``start_robot_2`` launch
      argument (default ``true``) with an ``IfCondition`` on the
      ``robot_2`` node.

   **Verification commands:**

   .. code-block:: console

      ros2 launch group<N>_gp1 system.launch.py
      ros2 launch group<N>_gp1 system.launch.py enable_debug:=true
      ros2 topic list -t
      ros2 topic echo /fleet/tasks
      ros2 topic echo /fleet/status
      ros2 topic hz /fleet/status
      ros2 topic info /fleet/tasks -v
      rqt_graph


.. dropdown:: Scenario 2 Grading Rubric
   :open:

   This rubric details how the 50 points from the
   `common rubric <gp1.html#grading-rubric>`_ map to Scenario 2
   deliverables.

   .. list-table::
      :widths: 40 8 52
      :header-rows: 1
      :class: compact-table

      * - Component
        - Pts
        - Criteria
      * - **Node Implementation (16 pts)**
        -
        -
      * - ``dispatcher``
        - 3
        - Publishes ``String`` (JSON) on ``/fleet/tasks`` at 1 Hz.
          Round-robin assignment across three robot IDs. OOP node with
          timer callback.
      * - ``robot_1``
        - 2
        - Subscribes to ``/fleet/tasks``, filters by robot ID, simulates
          0.5 s execution, publishes status on ``/fleet/status``.
      * - ``robot_2`` (slow)
        - 2
        - Same as ``robot_1`` but with 2 s sleep to demonstrate queue
          buildup.
      * - ``robot_3`` (fast)
        - 2
        - Same as ``robot_1`` but with 0.3 s sleep.
      * - ``monitor``
        - 3
        - Subscribes to ``/fleet/status``. Tracks per-robot task counts
          and last-report timestamps. Publishes summary on
          ``/fleet/report`` at 0.5 Hz. Logs warning
          (``get_logger().warn()``) if a robot is silent for 5 s.
      * - ``debug_logger`` (conditional)
        - 1
        - Subscribes to ``/fleet/tasks`` and ``/fleet/status``, logs
          all messages. Only started when ``enable_debug:=true``.
      * - Spinning and lifecycle
        - 3
        - Proper ``try/except/finally`` with ``rclpy.ok()`` guard in
          all entry points. Node classes separated from entry points.
      * - **QoS (10 pts)**
        -
        -
      * - Topic QoS profiles
        - 3
        - ``/fleet/tasks`` uses ``RELIABLE``/``TRANSIENT_LOCAL``/depth 5.
          ``/fleet/status`` uses ``BEST_EFFORT``/``VOLATILE``/depth 3.
          ``/fleet/report`` uses ``RELIABLE``/``VOLATILE``. Explicit
          ``QoSProfile`` objects.
      * - TRANSIENT_LOCAL demo
        - 3
        - ``robot_3`` started 5 s late still receives backlogged tasks.
          Documented in ``README.md``.
      * - Intentional mismatch
        - 2
        - ``RELIABLE`` subscriber to ``BEST_EFFORT`` ``/fleet/status``
          publisher receives no data. Documented with comments in code
          and diagnosed with ``ros2 topic info -v``.
      * - Queue overflow observation
        - 2
        - ``robot_2`` queue behavior documented in ``README.md``.
          Describes what happens when callback is slower than publish
          rate with depth 3.
      * - **Launch Files (10 pts)**
        -
        -
      * - ``system.launch.py``
        - 4
        - Starts dispatcher, all three robots, and monitor. All nodes
          use ``output="screen"`` and ``emulate_tty=True``.
      * - ``enable_debug`` argument
        - 2
        - ``DeclareLaunchArgument`` with default ``false``.
          ``debug_logger`` uses ``IfCondition``.
      * - ``start_robot_2`` argument
        - 2
        - ``DeclareLaunchArgument`` with default ``true``.
          ``robot_2`` uses ``IfCondition``. Enables manual testing of
          monitor stall detection.
      * - Robot ``GroupAction``
        - 2
        - All three robot nodes grouped in a ``GroupAction``.
      * - **Executors and Callback Groups (8 pts)**
        -
        -
      * - Monitor executor
        - 2
        - Uses ``MultiThreadedExecutor``.
      * - Monitor status subscription
        - 2
        - ``/fleet/status`` callback in a
          ``MutuallyExclusiveCallbackGroup`` with comment explaining
          shared dictionary protection.
      * - Monitor report timer
        - 2
        - Report timer in a ``ReentrantCallbackGroup`` with comment
          explaining independence.
      * - Robot node callback groups
        - 2
        - Task subscription and status timer in a
          ``MutuallyExclusiveCallbackGroup`` with comment explaining
          shared current-task state.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, scenario summary, node graph, design decisions,
          build/run instructions, queue overflow observation.
      * - Code quality
        - 3
        - Type hints, docstrings, ROS 2 logger with correct severity
          levels, consistent naming, no linting errors.
      * - **TOTAL**
        - **50**
        -
