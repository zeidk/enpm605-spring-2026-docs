====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Prerequisites
====================================================

One-time workspace and environment setup required before running any
code in this lecture.



.. dropdown:: Build the Demo Packages
   :open:

   Pull the latest code and build all demo packages used in this
   lecture before proceeding.

   .. code-block:: console

      cd ~/enpm605_ws
      git pull

   .. code-block:: console

      colcon build --symlink-install --packages-select parameters_demo custom_interfaces service_demo action_demo

   Source the workspace after each build:

   .. code-block:: console

      source install/setup.bash


Parameters
====================================================

A **parameter** is a configurable value that can be used to customize
the behavior of a node at runtime without modifying the code. Parameters
allow nodes to store and retrieve data, such as tuning constants, file
paths, or robot-specific settings.

.. code-block:: console

   colcon build --symlink-install --packages-select parameters_demo

**Resources**

- `Using Parameters in a Class (Python)
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html>`_
- `About Parameters
  <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html>`_
- `Using ros2 param
  <https://docs.ros.org/en/jazzy/How-To-Guides/Using-ros2-param.html>`_


.. dropdown:: Characteristics

   - Parameters can be set or updated during runtime using the CLI or
     within the node itself.
   - Nodes can declare and retrieve parameters, making them useful for
     settings that do not change frequently.
   - Parameters can have the following types: ``bool``, ``bool[]``,
     ``int``, ``int[]``, ``double``, ``double[]``, ``string``,
     ``string[]``, and ``byte[]``.

   .. warning::

      Each parameter belongs to a specific node and cannot be accessed
      globally by other nodes.


.. dropdown:: Sensor Node Parameters -- Real-World Example

   Sensor nodes in robotics typically expose many parameters to control
   hardware behavior. The table below shows example parameters for a
   camera node and a LiDAR node, along with their update behavior:

   **Camera Node Parameters**

   .. list-table::
      :widths: 30 12 20 18
      :header-rows: 1
      :class: compact-table

      * - Parameter
        - Type
        - Default
        - Update
      * - ``camera_name``
        - ``str``
        - ``"front_cam"``
        - Freely writable
      * - ``camera_frame_id``
        - ``str``
        - ``"cam_link"``
        - Freely writable
      * - ``fps``
        - ``int``
        - ``30``
        - Timer rebuild
      * - ``exposure_auto``
        - ``bool``
        - ``True``
        - Freely writable
      * - ``exposure_time_us``
        - ``int``
        - ``10000``
        - Freely writable
      * - ``brightness``
        - ``int``
        - ``128``
        - Freely writable
      * - ``image_width``
        - ``int``
        - ``1920``
        - Node restart
      * - ``image_height``
        - ``int``
        - ``1080``
        - Node restart
      * - ``encoding``
        - ``str``
        - ``"bgr8"``
        - Node restart
      * - ``camera_info_url``
        - ``str``
        - ``""``
        - Node restart

   **LiDAR Node Parameters**

   .. list-table::
      :widths: 30 12 20 18
      :header-rows: 1
      :class: compact-table

      * - Parameter
        - Type
        - Default
        - Update
      * - ``lidar_name``
        - ``str``
        - ``"top_lidar"``
        - Freely writable
      * - ``lidar_frame_id``
        - ``str``
        - ``"lidar_link"``
        - Freely writable
      * - ``min_range``
        - ``float``
        - ``0.1``
        - Freely writable
      * - ``max_range``
        - ``float``
        - ``100.0``
        - Freely writable
      * - ``min_angle``
        - ``float``
        - ``-3.14159``
        - Freely writable
      * - ``max_angle``
        - ``float``
        - ``3.14159``
        - Freely writable
      * - ``intensity_threshold``
        - ``float``
        - ``0.0``
        - Freely writable
      * - ``scan_frequency``
        - ``int``
        - ``10``
        - Timer rebuild
      * - ``port``
        - ``str``
        - ``"/dev/lidar0"``
        - Node restart
      * - ``return_mode``
        - ``str``
        - ``"strongest"``
        - Node restart

   **Update categories:**

   - **Freely writable** -- the parameter can be changed at runtime and
     takes effect immediately.
   - **Timer rebuild** -- the parameter requires canceling and recreating
     the timer to change its frequency.
   - **Node restart** -- the parameter is read only during initialization
     and requires restarting the node to apply changes.


.. dropdown:: CLI for Parameters

   .. code-block:: console

      ros2 param -h

   .. code-block:: text

      Commands:
        delete      Delete parameter
        describe    Show descriptive information about declared parameters
        dump        Dump the parameters of a node to a yaml file
        get         Get parameter
        list        Output a list of available parameters
        load        Load parameter file for a node
        set         Set parameter

   **Demonstration**

   .. code-block:: console

      # Start a node
      ros2 run demo_nodes_py talker

      # List all parameters
      ros2 param list /talker

      # Get information about a parameter
      ros2 param get /talker use_sim_time


