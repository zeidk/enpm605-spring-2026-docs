====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 11. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/`` workspace
in the appropriate packages (``frame_demo``, ``tf2_demo``, or
``robot_control_demo``).


.. dropdown:: Exercise 1 -- Quaternion Utility Library
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build a Python module that converts between orientation
    representations and verify it against ``scipy.spatial.transform``.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``frame_demo/frame_demo/quat_utils.py`` that
    implements the following functions.

    1. **``axis_angle_to_quaternion(axis, angle)``**:

       - Input: a 3-element unit vector ``axis`` and a rotation
         ``angle`` in radians.
       - Output: a tuple ``(w, x, y, z)`` using the half-angle
         formula:

         .. math::

            w = \cos\!\left(\frac{\theta}{2}\right), \quad
            (x, y, z) = \sin\!\left(\frac{\theta}{2}\right) \cdot \mathbf{u}

       - Raise ``ValueError`` if the axis is not a unit vector
         (tolerance: ``1e-6``).

    2. **``quaternion_to_euler(w, x, y, z)``**:

       - Input: a unit quaternion ``(w, x, y, z)``.
       - Output: a tuple ``(roll, pitch, yaw)`` in radians.
       - Use the standard ZYX (Tait-Bryan) convention.

    3. **``quaternion_multiply(q1, q2)``**:

       - Input: two quaternions as ``(w, x, y, z)`` tuples.
       - Output: the Hamilton product ``q1 * q2`` as a
         ``(w, x, y, z)`` tuple.

    4. **``normalize_quaternion(w, x, y, z)``**:

       - Input: a quaternion (not necessarily unit).
       - Output: the corresponding unit quaternion.
       - Raise ``ValueError`` if the magnitude is zero.

    Write a ``main()`` function that:

    - Computes the quaternion for a :math:`90°` rotation about the
      :math:`x`-axis using ``axis_angle_to_quaternion``.
    - Computes the quaternion for a :math:`90°` rotation about the
      :math:`z`-axis.
    - Composes them (z-rotation applied first, then x-rotation) using
      ``quaternion_multiply``.
    - Converts the result to Euler angles.
    - Prints all intermediate and final values.
    - Verifies the result against
      ``scipy.spatial.transform.Rotation`` and prints ``PASS`` or
      ``FAIL``.

    **Verification**

    .. code-block:: console

       cd ~/enpm605_ws && colcon build --symlink-install --packages-select frame_demo
       source install/setup.bash
       ros2 run frame_demo quat_utils


.. dropdown:: Exercise 2 -- Static Transform Broadcaster Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a ROS 2 node that publishes a static transform from
    ``base_link`` to a custom sensor frame using parameters loaded
    from a YAML file.


    .. raw:: html

       <hr>


    **Specification**

    Create ``frame_demo/frame_demo/sensor_frame_publisher.py``.

    1. **``SensorFramePublisher(Node)``** class:

       - ``__init__``: declares the following parameters:

         - ``parent_frame`` (string, default ``"base_link"``)
         - ``child_frame`` (string, default ``"sensor_link"``)
         - ``translation`` (double array, default ``[0.0, 0.0, 0.0]``)
         - ``rotation_rpy`` (double array, default ``[0.0, 0.0, 0.0]``)

       - Converts the roll-pitch-yaw values to a quaternion using
         ``scipy.spatial.transform.Rotation.from_euler("xyz", [r, p, y])``.
       - Creates a ``StaticTransformBroadcaster`` and publishes the
         transform once.
       - Logs the published transform at ``info`` level.

    2. **YAML parameter file** ``config/sensor_frame.yaml``:

       .. code-block:: yaml

          /sensor_frame_publisher:
            ros__parameters:
              parent_frame: "base_link"
              child_frame: "camera_link"
              translation: [0.1, 0.0, 0.25]
              rotation_rpy: [0.0, -0.2618, 0.0]

    3. **Launch file** ``launch/sensor_frame.launch.py``:

       - Starts the ``sensor_frame_publisher`` node with the YAML
         parameter file.

    4. Register the entry point in ``setup.py`` and install the config
       and launch directories.

    **Expected behavior**

    - The node starts, publishes the static transform, and keeps
      running.
    - ``ros2 run tf2_ros tf2_echo base_link camera_link`` shows the
      transform.
    - ``ros2 run rqt_tf_tree rqt_tf_tree --force-discover`` shows
      ``base_link`` → ``camera_link`` in the tree.

    **Verification**

    .. code-block:: console

       cd ~/enpm605_ws && colcon build --symlink-install --packages-select frame_demo
       source install/setup.bash

       # Terminal 1
       ros2 launch frame_demo sensor_frame.launch.py

       # Terminal 2
       ros2 run tf2_ros tf2_echo base_link camera_link

       # Terminal 3
       ros2 run rqt_tf_tree rqt_tf_tree --force-discover


