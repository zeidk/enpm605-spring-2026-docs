====================================================
Scenario 3: Sensor Fusion Pipeline
====================================================


Domain
======

An autonomous vehicle perception stack fuses data from a camera and a
LiDAR sensor. Each sensor publishes at a different rate. A fusion node
combines the latest readings from both sensors and publishes a fused
report. A logger node records the fused output for offline analysis.


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
      * - ``camera_node``
        - Publishes ``std_msgs/msg/String`` on ``/sensors/camera`` at
          10 Hz. Each message contains a simulated image ID string
          (e.g., ``"frame_0001"``, ``"frame_0002"``, ...).
      * - ``lidar_node``
        - Publishes ``std_msgs/msg/Float64`` on ``/sensors/lidar`` at
          5 Hz. Each message contains a simulated distance reading
          using ``random.uniform(0.5, 50.0)``.
      * - ``fusion_node``
        - Subscribes to ``/sensors/camera`` and ``/sensors/lidar``.
          Stores the latest value from each sensor. Publishes a
          ``std_msgs/msg/String`` fused report on ``/perception/fused``
          at 5 Hz containing the latest camera frame ID and LiDAR
          distance.
      * - ``safety_monitor``
        - Subscribes to ``/perception/fused``. Parses the fused message
          and uses ``self.get_logger().warn()`` if the LiDAR distance is
          below 2.0 m (obstacle too close). Publishes
          ``std_msgs/msg/String`` alerts on ``/perception/alerts`` only
          when a warning condition is detected.
      * - ``logger`` *(optional, conditional)*
        - Subscribes to ``/perception/fused`` and logs each message with
          a timestamp. Started only when ``enable_logger`` is ``true``.
      * - ``config_publisher``
        - Publishes ``std_msgs/msg/String`` on ``/system/config`` once
          at startup with ``TRANSIENT_LOCAL`` durability. The message
          contains a JSON string with system configuration (e.g.,
          ``{"fusion_rate": 5, "alert_threshold": 2.0}``). Any node
          that starts later can read this configuration.

   **Topics**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - QoS
      * - ``/sensors/camera``
        - ``std_msgs/msg/String``
        - ``BEST_EFFORT``, ``VOLATILE``, depth 1
      * - ``/sensors/lidar``
        - ``std_msgs/msg/Float64``
        - ``BEST_EFFORT``, ``VOLATILE``, depth 1
      * - ``/perception/fused``
        - ``std_msgs/msg/String``
        - ``RELIABLE``, ``VOLATILE``, depth 10
      * - ``/perception/alerts``
        - ``std_msgs/msg/String``
        - ``RELIABLE``, ``VOLATILE``, depth 10
      * - ``/system/config``
        - ``std_msgs/msg/String``
        - ``RELIABLE``, ``TRANSIENT_LOCAL``, depth 1


.. dropdown:: Specific Requirements
   :open:

   In addition to the common requirements in the main GP 1 page:

   1. **QoS -- TRANSIENT_LOCAL**: The ``config_publisher`` publishes a
      single configuration message with ``TRANSIENT_LOCAL`` durability.
      The ``fusion_node`` and ``safety_monitor`` subscribe to
      ``/system/config`` with matching ``TRANSIENT_LOCAL`` durability and
      use the configuration values. Demonstrate that nodes starting after
      the config publisher still receive the config message.

   2. **QoS -- Intentional mismatch**: Create a test subscriber (can be
      in the ``safety_monitor`` or a separate debug node) that subscribes
      to ``/sensors/camera`` with ``RELIABLE`` reliability. The camera
      publisher uses ``BEST_EFFORT``. This is incompatible and will
      receive no data. Add a comment block explaining the mismatch and how
      ``ros2 topic info /sensors/camera -v`` reveals it.

   3. **QoS -- Sensor depth 1**: Both sensor topics use depth 1. This
      means only the most recent message is buffered. If the fusion node's
      callback is slow, intermediate messages are dropped. Document this
      design choice in ``README.md``.

   4. **Fusion node callback groups**: The ``fusion_node`` must use a
      ``MultiThreadedExecutor``. The camera and LiDAR subscription
      callbacks must be in a ``MutuallyExclusiveCallbackGroup`` because
      they both write to shared state (the latest camera frame and LiDAR
      distance). The fused-output publishing timer must be in a separate
      ``ReentrantCallbackGroup`` so it can fire on schedule without
      waiting for a sensor callback to finish.

   5. **Safety monitor**: The ``safety_monitor`` subscribes to
      ``/perception/fused``, parses the message, and checks the LiDAR
      distance. If distance < 2.0 m, it publishes an alert on
      ``/perception/alerts`` and logs with ``self.get_logger().warn()``.
      Use ``self.get_logger().info()`` for normal fused output. The subscription
      callback and alert publisher can share a
      ``MutuallyExclusiveCallbackGroup`` since they access the same
      alert state.

   6. **Launch files**:

      - ``system.launch.py``: starts the config publisher, both sensor
        nodes, the fusion node, and the safety monitor.
      - ``enable_logger`` argument (default ``false``): conditionally
        starts the ``logger`` node.
      - Sensor nodes (``camera_node`` and ``lidar_node``) grouped in a
        ``GroupAction``.
      - An ``alert_threshold`` argument (default ``2.0``) that
        is passed to the safety monitor as a ROS parameter override
        (``--ros-args -p``).


