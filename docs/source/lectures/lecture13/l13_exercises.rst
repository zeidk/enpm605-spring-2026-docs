====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 13. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/bt_demo/``
or ``~/enpm605_ws/src/integration_demo/`` workspace as indicated.


.. dropdown:: Exercise 1 -- Simple Behavior Tree with py_trees
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice building a basic behavior tree using ``py_trees``
    composites and custom behaviors.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``bt_demo/simple_tree.py`` that implements the
    following.

    1. **``CheckCondition(Behaviour)``** class:

       - ``__init__(self, name: str, condition_value: bool)``
         that calls ``super().__init__(name)`` and stores
         ``_condition_value``.
       - ``update(self) -> Status``: returns ``SUCCESS`` if
         ``_condition_value`` is ``True``, otherwise ``FAILURE``.

    2. **``SayMessage(Behaviour)``** class:

       - ``__init__(self, name: str, message: str)``
         that calls ``super().__init__(name)`` and stores ``_message``.
       - ``update(self) -> Status``: prints the message using
         ``self.logger.info()``, then returns ``SUCCESS``.

    3. **``CountdownAction(Behaviour)``** class:

       - ``__init__(self, name: str, count: int = 3)``
         that calls ``super().__init__(name)`` and stores
         ``_count`` and ``_remaining``.
       - ``initialise(self) -> None``: resets ``_remaining`` to
         ``_count``.
       - ``update(self) -> Status``: decrements ``_remaining``.
         Returns ``RUNNING`` if ``_remaining > 0``, otherwise
         returns ``SUCCESS``.

    4. **Build the tree** in a ``main()`` function:

       - Create a **Sequence** (``memory=True``) named
         ``"MainSequence"`` with children:

         - ``CheckCondition("Ready?", True)``
         - ``CountdownAction("Countdown", 3)``
         - ``SayMessage("Done", "All tasks complete!")``

       - Tick the tree in a loop until the root returns ``SUCCESS``
         or ``FAILURE``.

    **Expected behavior**

    Running ``python3 simple_tree.py`` should produce output similar to:

    .. code-block:: text

       [INFO] Tick 1: MainSequence -> RUNNING (Countdown in progress)
       [INFO] Tick 2: MainSequence -> RUNNING (Countdown in progress)
       [INFO] Tick 3: MainSequence -> RUNNING (Countdown in progress)
       [INFO] Done: All tasks complete!
       [INFO] Tick 4: MainSequence -> SUCCESS

    **Verification commands**

    .. code-block:: console

       cd ~/enpm605_ws/src/bt_demo
       python3 bt_demo/simple_tree.py


.. dropdown:: Exercise 2 -- Blackboard Communication
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice using the Blackboard for inter-behavior data sharing.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``bt_demo/blackboard_tree.py`` that implements the
    following.

    1. **``SensorReader(Behaviour)``** class:

       - Registers Blackboard write access for key ``"distance"``.
       - ``initialise(self)``: sets a simulated distance value
         starting at ``5.0``.
       - ``update(self)``: decrements the distance by ``0.5``, writes
         it to the Blackboard, and returns ``SUCCESS``.

    2. **``DistanceChecker(Behaviour)``** class:

       - Registers Blackboard read access for key ``"distance"``.
       - ``update(self)``: reads ``distance`` from the Blackboard.
         Returns ``SUCCESS`` if ``distance > 1.0``, otherwise
         ``FAILURE``.

    3. **``StopAction(Behaviour)``** class:

       - Registers Blackboard read access for key ``"distance"``.
       - ``update(self)``: logs
         ``"Stopping! Obstacle at <distance> m"`` and returns
         ``SUCCESS``.

    4. **Build the tree** in a ``main()`` function:

       - Create a **Sequence** (``memory=False``) named
         ``"ObstacleAvoidance"`` with children:

         - ``SensorReader("ReadSensor")``
         - ``DistanceChecker("CheckDistance")``

       - Wrap the Sequence and a ``StopAction("EmergencyStop")`` in a
         **Selector** (``memory=False``) named ``"Root"``:

         - First child: the Sequence (proceed if distance is safe).
         - Second child: ``StopAction`` (fallback if distance is
           unsafe).

       - Tick the tree in a loop. The tree should initially proceed
         (distance > 1.0) and eventually stop when the distance
         drops below the threshold.

    **Expected behavior**

    .. code-block:: text

       [Tick 1] distance=4.5 -> proceeding
       [Tick 2] distance=4.0 -> proceeding
       ...
       [Tick 7] distance=1.5 -> proceeding
       [Tick 8] distance=1.0 -> Stopping! Obstacle at 1.0 m

    **Verification commands**

    .. code-block:: console

       cd ~/enpm605_ws/src/bt_demo
       python3 bt_demo/blackboard_tree.py