.. dropdown:: Exercise 3 -- Transform Listener and Logger
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a node that periodically looks up the transform between two
    frames and logs the position and orientation (as Euler angles).


    .. raw:: html

       <hr>


    **Specification**

    Create ``frame_demo/frame_demo/frame_logger.py``.

    1. **``FrameLogger(Node)``** class:

       - ``__init__``: declares two parameters:

         - ``target_frame`` (string, default ``"odom"``)
         - ``source_frame`` (string, default ``"base_link"``)

       - Creates a ``Buffer`` and a ``TransformListener``.
       - Creates a timer at 1 Hz.

    2. **Timer callback** ``_timer_callback(self)``:

       - Calls ``self._tf_buffer.lookup_transform(target, source,
         rclpy.time.Time(), timeout=Duration(seconds=0.1))``.
       - Extracts the translation ``(x, y, z)``.
       - Converts the quaternion to Euler angles using
         ``scipy.spatial.transform.Rotation``.
       - Logs translation and Euler angles (degrees) at ``info`` level.
       - Catches ``TransformException`` and logs a warning instead.

    **Expected behavior**

    - With the ROSbot simulation running, the node logs the robot's
      pose in the ``odom`` frame once per second.
    - Moving the robot (e.g., with ``teleop_twist_keyboard``) shows
      the logged values changing.

    **Verification**

    .. code-block:: console

       # Terminal 1
       ros2 launch rosbot_gazebo empty_world.launch.py

       # Terminal 2
       cd ~/enpm605_ws && colcon build --symlink-install --packages-select frame_demo
       source install/setup.bash
       ros2 run frame_demo frame_logger

       # Terminal 3
       ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true


.. dropdown:: Exercise 4 -- Proportional Go-to-Goal Controller
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a two-phase proportional controller that drives a
    differential-drive robot to a goal pose (position + final heading)
    using odometry feedback.


    .. raw:: html

       <hr>


    **Specification**

    Create ``robot_control_demo/robot_control_demo/goto_goal.py``.

    1. **``GoToGoal(Node)``** class:

       - ``__init__``: declares the following parameters with defaults:

         - ``goal_x`` (double, ``3.0``)
         - ``goal_y`` (double, ``2.0``)
         - ``goal_heading`` (double, ``1.57``) — desired final yaw in
           radians
         - ``k_rho`` (double, ``0.5``) — linear gain
         - ``k_alpha`` (double, ``1.0``) — angular gain (drive phase)
         - ``k_heading`` (double, ``1.5``) — angular gain (rotate phase)
         - ``position_tolerance`` (double, ``0.05``) — meters
         - ``heading_tolerance`` (double, ``0.05``) — radians

       - Creates a publisher on ``/cmd_vel``
         (``geometry_msgs/msg/TwistStamped``).
       - Subscribes to ``/odometry/filtered``
         (``nav_msgs/msg/Odometry``).
       - Creates a timer at 20 Hz for the control loop.
       - Tracks the current phase: ``DRIVE`` or ``ROTATE``.

    2. **Odometry callback** ``_odom_callback(self, msg)``:

       - Extracts ``x``, ``y`` from ``msg.pose.pose.position``.
       - Extracts yaw from the quaternion using
         ``scipy.spatial.transform.Rotation``.

    3. **Control loop** ``_control_loop(self)``:

       - **DRIVE phase**:

         - Compute distance error:
           :math:`\rho = \sqrt{(x_g - x)^2 + (y_g - y)^2}`
         - Compute heading error to goal:
           :math:`\alpha = \text{atan2}(y_g - y, x_g - x) - \psi`
         - Normalize :math:`\alpha` to :math:`[-\pi, \pi]`.
         - Set ``linear.x = k_rho * rho`` and
           ``angular.z = k_alpha * alpha``.
         - Clamp linear velocity to ``[0, 0.5]`` m/s and angular
           velocity to ``[-1.0, 1.0]`` rad/s.
         - If :math:`\rho <` ``position_tolerance``, switch to
           ``ROTATE`` phase.

       - **ROTATE phase**:

         - Compute heading error:
           :math:`e_\psi = \psi_{\text{goal}} - \psi`
         - Normalize to :math:`[-\pi, \pi]`.
         - Set ``linear.x = 0.0`` and
           ``angular.z = k_heading * e_psi``.
         - Clamp angular velocity to ``[-1.0, 1.0]`` rad/s.
         - If :math:`|e_\psi| <` ``heading_tolerance``, publish a
           zero-velocity command, log ``"Goal reached!"``, and stop
           the timer.

    4. Register the entry point in ``setup.py``.

    **Expected behavior**

    - The robot drives toward the goal position with a smooth curved
      trajectory (simultaneous linear + angular motion).
    - Once within ``position_tolerance`` of the goal, the robot stops
      translating and rotates in place to the desired heading.
    - Velocities decrease as the robot approaches the goal.

    **Verification**

    .. code-block:: console

       # Terminal 1
       ros2 launch rosbot_gazebo empty_world.launch.py

       # Terminal 2
       cd ~/enpm605_ws && colcon build --symlink-install --packages-select robot_control_demo
       source install/setup.bash
       ros2 run robot_control_demo goto_goal --ros-args \
           -p goal_x:=3.0 -p goal_y:=2.0 -p goal_heading:=1.57

       # Optional: visualize in RViz2 with Odometry display on /odometry/filtered
