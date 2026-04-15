====================================================
Simulation and Provided Infrastructure
====================================================


Simulation Setup
================

The simulation uses a custom Gazebo world with three ArUco boxes arranged
in a triangle. The world file is located at:

.. code-block:: text

   ~/rosbot_ws/src/husarion_gz_worlds/worlds/aruco_triangle_world.sdf

**World layout:**

.. list-table::
   :widths: 10 25 15 50
   :header-rows: 1
   :class: compact-table

   * - Box
     - Position (x, y, z)
     - Yaw
     - Marker orientation
   * - box_1
     - (4.0, 0.0, 0.25)
     - 0
     - Marker faces **-X** (toward the origin)
   * - box_2
     - (0.0, 4.0, 0.25)
     - |pi|/2
     - Marker faces **-Y** (toward the origin)
   * - box_3
     - (0.0, -4.0, 0.25)
     - -|pi|/2
     - Marker faces **+Y** (toward the origin)

.. |pi| unicode:: U+03C0

The robot starts at the origin ``(0, 0, 0)``.

**Launch the simulation** (in a separate terminal sourced from ``~/rosbot_ws``):

.. code-block:: console

   ros2 launch rosbot_gazebo simulation.yaml \
       gz_world:=$HOME/rosbot_ws/src/husarion_gz_worlds/worlds/aruco_triangle_world.sdf \
       robot_model:=rosbot_xl


Provided Infrastructure
=======================

The following nodes are **provided** and must be launched from your launch
file. Do **not** copy or modify them.


.. dropdown:: Proportional Controller (``robot_control_demo/p_controller``)
   :open:

   A two-phase proportional controller that drives the robot to a goal
   position **and** orientation.

   **Interface:**

   .. list-table::
      :widths: 25 30 45
      :header-rows: 1
      :class: compact-table

      * - Direction
        - Topic / Type
        - Description
      * - **Subscribes**
        - ``/goal_pose`` (``PoseStamped``)
        - Goal position (x, y) and orientation (yaw, encoded as a
          quaternion). Publishing a new goal resets the controller.
      * - **Subscribes**
        - ``/odometry/filtered`` (``Odometry``)
        - Robot pose feedback from the EKF.
      * - **Publishes**
        - ``/cmd_vel`` (``TwistStamped``)
        - Velocity commands to the differential-drive controller.
      * - **Publishes**
        - ``/goal_reached`` (``Bool``)
        - Publishes ``True`` when the robot has reached the goal
          position **and** orientation within tolerance.

   **Behavior:**

   - When no goal is set (default parameters are all zero), the
     controller idles and waits for a ``PoseStamped`` on ``/goal_pose``.
   - **Phase 1 (position):** drives toward ``(goal_x, goal_y)`` using
     proportional gains ``k_rho`` (linear) and ``k_alpha`` (angular).
   - **Phase 2 (orientation):** once within ``goal_tolerance`` of the
     target position, rotates in place to reach ``goal_yaw`` using gain
     ``k_yaw``.
   - When both tolerances are satisfied, publishes ``Bool(data=True)``
     on ``/goal_reached`` and sends a zero-velocity stop command.

   **Parameters:**

   .. list-table::
      :widths: 25 15 60
      :header-rows: 1
      :class: compact-table

      * - Parameter
        - Default
        - Description
      * - ``k_rho``
        - 0.4
        - Proportional gain on distance to goal (linear velocity).
      * - ``k_alpha``
        - 0.8
        - Proportional gain on heading error (angular velocity, phase 1).
      * - ``k_yaw``
        - 0.8
        - Proportional gain on yaw error (angular velocity, phase 2).
      * - ``goal_tolerance``
        - 0.10
        - Distance in meters at which the position goal is reached.
      * - ``yaw_tolerance``
        - 0.05
        - Yaw error in radians at which the orientation goal is reached.

   **Publishing a goal** (convert yaw to quaternion using ``scipy``):

   .. code-block:: python

      from geometry_msgs.msg import PoseStamped
      from scipy.spatial.transform import Rotation as R

      goal = PoseStamped()
      goal.header.stamp = self.get_clock().now().to_msg()
      goal.header.frame_id = "odom"
      goal.pose.position.x = 2.0
      goal.pose.position.y = 0.0
      quat = R.from_euler("z", 1.5708).as_quat()  # [x, y, z, w]
      goal.pose.orientation.x = quat[0]
      goal.pose.orientation.y = quat[1]
      goal.pose.orientation.z = quat[2]
      goal.pose.orientation.w = quat[3]
      self._goal_pub.publish(goal)