Declaring Parameters
----------------------------------------------------

Parameters **must be explicitly declared** before they can be accessed
within a node. If you try to access a parameter without declaring it
first, ROS 2 will throw an error.


.. dropdown:: Approach #1: Basic Declaration

   .. code-block:: python

      self.declare_parameter("camera_name", "front_cam")
      self.declare_parameter("fps", 30)

   - ``camera_name`` is given the default value ``"front_cam"``
   - ``fps`` is given the default value ``30``


.. dropdown:: Approach #2: Declaration with Constraints and Metadata

   .. code-block:: python

      from rcl_interfaces.msg import ParameterDescriptor, IntegerRange

      self.declare_parameter(
          "camera_name", "front_cam",
          descriptor=ParameterDescriptor(description="Name of the camera")
      )
      self.declare_parameter(
          "fps", 30,
          descriptor=ParameterDescriptor(
              description="Camera frame rate in Hz",
              integer_range=[IntegerRange(from_value=1, to_value=60, step=1)]
          )
      )

   .. note::

      Constraints and metadata will be used with
      ``ros2 param describe``.


.. dropdown:: Approach #3: Declaring Multiple Parameters at Once

   .. code-block:: python

      from rcl_interfaces.msg import ParameterDescriptor, IntegerRange

      self.declare_parameters(
          namespace="",
          parameters=[
              (
                  "camera_name", "front_cam",
                  ParameterDescriptor(description="Camera name"),
              ),
              (
                  "fps", 30,
                  ParameterDescriptor(
                      description="Camera frame rate in Hz",
                      integer_range=[
                          IntegerRange(from_value=1, to_value=60, step=1)
                      ],
                  ),
              ),
          ],
      )


.. dropdown:: Verifying Declared Parameters

   .. code-block:: console

      ros2 param list /camera_demo

   .. code-block:: text

      camera_name
      fps
      ...

   .. code-block:: console

      ros2 param get /camera_demo camera_name

   .. code-block:: text

      String value is: front_cam

   .. code-block:: console

      ros2 param get /camera_demo fps

   .. code-block:: text

      Integer value is: 30

   .. code-block:: console

      ros2 param describe /camera_demo fps

   .. code-block:: text

      Parameter name: fps
        Type: integer
        Description: Camera frame rate in Hz
        Constraints:
          Min value: 1
          Max value: 60
          Step: 1


Retrieving Parameters
----------------------------------------------------

After declaring a parameter, you might want to retrieve its value for
several reasons:

- **Initialization**: Parameters are often declared with default values,
  but you may need to retrieve the actual value to initialize parts of
  your node based on this configuration.
- **Dynamic reconfiguration**: Parameters can be changed at runtime.
  Retrieving the parameter allows your node to react to changes and
  adjust its behavior dynamically.
- **Operational tuning**: Parameters are frequently used for tuning
  algorithms or adjusting settings for sensors and actuators.


.. dropdown:: Retrieving Parameter Values

   .. code-block:: python

      # Get param camera_name and store it for later use
      self._camera_name = (
          self.get_parameter("camera_name")
          .get_parameter_value()
          .string_value
      )

      # Get param fps and store it for later use
      self._fps = (
          self.get_parameter("fps")
          .get_parameter_value()
          .integer_value
      )


Using Parameters
----------------------------------------------------

Implement parameters as functional class attributes to control node
behavior and provide meaningful context.


.. dropdown:: Using Parameters in Practice

   The ``camera_name`` parameter provides meaningful context in logs:

   .. code-block:: python

      self.get_logger().info(f"Image published from: {self._camera_name}")

   The ``fps`` parameter directly controls publishing frequency:

   .. code-block:: python

      self._image_timer = self.create_timer(
          1.0 / self._fps, self._image_pub_callback
      )

   .. admonition:: Think About It
      :class: hint

      Even with ``fps`` set to 30 Hz,
      ``ros2 topic hz /camera/image_color`` reveals a significantly
      lower actual rate. Why? How do we solve this?


.. dropdown:: Requested vs. Actual Performance

   ``ros2 topic bw /camera/image_color`` demonstrates the high
   bandwidth cost of image transmission.

   - Can we decrease the image size?
   - Can we log once in a while and not in each cycle?
   - Can we prevent the same computations from happening in the
     callback?

   .. note::

      This illustrates the important distinction between *requested*
      performance and *system-constrained* reality. Always measure the
      actual publishing frequency of your nodes to ensure they meet your
      application requirements.


Setting Parameters
----------------------------------------------------

Setting parameters involves *modifying the value of a declared parameter
either prior to or during the execution of the node*. This allows
dynamic node configuration without requiring code modifications or
recompilation.

There are several ways to set parameters:

1. Configure individual parameters using the CLI.
2. Define individual parameters within a launch file.
3. Use a parameter file (YAML file).
4. Set parameters programmatically.
5. Set parameters with ``ros2 param set``.
6. Use parameters as launch file arguments.


.. dropdown:: Configure Individual Parameters (CLI)
   :open:

   Use ``--ros-args`` to pass arguments to a node on the command line.
   Use ``-p <parameter>:=<value>`` to set a value for a parameter.

   .. code-block:: console

      ros2 run parameters_demo camera_demo

   .. code-block:: text

      [INFO][...][camera_demo]: Published random camera image from: front_cam

   .. code-block:: console

      ros2 run parameters_demo camera_demo --ros-args -p camera_name:='rear_cam'

   .. code-block:: text

      [INFO][...][camera_demo]: Published random camera image from: rear_cam

   .. admonition:: Think About It
      :class: hint

      Assign different values to the ``fps`` parameter: 1, 10, 50,
      and 70.


.. dropdown:: Individual Parameters in Launch Files

   Set parameter values in a launch file:

   .. code-block:: python

      camera_node = Node(
          package='parameters_demo',
          executable='camera_demo',
          parameters=[
              {'camera_name': 'rear_cam'},
              {'fps': 15}
          ],
          output='screen',
          emulate_tty=True
      )

   .. code-block:: console

      ros2 launch parameters_demo demo1.launch.py


.. dropdown:: Parameter Files (YAML)

   A **parameter file** in ROS 2 is a `YAML <https://yaml.org/>`_
   configuration file that stores parameters for one or more nodes.

   .. code-block:: yaml

      camera_demo:  # Name of the node
        ros__parameters:
          camera_name: 'front_cam'
          camera_frame_id: 'cam_link'
          fps: 30
          exposure_auto: true
          exposure_time_us: 10000
          brightness: 128
          image_width: 1920
          image_height: 1080
          encoding: 'bgr8'
          camera_info_url: ''

      lidar_demo:  # Name of the node
        ros__parameters:
          lidar_name: 'top_lidar'
          lidar_frame_id: 'lidar_link'
          min_range: 0.1
          max_range: 100.0
          min_angle: -3.14159
          max_angle: 3.14159
          intensity_threshold: 0.0
          scan_frequency: 10
          port: '/dev/lidar0'
          return_mode: 'strongest'

   - YAML files are usually placed in the ``config/`` directory (best
     practice).
   - Ensure you edit ``setup.py`` to install the ``config/`` folder.

   **Parameter file with CLI:**

   Use ``--ros-args`` and ``--params-file <path>`` to pass the
   parameter file to the node (relative or absolute path):

   .. code-block:: console

      ros2 run parameters_demo camera_demo --ros-args --params-file <file path>

   **Parameter file with launch files:**

   .. code-block:: python

      parameters_demo_file = PathJoinSubstitution(
          [FindPackageShare("parameters_demo"), "config", "parameters_demo.yaml"]
      )

      camera_node = Node(
          package="parameters_demo",
          executable="camera_demo",
          parameters=[parameters_demo_file],
          output="screen",
          emulate_tty=True,
      )

   .. code-block:: console

      ros2 launch parameters_demo demo2.launch.py


.. dropdown:: Set Parameters Programmatically

   Parameters can be defined and modified directly within your program.
   This enables dynamic adjustments in which different values are
   assigned to the same parameter based on specific logic.

   .. code-block:: python

      from rclpy.parameter import Parameter

      self.set_parameters([Parameter("fps", Parameter.Type.INTEGER, 15)])

   .. tip::

      This is useful when the node needs to adjust its own behavior
      based on runtime conditions -- e.g., reducing the frame rate
      when CPU usage is high.

   **Demonstration**

   .. code-block:: console

      # Start all nodes
      ros2 launch parameters_demo demo2.launch.py

      # Display parameters for camera_demo
      ros2 param list camera_demo

      # Get the parameter value
      ros2 param get camera_demo camera_name

   .. code-block:: text

      String value is: rear_cam

   .. code-block:: console

      # Change the value
      ros2 param set camera_demo camera_name 'front_cam'

   .. code-block:: text

      Set parameter successful

   .. code-block:: console

      # Get the parameter value
      ros2 param get camera_demo camera_name

   .. code-block:: text

      String value is: rear_cam


.. dropdown:: Why Did the Value Not Change?

   .. warning::

      The value of ``camera_name`` has been updated, but the attribute
      in the code still reflects the previous value. After a parameter
      is read during initialization, the node does not observe
      subsequent updates unless it is explicitly notified.

   .. note::

      Add an on-set-parameters callback so the node is notified
      immediately when the parameter is modified. The method
      ``add_on_set_parameters_callback()`` registers a callback function
      that will be automatically invoked whenever someone attempts to
      change the node's parameters through the ROS 2 parameter API
      (like using ``ros2 param set`` or calling the parameter service
      directly).