.. dropdown:: Expected Behavior
   :open:

   **Normal operation:**

   .. code-block:: text

      [INFO] [<timestamp>] [config_publisher]: Published system config: {"fusion_rate": 5, "alert_threshold": 2.0}
      [INFO] [<timestamp>] [camera_node]: Publishing frame_0001
      [INFO] [<timestamp>] [lidar_node]: Publishing distance: 15.3
      [INFO] [<timestamp>] [fusion_node]: Fused -- camera: frame_0001, lidar: 15.3 m
      [INFO] [<timestamp>] [fusion_node]: Fused -- camera: frame_0005, lidar: 8.7 m

   **Obstacle detected:**

   .. code-block:: text

      [INFO] [<timestamp>] [fusion_node]: Fused -- camera: frame_0042, lidar: 1.3 m
      [WARNING] [<timestamp>] [safety_monitor]: Obstacle at 1.3 m (threshold: 2.0 m)

   **Late-joining node receives config:**

   Start the system, then manually start a new subscriber to
   ``/system/config``:

   .. code-block:: console

      ros2 topic echo /system/config --once

   The config message should be received immediately.

   **Verification commands:**

   .. code-block:: console

      ros2 launch group<N>_gp1 system.launch.py
      ros2 launch group<N>_gp1 system.launch.py enable_logger:=true
      ros2 launch group<N>_gp1 system.launch.py alert_threshold:=5.0
      ros2 topic list -t
      ros2 topic echo /perception/fused
      ros2 topic echo /perception/alerts
      ros2 topic hz /sensors/camera
      ros2 topic info /sensors/camera -v
      rqt_graph


.. dropdown:: Scenario 3 Grading Rubric
   :open:

   This rubric details how the 50 points from the
   `common rubric <gp1.html#grading-rubric>`_ map to Scenario 3
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
      * - ``camera_node``
        - 2
        - Publishes ``String`` (frame IDs) on ``/sensors/camera`` at
          10 Hz. OOP node with timer callback.
      * - ``lidar_node``
        - 2
        - Publishes ``Float64`` on ``/sensors/lidar`` at 5 Hz with
          simulated random distance values.
      * - ``fusion_node``
        - 4
        - Subscribes to ``/sensors/camera`` and ``/sensors/lidar``.
          Stores latest values. Publishes ``String`` fused report on
          ``/perception/fused`` at 5 Hz.
      * - ``safety_monitor``
        - 3
        - Subscribes to ``/perception/fused``. Parses message and
          checks LiDAR distance. Logs warning
          (``get_logger().warn()``) and publishes alert on
          ``/perception/alerts`` if distance < threshold. Uses
          ``get_logger().info()`` for normal operation.
      * - ``config_publisher``
        - 2
        - Publishes JSON config ``String`` on ``/system/config`` once
          at startup with ``TRANSIENT_LOCAL``.
      * - ``logger`` (conditional)
        - 1
        - Subscribes to ``/perception/fused`` and logs each message.
          Only started when ``enable_logger:=true``.
      * - Spinning and lifecycle
        - 2
        - Proper ``try/except/finally`` with ``rclpy.ok()`` guard in
          all entry points. Node classes separated from entry points.
      * - **QoS (10 pts)**
        -
        -
      * - Sensor topics QoS
        - 2
        - Camera and LiDAR use ``BEST_EFFORT``/``VOLATILE``/depth 1.
          Explicit ``QoSProfile`` objects.
      * - Fused and alerts QoS
        - 2
        - ``/perception/fused`` and ``/perception/alerts`` use
          ``RELIABLE``/``VOLATILE``/depth 10.
      * - TRANSIENT_LOCAL demo
        - 3
        - ``/system/config`` uses ``RELIABLE``/``TRANSIENT_LOCAL``.
          Nodes starting after ``config_publisher`` receive the config.
          Documented in ``README.md``.
      * - Intentional mismatch
        - 3
        - ``RELIABLE`` subscriber to ``BEST_EFFORT`` ``/sensors/camera``
          publisher receives no data. Documented with comment block in
          code explaining the mismatch and how ``ros2 topic info -v``
          reveals it.
      * - **Launch Files (10 pts)**
        -
        -
      * - ``system.launch.py``
        - 4
        - Starts config publisher, both sensors, fusion node, and
          safety monitor. All nodes use ``output="screen"`` and
          ``emulate_tty=True``.
      * - ``enable_logger`` argument
        - 2
        - ``DeclareLaunchArgument`` with default ``false``. Logger
          node uses ``IfCondition``.
      * - ``alert_threshold`` argument
        - 2
        - ``DeclareLaunchArgument`` with default ``2.0``. Passed to
          safety monitor as a ROS parameter override.
      * - Sensor ``GroupAction``
        - 2
        - Camera and LiDAR nodes grouped in a ``GroupAction``.
      * - **Executors and Callback Groups (8 pts)**
        -
        -
      * - Fusion node executor
        - 2
        - Uses ``MultiThreadedExecutor``.
      * - Sensor subscriptions group
        - 3
        - Camera and LiDAR callbacks in a
          ``MutuallyExclusiveCallbackGroup`` with comment explaining
          shared state protection (latest frame and distance).
      * - Fused output timer group
        - 3
        - Fused publisher timer in a ``ReentrantCallbackGroup`` with
          comment explaining independence from sensor callbacks.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, scenario summary, node graph, design decisions
          (including depth-1 sensor choice), build/run instructions.
      * - Code quality
        - 3
        - Type hints, docstrings, ROS 2 logger with correct severity
          levels, consistent naming, no linting errors.
      * - **TOTAL**
        - **50**
        -