.. dropdown:: ArUco Detector (``frame_demo/aruco_detector``)
   :open:

   Detects ArUco markers in the robot's camera stream and broadcasts
   each marker's 6-DoF pose as a TF frame.

   **TF output:**

   - **Parent frame:** the camera optical frame (from the image header,
     typically ``oak_rgb_camera_frame``).
   - **Child frame:** ``aruco_marker_<id>`` where ``<id>`` is the
     integer marker ID detected by OpenCV (e.g., ``aruco_marker_2``,
     ``aruco_marker_4``, ``aruco_marker_5``).

   The TF tree chains these frames automatically:

   .. code-block:: text

      odom -> base_link -> ... -> oak_rgb_camera_frame -> aruco_marker_<id>

   This means you can look up the marker pose **relative to odom** with:

   .. code-block:: python

      transform = self._tf_buffer.lookup_transform(
          "odom",                          # target frame
          f"aruco_marker_{marker_id}",     # source frame
          rclpy.time.Time(),               # latest available
          rclpy.duration.Duration(seconds=1.0),  # timeout
      )
      marker_x = transform.transform.translation.x
      marker_y = transform.transform.translation.y

   **Parameters:**

   .. list-table::
      :widths: 30 15 55
      :header-rows: 1
      :class: compact-table

      * - Parameter
        - Default
        - Description
      * - ``camera_image_topic``
        - ``/oak/rgb/color``
        - Color image topic to subscribe to.
      * - ``camera_info_topic``
        - ``/oak/stereo/camera_info``
        - CameraInfo topic with camera intrinsics.
      * - ``marker_size``
        - 0.194
        - Physical edge length of each ArUco marker (meters).
      * - ``dictionary_id``
        - ``DICT_5X5_250``
        - OpenCV ArUco dictionary constant name.

   .. note::

      The marker IDs visible at each waypoint depend on which face of the
      ArUco box is oriented toward the camera. You will **not** know the
      IDs in advance. Your code must dynamically discover which marker ID
      is visible and look up the corresponding TF frame.


Waypoints Configuration
=======================

The following YAML file defines the three waypoints where the robot should
navigate to observe the ArUco markers. **Copy this file into your
package** at ``config/waypoints.yaml``.

.. code-block:: yaml

   # Waypoints for the ArUco marker triangle assignment.
   #
   # Each waypoint is a viewing position where the robot's forward-facing
   # camera has a clear line-of-sight to one ArUco box.
   #
   # World layout (aruco_triangle_world.sdf):
   #   Box 1: (4.0,  0.0, 0.25)  yaw=0      -> marker faces -X
   #   Box 2: (0.0,  4.0, 0.25)  yaw=pi/2   -> marker faces -Y
   #   Box 3: (0.0, -4.0, 0.25)  yaw=-pi/2  -> marker faces +Y
   #
   # Arrays are parallel: waypoint_x[i], waypoint_y[i], waypoint_yaw[i]
   # define the i-th goal pose.

   /**:
     ros__parameters:
       waypoint_x:   [ 2.0,  0.0,  0.0]
       waypoint_y:   [ 0.0,  2.0, -2.0]
       waypoint_yaw: [ 0.0,  1.5708, -1.5708]


.. important::

   Load this file in your launch file using the ``parameters`` field of
   the ``Node`` action so that ``waypoint_x``, ``waypoint_y``, and
   ``waypoint_yaw`` are available in your navigator node via
   ``self.get_parameter()``.
