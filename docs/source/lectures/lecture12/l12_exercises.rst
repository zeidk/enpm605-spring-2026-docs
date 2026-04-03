====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 12. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/`` workspace
using the packages ``lifecycle_demo`` and ``nav2_demo``.


.. dropdown:: Exercise 1 -- Lifecycle Publisher
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a lifecycle-managed publisher node that demonstrates all
    state transitions and publishes messages only when in the Active
    state.


    .. raw:: html

       <hr>


    **Specification**

    Create the package ``lifecycle_demo`` and the file
    ``lifecycle_demo/managed_counter.py`` that implements the following.

    1. **``ManagedCounter(LifecycleNode)``** class:

       - ``__init__(self)``: call ``super().__init__("managed_counter")``,
         initialize ``_publisher = None``, ``_timer = None``, and
         ``_count = 0``.
       - ``on_configure(self, state)``: create a lifecycle publisher on
         topic ``/counter`` with message type ``std_msgs/msg/Int64`` and
         queue depth 10.  Return ``TransitionCallbackReturn.SUCCESS``.
       - ``on_activate(self, state)``: create a timer with period 1.0
         seconds that calls ``_timer_callback``.  Return
         ``TransitionCallbackReturn.SUCCESS`` after calling
         ``super().on_activate(state)``.
       - ``on_deactivate(self, state)``: destroy the timer.  Return
         ``TransitionCallbackReturn.SUCCESS`` after calling
         ``super().on_deactivate(state)``.
       - ``on_cleanup(self, state)``: set ``_publisher = None`` and
         ``_count = 0``.  Return ``TransitionCallbackReturn.SUCCESS``.
       - ``on_shutdown(self, state)``: log ``"Shutting down"`` and
         release all resources.  Return
         ``TransitionCallbackReturn.SUCCESS``.
       - ``_timer_callback(self)``: publish ``_count`` as an ``Int64``
         message and increment ``_count``.

    2. **``scripts/run_managed_counter.py``** entry point:

       - Initialize ``rclpy``, instantiate ``ManagedCounter``.
       - Spin the node, handle ``KeyboardInterrupt``.
       - Destroy the node and call ``rclpy.shutdown()`` in a ``finally``
         block.

    3. Register the entry point in ``setup.py``:

       .. code-block:: python

          'managed_counter = scripts.run_managed_counter:main',

    **Expected behavior**

    After launching the node:

    .. code-block:: console

       ros2 run lifecycle_demo managed_counter

    The node starts in the Unconfigured state.  Use the lifecycle CLI
    to transition through states:

    .. code-block:: console

       ros2 lifecycle set /managed_counter configure
       ros2 lifecycle set /managed_counter activate

    The node should begin publishing incrementing integers on
    ``/counter`` at 1 Hz:

    .. code-block:: text

       [INFO] [managed_counter]: Published: 0
       [INFO] [managed_counter]: Published: 1
       [INFO] [managed_counter]: Published: 2

    Deactivating the node should stop publishing:

    .. code-block:: console

       ros2 lifecycle set /managed_counter deactivate

    **Verification commands**

    .. code-block:: console

       ros2 lifecycle nodes                    # should show /managed_counter
       ros2 lifecycle get /managed_counter     # should show current state
       ros2 topic echo /counter               # should show incrementing values when Active
       ros2 topic hz /counter                  # should show ~1 Hz when Active


.. dropdown:: Exercise 2 -- Launch Nav2 in Simulation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Launch the full Nav2 stack in the Gazebo simulation environment
    from L11 and verify that all lifecycle nodes are active.


    .. raw:: html

       <hr>


    **Specification**

    Create the package ``nav2_demo`` with a launch file and
    configuration:

    1. **``config/nav2_params.yaml``**: Copy the default Nav2 parameter
       file and modify the following:

       - Set ``robot_radius`` to match your simulated robot.
       - Set ``use_sim_time: true`` for all nodes.
       - Configure the scan topic to match your robot's LiDAR topic.

    2. **``maps/sim_map.yaml``** and **``maps/sim_map.pgm``**: Generate
       a map of the simulation world using SLAM Toolbox (see lecture
       content for instructions).

    3. **``launch/nav2_sim_launch.py``**: Create a launch file that:

       - Includes the Gazebo launch from L11.
       - Includes ``nav2_bringup`` ``bringup_launch.py`` with your map
         and parameter file.
       - Launches RViz with the Nav2 default configuration.

    **Expected behavior**

    Running the launch file should start Gazebo, Nav2, and RViz:

    .. code-block:: console

       ros2 launch nav2_demo nav2_sim_launch.py

    The terminal should show:

    .. code-block:: text

       [lifecycle_manager]: Configuring map_server
       [lifecycle_manager]: Configuring amcl
       [lifecycle_manager]: Configuring planner_server
       [lifecycle_manager]: Configuring controller_server
       [lifecycle_manager]: Configuring behavior_server
       [lifecycle_manager]: Configuring bt_navigator
       [lifecycle_manager]: Managed nodes are active

    **Verification commands**

    .. code-block:: console

       ros2 lifecycle nodes                          # should list all Nav2 nodes
       ros2 lifecycle get /planner_server            # should show "active"
       ros2 lifecycle get /controller_server         # should show "active"
       ros2 topic list | grep costmap                # should show costmap topics
       ros2 service list | grep compute_path_to_pose # should show the planner service


