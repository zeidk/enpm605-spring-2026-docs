====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 11. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/`` workspace
in the appropriate packages (``gazebo_demo``, ``tf2_demo``, or
``robot_control_demo``).


.. dropdown:: Exercise 1 -- Launch Gazebo with a Custom World
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating an SDF world file and a ROS 2 launch file that
    starts Gazebo Harmonic with the ``ros_gz_bridge``.


    .. raw:: html

       <hr>


    **Specification**

    Create the following files in the ``gazebo_demo`` package:

    1. **``worlds/obstacle_world.sdf``**: An SDF world file containing:

       - The required system plugins (``Physics``, ``SceneBroadcaster``,
         ``UserCommands``, ``Sensors``).
       - A ground plane and directional light.
       - At least three box-shaped obstacles placed at different
         positions in the world.
       - Physics configured with ``max_step_size`` of ``0.001`` and
         ``real_time_factor`` of ``1.0``.

    2. **``launch/obstacle_world.launch.py``**: A launch file that:

       - Starts Gazebo with ``obstacle_world.sdf``.
       - Starts ``ros_gz_bridge`` bridging ``/clock`` to
         ``rosgraph_msgs/msg/Clock``.

    **Expected behavior**

    Running the launch file should open Gazebo with a ground plane,
    lighting, and three visible box obstacles:

    .. code-block:: console

       ros2 launch gazebo_demo obstacle_world.launch.py

    **Verification commands**

    .. code-block:: console

       # Gazebo should be running
       ps aux | grep gz

       # Clock topic should be available
       ros2 topic list | grep clock
       ros2 topic hz /clock       # should show non-zero Hz


.. dropdown:: Exercise 2 -- Spawn and Drive a Robot
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice spawning a robot model into Gazebo and controlling it
    with velocity commands through the bridge.


    .. raw:: html

       <hr>


    **Specification**

    Extend the ``gazebo_demo`` package:

    1. **``models/diff_drive.sdf``**: An SDF model with:

       - A ``base_link`` with a box visual and collision.
       - Two cylindrical wheels connected via revolute joints
         (``left_wheel_joint``, ``right_wheel_joint``).
       - A caster ball (sphere) for stability.
       - The ``gz::sim::systems::DiffDrive`` plugin configured with
         ``wheel_separation``, ``wheel_radius``, ``cmd_vel`` topic,
         and ``odom`` topic.

    2. **``launch/drive_robot.launch.py``**: A launch file that:

       - Launches Gazebo with the obstacle world from Exercise 1.
       - Spawns the ``diff_drive`` model at position (0, 0, 0.1).
       - Starts ``ros_gz_bridge`` bridging ``/cmd_vel``
         (ROS 2 to Gazebo), ``/odom`` (Gazebo to ROS 2), ``/clock``,
         and ``/tf``.

    **Expected behavior**

    After launching, you should be able to drive the robot using
    ``teleop_twist_keyboard``:

    .. code-block:: console

       # Terminal 1
       ros2 launch gazebo_demo drive_robot.launch.py

       # Terminal 2
       ros2 run teleop_twist_keyboard teleop_twist_keyboard

    The robot should move forward, backward, and turn in response to
    keyboard input.

    **Verification commands**

    .. code-block:: console

       ros2 topic list               # should show /cmd_vel, /odom, /tf
       ros2 topic echo /odom --once  # should show changing pose values
       ros2 topic hz /odom           # should show ~50 Hz


.. dropdown:: Exercise 3 -- TF2 Broadcaster and Listener
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice writing a static transform broadcaster and a transform
    listener that queries the TF tree.


    .. raw:: html

       <hr>


    **Specification**

    Create the following files in the ``tf2_demo`` package:

    1. **``tf2_demo/sensor_frame_broadcaster.py``**:

       - A ``SensorFrameBroadcaster(Node)`` class that uses
         ``StaticTransformBroadcaster`` to publish two static
         transforms:

         - ``base_link`` -> ``lidar_link`` with translation
           (0.15, 0.0, 0.1) and zero rotation.
         - ``base_link`` -> ``camera_link`` with translation
           (0.2, 0.0, 0.12) and zero rotation.

       - Publish both transforms in ``__init__`` (static transforms
         are published once).

    2. **``tf2_demo/frame_monitor.py``**:

       - A ``FrameMonitor(Node)`` class that uses ``Buffer`` and
         ``TransformListener``.
       - A 1 Hz timer callback that looks up the transform from
         ``odom`` to ``lidar_link`` and logs the translation.
       - Handle ``TransformException`` gracefully with a warning log.

    3. Register both nodes as entry points in ``setup.py``:

       .. code-block:: python

          'sensor_broadcaster = scripts.run_sensor_broadcaster:main',
          'frame_monitor = scripts.run_frame_monitor:main',

    **Expected behavior**

    With the simulation running (from Exercise 2):

    .. code-block:: console

       # Terminal 1: simulation
       ros2 launch gazebo_demo drive_robot.launch.py

       # Terminal 2: static broadcaster
       ros2 run tf2_demo sensor_broadcaster

       # Terminal 3: frame monitor
       ros2 run tf2_demo frame_monitor

    The frame monitor should log the lidar position in the odom
    frame at 1 Hz, updating as the robot moves.

    **Verification commands**

    .. code-block:: console

       ros2 run tf2_tools view_frames       # PDF should show all frames
       ros2 run tf2_ros tf2_echo odom lidar_link
       ros2 topic echo /tf_static --once    # should show both static transforms


.. dropdown:: Exercise 4 -- Obstacle Avoidance Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Combine sensor reading with robot control to implement a simple
    reactive obstacle avoidance behavior.


    .. raw:: html

       <hr>


    **Specification**

    Create the following in the ``robot_control_demo`` package:

    1. **``robot_control_demo/obstacle_avoider.py``**:

       - An ``ObstacleAvoider(Node)`` class with:

         - A subscriber to ``/lidar`` (``sensor_msgs/msg/LaserScan``).
         - A publisher to ``/cmd_vel`` (``geometry_msgs/msg/Twist``).
         - A parameter ``min_distance`` (default ``0.5`` m).
         - A parameter ``forward_speed`` (default ``0.3`` m/s).
         - A parameter ``turn_speed`` (default ``0.5`` rad/s).
         - In the lidar callback:

           - Compute the minimum distance in the front 60-degree arc
             of the scan.
           - If ``min_front_distance > min_distance``: drive forward.
           - Else: stop forward motion and turn in place.
           - Publish the ``Twist`` command.

    2. Register the entry point in ``setup.py``:

       .. code-block:: python

          'obstacle_avoider = scripts.run_obstacle_avoider:main',

    **Expected behavior**

    The robot drives forward until it detects an obstacle within
    ``min_distance``, then turns in place until the path is clear,
    and resumes forward motion:

    .. code-block:: console

       # Terminal 1: simulation with lidar bridge
       ros2 launch gazebo_demo drive_robot.launch.py

       # Terminal 2: obstacle avoider
       ros2 run robot_control_demo obstacle_avoider

    **Verification commands**

    .. code-block:: console

       ros2 topic hz /cmd_vel         # should show continuous publishing
       ros2 topic echo /cmd_vel       # should alternate between forward and turning
       ros2 param get /obstacle_avoider min_distance   # should return 0.5
