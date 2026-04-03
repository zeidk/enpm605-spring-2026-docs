====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Prerequisites
====================================================

One-time workspace and environment setup required before running any
code in this lecture.


.. dropdown:: One-Time Setup

   Clone the course workspace and configure your shell so ROS 2 can
   find all packages automatically.

   **Clone the course workspace**

   .. code-block:: console

      git clone https://github.com/zeidk/enpm605-spring-2026-ros.git ~/enpm605_ws

   **Add the setup script to your shell rc file**

   .. code-block:: console

      # Bash users
      echo "source ~/enpm605_ws/enpm605.sh" >> ~/.bashrc

      # Zsh users
      echo "source ~/enpm605_ws/enpm605.sh" >> ~/.zshrc

   **Reload your shell**

   .. code-block:: console

      source ~/.bashrc   # bash users
      source ~/.zshrc    # zsh users

   **Run the setup function once per terminal**

   .. code-block:: console

      enpm605

   .. note::

      The ``enpm605`` function must be run once in every new terminal
      before using ``ros2`` commands. It sources the ROS 2 base
      installation and the course workspace in the correct order.


.. dropdown:: Gazebo Harmonic Installation

   Gazebo Harmonic should already be installed if you followed the
   course VM setup. Verify the installation:

   .. code-block:: console

      gz sim --version

   If Gazebo is not installed, follow the official installation guide
   for Ubuntu 24.04:

   .. code-block:: console

      sudo apt-get update
      sudo apt-get install ros-jazzy-ros-gz

   This metapackage installs Gazebo Harmonic along with all ROS 2
   integration packages (``ros_gz_bridge``, ``ros_gz_sim``,
   ``ros_gz_image``).


Introduction to Gazebo Harmonic
====================================================

Gazebo is a high-fidelity 3D robotics simulator that provides
physics simulation, sensor models, and rendering for testing robot
software before deploying on real hardware.


.. dropdown:: What Is Gazebo?

   Gazebo simulates robots in a virtual 3D world with realistic
   physics (contacts, gravity, friction), sensor models (lidar,
   camera, IMU, GPS), and actuator dynamics. It allows you to:

   - Test control algorithms without risking hardware damage.
   - Iterate rapidly on software without setting up physical robots.
   - Generate reproducible test scenarios for regression testing.
   - Simulate multiple robots and complex environments.

   Gazebo is the most widely used simulator in the ROS ecosystem and
   is the default simulator for many robotics competitions, including
   the DARPA SubT Challenge and the RoboCup Virtual Robot League.


.. dropdown:: Gazebo Harmonic vs. Gazebo Classic

   Gazebo has undergone a major architecture rewrite. The naming can
   be confusing:

   - **Gazebo Classic** (versions 1-11): The original simulator,
     tightly coupled with ROS 1. End-of-life as of 2025.
   - **Gazebo** (formerly Ignition Gazebo): The modern rewrite with a
     modular plugin architecture, improved rendering (Ogre 2.x), and
     a transport layer independent of ROS.

   **Gazebo Harmonic** is a Long-Term Support (LTS) release paired
   with ROS 2 Jazzy. Key differences from Classic:

   .. list-table::
      :header-rows: 1
      :widths: 30 35 35

      * - Feature
        - Gazebo Classic
        - Gazebo Harmonic
      * - Transport
        - Custom (gazebo transport)
        - Gazebo Transport (Protobuf-based)
      * - Physics engine
        - ODE (default)
        - DART (default), Bullet, TPE
      * - Rendering
        - Ogre 1.x
        - Ogre 2.x (PBR, shadows)
      * - Plugin API
        - Monolithic
        - Entity-Component-System (ECS)
      * - ROS integration
        - Built-in
        - Via ``ros_gz_bridge``
      * - Model format
        - SDF + URDF
        - SDF (preferred) + URDF

   .. warning::

      Do not install Gazebo Classic alongside Gazebo Harmonic. The
      packages conflict and will cause build failures.


