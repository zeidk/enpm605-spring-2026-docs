====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the
concepts from Lecture 14. Each exercise asks you to **write code
from scratch** based on a specification -- no starter code is
provided.

All files should be created inside your ``~/enpm605_ws/src/``
workspace in the appropriate packages (``lifecycle_demo``,
``bag_demo``, or your own extension package).


.. dropdown:: Exercise 1 -- Implement a CLI-Driven Lifecycle Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a Python lifecycle node that publishes a counter
    string at 2 Hz, but only while in the **Active** state. Drive
    the transitions externally with ``ros2 lifecycle set``.


    .. raw:: html

       <hr>


    **Specification**

    1. Create a node ``counter_publisher`` extending
       ``LifecycleNode`` from ``rclpy_lifecycle``.

    2. Allocate the publisher in ``on_configure`` using
       ``create_lifecycle_publisher`` for ``std_msgs/String`` on the
       topic ``/counter``.

    3. Create the timer in ``on_activate`` (and call
       ``super().on_activate(state)`` first). Cancel it in
       ``on_deactivate``.

    4. In ``on_cleanup``, drop the publisher reference and reset the
       counter to ``0``.

    5. Publish a string of the form ``"count=<n>"`` where ``<n>`` is
       an incrementing integer.

    **Verification**

    - ``ros2 lifecycle get /counter_publisher`` shows ``unconfigured``
      at startup.
    - After ``configure`` then ``activate``,
      ``ros2 topic echo /counter`` prints
      ``data: 'count=0'``, ``count=1``, ... at 2 Hz.
    - After ``deactivate``, ``/counter`` stops publishing without
      the node exiting.
    - After ``cleanup`` then ``configure`` then ``activate``, the
      counter restarts at ``0``.


.. dropdown:: Exercise 2 -- Add a Programmatic Self-Cycle
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Extend Exercise 1 so the node can **drive its own state
    transitions** by calling its own ``change_state`` service.


    .. raw:: html

       <hr>


    **Specification**

    1. Add a regular timer (not lifecycle-managed) that fires every
       ``5.0`` seconds.

    2. Maintain an index that walks through the cycle
       ``[CONFIGURE, ACTIVATE, DEACTIVATE, CLEANUP]`` from
       ``lifecycle_msgs.msg.Transition``.

    3. In the timer callback, call the
       ``/counter_publisher/change_state`` service **asynchronously**
       (``call_async``) with the next transition id.

    4. Register a done callback on the future that logs whether
       ``result.success`` is ``True``.

    5. Provide a launch file that starts the node already in
       self-cycling mode (no external ``ros2 lifecycle set`` calls
       needed).

    **Verification**

    - Running ``ros2 lifecycle get /counter_publisher`` repeatedly
      shows the state advancing through Unconfigured :math:`\to`
      Inactive :math:`\to` Active :math:`\to` Inactive :math:`\to`
      Unconfigured every 5 s.
    - ``ros2 topic echo /counter`` shows messages appearing only
      during the Active windows.
    - The done callback log line confirms each transition succeeded.


.. dropdown:: Exercise 3 -- Record and Inspect a Navigation Bag
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Record a short Nav2 navigation run as an MCAP bag, inspect it
    with ``ros2 bag info``, and replay it with the live simulation
    closed.


    .. raw:: html

       <hr>


    **Specification**

    1. Make sure the MCAP plugin is installed:

       .. code-block:: console

          sudo apt install ros-jazzy-rosbag2-storage-mcap

    2. In one terminal, launch the simulation:

       .. code-block:: console

          ros2 launch rosbot_gazebo husarion_world.launch.py rviz:=False

    3. In a second terminal, start recording:

       .. code-block:: console

          ros2 bag record -o nav_run --storage mcap \
              /odometry/filtered /scan /cmd_vel /tf /tf_static /map

    4. In a third terminal, launch Nav2 and send a goal:

       .. code-block:: console

          ros2 launch nav_demo map_nav.launch.py mode:=navigation

    5. After the robot reaches the goal, stop recording with
       ``Ctrl+C``.

    6. Inspect the resulting bag:

       .. code-block:: console

          ros2 bag info nav_run

    **Verification**

    - All six topics appear in the ``ros2 bag info`` output.
    - ``/tf_static`` has at least one message.
    - The bag duration matches the wall-clock duration of the run
      (within 1 s).
    - The ``nav_run`` directory contains a ``metadata.yaml`` and one
      or more ``.mcap`` files.


.. dropdown:: Exercise 4 -- Visualize the Bag in Foxglove Studio
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Open the recorded MCAP bag in Foxglove Studio and build a
    multi-panel layout that shows the LiDAR scan, the trajectory,
    and the velocity commands together.


    .. raw:: html

       <hr>


    **Specification**

    1. Install Foxglove Studio (Debian package, snap, or browser).
    2. Open ``nav_run_0.mcap`` (the file inside the bag directory,
       not the directory itself).
    3. Build a layout with at least three panels:

       - **3D panel**: display frame ``map``; enable ``/scan``,
         ``/tf``, and ``/map`` so the robot, its laser hits, and
         the static map appear together.
       - **Plot panel**: plot
         ``/odometry/filtered.pose.pose.position.x`` against
         ``...y`` to draw the parametric trajectory.
       - **Raw Messages panel**: subscribe to ``/cmd_vel`` so you
         can scrub through individual ``TwistStamped`` messages.

    4. Export the layout via **Layouts** :math:`\to` **Export
       layout to file** and save it as ``nav_run_layout.json``
       inside your ``bag_demo`` package.

    **Verification**

    - All three panels stay synchronized to the playhead while the
      bag plays.
    - The 3D scene shows the robot moving across the saved map and
      the laser hits update with each ``/scan`` message.
    - The plot draws a smooth XY trajectory matching the path the
      robot actually drove.
    - The exported layout reopens correctly from a fresh Foxglove
      session.