.. dropdown:: Parameter Change Callback

   Register a callback function for parameter changes:

   .. code-block:: python

      self.add_on_set_parameters_callback(self._parameter_update_cb)

   Define the callback:

   .. code-block:: python

      def _parameter_update_cb(self, params):
          success = False
          for param in params:
              if param.name == "camera_name":
                  if param.type_ == Parameter.Type.STRING:  # validation
                      success = True
                      self._camera_name = param.value  # modify the attribute
              elif param.name == "fps":
                  if param.type_ == Parameter.Type.INTEGER:
                      self._fps = param.value
                      success = True
          return SetParametersResult(successful=success)

   **Demonstration**

   .. code-block:: console

      ros2 launch parameters_demo demo2.launch.py
      ros2 param set camera_demo camera_name 'front_cam'


.. dropdown:: Updating Timer Frequency

   A timer is initialized when the node is created and executes its
   associated callback once the node begins running. To modify the
   timer's frequency, it must be **canceled and then recreated** using
   the updated frequency.

   .. code-block:: python

      # 1. Cancel the timer
      self._image_timer.cancel()

      # 2. Recreate the timer
      self._image_timer = self.create_timer(
          1 / self._fps, self._image_pub_callback
      )

   .. code-block:: console

      ros2 run parameters_demo camera_demo
      ros2 topic hz /camera/image_color
      ros2 param set camera_demo fps 10


.. dropdown:: Use Parameters as Launch File Arguments

   Parameters are typically hardcoded in a YAML file, but they can also
   be exposed as launch file arguments. This allows the caller to
   override specific parameter values at launch time without modifying
   the YAML file or the node source code.

   Declare the parameter that will be overridable:

   .. code-block:: python

      # lidar_demo.py
      self.declare_parameter("lidar_model", "default_lidar")

   Declare a launch argument and forward it to the node via
   ``parameters``:

   .. code-block:: python

      # demo3.launch.py
      from launch.actions import DeclareLaunchArgument
      from launch.substitutions import LaunchConfiguration

      lidar_model = LaunchConfiguration("lidar_model")
      lidar_model_arg = DeclareLaunchArgument(
          "lidar_model", default_value="velodyne"
      )
      lidar_node = Node(
          package="parameters_demo",
          executable="lidar_demo",
          parameters=[parameters_demo_file, {"lidar_model": lidar_model}],
          output="screen",
          emulate_tty=True,
      )
      ld.add_action(lidar_model_arg)
      ld.add_action(lidar_node)

   .. code-block:: console

      ros2 launch parameters_demo demo3.launch.py lidar_model:=ouster


Custom Interfaces
====================================================

Custom interface definitions allow you to create domain-specific
message, service, and action types.


.. dropdown:: Why Custom Interfaces?

   While ROS 2 provides common message types (``std_msgs``,
   ``geometry_msgs``, ``sensor_msgs``), real robotic applications often
   require domain-specific data structures.

   - A warehouse robot needs an ``OrderStatus`` message with fields
     unique to its workflow.
   - A manipulation pipeline needs a ``GraspPose`` service combining
     geometry and gripper configuration.
   - A navigation system needs a ``Navigate`` action with waypoints,
     progress feedback, and completion results.

   Custom interfaces are defined in ``.msg``, ``.srv``, or ``.action``
   files and compiled into Python (and C++) classes by the ROS 2 build
   system.

   .. note::

      Interface packages are always **CMake** packages (``ament_cmake``),
      even if all your nodes are in Python. This is because the code
      generators (``rosidl``) require CMake infrastructure.


.. dropdown:: Interface Package Structure

   A dedicated interface package keeps generated types separate from
   node implementations.

   .. code-block:: text

      custom_interfaces/
      ├── CMakeLists.txt
      ├── package.xml
      ├── msg/
      │   └── SensorReading.msg
      ├── srv/
      │   └── ComputeTrajectory.srv
      └── action/
          └── Navigate.action

   **package.xml dependencies** (required for all interface packages):

   .. code-block:: xml

      <buildtool_depend>ament_cmake</buildtool_depend>
      <buildtool_depend>rosidl_default_generators</buildtool_depend>
      <exec_depend>rosidl_default_runtime</exec_depend>
      <member_of_group>rosidl_interface_packages</member_of_group>


