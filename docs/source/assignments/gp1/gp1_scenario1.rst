====================================================
Scenario 1: Multi-Sensor Monitoring System
====================================================


Domain
======

A facility monitoring station collects data from multiple environmental
sensors deployed across a building. Each sensor publishes readings at a
different rate. A central aggregator node collects all sensor data and
publishes a consolidated summary. A watchdog node monitors sensor
health by detecting missing data.


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
      * - ``temperature_sensor``
        - Publishes ``std_msgs/msg/Float64`` on ``/sensors/temperature``
          at 2 Hz. Simulates temperature readings between 18.0 and 30.0
          using ``random.uniform()``.
      * - ``humidity_sensor``
        - Publishes ``std_msgs/msg/Float64`` on ``/sensors/humidity``
          at 1 Hz. Simulates humidity readings between 30.0 and 80.0.
      * - ``battery_sensor``
        - Publishes ``std_msgs/msg/Int64`` on ``/sensors/battery`` at
          0.5 Hz. Simulates a battery level that decreases by 1 each
          tick (starting at 100).
      * - ``aggregator``
        - Subscribes to all three sensor topics. Maintains the latest
          value from each sensor. Publishes a ``std_msgs/msg/String``
          summary on ``/monitoring/summary`` at 1 Hz containing the
          latest temperature, humidity, and battery values.
      * - ``watchdog``
        - Subscribes to ``/sensors/temperature`` and
          ``/sensors/humidity``. Uses a 3-second timer to check whether
          data has been received from each sensor within the last 3
          seconds. Logs a warning if a sensor is silent.
      * - ``logger`` *(optional, conditional)*
        - Subscribes to ``/monitoring/summary`` and logs each message.
          Started only when a launch argument ``enable_logger`` is
          ``true``.

   **Topics**

   .. list-table::
      :widths: 35 30 35
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - QoS
      * - ``/sensors/temperature``
        - ``std_msgs/msg/Float64``
        - ``BEST_EFFORT``, ``VOLATILE``
      * - ``/sensors/humidity``
        - ``std_msgs/msg/Float64``
        - ``BEST_EFFORT``, ``VOLATILE``
      * - ``/sensors/battery``
        - ``std_msgs/msg/Int64``
        - ``RELIABLE``, ``TRANSIENT_LOCAL``
      * - ``/monitoring/summary``
        - ``std_msgs/msg/String``
        - ``RELIABLE``, ``VOLATILE``


.. dropdown:: Specific Requirements
   :open:

   In addition to the common requirements in the main GP 1 page:

   1. **QoS -- TRANSIENT_LOCAL**: The ``battery_sensor`` must use
      ``TRANSIENT_LOCAL`` durability so that the ``aggregator`` receives
      the last battery reading even if it starts after the battery sensor.
      Demonstrate this by launching the aggregator 5 seconds after the
      sensors and verifying the first summary already contains a battery
      value.

   2. **QoS -- Intentional mismatch**: Create a second subscriber in the
      ``watchdog`` node that subscribes to ``/sensors/battery`` with
      ``RELIABLE`` reliability but ``VOLATILE`` durability. The battery
      publisher uses ``TRANSIENT_LOCAL``. This is a **compatible** pairing
      (subscriber is less strict). Then create a third subscriber with
      ``TRANSIENT_LOCAL`` durability and ``BEST_EFFORT`` reliability
      connecting to the ``RELIABLE`` battery publisher -- this is the
      **incompatible** pairing. Add comments documenting both cases.

   3. **Aggregator callback groups**: The ``aggregator`` node must use a
      ``MultiThreadedExecutor``. The three sensor subscription callbacks
      must be in a ``MutuallyExclusiveCallbackGroup`` (they all write to
      shared state: the latest sensor values). The summary publisher timer
      must be in a separate ``ReentrantCallbackGroup`` (it only reads the
      latest values and can run independently).

   4. **Watchdog**: The watchdog node must track the timestamp of the last
      received message for each sensor. The 3-second timer callback checks
      whether ``time.time() - last_received > 3.0`` for each sensor and
      logs a warning using ``self.get_logger().warn()`` if true. Use
      ``self.get_logger().info()`` when all sensors are reporting normally.

   5. **Launch files**:

      - ``system.launch.py``: starts all sensor nodes, the aggregator,
        and the watchdog.
      - ``enable_logger`` argument (default ``false``): conditionally
        starts the ``logger`` node.
      - Sensor nodes grouped in a ``GroupAction``.