.. dropdown:: Exercise 3 -- BT with ROS 2 Topics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Integrate a behavior tree with ROS 2 by subscribing to a topic
    and publishing commands based on tree decisions.


    .. raw:: html

       <hr>


    **Specification**

    Create two files in ``bt_demo/``:

    1. **``bt_demo/sensor_publisher.py``** -- A ROS 2 node that
       publishes simulated sensor data:

       - Publishes ``std_msgs/Float64`` on ``/sensor/distance`` at
         2 Hz.
       - The distance value starts at ``5.0`` and decreases by
         ``0.3`` each cycle until it reaches ``0.0``.

    2. **``bt_demo/bt_ros_node.py``** -- A ROS 2 node that runs a
       behavior tree:

       - **``SubscribeDistance(Behaviour)``**: subscribes to
         ``/sensor/distance`` and writes the value to Blackboard key
         ``"distance"``.
       - **``IsPathClear(Behaviour)``**: reads ``"distance"`` from
         the Blackboard, returns ``SUCCESS`` if ``> 1.5``, else
         ``FAILURE``.
       - **``PublishForward(Behaviour)``**: publishes
         ``geometry_msgs/Twist`` with ``linear.x = 0.5`` on
         ``/cmd_vel``.
       - **``PublishStop(Behaviour)``**: publishes
         ``geometry_msgs/Twist`` with ``linear.x = 0.0`` on
         ``/cmd_vel``.
       - Tree structure:

         .. code-block:: text

            [Selector: Root]
              -> [Sequence: DriveForward]
              |    -> IsPathClear
              |    -> PublishForward
              -> PublishStop

       - Tick the tree at 2 Hz using a ROS 2 timer.

    3. Register both as entry points in ``setup.py``:

       .. code-block:: python

          'sensor_pub = scripts.run_sensor_publisher:main',
          'bt_node = scripts.run_bt_ros_node:main',

    **Expected behavior**

    Terminal 1:

    .. code-block:: console

       ros2 run bt_demo sensor_pub

    Terminal 2:

    .. code-block:: console

       ros2 run bt_demo bt_node

    Terminal 3 (observe):

    .. code-block:: console

       ros2 topic echo /cmd_vel

    Initially ``/cmd_vel`` publishes ``linear.x: 0.5`` (moving
    forward). Once the distance drops below ``1.5``, it switches to
    ``linear.x: 0.0`` (stopped).

    **Verification commands**

    .. code-block:: console

       ros2 topic hz /sensor/distance    # should show ~2 Hz
       ros2 topic echo /cmd_vel          # should switch from 0.5 to 0.0
       ros2 node list                    # should show both nodes


.. dropdown:: Exercise 4 -- Mini Integration Demo
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build a small integration demo that combines lifecycle node
    management with BT-driven navigation.


    .. raw:: html

       <hr>


    **Specification**

    Create files in ``integration_demo/``:

    1. **``integration_demo/managed_sensor.py``** -- A lifecycle node
       that:

       - On ``configure``: creates a publisher for
         ``std_msgs/Float64`` on ``/battery_level``.
       - On ``activate``: creates a timer that publishes a battery
         level starting at ``100.0`` and decreasing by ``1.0`` each
         second.
       - On ``deactivate``: cancels the timer.

    2. **``integration_demo/bt_coordinator.py``** -- A regular ROS 2
       node that runs a behavior tree:

       - **``ActivateSensorNode(Behaviour)``**: calls the
         ``/managed_sensor/change_state`` service to transition the
         sensor node to ``active``.
       - **``ReadBattery(Behaviour)``**: subscribes to
         ``/battery_level`` and writes the value to the Blackboard.
       - **``CheckBattery(Behaviour)``**: reads battery level from
         the Blackboard, returns ``SUCCESS`` if ``> 20.0``, else
         ``FAILURE``.
       - **``LogLowBattery(Behaviour)``**: logs a warning message
         and returns ``SUCCESS``.

       - Tree structure:

         .. code-block:: text

            [Sequence: Root]
              -> ActivateSensorNode  (runs once, then SUCCESS)
              -> [Parallel: Monitor]
                   -> ReadBattery
                   -> [Selector: BatteryCheck]
                        -> CheckBattery
                        -> LogLowBattery

    3. Create a launch file ``launch/mini_integration_launch.py``
       that starts both nodes.

    **Expected behavior**

    .. code-block:: console

       ros2 launch integration_demo mini_integration_launch.py

    The managed sensor node transitions to active and publishes
    battery levels. The BT monitors the battery. When the level drops
    below 20.0, the tree logs a low battery warning on each tick.

    **Verification commands**

    .. code-block:: console

       ros2 topic echo /battery_level      # should show decreasing values
       ros2 lifecycle get /managed_sensor   # should show "active"
       ros2 node list                       # should show both nodes