.. dropdown:: Defining a Custom Message (.msg)

   A ``.msg`` file defines the fields of a topic message. Each line
   contains a type and a field name.

   .. code-block:: text

      # msg/SensorReading.msg
      std_msgs/Header header
      string sensor_id
      float64 temperature
      float64 humidity
      bool is_valid

   **Supported field types:**

   - Primitives: ``bool``, ``int8``, ``int16``, ``int32``, ``int64``,
     ``uint8``, ``uint16``, ``uint32``, ``uint64``, ``float32``,
     ``float64``, ``string``
   - Arrays: ``float64[]`` (unbounded), ``float64[3]`` (fixed-size),
     ``float64[<=10]`` (bounded)
   - Other message types: ``std_msgs/Header``, ``geometry_msgs/Pose``
   - Constants: ``int32 MAX_SENSORS=10``

   **CMakeLists.txt** -- register the message for code generation:

   .. code-block:: cmake

      find_package(rosidl_default_generators REQUIRED)
      find_package(std_msgs REQUIRED)

      rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/SensorReading.msg"
        DEPENDENCIES std_msgs
      )

   **Using in Python:**

   .. code-block:: python

      from custom_interfaces.msg import SensorReading

      msg = SensorReading()
      msg.sensor_id = "lidar_front"
      msg.temperature = 25.3
      msg.is_valid = True


.. dropdown:: Defining a Custom Service (.srv)

   A ``.srv`` file defines a request and response separated by ``---``.

   .. code-block:: text

      # srv/ComputeTrajectory.srv
      # Request
      geometry_msgs/Pose start_pose
      geometry_msgs/Pose goal_pose
      float64 max_velocity
      ---
      # Response
      bool success
      string message
      geometry_msgs/Pose[] waypoints

   **CMakeLists.txt** -- add the service to the same
   ``rosidl_generate_interfaces`` call:

   .. code-block:: cmake

      rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/SensorReading.msg"
        "srv/ComputeTrajectory.srv"
        DEPENDENCIES std_msgs geometry_msgs
      )

   **Using in Python:**

   .. code-block:: python

      from custom_interfaces.srv import ComputeTrajectory

      # In a service server callback
      def compute_callback(self, request, response):
          response.success = True
          response.message = "Trajectory computed"
          response.waypoints = [...]
          return response


.. dropdown:: Defining a Custom Action (.action)

   An ``.action`` file has three sections separated by ``---``: goal,
   result, and feedback.

   .. code-block:: text

      # action/Navigate.action
      # Goal
      geometry_msgs/Pose target_pose
      float64 max_speed
      ---
      # Result
      bool success
      float64 total_distance
      float64 elapsed_time
      ---
      # Feedback
      geometry_msgs/Pose current_pose
      float64 distance_remaining
      float64 percent_complete

   **CMakeLists.txt:**

   .. code-block:: cmake

      find_package(action_msgs REQUIRED)

      rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/SensorReading.msg"
        "srv/ComputeTrajectory.srv"
        "action/Navigate.action"
        DEPENDENCIES std_msgs geometry_msgs action_msgs
      )

   **Using in Python:**

   .. code-block:: python

      from custom_interfaces.action import Navigate

      goal = Navigate.Goal()
      goal.target_pose.position.x = 5.0
      goal.max_speed = 1.0

   .. note::

      After modifying any interface file, you must rebuild the
      ``custom_interfaces`` package and re-source the workspace before
      dependent packages can see the changes.


.. dropdown:: Building and Verifying

   **Build the interface package:**

   .. code-block:: console

      colcon build --symlink-install --packages-select custom_interfaces
      source install/setup.bash

   **Verify the interfaces were generated:**

   .. code-block:: console

      # List all interfaces in the package
      ros2 interface list | grep custom_interfaces

      # Show message definition
      ros2 interface show custom_interfaces/msg/SensorReading

      # Show service definition
      ros2 interface show custom_interfaces/srv/ComputeTrajectory

      # Show action definition
      ros2 interface show custom_interfaces/action/Navigate


Services
====================================================

Services implement synchronous request/response communication between
nodes.


.. dropdown:: Service Communication Model

   A **service** is a pair: a server that provides a capability and a
   client that requests it. Unlike topics (continuous data streams),
   services are used for discrete, one-shot operations that return a
   result.

   - The **server** advertises the service and waits for requests. When
     a request arrives, it executes a callback and returns a response.
   - The **client** sends a request and waits for the response. The
     wait can be synchronous (blocking) or asynchronous (non-blocking).
   - A service is defined by its **type** (the ``.srv`` definition) and
     its **name** (a string like ``/compute_trajectory``).

   **When to use services vs. topics:**

   .. list-table::
      :widths: 20 40 40
      :header-rows: 1
      :class: compact-table

      * -
        - Topic
        - Service
      * - Pattern
        - Publisher/subscriber (1:N)
        - Client/server (1:1 per call)
      * - Timing
        - Continuous, periodic
        - On-demand, one-shot
      * - Examples
        - Sensor data, odometry, ``cmd_vel``
        - Spawn model, compute IK, trigger action
      * - Blocking?
        - No
        - Client blocks until response

   **Resources**

   - `ROS 2 Documentation: Understanding Services
     <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html>`_