.. dropdown:: Expected Behavior
   :open:

   **Normal operation:**

   .. code-block:: text

      [INFO] [<timestamp>] [aggregator]: Summary -- temp: 23.4, humidity: 55.2, battery: 97
      [INFO] [<timestamp>] [aggregator]: Summary -- temp: 24.1, humidity: 54.8, battery: 96
      [INFO] [<timestamp>] [watchdog]: All sensors reporting normally.

   **Sensor goes silent** -- to test this, run one sensor separately
   with ``ros2 run`` in its own terminal instead of the launch file,
   then stop it with Ctrl-C:

   .. code-block:: console

      # Terminal 1: launch the system without the temperature sensor
      ros2 launch group<N>_gp1 system.launch.py start_temperature:=false

      # Terminal 2: start the temperature sensor manually
      ros2 run group<N>_gp1 temperature_sensor

      # Press Ctrl-C in Terminal 2 to simulate a sensor failure

   The watchdog should detect the silence and log:

   .. code-block:: text

      [WARNING] [<timestamp>] [watchdog]: temperature_sensor has not reported in 3.0 s

   .. note::

      To support this testing workflow, add a ``start_temperature``
      launch argument (default ``true``) with an ``IfCondition`` on
      the temperature sensor node. This lets you exclude it from the
      launch file and run it manually in a separate terminal.

   **Verification commands:**

   .. code-block:: console

      ros2 launch group<N>_gp1 system.launch.py
      ros2 launch group<N>_gp1 system.launch.py enable_logger:=true
      ros2 topic list -t
      ros2 topic echo /monitoring/summary
      ros2 topic hz /sensors/temperature
      ros2 topic info /sensors/battery -v
      rqt_graph


.. dropdown:: Scenario 1 Grading Rubric
   :open:

   This rubric details how the 50 points from the
   `common rubric <gp1.html#grading-rubric>`_ map to Scenario 1
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
      * - ``temperature_sensor``
        - 2
        - Publishes ``Float64`` on ``/sensors/temperature`` at 2 Hz
          with simulated random values. OOP node with timer callback.
      * - ``humidity_sensor``
        - 2
        - Publishes ``Float64`` on ``/sensors/humidity`` at 1 Hz
          with simulated random values.
      * - ``battery_sensor``
        - 2
        - Publishes ``Int64`` on ``/sensors/battery`` at 0.5 Hz
          with decrementing counter.
      * - ``aggregator``
        - 4
        - Subscribes to all three sensor topics. Stores latest values.
          Publishes ``String`` summary on ``/monitoring/summary`` at
          1 Hz.
      * - ``watchdog``
        - 3
        - Subscribes to temperature and humidity. Tracks last-received
          timestamps. Logs warning (``get_logger().warn()``) if no
          data in 3 s. Logs info when all sensors are normal.
      * - ``logger`` (conditional)
        - 1
        - Subscribes to ``/monitoring/summary`` and logs each message.
          Only started when ``enable_logger:=true``.
      * - Spinning and lifecycle
        - 2
        - Proper ``try/except/finally`` with ``rclpy.ok()`` guard in
          all entry points. Node classes separated from entry points.
      * - **QoS (10 pts)**
        -
        -
      * - Sensor topics QoS
        - 3
        - Temperature and humidity use ``BEST_EFFORT``/``VOLATILE``.
          Battery uses ``RELIABLE``/``TRANSIENT_LOCAL``. Explicit
          ``QoSProfile`` objects (not integer shorthand).
      * - TRANSIENT_LOCAL demo
        - 3
        - Aggregator started after battery sensor still receives last
          battery value. Documented in ``README.md``.
      * - Intentional mismatch
        - 4
        - Compatible pairing (``RELIABLE``/``VOLATILE`` subscriber to
          ``RELIABLE``/``TRANSIENT_LOCAL`` publisher) works. Incompatible
          pairing (``BEST_EFFORT``/``TRANSIENT_LOCAL`` subscriber to
          ``RELIABLE`` publisher) receives no data. Both documented with
          comments in code.
      * - **Launch Files (10 pts)**
        -
        -
      * - ``system.launch.py``
        - 4
        - Starts all sensor nodes, aggregator, and watchdog. All nodes
          use ``output="screen"`` and ``emulate_tty=True``.
      * - ``enable_logger`` argument
        - 2
        - ``DeclareLaunchArgument`` with default ``false``. Logger node
          uses ``IfCondition``.
      * - ``start_temperature`` argument
        - 2
        - ``DeclareLaunchArgument`` with default ``true``. Temperature
          node uses ``IfCondition``. Enables manual testing of watchdog.
      * - Sensor ``GroupAction``
        - 2
        - All three sensor nodes grouped in a ``GroupAction``.
      * - **Executors and Callback Groups (8 pts)**
        -
        -
      * - Aggregator executor
        - 2
        - Uses ``MultiThreadedExecutor``.
      * - Sensor subscriptions group
        - 3
        - Three sensor callbacks in a ``MutuallyExclusiveCallbackGroup``
          with comment explaining shared state protection.
      * - Summary timer group
        - 3
        - Summary publisher timer in a ``ReentrantCallbackGroup`` with
          comment explaining independence from sensor callbacks.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, scenario summary, node graph, design decisions,
          build/run instructions.
      * - Code quality
        - 3
        - Type hints, docstrings, ROS 2 logger with correct severity
          levels, consistent naming, no linting errors.
      * - **TOTAL**
        - **50**
        -