.. dropdown:: Exercise 3 -- Programmatic Navigation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a Python script that sends a navigation goal to Nav2 using
    the ``BasicNavigator`` API and reports success or failure.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``nav2_demo/goal_sender.py`` that implements the
    following.

    1. **``send_goal(x, y, yaw)``** function:

       - Initialize ``rclpy`` and create a ``BasicNavigator`` instance.
       - Wait for Nav2 to be active using
         ``navigator.waitUntilNav2Active()``.
       - Set the initial pose at the origin (0, 0, 0).
       - Create a ``PoseStamped`` goal at the given (x, y) position
         with the given yaw orientation (convert yaw to quaternion).
       - Call ``navigator.goToPose(goal)``.
       - Poll ``navigator.isTaskComplete()`` in a loop, printing
         feedback (distance remaining, ETA) every 0.5 seconds.
       - Check the result and log whether the goal was reached,
         canceled, or failed.
       - Call ``navigator.lifecycleShutdown()`` and
         ``rclpy.shutdown()``.

    2. **``scripts/run_goal_sender.py``** entry point that calls
       ``send_goal(2.0, 1.0, 0.0)``.

    3. Register the entry point in ``setup.py``:

       .. code-block:: python

          'goal_sender = scripts.run_goal_sender:main',

    **Expected behavior**

    With Nav2 running (from Exercise 2), run:

    .. code-block:: console

       ros2 run nav2_demo goal_sender

    The robot should navigate to position (2.0, 1.0) in the map frame.
    The terminal should show progress feedback and a final result:

    .. code-block:: text

       [INFO] Waiting for Nav2 to be active...
       [INFO] Nav2 is active. Sending goal: x=2.0, y=1.0, yaw=0.0
       [INFO] Distance remaining: 2.24m
       [INFO] Distance remaining: 1.85m
       ...
       [INFO] Goal reached!

    **Verification commands**

    .. code-block:: console

       ros2 topic echo /navigate_to_pose/_action/status   # should show SUCCEEDED
       ros2 topic echo /plan         # should show the planned path while navigating


.. dropdown:: Exercise 4 -- Waypoint Patrol
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a Python script that commands the robot to follow a sequence
    of waypoints in a patrol pattern.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``nav2_demo/waypoint_patrol.py`` that implements
    the following.

    1. **``WaypointPatrol``** class:

       - ``__init__(self, waypoints: list[tuple[float, float]])``:
         store the list of (x, y) waypoints.
       - ``run(self)``: initialize ``rclpy``, create a
         ``BasicNavigator``, wait for Nav2, set initial pose, convert
         the waypoint tuples to ``PoseStamped`` messages with
         ``orientation.w = 1.0``, call ``navigator.followWaypoints()``,
         poll for completion while printing the current waypoint index,
         check the final result, and shut down.

    2. **``scripts/run_waypoint_patrol.py``** entry point that creates
       a ``WaypointPatrol`` with at least four waypoints forming a
       rectangle and calls ``run()``.

    3. Register the entry point in ``setup.py``:

       .. code-block:: python

          'waypoint_patrol = scripts.run_waypoint_patrol:main',

    **Expected behavior**

    With Nav2 running:

    .. code-block:: console

       ros2 run nav2_demo waypoint_patrol

    The robot should visit each waypoint in order:

    .. code-block:: text

       [INFO] Starting waypoint patrol with 4 waypoints
       [INFO] Navigating to waypoint 1/4: (1.0, 0.0)
       [INFO] Navigating to waypoint 2/4: (1.0, 1.5)
       [INFO] Navigating to waypoint 3/4: (0.0, 1.5)
       [INFO] Navigating to waypoint 4/4: (0.0, 0.0)
       [INFO] Patrol complete!

    **Verification commands**

    .. code-block:: console

       ros2 topic echo /waypoints     # should show the waypoint list
       ros2 topic echo /plan          # should show successive planned paths
