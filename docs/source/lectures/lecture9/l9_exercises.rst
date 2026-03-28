====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 9. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your
``~/enpm605_ws/src/parameters_demo/`` or
``~/enpm605_ws/src/executors_demo/`` workspace packages as specified
per exercise.


.. dropdown:: Exercise 1 -- Configurable Publisher
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice declaring and retrieving ROS 2 parameters, overriding them
    from the CLI, and using them to control a publisher's behavior.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``parameters_demo/configurable_publisher.py`` that
    implements the following.

    1. **``ConfigurablePublisher(Node)``** class:

       - ``__init__(self, node_name: str)`` that calls
         ``super().__init__(node_name)``, declares two parameters:
         ``topic_name`` (default ``"data"``) and ``publish_rate``
         (default ``1.0`` Hz), retrieves both parameters and stores
         them as ``_topic_name`` and ``_publish_rate``, creates a
         publisher on the resolved topic name with message type
         ``std_msgs/msg/Float64`` and queue depth ``10``, initializes
         a counter ``_count = 0``, and creates a timer using the
         resolved rate.
       - ``_timer_callback(self) -> None``: publishes a
         ``Float64`` message whose ``data`` field is the current value
         of ``_count`` cast to ``float``, logs the value and topic
         name, and increments ``_count``.

    2. **Entry point** ``scripts/run_configurable_publisher.py``:

       - Standard lifecycle: ``rclpy.init()``, instantiate
         ``ConfigurablePublisher("configurable_publisher")``,
         ``rclpy.spin()``, ``destroy_node()``, ``rclpy.shutdown()``.

    3. Register in ``setup.py``:

       .. code-block:: python

          'configurable_publisher = scripts.run_configurable_publisher:main',

    **Expected behavior**

    Default run:

    .. code-block:: console

       ros2 run parameters_demo configurable_publisher

    Override both parameters:

    .. code-block:: console

       ros2 run parameters_demo configurable_publisher \
           --ros-args -p topic_name:='sensor_data' -p publish_rate:=5.0

    **Verification commands**

    .. code-block:: console

       ros2 param list /configurable_publisher
       ros2 param get /configurable_publisher topic_name
       ros2 param get /configurable_publisher publish_rate
       ros2 topic hz /sensor_data   # should match publish_rate


.. dropdown:: Exercise 2 -- Parameter File Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating a YAML parameter file, loading it from a launch
    file, and reacting to runtime parameter changes via a callback.


    .. raw:: html

       <hr>


    **Specification**

    **Part A -- YAML parameter file**

    Create ``parameters_demo/config/sensor_config.yaml`` with the
    following content:

    .. code-block:: yaml

       sensor_node:
         ros__parameters:
           sensor_name: 'imu_sensor'
           sample_rate: 100
           frame_id: 'imu_link'

    Edit ``setup.py`` to install the ``config/`` directory.

    **Part B -- Sensor node**

    Create ``parameters_demo/sensor_node.py``:

    1. **``SensorNode(Node)``** class:

       - Declares three parameters: ``sensor_name`` (str, default
         ``"default_sensor"``), ``sample_rate`` (int, default ``10``),
         and ``frame_id`` (str, default ``"base_link"``).
       - Retrieves all three and stores them as ``_sensor_name``,
         ``_sample_rate``, and ``_frame_id``.
       - Creates a timer with period ``1.0 / _sample_rate``.
       - Registers an on-set-parameters callback
         (``add_on_set_parameters_callback``) that updates the stored
         attributes when any parameter changes. Return
         ``SetParametersResult(successful=True)`` on valid updates.
       - ``_timer_callback``: logs the sensor name, frame ID, and a
         simulated reading (e.g., a counter).

    **Part C -- Launch file**

    Create ``launch/sensor_demo.launch.py`` that loads the parameter
    file and starts ``sensor_node``.

    **Expected behavior**

    .. code-block:: console

       ros2 launch parameters_demo sensor_demo.launch.py

    Test dynamic update:

    .. code-block:: console

       ros2 param set sensor_node sensor_name 'front_imu'
       # Log output should immediately reflect the new name

    **Verification**

    .. code-block:: console

       ros2 param list /sensor_node
       ros2 param describe /sensor_node sample_rate