.. dropdown:: Architecture Overview

   Gazebo Harmonic uses an Entity-Component-System (ECS) architecture:

   - **Entities** are unique identifiers (integers) for every object
     in the simulation: worlds, models, links, joints, sensors.
   - **Components** are data attached to entities: pose, velocity,
     mesh geometry, sensor configuration.
   - **Systems** are plugins that operate on components each
     simulation step: physics, rendering, sensor data generation,
     user plugins.

   The simulation server (``gz sim -s``) runs headless and handles
   physics. The GUI client (``gz sim -g``) connects for visualization.
   They communicate over Gazebo Transport, which is independent of
   ROS 2.


.. dropdown:: Verifying the Installation

   After installing, confirm that both the simulator and ROS 2
   integration are functional:

   .. code-block:: console

      # Check Gazebo version
      gz sim --version

      # Launch an empty world
      gz sim empty.sdf

      # Check ROS 2 bridge package
      ros2 pkg list | grep ros_gz

   You should see packages including ``ros_gz_bridge``,
   ``ros_gz_sim``, and ``ros_gz_image`` in the output.

   .. tip::

      If ``gz sim`` fails with a rendering error in a VM, ensure
      3D acceleration is enabled in your VM settings and that the
      ``LIBGL_ALWAYS_SOFTWARE=1`` environment variable is set if
      needed.


SDF World and Model Files
====================================================

Simulation Description Format (SDF) is the XML-based format used to
describe worlds, models, sensors, and physics in Gazebo.


.. dropdown:: World File Structure

   A world file defines the simulation environment: ground plane,
   lighting, physics parameters, and models. A minimal world:

   .. code-block:: xml

      <?xml version="1.0" ?>
      <sdf version="1.9">
        <world name="demo_world">

          <!-- Physics configuration -->
          <physics name="1ms" type="dart">
            <max_step_size>0.001</max_step_size>
            <real_time_factor>1.0</real_time_factor>
          </physics>

          <!-- Plugins required for simulation -->
          <plugin filename="gz-sim-physics-system"
                  name="gz::sim::systems::Physics"/>
          <plugin filename="gz-sim-scene-broadcaster-system"
                  name="gz::sim::systems::SceneBroadcaster"/>
          <plugin filename="gz-sim-user-commands-system"
                  name="gz::sim::systems::UserCommands"/>
          <plugin filename="gz-sim-sensors-system"
                  name="gz::sim::systems::Sensors">
            <render_engine>ogre2</render_engine>
          </plugin>

          <!-- Lighting -->
          <light type="directional" name="sun">
            <cast_shadows>true</cast_shadows>
            <pose>0 0 10 0 0 0</pose>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </light>

          <!-- Ground plane -->
          <include>
            <uri>
              https://fuel.gazebosim.org/1.0/OpenRobotics/models/Ground Plane
            </uri>
          </include>

        </world>
      </sdf>

   .. note::

      The ``physics``, ``SceneBroadcaster``, ``UserCommands``, and
      ``Sensors`` system plugins must be included explicitly in Gazebo
      Harmonic. Without them, physics will not step, models will not
      appear in the GUI, and sensors will not produce data.


.. dropdown:: Model Definition

   A model in SDF consists of links (rigid bodies) connected by
   joints. Each link has visual (appearance), collision (physics),
   and inertial (mass) properties:

   .. code-block:: xml

      <model name="simple_robot">
        <pose>0 0 0.1 0 0 0</pose>

        <link name="base_link">
          <inertial>
            <mass>5.0</mass>
            <inertia>
              <ixx>0.042</ixx><iyy>0.042</iyy><izz>0.075</izz>
            </inertia>
          </inertial>

          <visual name="base_visual">
            <geometry>
              <box><size>0.4 0.3 0.1</size></box>
            </geometry>
            <material>
              <ambient>0.2 0.2 0.8 1</ambient>
            </material>
          </visual>

          <collision name="base_collision">
            <geometry>
              <box><size>0.4 0.3 0.1</size></box>
            </geometry>
          </collision>
        </link>
      </model>

   .. tip::

      Always define inertial properties for every link. Without them,
      the physics engine treats the link as having zero mass, which
      causes numerical instability and unrealistic behavior.