.. dropdown:: Writing a Service Server

   A service server registers a callback that runs when a client sends
   a request.

   .. code-block:: python

      import rclpy
      from rclpy.node import Node
      from custom_interfaces.srv import ComputeTrajectory


      class TrajectoryServer(Node):
          def __init__(self):
              super().__init__("trajectory_server")
              self._srv = self.create_service(
                  ComputeTrajectory,
                  "compute_trajectory",
                  self._compute_callback,
              )
              self.get_logger().info("Trajectory service ready.")

          def _compute_callback(self, request, response):
              self.get_logger().info(
                  f"Computing trajectory from {request.start_pose} "
                  f"to {request.goal_pose} at max {request.max_velocity} m/s"
              )
              # Perform computation
              response.success = True
              response.message = "Trajectory computed successfully"
              return response


      def main(args=None):
          rclpy.init(args=args)
          node = TrajectoryServer()
          rclpy.spin(node)
          rclpy.shutdown()

   - ``create_service(srv_type, name, callback)`` registers the service.
   - The callback receives two arguments: the request and a
     pre-constructed response object. Populate the response fields and
     return it.
   - The server remains active as long as the node is spinning.


.. dropdown:: Writing a Service Client (Asynchronous)

   The **asynchronous** client sends a request and continues processing
   other callbacks while waiting for the response. This is the
   recommended pattern.

   .. code-block:: python

      import rclpy
      from rclpy.node import Node
      from custom_interfaces.srv import ComputeTrajectory
      from geometry_msgs.msg import Pose


      class TrajectoryClient(Node):
          def __init__(self):
              super().__init__("trajectory_client")
              self._client = self.create_client(
                  ComputeTrajectory, "compute_trajectory"
              )
              # Wait for the service to become available
              while not self._client.wait_for_service(timeout_sec=1.0):
                  self.get_logger().info("Waiting for service...")

              self._send_request()

          def _send_request(self):
              request = ComputeTrajectory.Request()
              request.start_pose = Pose()
              request.goal_pose = Pose()
              request.goal_pose.position.x = 5.0
              request.max_velocity = 1.0

              future = self._client.call_async(request)
              future.add_done_callback(self._response_callback)

          def _response_callback(self, future):
              response = future.result()
              if response.success:
                  self.get_logger().info(f"Success: {response.message}")
              else:
                  self.get_logger().error(f"Failed: {response.message}")


      def main(args=None):
          rclpy.init(args=args)
          node = TrajectoryClient()
          rclpy.spin(node)
          rclpy.shutdown()

   - ``call_async(request)`` returns a ``Future`` object immediately.
   - ``add_done_callback()`` registers a function to be called when the
     response arrives.
   - The node continues spinning and processing other callbacks while
     waiting.

   .. tip::

      Always use ``wait_for_service()`` before sending the first
      request. Without it, the call will fail if the server has not
      started yet.


.. dropdown:: Writing a Service Client (Synchronous)

   The **synchronous** client blocks the calling thread until the
   response arrives. This is simpler but can cause problems.

   .. code-block:: python

      class SyncTrajectoryClient(Node):
          def __init__(self):
              super().__init__("sync_trajectory_client")
              self._client = self.create_client(
                  ComputeTrajectory, "compute_trajectory"
              )
              while not self._client.wait_for_service(timeout_sec=1.0):
                  self.get_logger().info("Waiting for service...")

              self._send_request()

          def _send_request(self):
              request = ComputeTrajectory.Request()
              request.goal_pose.position.x = 5.0
              request.max_velocity = 1.0

              # Blocking call -- use only from a dedicated thread
              response = self._client.call(request)
              self.get_logger().info(f"Result: {response.message}")

   .. warning::

      **Never call** ``self._client.call()`` **from the main executor
      thread.** The synchronous call blocks the thread, which prevents
      the executor from processing the response callback, creating a
      **deadlock**. Use ``call()`` only from a separate thread or a
      ``ReentrantCallbackGroup``. Prefer ``call_async()`` in most cases.


.. dropdown:: Service CLI Tools

   .. code-block:: console

      # List all active services
      ros2 service list

      # Show the type of a service
      ros2 service type /compute_trajectory

      # Find services by type
      ros2 service find custom_interfaces/srv/ComputeTrajectory

      # Call a service from the command line
      ros2 service call /compute_trajectory custom_interfaces/srv/ComputeTrajectory \
          "{start_pose: {position: {x: 0.0}}, goal_pose: {position: {x: 5.0}}, max_velocity: 1.0}"


Actions
====================================================

Actions extend services with feedback and cancellation for
long-running tasks.