.. dropdown:: Exercise 3 -- Mutex vs Single-Threaded Comparison
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Observe the behavior difference between a
    ``SingleThreadedExecutor`` and a ``MultiThreadedExecutor`` with a
    ``MutuallyExclusiveCallbackGroup`` containing a slow callback.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``executors_demo/slow_callback_demo.py`` that
    implements the following.

    1. **``SlowCallbackDemo(Node)``** class:

       - ``__init__(self)``: calls ``super().__init__("slow_cb_demo")``,
         creates a ``MutuallyExclusiveCallbackGroup`` stored as
         ``_group``, and creates three timers:

         - ``_fast_timer``: 2 Hz, 50 ms execution (simulated with
           ``time.sleep(0.05)``), assigned to ``_group``.
         - ``_slow_timer``: 1 Hz, 600 ms execution
           (``time.sleep(0.60)``), assigned to ``_group``.
         - ``_monitor_timer``: 5 Hz, negligible execution, assigned to
           ``_group``. Logs ``"monitor tick"`` without sleeping.

    2. Three callbacks each logging their name and the current wall
       time at entry and exit.

    3. **Two entry points** in ``scripts/``:

       - ``run_single_threaded.py``: uses ``rclpy.spin(node)``
         (implicitly single-threaded).
       - ``run_multi_threaded.py``: uses
         ``MultiThreadedExecutor(num_threads=4)``.

    4. Register both in ``setup.py``.

    **Observation questions (answer as comments at the top of each
    entry point file)**

    - In the single-threaded case, what happens to ``_fast_timer`` and
      ``_monitor_timer`` while ``_slow_timer`` is executing?
    - In the multi-threaded case with a mutex group, is there any
      difference in behavior? Why or why not?

    **Verification**

    .. code-block:: console

       ros2 run executors_demo single_threaded_slow
       ros2 run executors_demo multi_threaded_slow


.. dropdown:: Exercise 4 -- Reentrant Pipeline
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build a node with two independent callback pipelines using a
    ``ReentrantCallbackGroup``, observe that they overlap correctly,
    and introduce a deliberate race condition to see what goes wrong.


    .. raw:: html

       <hr>


    **Specification**

    Create ``executors_demo/reentrant_pipeline.py``.

    1. **``ReentrantPipeline(Node)``** class with one
       ``ReentrantCallbackGroup``:

       - ``_camera_cb``: fires at 5 Hz, takes 80 ms
         (``time.sleep(0.08)``). Appends a timestamped entry to a
         shared list ``self._log``.
       - ``_lidar_cb``: fires at 5 Hz, takes 80 ms
         (``time.sleep(0.08)``). Appends a timestamped entry to the
         same ``self._log``.
       - ``_report_cb``: fires at 1 Hz, prints the length and last
         three entries of ``self._log``.

    2. Entry point ``scripts/run_reentrant_pipeline.py`` using
       ``MultiThreadedExecutor(num_threads=4)``.

    3. Register in ``setup.py``.

    **Part B -- Introduce and fix a race condition**

    Both ``_camera_cb`` and ``_lidar_cb`` append to the same list
    without a lock. Run the node for several seconds and note whether
    you ever observe a corrupted log (duplicated or missing entries).
    Then:

    - Protect ``self._log`` with a ``threading.Lock``.
    - Verify that the log is now consistent.

    **Written reflection (include as a comment block at the top of the
    file)**

    - Did you observe a race condition without the lock? Why is list
      ``append`` generally safe in CPython but not guaranteed across all
      Python implementations?
    - What would happen if you switched the group to
      ``MutuallyExclusiveCallbackGroup``? Would the race condition
      disappear? At what cost?