.. dropdown:: Adding Sensors

   Sensors are attached to links and generate data each simulation
   step. Common sensor types:

   **Lidar sensor:**

   .. code-block:: xml

      <sensor name="lidar" type="gpu_lidar">
        <pose>0 0 0.15 0 0 0</pose>
        <update_rate>10</update_rate>
        <lidar>
          <scan>
            <horizontal>
              <samples>360</samples>
              <resolution>1</resolution>
              <min_angle>-3.14159</min_angle>
              <max_angle>3.14159</max_angle>
            </horizontal>
          </scan>
          <range>
            <min>0.1</min>
            <max>10.0</max>
          </range>
        </lidar>
        <always_on>true</always_on>
        <visualize>true</visualize>
        <topic>lidar</topic>
      </sensor>

   **Camera sensor:**

   .. code-block:: xml

      <sensor name="camera" type="camera">
        <pose>0.2 0 0.15 0 0 0</pose>
        <update_rate>30</update_rate>
        <camera>
          <horizontal_fov>1.047</horizontal_fov>
          <image>
            <width>640</width>
            <height>480</height>
          </image>
          <clip>
            <near>0.1</near>
            <far>100</far>
          </clip>
        </camera>
        <always_on>true</always_on>
        <topic>camera</topic>
      </sensor>

   **IMU sensor:**

   .. code-block:: xml

      <sensor name="imu" type="imu">
        <update_rate>100</update_rate>
        <imu>
          <angular_velocity>
            <x><noise type="gaussian">
              <mean>0.0</mean><stddev>0.001</stddev>
            </noise></x>
          </angular_velocity>
        </imu>
        <always_on>true</always_on>
        <topic>imu</topic>
      </sensor>


.. dropdown:: Physics Settings

   The ``<physics>`` element controls simulation accuracy and speed:

   - ``max_step_size``: Time advanced per physics step (default
     ``0.001`` s). Smaller values increase accuracy but reduce speed.
   - ``real_time_factor``: Target ratio of simulation time to wall
     time. ``1.0`` means real-time; ``0`` means run as fast as
     possible.

   .. code-block:: xml

      <physics name="sim_physics" type="dart">
        <max_step_size>0.001</max_step_size>
        <real_time_factor>1.0</real_time_factor>
      </physics>

   .. warning::

      Setting ``max_step_size`` too large (e.g., ``0.01``) can cause
      objects to pass through each other and joints to become
      unstable. For contact-heavy simulations, keep it at ``0.001``
      or smaller.


ros_gz_bridge
====================================================

Since Gazebo Harmonic uses its own transport layer (Gazebo Transport),
a bridge is needed to convert Gazebo messages into ROS 2 messages and
vice versa.


.. dropdown:: What Is ros_gz_bridge?

   ``ros_gz_bridge`` is a ROS 2 node that subscribes to Gazebo
   Transport topics and republishes their data as ROS 2 messages (and
   vice versa). It handles the serialization conversion between
   Gazebo's Protobuf messages and ROS 2's IDL messages.

   Without the bridge, ``ros2 topic list`` will not show any Gazebo
   sensor data, and ``ros2 topic pub`` commands will not reach
   Gazebo actuators.


