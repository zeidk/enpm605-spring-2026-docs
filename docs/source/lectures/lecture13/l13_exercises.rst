====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the
concepts from Lecture 13. Each exercise asks you to **write code from
scratch** based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/``
workspace in the appropriate packages (``nav_demo`` or your own
extension package).


.. dropdown:: Exercise 1 -- Build, Save, and Reload a Map
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build an occupancy grid of the Husarion world using
    ``slam_toolbox``, save it to disk, and reload it for AMCL-based
    navigation.


    .. raw:: html

       <hr>


    **Specification**

    1. Launch Gazebo and ``slam_toolbox`` in mapping mode:

       .. code-block:: console

          # T1
          ros2 launch rosbot_gazebo husarion_world.launch.py
          # T2
          ros2 launch nav_demo map_nav.launch.py mode:=mapping

    2. Drive the robot with teleop to cover the entire environment.
       Aim for **at least one loop closure** by returning to your
       starting area after exploring all rooms.

    3. Save the map under ``~/enpm605_ws/maps/my_map`` using
       ``nav2_map_server``:

       .. code-block:: console

          ros2 run nav2_map_server map_saver_cli -f ~/enpm605_ws/maps/my_map

    4. Verify the two files ``my_map.pgm`` and ``my_map.yaml`` exist
       and open the ``.pgm`` in an image viewer.

    5. Re-launch in navigation mode pointing to your saved map and
       confirm the robot localizes after a single **2D Pose Estimate**
       click in RViz2.

    **Verification**

    - White, black, and grey regions of the ``.pgm`` correspond to
      free, occupied, and unknown space.
    - In RViz2, the AMCL particle cloud converges to a tight cluster
      around the robot within a few seconds of motion.
    - A **Nav2 Goal** click successfully drives the robot to the
      requested pose.


.. dropdown:: Exercise 2 -- Inflation Radius and Path Quality
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Investigate how the inflation layer's radius affects the planned
    path and the robot's clearance from obstacles.


    .. raw:: html

       <hr>


    **Specification**

    1. Locate the Nav2 parameter file used by ``map_nav.launch.py``
       (typically ``nav_demo/config/nav2_params.yaml``).
    2. Set the ``inflation_layer.inflation_radius`` of the **global
       costmap** to each of the following values, one at a time:

       - ``0.10``
       - ``0.30``
       - ``0.55``
       - ``0.80``

    3. For each value, launch navigation, send the same goal from
       RViz2, and:

       - Capture a screenshot of the planned path overlaid on the
         global costmap.
       - Note whether the path is feasible (the robot reaches the
         goal) or fails (no plan, recovery loop, or collision).

    4. Write a short reflection (one paragraph) answering: at what
       radius does the planner start refusing to plan through
       narrow doorways, and why?

    **Verification**

    - Four screenshots labelled with their inflation radius.
    - One paragraph of analysis tying the result to the robot's
      circumscribed radius.


.. dropdown:: Exercise 3 -- Sequential Goals with BasicNavigator
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a Python node that drives the robot through a sequence of
    three goals using the ``nav2_simple_commander`` API and reports
    feedback while moving.


    .. raw:: html

       <hr>


    **Specification**

    Create ``nav_demo/nav_demo/sequential_goals.py``.

    1. The node must:

       - Instantiate a ``BasicNavigator``.
       - Set the initial pose from the latest ``map`` ->
         ``base_link`` TF lookup (use a 2-second timeout).
       - Call ``waitUntilNav2Active()`` before sending goals.

    2. Define **three** goal poses (read from ROS 2 parameters):

       - ``goal_1`` (default ``[2.0, 0.0, 0.0]``)
       - ``goal_2`` (default ``[5.0, 1.0, 1.57]``)
       - ``goal_3`` (default ``[-5.42, 11.22, 3.14]``)

       Each parameter is a length-3 ``double_array`` of
       :math:`(x, y, \text{yaw})`.

    3. Send the goals **one at a time** with ``goToPose``. Between
       goals:

       - Print feedback every second: distance remaining and time
         elapsed.
       - When the goal completes, log the final ``TaskResult``
         (SUCCEEDED / CANCELED / FAILED).

    4. After all three goals, exit cleanly with ``rclpy.shutdown()``.

    **Verification**

    .. code-block:: console

       # T1
       ros2 launch rosbot_gazebo husarion_world.launch.py rviz:=False
       # T2
       ros2 launch nav_demo map_nav.launch.py mode:=navigation
       # T3
       ros2 run nav_demo sequential_goals

    The robot visits all three goals in order, and the terminal shows
    distance-remaining feedback for each leg.


.. dropdown:: Exercise 4 -- Cancel-on-Distance Behavior
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Extend the sequential-goals node from Exercise 3 with a safety
    behavior: if the robot has not made progress (distance remaining
    has not decreased) for five seconds, cancel the current goal and
    move on to the next one.


    .. raw:: html

       <hr>


    **Specification**

    1. Inside the goal-monitoring loop, track ``distance_remaining``
       from each feedback message.
    2. Maintain a ``last_progress_time`` timestamp; update it whenever
       ``distance_remaining`` decreases by at least ``0.05`` m.
    3. If ``now - last_progress_time > 5.0`` seconds while the goal
       is still active:

       - Call ``self._navigator.cancelTask()``.
       - Log ``"No progress -- cancelling goal."`` at WARN level.
       - Continue with the next goal in the sequence.

    4. The node must always finish, even if some goals were
       cancelled, and print a final summary like::

          goal_1: SUCCEEDED
          goal_2: CANCELED
          goal_3: SUCCEEDED

    **Verification**

    Place a wall in Gazebo (or pick a goal inside an obstacle) so
    that one of the goals becomes unreachable. The node should
    cancel that goal after five seconds of no progress and continue
    with the remaining goals without crashing.