.. dropdown:: Action Communication Model

   An **action** is a three-part communication pattern designed for
   tasks that take a noticeable amount of time: navigation, arm motion,
   image processing pipelines, etc.

   1. **Goal** -- the client sends a goal to the server (e.g., "navigate
      to (5, 3)").
   2. **Feedback** -- the server periodically publishes progress updates
      while executing (e.g., "distance remaining: 2.3 m").
   3. **Result** -- when the task completes (or is canceled), the server
      returns a final result (e.g., "total distance: 7.1 m, elapsed
      time: 14.2 s").

   Actions are built on top of services and topics internally:

   - A service for sending goals and receiving acceptance/rejection
   - A service for querying the result
   - A service for canceling goals
   - A topic for publishing feedback

   **When to use actions vs. services:**

   .. list-table::
      :widths: 20 40 40
      :header-rows: 1
      :class: compact-table

      * -
        - Service
        - Action
      * - Duration
        - Short (< 1 s)
        - Long (seconds to minutes)
      * - Feedback
        - None
        - Periodic progress updates
      * - Cancellation
        - Not possible
        - Built-in cancel request
      * - Examples
        - Spawn model, get map
        - Navigate to goal, pick & place

   **Resources**

   - `ROS 2 Documentation: Understanding Actions
     <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html>`_
   - `ROS 2 Documentation: Writing an Action Server and Client (Python)
     <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html>`_


.. dropdown:: Writing an Action Server

   An action server handles incoming goals, publishes feedback during
   execution, and returns a result.

   .. code-block:: python

      import time
      import rclpy
      from rclpy.action import ActionServer
      from rclpy.node import Node
      from custom_interfaces.action import Navigate


      class NavigateServer(Node):
          def __init__(self):
              super().__init__("navigate_server")
              self._action_server = ActionServer(
                  self,
                  Navigate,
                  "navigate",
                  self._execute_callback,
              )
              self.get_logger().info("Navigate action server ready.")

          def _execute_callback(self, goal_handle):
              self.get_logger().info(
                  f"Navigating to ({goal_handle.request.target_pose.position.x}, "
                  f"{goal_handle.request.target_pose.position.y})"
              )

              feedback = Navigate.Feedback()
              total_distance = 10.0  # Simulated distance

              for i in range(10):
                  # Check for cancellation
                  if goal_handle.is_cancel_requested:
                      goal_handle.canceled()
                      self.get_logger().info("Navigation canceled.")
                      result = Navigate.Result()
                      result.success = False
                      return result

                  # Simulate progress
                  feedback.distance_remaining = total_distance - (i + 1)
                  feedback.percent_complete = float((i + 1) * 10)
                  goal_handle.publish_feedback(feedback)
                  self.get_logger().info(
                      f"Progress: {feedback.percent_complete:.0f}%"
                  )
                  time.sleep(1.0)

              # Mark goal as succeeded
              goal_handle.succeed()
              result = Navigate.Result()
              result.success = True
              result.total_distance = total_distance
              result.elapsed_time = 10.0
              return result


      def main(args=None):
          rclpy.init(args=args)
          node = NavigateServer()
          rclpy.spin(node)
          rclpy.shutdown()

   - ``ActionServer(node, action_type, name, execute_callback)`` creates
     the server. The execute callback runs when a goal is accepted.
   - ``goal_handle.publish_feedback(feedback)`` sends progress to the
     client.
   - ``goal_handle.succeed()`` or ``goal_handle.canceled()`` sets the
     terminal state before returning the result.


.. dropdown:: Goal Handling and Cancellation

   By default, every incoming goal is automatically accepted. Override
   ``goal_callback`` and ``cancel_callback`` for finer control.

   .. code-block:: python

      from rclpy.action import CancelResponse, GoalResponse

      class NavigateServerAdvanced(Node):
          def __init__(self):
              super().__init__("navigate_server_adv")
              self._action_server = ActionServer(
                  self,
                  Navigate,
                  "navigate",
                  execute_callback=self._execute_callback,
                  goal_callback=self._goal_callback,
                  cancel_callback=self._cancel_callback,
              )

          def _goal_callback(self, goal_request):
              """Accept or reject a goal before execution begins."""
              if goal_request.max_speed <= 0.0:
                  self.get_logger().warn("Rejected: speed must be positive.")
                  return GoalResponse.REJECT
              self.get_logger().info("Goal accepted.")
              return GoalResponse.ACCEPT

          def _cancel_callback(self, goal_handle):
              """Accept or reject a cancellation request."""
              self.get_logger().info("Cancel request received -- accepting.")
              return CancelResponse.ACCEPT

   - ``GoalResponse.ACCEPT`` and ``GoalResponse.REJECT`` control
     whether the goal enters execution.
   - ``CancelResponse.ACCEPT`` signals the execute callback to check
     ``goal_handle.is_cancel_requested`` and clean up.


.. dropdown:: Writing an Action Client

   An action client sends a goal, receives feedback updates, and
   retrieves the final result.

   .. code-block:: python

      import rclpy
      from rclpy.action import ActionClient
      from rclpy.node import Node
      from custom_interfaces.action import Navigate
      from geometry_msgs.msg import Pose


      class NavigateClient(Node):
          def __init__(self):
              super().__init__("navigate_client")
              self._client = ActionClient(self, Navigate, "navigate")

          def send_goal(self, x, y):
              self.get_logger().info("Waiting for action server...")
              self._client.wait_for_server()

              goal = Navigate.Goal()
              goal.target_pose.position.x = x
              goal.target_pose.position.y = y
              goal.max_speed = 1.0

              self.get_logger().info(f"Sending goal: ({x}, {y})")
              send_goal_future = self._client.send_goal_async(
                  goal, feedback_callback=self._feedback_callback
              )
              send_goal_future.add_done_callback(self._goal_response_callback)

          def _goal_response_callback(self, future):
              goal_handle = future.result()
              if not goal_handle.accepted:
                  self.get_logger().error("Goal rejected.")
                  return
              self.get_logger().info("Goal accepted.")
              result_future = goal_handle.get_result_async()
              result_future.add_done_callback(self._result_callback)

          def _feedback_callback(self, feedback_msg):
              feedback = feedback_msg.feedback
              self.get_logger().info(
                  f"Feedback: {feedback.percent_complete:.0f}% complete, "
                  f"{feedback.distance_remaining:.1f} m remaining"
              )

          def _result_callback(self, future):
              result = future.result().result
              if result.success:
                  self.get_logger().info(
                      f"Navigation complete! Distance: {result.total_distance:.1f} m, "
                      f"Time: {result.elapsed_time:.1f} s"
                  )
              else:
                  self.get_logger().warn("Navigation failed or was canceled.")


      def main(args=None):
          rclpy.init(args=args)
          node = NavigateClient()
          node.send_goal(5.0, 3.0)
          rclpy.spin(node)
          rclpy.shutdown()

   - ``send_goal_async(goal, feedback_callback=...)`` is the
     asynchronous pattern. It returns a ``Future`` that resolves to a
     ``GoalHandle``.
   - From the ``GoalHandle``, call ``get_result_async()`` to get another
     ``Future`` for the final result.
   - The ``feedback_callback`` is invoked every time the server publishes
     a feedback message.


.. dropdown:: Canceling an Action

   A client can request cancellation of an active goal.

   .. code-block:: python

      # Store the goal handle from _goal_response_callback
      self._goal_handle = goal_handle

      # Later, cancel the goal
      cancel_future = self._goal_handle.cancel_goal_async()
      cancel_future.add_done_callback(self._cancel_callback)

      def _cancel_callback(self, future):
          cancel_response = future.result()
          if len(cancel_response.goals_canceling) > 0:
              self.get_logger().info("Goal successfully canceled.")
          else:
              self.get_logger().warn("Cancel request was rejected.")

   - Cancellation is **cooperative**: the server must check
     ``goal_handle.is_cancel_requested`` in its execute loop and
     call ``goal_handle.canceled()`` to acknowledge.
   - The cancel callback on the server (``_cancel_callback``) decides
     whether to honor the request.


.. dropdown:: Action CLI Tools

   .. code-block:: console

      # List all active actions
      ros2 action list

      # Show the type of an action
      ros2 action type /navigate

      # Show action info (servers, clients)
      ros2 action info /navigate

      # Send a goal from the command line
      ros2 action send_goal /navigate custom_interfaces/action/Navigate \
          "{target_pose: {position: {x: 5.0, y: 3.0}}, max_speed: 1.0}"

      # Send a goal with feedback display
      ros2 action send_goal /navigate custom_interfaces/action/Navigate \
          "{target_pose: {position: {x: 5.0, y: 3.0}}, max_speed: 1.0}" --feedback


Choosing the Right Communication Pattern
====================================================

A summary to help decide when to use each ROS 2 communication
mechanism.


.. dropdown:: Decision Guide

   .. list-table::
      :widths: 15 20 20 20 25
      :header-rows: 1
      :class: compact-table

      * - Mechanism
        - Pattern
        - Duration
        - Feedback
        - Example
      * - **Topic**
        - Pub/Sub (1:N)
        - Continuous
        - N/A
        - Sensor data, ``cmd_vel``
      * - **Service**
        - Req/Resp (1:1)
        - Short
        - None
        - Spawn entity, compute IK
      * - **Action**
        - Goal/Feedback/Result
        - Long
        - Periodic
        - Navigate, pick-and-place
      * - **Parameter**
        - Get/Set on node
        - Instant
        - Callback
        - Tuning gains, thresholds

   **Rules of thumb:**

   1. If data flows continuously and multiple consumers may need it,
      use a **topic**.
   2. If you need a one-shot request with an immediate response, use a
      **service**.
   3. If the task takes noticeable time and you need progress or
      cancellation, use an **action**.
   4. If you are configuring node behavior without changing its code,
      use a **parameter**.