.. dropdown:: Configuring the Bridge

   The bridge can be configured via command-line arguments or a YAML
   parameter file. The command-line approach specifies each bridge
   mapping as a string:

   .. code-block:: console

      ros2 run ros_gz_bridge parameter_bridge \
        /lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan \
        /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist \
        /camera@sensor_msgs/msg/Image[gz.msgs.Image \
        /imu@sensor_msgs/msg/Imu[gz.msgs.IMU

   The syntax for each mapping is:

   - ``/topic@ros_type[gz_type`` -- Gazebo to ROS 2 (one-way)
   - ``/topic@ros_type]gz_type`` -- ROS 2 to Gazebo (one-way)
   - ``/topic@ros_type[gz_type`` -- bidirectional (use ``@`` alone)

   .. note::

      The direction brackets are easy to confuse. Think of ``[`` as
      data flowing **from** Gazebo (left) **into** ROS 2 (right), and
      ``]`` as data flowing **from** ROS 2 (left) **into** Gazebo
      (right).


.. dropdown:: Common Bridge Mappings

   .. list-table::
      :header-rows: 1
      :widths: 25 35 35

      * - Use Case
        - ROS 2 Type
        - Gazebo Type
      * - Laser scan
        - ``sensor_msgs/msg/LaserScan``
        - ``gz.msgs.LaserScan``
      * - Camera image
        - ``sensor_msgs/msg/Image``
        - ``gz.msgs.Image``
      * - IMU data
        - ``sensor_msgs/msg/Imu``
        - ``gz.msgs.IMU``
      * - Velocity command
        - ``geometry_msgs/msg/Twist``
        - ``gz.msgs.Twist``
      * - Odometry
        - ``nav_msgs/msg/Odometry``
        - ``gz.msgs.Odometry``
      * - Clock
        - ``rosgraph_msgs/msg/Clock``
        - ``gz.msgs.Clock``
      * - Joint state
        - ``sensor_msgs/msg/JointState``
        - ``gz.msgs.Model``
      * - TF
        - ``tf2_msgs/msg/TFMessage``
        - ``gz.msgs.Pose_V``

   .. tip::

      Always bridge the ``/clock`` topic when running Gazebo. This
      ensures all ROS 2 nodes use simulation time rather than wall
      clock time. Set ``use_sim_time:=true`` on all nodes.


.. dropdown:: Bridge in a Launch File

   In practice, the bridge is started from a launch file alongside
   Gazebo:

   .. code-block:: python

      from launch import LaunchDescription
      from launch_ros.actions import Node

      def generate_launch_description():
          bridge = Node(
              package='ros_gz_bridge',
              executable='parameter_bridge',
              arguments=[
                  '/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                  '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                  '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
                  '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
              ],
              parameters=[{'use_sim_time': True}],
              output='screen',
          )

          return LaunchDescription([bridge])


Spawning Robots
====================================================

Once a Gazebo world is running, robot models can be spawned into
the simulation programmatically.


.. dropdown:: Using ros_gz_sim create

   The ``ros_gz_sim`` package provides a ``create`` node that spawns
   SDF or URDF models into a running Gazebo simulation:

   .. code-block:: console

      ros2 run ros_gz_sim create \
        -name my_robot \
        -file /path/to/robot.sdf \
        -x 0.0 -y 0.0 -z 0.1

   Arguments:

   - ``-name``: Unique name for the spawned model in Gazebo.
   - ``-file``: Path to the SDF or URDF file.
   - ``-x``, ``-y``, ``-z``: Initial position.
   - ``-R``, ``-P``, ``-Y``: Initial roll, pitch, yaw (radians).
   - ``-topic``: Alternative: provide the model description on a
     ROS 2 topic.

   .. warning::

      Spawning a model with a name that already exists in the
      simulation will fail silently. Always use unique names or
      delete existing models first.


.. dropdown:: Spawning from a Launch File

   .. code-block:: python

      from launch import LaunchDescription
      from launch_ros.actions import Node

      def generate_launch_description():
          spawn = Node(
              package='ros_gz_sim',
              executable='create',
              arguments=[
                  '-name', 'diff_drive_robot',
                  '-file', '/path/to/diff_drive.sdf',
                  '-x', '0.0',
                  '-y', '0.0',
                  '-z', '0.1',
              ],
              output='screen',
          )

          return LaunchDescription([spawn])

   .. tip::

      Use ``os.path.join(get_package_share_directory('gazebo_demo'),
      'models', 'robot.sdf')`` to locate model files relative to
      the installed package, rather than hardcoding absolute paths.


.. dropdown:: Model States and Initial Pose

   After spawning, the model's state (pose, velocity) is managed by
   the physics engine. You can query the model state using Gazebo
   Transport:

   .. code-block:: console

      gz topic -e -t /world/demo_world/dynamic_pose/info

   To set the initial pose precisely, use the spawn arguments
   (``-x``, ``-y``, ``-z``, ``-R``, ``-P``, ``-Y``). Alternatively,
   the ``UserCommands`` system plugin allows you to set model poses
   at runtime through Gazebo Transport services.


TF2 Fundamentals
====================================================

TF2 is the ROS 2 transform library that tracks the pose of every
coordinate frame in a robotic system over time.


.. dropdown:: Coordinate Frames and Transforms

   Every component of a robot has its own coordinate frame: the base,
   each wheel, each sensor, the end-effector. TF2 maintains a tree
   of transforms that relates all frames to each other.

   A transform specifies the position (translation) and orientation
   (rotation as a quaternion) of one frame relative to another:

   - ``map`` -> ``odom`` -> ``base_link`` -> ``lidar_link``
   - ``map`` -> ``odom`` -> ``base_link`` -> ``camera_link``

   To find the pose of the lidar in the map frame, TF2 chains the
   transforms: ``map`` -> ``odom`` -> ``base_link`` ->
   ``lidar_link``.

   .. note::

      TF2 organizes frames as a **tree**, not a graph. Every frame
      has exactly one parent. There are no cycles and no frames with
      multiple parents.


.. dropdown:: Static vs. Dynamic Transforms

   - **Static transforms** never change over time. Example: the
     fixed offset from ``base_link`` to ``lidar_link`` on a robot
     where the lidar is bolted to the chassis. Published once on
     ``/tf_static`` with ``TRANSIENT_LOCAL`` durability.

   - **Dynamic transforms** change continuously. Example: the
     transform from ``odom`` to ``base_link`` updates as the robot
     moves. Published on ``/tf`` at a regular rate.

   .. code-block:: console

      # View the current TF tree
      ros2 run tf2_tools view_frames

      # Echo a specific transform
      ros2 run tf2_ros tf2_echo map base_link

   .. tip::

      Use ``ros2 run tf2_tools view_frames`` to generate a PDF of
      the complete TF tree. This is invaluable for debugging
      transform issues.


.. dropdown:: Writing a Transform Broadcaster

   A transform broadcaster publishes transforms to the ``/tf`` or
   ``/tf_static`` topic. Here is a dynamic broadcaster that
   publishes the ``odom`` -> ``base_link`` transform:

   .. code-block:: python

      import rclpy
      from rclpy.node import Node
      from geometry_msgs.msg import TransformStamped
      from tf2_ros import TransformBroadcaster
      import math


      class OdomBroadcaster(Node):
          def __init__(self):
              super().__init__('odom_broadcaster')
              self._tf_broadcaster = TransformBroadcaster(self)
              self._timer = self.create_timer(0.1, self._broadcast_transform)
              self._x = 0.0
              self._theta = 0.0

          def _broadcast_transform(self):
              t = TransformStamped()
              t.header.stamp = self.get_clock().now().to_msg()
              t.header.frame_id = 'odom'
              t.child_frame_id = 'base_link'

              t.transform.translation.x = self._x
              t.transform.translation.y = 0.0
              t.transform.translation.z = 0.0

              # Quaternion from yaw angle
              t.transform.rotation.z = math.sin(self._theta / 2.0)
              t.transform.rotation.w = math.cos(self._theta / 2.0)

              self._tf_broadcaster.sendTransform(t)

              # Simulate forward motion
              self._x += 0.01

   For static transforms, use ``StaticTransformBroadcaster`` instead:

   .. code-block:: python

      from tf2_ros import StaticTransformBroadcaster

      self._static_broadcaster = StaticTransformBroadcaster(self)
      # Call sendTransform() once in __init__


.. dropdown:: Writing a Transform Listener

   A transform listener queries the TF2 buffer for the transform
   between any two frames:

   .. code-block:: python

      import rclpy
      from rclpy.node import Node
      from tf2_ros import Buffer, TransformListener


      class FrameListener(Node):
          def __init__(self):
              super().__init__('frame_listener')
              self._tf_buffer = Buffer()
              self._tf_listener = TransformListener(self._tf_buffer, self)
              self._timer = self.create_timer(1.0, self._on_timer)

          def _on_timer(self):
              try:
                  transform = self._tf_buffer.lookup_transform(
                      'map', 'base_link', rclpy.time.Time()
                  )
                  pos = transform.transform.translation
                  self.get_logger().info(
                      f'Robot at: x={pos.x:.2f}, y={pos.y:.2f}, z={pos.z:.2f}'
                  )
              except Exception as e:
                  self.get_logger().warn(f'Transform not available: {e}')

   .. note::

      Passing ``rclpy.time.Time()`` (time zero) to
      ``lookup_transform`` requests the **latest** available
      transform. To get the transform at a specific time, pass a
      ``Time`` message.


Mobile Robot Control
====================================================

Mobile robot control in ROS 2 revolves around velocity commands
(``cmd_vel``), the differential drive model, and sensor feedback.


.. dropdown:: cmd_vel and Twist Messages

   The standard interface for commanding mobile robot velocity in
   ROS 2 is the ``/cmd_vel`` topic using ``geometry_msgs/msg/Twist``
   messages:

   .. code-block:: python

      from geometry_msgs.msg import Twist

      msg = Twist()
      msg.linear.x = 0.5    # Forward velocity (m/s)
      msg.linear.y = 0.0    # Lateral velocity (0 for diff drive)
      msg.linear.z = 0.0    # Vertical velocity (0 for ground robot)
      msg.angular.x = 0.0   # Roll rate (0 for ground robot)
      msg.angular.y = 0.0   # Pitch rate (0 for ground robot)
      msg.angular.z = 0.3   # Yaw rate (rad/s)

   For a differential-drive robot, only ``linear.x`` (forward/backward)
   and ``angular.z`` (turn left/right) are used. All other fields
   must be ``0.0``.

   .. warning::

      Sending a single ``Twist`` message moves the robot briefly,
      then the velocity command expires and the robot stops (depending
      on the controller timeout). You must publish ``cmd_vel``
      continuously (typically at 10-50 Hz) to maintain motion.


.. dropdown:: Differential Drive Plugin

   In Gazebo, a differential-drive controller is added to the robot
   model as a system plugin:

   .. code-block:: xml

      <plugin filename="gz-sim-diff-drive-system"
              name="gz::sim::systems::DiffDrive">
        <left_joint>left_wheel_joint</left_joint>
        <right_joint>right_wheel_joint</right_joint>
        <wheel_separation>0.3</wheel_separation>
        <wheel_radius>0.05</wheel_radius>
        <max_linear_acceleration>1.0</max_linear_acceleration>
        <max_angular_acceleration>2.0</max_angular_acceleration>
        <odom_publish_frequency>50</odom_publish_frequency>
        <topic>cmd_vel</topic>
        <odom_topic>odom</odom_topic>
        <frame_id>odom</frame_id>
        <child_frame_id>base_link</child_frame_id>
        <tf_topic>tf</tf_topic>
      </plugin>

   This plugin:

   - Subscribes to ``cmd_vel`` on Gazebo Transport.
   - Computes individual wheel velocities from the Twist command.
   - Publishes odometry on the ``odom`` topic.
   - Publishes the ``odom`` -> ``base_link`` transform on ``tf``.


.. dropdown:: Teleop

   For manual testing, use ``teleop_twist_keyboard`` to send
   ``cmd_vel`` commands from the keyboard:

   .. code-block:: console

      ros2 run teleop_twist_keyboard teleop_twist_keyboard

   This node reads key presses and publishes corresponding ``Twist``
   messages. Use ``i`` to go forward, ``j``/``l`` to turn, ``k`` to
   stop, and ``,`` to go backward.

   .. tip::

      Install teleop if not available:

      .. code-block:: console

         sudo apt-get install ros-jazzy-teleop-twist-keyboard


.. dropdown:: Reading Sensor Data in Python

   **Lidar (LaserScan):**

   .. code-block:: python

      from sensor_msgs.msg import LaserScan


      class LidarReader(Node):
          def __init__(self):
              super().__init__('lidar_reader')
              self.create_subscription(
                  LaserScan, '/lidar', self._lidar_callback, 10
              )

          def _lidar_callback(self, msg: LaserScan):
              # msg.ranges is a list of distances (meters)
              min_dist = min(msg.ranges)
              self.get_logger().info(f'Closest obstacle: {min_dist:.2f} m')

   **Camera (Image):**

   .. code-block:: python

      from sensor_msgs.msg import Image


      class CameraReader(Node):
          def __init__(self):
              super().__init__('camera_reader')
              self.create_subscription(
                  Image, '/camera', self._image_callback, 10
              )

          def _image_callback(self, msg: Image):
              self.get_logger().info(
                  f'Image: {msg.width}x{msg.height}, '
                  f'encoding: {msg.encoding}'
              )

   **IMU:**

   .. code-block:: python

      from sensor_msgs.msg import Imu


      class ImuReader(Node):
          def __init__(self):
              super().__init__('imu_reader')
              self.create_subscription(
                  Imu, '/imu', self._imu_callback, 10
              )

          def _imu_callback(self, msg: Imu):
              accel = msg.linear_acceleration
              self.get_logger().info(
                  f'Accel: x={accel.x:.2f}, y={accel.y:.2f}, z={accel.z:.2f}'
              )

   .. note::

      All sensor subscriber nodes must set ``use_sim_time`` to
      ``True`` when running with Gazebo so that message timestamps
      are consistent with simulation time.


Putting It Together
====================================================

A complete simulation pipeline involves launching Gazebo, starting
the bridge, spawning the robot, and running control and sensing
nodes.


.. dropdown:: Complete Launch File

   The following launch file demonstrates the full pipeline:

   .. code-block:: python

      import os
      from launch import LaunchDescription
      from launch.actions import (
          DeclareLaunchArgument,
          IncludeLaunchDescription,
      )
      from launch.launch_description_sources import (
          PythonLaunchDescriptionSource,
      )
      from launch_ros.actions import Node
      from ament_index_python.packages import get_package_share_directory


      def generate_launch_description():
          pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
          pkg_gazebo_demo = get_package_share_directory('gazebo_demo')

          world_file = os.path.join(
              pkg_gazebo_demo, 'worlds', 'demo_world.sdf'
          )

          # 1. Start Gazebo
          gazebo = IncludeLaunchDescription(
              PythonLaunchDescriptionSource(
                  os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
              ),
              launch_arguments={'gz_args': f'-r {world_file}'}.items(),
          )

          # 2. Spawn the robot
          spawn = Node(
              package='ros_gz_sim',
              executable='create',
              arguments=[
                  '-name', 'diff_drive_robot',
                  '-file', os.path.join(
                      pkg_gazebo_demo, 'models', 'diff_drive.sdf'
                  ),
                  '-x', '0.0', '-y', '0.0', '-z', '0.1',
              ],
              output='screen',
          )

          # 3. Bridge Gazebo topics to ROS 2
          bridge = Node(
              package='ros_gz_bridge',
              executable='parameter_bridge',
              arguments=[
                  '/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                  '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                  '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
                  '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                  '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                  '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
              ],
              parameters=[{'use_sim_time': True}],
              output='screen',
          )

          # 4. Robot control node
          controller = Node(
              package='robot_control_demo',
              executable='robot_controller',
              parameters=[{'use_sim_time': True}],
              output='screen',
          )

          return LaunchDescription([
              gazebo,
              spawn,
              bridge,
              controller,
          ])


.. dropdown:: Driving the Robot

   With the simulation running, you can drive the robot from the
   command line:

   .. code-block:: console

      # Drive forward at 0.2 m/s
      ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
        "{linear: {x: 0.2}, angular: {z: 0.0}}"

      # Turn in place at 0.5 rad/s
      ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
        "{linear: {x: 0.0}, angular: {z: 0.5}}"

      # Stop the robot
      ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
        "{linear: {x: 0.0}, angular: {z: 0.0}}"


.. dropdown:: Verifying the System

   Once the launch file is running, verify all components:

   .. code-block:: console

      # Check active topics
      ros2 topic list

      # Verify sensor data is flowing
      ros2 topic hz /lidar
      ros2 topic hz /imu

      # Check the TF tree
      ros2 run tf2_tools view_frames

      # Echo odometry
      ros2 topic echo /odom --once

      # Check that the bridge is active
      ros2 node list | grep bridge

   .. tip::

      If sensor topics are not visible, check that:

      1. The Gazebo world includes the ``Sensors`` system plugin.
      2. The ``ros_gz_bridge`` is running with correct topic mappings.
      3. Sensor topics match between the SDF file and bridge config.
