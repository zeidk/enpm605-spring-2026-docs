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

   Pull the latest code, install dependencies, and build all Lecture 10
   demo packages.

   .. code-block:: console

      cd ~/enpm605_ws && git pull

   Install dependencies:

   .. code-block:: console

      rosdep install --from-paths src --ignore-packages-from-source -y

   - Scans every ``package.xml`` under ``src/`` and installs any missing
     system dependencies (e.g., ``rclpy``, ``std_msgs``).
   - ``--ignore-packages-from-source`` skips dependencies that are
     already in the workspace (e.g., ``custom_interfaces``).
   - ``-y`` auto-confirms installation prompts.

   Build the Lecture 10 packages:

   .. code-block:: console

      colcon build --symlink-install --packages-up-to lecture10_demo

   - ``lecture10_demo`` is a **metapackage** that declares dependencies
     on ``parameters_demo``, ``custom_interfaces``, ``service_demo``,
     ``message_demo``, and ``action_demo``.
   - ``--packages-up-to`` builds the named package *and all its
     dependencies* in the correct order.

   Source the workspace:

   .. code-block:: console

      source install/setup.bash


Parameters
====================================================

A **parameter** is a configurable value that can be used to customize
the behavior of a node at runtime without modifying the code. Parameters
allow nodes to store and retrieve data, such as tuning constants, file
paths, or robot-specific settings.

.. admonition:: Resources
   :class: resources

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


.. dropdown:: Parameters in Autonomous Vehicles

   .. only:: html

      .. figure:: /_static/images/L10/param_av_light.png
         :alt: Parameters in autonomous vehicles
         :width: 70%
         :align: center
         :class: only-light

         Parameters are used extensively in autonomous vehicle stacks to
         configure sensors, controllers, and planners at runtime.

      .. figure:: /_static/images/L10/param_av_dark.png
         :alt: Parameters in autonomous vehicles
         :width: 70%
         :align: center
         :class: only-dark

         Parameters are used extensively in autonomous vehicle stacks to
         configure sensors, controllers, and planners at runtime.


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

   .. admonition:: Demonstration
      :class: demonstration

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

   .. note::

      The parameters ``camera_name`` and ``fps`` are both marked as
      freely writable in the sensor parameters table, meaning their
      values can be updated at runtime without restarting the node.


.. dropdown:: Approach #2: Declaration with Constraints and Metadata

   .. code-block:: python

      from rcl_interfaces.msg import ParameterDescriptor, IntegerRange

      self.declare_parameter(
          "camera_name", "front_cam",
          ParameterDescriptor(description="Name of the camera")
      )
      self.declare_parameter(
          "fps", 30,
          ParameterDescriptor(
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

      ros2 run parameters_demo camera_demo

   .. code-block:: console

      ros2 param list /camera_demo

   .. code-block:: text

      brightness
      camera_frame_id
      camera_info_url
      camera_name
      encoding
      exposure_auto
      exposure_time_us
      fps
      image_height
      image_width
      use_sim_time

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

After declaring a parameter, you might want to retrieve its value with
``get_value()`` for several reasons:

- **Initialization**: Parameters are often declared with default values,
  but you may need to retrieve the actual value to initialize parts of
  your node or its functionalities based on this configuration.
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

Once parameters are stored in class attributes, use them to control node
behavior and to provide meaningful context.


.. dropdown:: Using Parameters in Practice

   **Example: Provide Meaningful Context in Logs**

   .. code-block:: python

      self.get_logger().info(f"Image published from: {self._camera_name}")

   **Example: Control Publishing Frequency**

   .. code-block:: python

      self._image_timer = self.create_timer(
          1.0 / self._fps, self._image_pub_callback
      )

   .. admonition:: Demonstration
      :class: demonstration

      .. code-block:: console

         ros2 run parameters_demo camera_demo

   .. admonition:: Think About It
      :class: hint

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

Parameters can be set before or during node execution, allowing dynamic
configuration without modifying or recompiling the source code.

There are several ways to set parameters:

1. Pass individual values on the command line (``-p``).
2. Hardcode values in a launch file.
3. Load a YAML parameter file.
4. Dynamic updates with ``set_parameters()`` or ``ros2 param set``.
5. Expose values as overridable launch file arguments.


.. dropdown:: 1. Pass Individual Values (CLI)
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


.. dropdown:: 2. Hardcode Values in Launch Files

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


.. dropdown:: 3. Load a YAML Parameter File

   A **parameter file** in ROS 2 is a `YAML <https://yaml.org/>`_
   configuration file that stores parameters for one or more nodes.

   .. code-block:: yaml

      camera_demo:  # Name of the node
        ros__parameters:
          camera_name: 'rear_cam'
          fps: 15
          ...

      lidar_demo:  # Name of the node
        ros__parameters:
          lidar_name: 'top_lidar'
          scan_frequency: 20
          ...

   - YAML files are usually placed in the ``config/`` directory (best
     practice).
   - Ensure you edit ``setup.py`` to install the ``config/`` folder.

   **Parameter file with CLI:**

   Use ``--ros-args`` and ``--params-file <path>`` to pass the
   parameter file to the node (relative or absolute path):

   .. code-block:: console

      ros2 run parameters_demo camera_demo --ros-args --params-file <file path>

   **Parameter file with launch files:**

   Store the path of the parameter file:

   .. code-block:: python

      parameters_demo_file = PathJoinSubstitution(
          [FindPackageShare("parameters_demo"), "config", "parameters_demo.yaml"]
      )

   Pass the parameter file to the node:

   .. code-block:: python

      camera_node = Node(
          package="parameters_demo",
          executable="camera_demo",
          parameters=[parameters_demo_file],
          output="screen",
          emulate_tty=True,
      )

   .. code-block:: console

      ros2 launch parameters_demo demo2.launch.py


.. dropdown:: 4. Modifying Parameters at Runtime

   Parameters can be modified at runtime to enable dynamic adjustments.

   **Programmatically:**

   .. code-block:: python

      from rclpy.parameter import Parameter

      self.set_parameters([Parameter("fps", Parameter.Type.INTEGER, 15)])

   .. tip::

      This is useful when the node needs to adjust its own behavior
      based on runtime conditions -- e.g., reducing the frame rate
      when CPU usage is high.

   **CLI: ros2 param set**

   .. note::

      Sends a parameter update request to a running node without
      restarting it or modifying the source code.


.. dropdown:: Why Did the Value Not Change?

   .. warning::

      After a parameter is read during initialization, the node does not
      observe subsequent updates unless it is explicitly notified.

   .. note::

      Add an on-set-parameters callback so the node is notified
      immediately when the parameter is modified. The method
      ``add_on_set_parameters_callback()`` registers a callback function
      that will be automatically invoked whenever someone attempts to
      change the node's parameters through the ROS 2 parameter API.


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

   .. admonition:: Demonstration
      :class: demonstration

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


.. dropdown:: 5. Use Parameters as Launch File Arguments

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

Custom interface definitions allow you to create **domain-specific**
message, service, and action types beyond what ``std_msgs``,
``geometry_msgs``, and ``sensor_msgs`` provide.

.. admonition:: Resources
   :class: resources

   - `Creating Custom msg and srv Files
     <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html>`_
   - `About ROS 2 Interfaces
     <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html>`_


.. dropdown:: Verify the Interfaces

   .. code-block:: console

      # List all interfaces in the package
      ros2 interface list | grep custom_interfaces

      # Show message definition
      ros2 interface show custom_interfaces/msg/TaskStatus

      # Show service definition
      ros2 interface show custom_interfaces/srv/ComputeTrajectory

      # Show action definition
      ros2 interface show custom_interfaces/action/Navigate


.. dropdown:: Why Custom Interfaces?

   - A warehouse robot needs a ``TaskStatus`` message with fields unique
     to its workflow.
   - A navigation pipeline needs a ``ComputeTrajectory`` service to
     compute a trajectory between two points.
   - A navigation system needs a ``Navigate`` action with waypoints,
     progress feedback, and completion results.

   .. warning::

      Interface packages are always **CMake** packages (``ament_cmake``),
      even if all your nodes are in Python. The code generators
      (``rosidl``) require CMake infrastructure.


.. dropdown:: Interface Package Structure

   A dedicated interface package keeps generated types separate from
   node implementations.

   .. code-block:: text

      custom_interfaces/
      +-- CMakeLists.txt
      +-- package.xml
      +-- msg/
      |   +-- TaskStatus.msg
      +-- srv/
      |   +-- ComputeTrajectory.srv
      +-- action/
          +-- Navigate.action

   **package.xml dependencies** (required for all interface packages):

   .. code-block:: xml

      <buildtool_depend>ament_cmake</buildtool_depend>
      <buildtool_depend>rosidl_default_generators</buildtool_depend>
      <exec_depend>rosidl_default_runtime</exec_depend>
      <member_of_group>rosidl_interface_packages</member_of_group>


Defining a Custom Message (.msg)
----------------------------------------------------

A ``.msg`` file defines the fields of a topic message. Each line
contains a type and a field name.


.. dropdown:: TaskStatus.msg

   .. code-block:: text

      # Status constants
      uint8 PENDING=0
      uint8 IN_PROGRESS=1
      uint8 COMPLETED=2
      uint8 FAILED=3

      # Fields
      std_msgs/Header header
      string task_id
      string task_description
      uint8 status
      float64 completion_percentage
      string message

   **Why Use Constants?**

   - Without constants, code uses **magic numbers** like
     ``msg.status = 2`` (unclear and error-prone).
   - Constants provide **self-documenting** names:
     ``msg.status = TaskStatus.COMPLETED``
   - They are compiled into **class-level attributes** in the target
     language, ensuring a **single source of truth** shared across all
     nodes.
   - Any node importing ``TaskStatus`` gets the same constant values
     (no need to redefine them).


.. dropdown:: CMakeLists.txt for Custom Message

   .. code-block:: cmake

      find_package(rosidl_default_generators REQUIRED)
      find_package(std_msgs REQUIRED)

      rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/TaskStatus.msg"
        DEPENDENCIES std_msgs
      )

   - ``rosidl_generate_interfaces`` generates Python and C++ code from
     the ``.msg`` definition.
   - The generated code is placed in the ``install/`` folder of the
     workspace (e.g., ``install/custom_interfaces/lib/python3/
     dist-packages/custom_interfaces/msg/``).
   - After building, **source the workspace** so Python can find the
     generated module.


.. dropdown:: Using TaskStatus in a Node

   .. code-block:: python

      msg = TaskStatus()
      msg.header.stamp = self.get_clock().now().to_msg()
      msg.task_id = "task_001"
      msg.task_description = "Pick and place operation"
      msg.status = TaskStatus.COMPLETED  # Use constant, not magic number
      msg.completion_percentage = 100.0
      msg.message = "Task completed successfully"

   .. admonition:: Demonstration
      :class: demonstration

      .. code-block:: console

         ros2 run message_demo task_status_demo
         ros2 topic echo /task_status


Defining a Custom Service (.srv)
----------------------------------------------------

A ``.srv`` file defines a **request** and **response** separated by
``---``.


.. dropdown:: ComputeTrajectory.srv

   .. code-block:: text

      # Request
      geometry_msgs/Pose start_pose
      geometry_msgs/Pose goal_pose
      float64 max_velocity
      ---
      # Response
      bool success
      string message
      geometry_msgs/Pose[] waypoints

   **CMakeLists.txt:**

   .. code-block:: cmake

      rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/TaskStatus.msg"
        "srv/ComputeTrajectory.srv"
        DEPENDENCIES std_msgs geometry_msgs
      )


.. dropdown:: Using ComputeTrajectory in a Node

   .. code-block:: python

      from custom_interfaces.srv import ComputeTrajectory

      # In a service server callback
      def compute_callback(self, request, response):
          response.success = True
          response.message = "Trajectory computed"
          response.waypoints = [...]
          return response


Defining a Custom Action (.action)
----------------------------------------------------

An ``.action`` file has **three sections** separated by ``---``: goal,
result, and feedback.


.. dropdown:: Navigate.action

   .. code-block:: text

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


.. dropdown:: CMakeLists.txt for All Interfaces

   .. code-block:: cmake

      find_package(action_msgs REQUIRED)

      rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/TaskStatus.msg"
        "srv/ComputeTrajectory.srv"
        "action/Navigate.action"
        DEPENDENCIES std_msgs geometry_msgs action_msgs
      )

   **Using in a Node:**

   .. code-block:: python

      from custom_interfaces.action import Navigate

      goal = Navigate.Goal()
      goal.target_pose.position.x = 5.0
      goal.max_speed = 1.0

   .. note::

      After modifying any interface file, you must rebuild the
      ``custom_interfaces`` package and re-source the workspace before
      dependent packages can see the changes.


Services
====================================================

Services implement **request/response** communication between nodes.
Unlike topics (continuous data streams), services are used for discrete,
one-shot operations that return a result. The client can wait for the
response synchronously or asynchronously.

.. admonition:: Resources
   :class: resources

   - `Understanding Services
     <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html>`_
   - `Writing a Simple Service and Client (Python)
     <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html>`_


.. dropdown:: Service Communication Model

   - The **server** advertises the service and waits for requests. When
     a request arrives, it executes a callback and returns a response.
   - The **client** sends a request and waits for the response. The
     wait can be synchronous (blocking) or asynchronous (non-blocking).
   - A service is defined by its **type** (the ``.srv`` definition) and
     its **name** (e.g., ``/compute_trajectory``).

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
        - Sensor data, ``cmd_vel``
        - Spawn model, compute IK
      * - Blocking?
        - No
        - ``call()``: yes; ``call_async()``: no


Writing a Service Server
----------------------------------------------------

A service server registers a callback that runs when a client sends a
request. The callback receives the request, performs computation,
populates the response, and returns it.

In this demo we **simulate** trajectory computation -- the server logs
the request and returns a success message without actually computing a
path.


.. dropdown:: Server Constructor

   .. code-block:: python

      class TrajectoryServer(Node):
          def __init__(self, node_name: str) -> None:
              super().__init__(node_name)
              self._service = self.create_service(
                  ComputeTrajectory,
                  "compute_trajectory",
                  self._service_callback
              )
              self.get_logger().info("Trajectory server ready.")

   - ``create_service`` registers a service with three arguments:

     - ``ComputeTrajectory`` -- The service type (a ``.srv`` interface).
     - ``"compute_trajectory"`` -- The service name clients will call.
     - ``self._service_callback`` -- The callback that processes
       requests and returns responses.

   .. note::

      The server remains active as long as the node is running.


.. dropdown:: Service Callback

   .. code-block:: python

      def _service_callback(self, request, response):
          # Simulate waypoints along a straight line
          for i in range(1, 4):
              wp = Pose()
              wp.position.x = # computations
              response.waypoints.append(wp)

          response.success = True
          response.message = "Trajectory computed successfully"
          return response

   - This is the callback triggered when a client calls the service.
   - ``request`` and ``response`` are auto-populated from the ``.srv``
     definition.
   - Computes 3 evenly spaced waypoints between ``request.start_pose``
     and ``request.goal_pose``.
   - Appends each waypoint to ``response.waypoints``.
   - Sets ``response.success`` and ``response.message``, then returns
     the response.


.. dropdown:: Server Demonstration

   .. code-block:: console

      # Start the server
      ros2 run service_demo trajectory_server

      # Inspect
      ros2 service list
      ros2 service info /compute_trajectory
      ros2 service type /compute_trajectory

   **Call from CLI:**

   .. code-block:: console

      ros2 service call -h


Writing a Service Client
----------------------------------------------------

A service client creates a connection to a named service, sends a
request, and handles the response. Two calling patterns are available:

- **Asynchronous** (``call_async()``): returns a ``Future`` immediately
  and handles the response in a callback. The node continues spinning
  while waiting. This is the **recommended** pattern.
- **Synchronous** (``call()``): blocks the calling thread until the
  response arrives. Simpler, but requires a ``MultiThreadedExecutor``
  and a separate callback group to avoid deadlocks.

.. tip::

   You can call a service directly from the CLI without writing a
   client node.


.. dropdown:: Client Constructor

   .. code-block:: python

      class TrajectoryClient(Node):
          def __init__(self, node_name: str) -> None:
              super().__init__(node_name)
              self._client = self.create_client(
                  ComputeTrajectory, "compute_trajectory"
              )

              while not self._client.wait_for_service(timeout_sec=1.0):
                  self.get_logger().info("Waiting for service...")

              self._timer = self.create_timer(2.0, self._timer_callback)

          def _timer_callback(self) -> None:
              """Send a request every timer tick."""
              self._send_request()

   - ``create_client`` creates a service client with the service type
     and service name.
   - ``wait_for_service`` blocks until the server is available (1-second
     timeout per attempt).
   - A timer calls ``_send_request`` every 2 seconds. The timer is used
     for demonstration purposes. In reality you will not send a request
     periodically.


Asynchronous Calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **asynchronous** client sends a request and continues processing
other callbacks while waiting for the response. This is the
**recommended pattern**.


.. dropdown:: Async Call Diagram

   .. only:: html

      .. figure:: /_static/images/L10/async_service_call_light.png
         :alt: Asynchronous service call
         :width: 60%
         :align: center
         :class: only-light

         Asynchronous service call: the client sends a request and
         continues spinning while the response is processed in a callback.

      .. figure:: /_static/images/L10/async_service_call_dark.png
         :alt: Asynchronous service call
         :width: 60%
         :align: center
         :class: only-dark

         Asynchronous service call: the client sends a request and
         continues spinning while the response is processed in a callback.


.. dropdown:: Sending a Request (Async)

   .. code-block:: python

      def _send_request(self):
          request = ComputeTrajectory.Request()
          request.goal_pose.position.x = random.uniform(0.0, 10.0)
          request.max_velocity = 1.0

          future = self._client.call_async(request)

          future.add_done_callback(self._response_callback)

   - Creates a ``Request`` object and populates its fields.
   - ``call_async`` sends the request to the server without blocking.
   - ``add_done_callback`` registers ``_response_callback`` to run when
     the server's response arrives.


.. dropdown:: What is a Future?

   A ``Future`` is a placeholder for a result that **does not exist
   yet**.

   - Returned by any ``*_async()`` call (e.g., ``send_goal_async``,
     ``get_result_async``).
   - The call returns **immediately** -- no thread is blocked.
   - Attach a callback with ``future.add_done_callback(fn)`` -- the
     callback fires when the result arrives.
   - Inside the callback, ``future.result()`` retrieves the actual
     value.


.. dropdown:: Response Callback (Async)

   .. code-block:: python

      def _response_callback(self, future):
          response = future.result()
          if response.success:
              self.get_logger().info(f"Success: {response.message}")
              for i, wp in enumerate(response.waypoints):
                  self.get_logger().info(
                      f"  Waypoint {i}: ({wp.position.x}, "
                      f"{wp.position.y}, {wp.position.z})")
          else:
              self.get_logger().error(f"Failed: {response.message}")

   - ``future.result()`` retrieves the server's response.
   - If ``response.success`` is ``True``, logs the message and iterates
     over the waypoints.
   - Otherwise, logs an error with the failure message.


.. dropdown:: Async Client Demonstration

   .. code-block:: console

      # Terminal 1
      ros2 run service_demo trajectory_server

      # Terminal 2
      ros2 run service_demo trajectory_client_async


Synchronous Calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **synchronous** client blocks the calling thread until the response
arrives. This is simpler but requires careful executor and callback
group setup to avoid deadlocks.


.. dropdown:: Sync Call Diagram

   .. only:: html

      .. figure:: /_static/images/L10/sync_service_call_light.png
         :alt: Synchronous service call
         :width: 50%
         :align: center
         :class: only-light

         Synchronous service call: the client blocks the calling thread
         until the response arrives.

      .. figure:: /_static/images/L10/sync_service_call_dark.png
         :alt: Synchronous service call
         :width: 50%
         :align: center
         :class: only-dark

         Synchronous service call: the client blocks the calling thread
         until the response arrives.


.. dropdown:: Sync Client Constructor

   .. code-block:: python

      class TrajectoryClientSync(Node):
          def __init__(self, node_name: str) -> None:
              super().__init__(node_name)
              self._client_cb_group = MutuallyExclusiveCallbackGroup()
              self._client = self.create_client(
                  ComputeTrajectory, "compute_trajectory",
                  callback_group=self._client_cb_group
              )
              while not self._client.wait_for_service(timeout_sec=1.0):
                  self.get_logger().info("Waiting for service...")

              self._timer = self.create_timer(2.0, self._timer_callback)

          def _timer_callback(self) -> None:
              self._send_request()

   - The client is placed in a **separate callback group** to avoid
     deadlocks with the timer.
   - ``wait_for_service`` blocks until the server is available.
   - A timer calls ``_send_request`` every 2 seconds.


.. dropdown:: Sending a Request (Sync)

   .. code-block:: python

      def _send_request(self):
          request = ComputeTrajectory.Request()
          request.goal_pose.position.x = random.uniform(0.0, 10.0)
          request.max_velocity = 1.0
          self.get_logger().info("Sending synchronous request...")
          response = self._client.call(request)
          if response is not None and response.success:
              self.get_logger().info(f"Success: {response.message}")
              for i, wp in enumerate(response.waypoints):
                  self.get_logger().info(
                      f"  Waypoint {i}: ({wp.position.x}, "
                      f"{wp.position.y}, {wp.position.z})")

   - Creates a ``Request`` object and populates its fields.
   - ``call`` sends the request and **blocks** until the response
     arrives.
   - If the response is valid and successful, logs the waypoints.


.. dropdown:: Avoiding the Deadlock

   - ``call()`` blocks the current thread until the response arrives. If
     the timer callback and the service client share the same callback
     group, the executor cannot process the response while blocked --
     causing a **deadlock**.
   - **Fix 1**: Place the client in a **separate callback group** so the
     response can be processed on a different thread.
   - **Fix 2**: Use a ``MultiThreadedExecutor`` in the entry point so
     multiple threads are available.
   - Both fixes are required together -- a separate callback group
     without multiple threads still deadlocks.

   .. warning::

      Prefer ``call_async()`` in most cases. Use ``call()`` only when
      blocking behavior is explicitly needed and the executor setup
      supports it.


.. dropdown:: Sync Client Demonstration

   .. code-block:: console

      # Terminal 1
      ros2 run service_demo trajectory_server

      # Terminal 2
      ros2 run service_demo trajectory_client_sync


.. dropdown:: Asynchronous vs. Synchronous Comparison

   .. list-table::
      :widths: 25 35 40
      :header-rows: 1
      :class: compact-table

      * -
        - Async (``call_async()``)
        - Sync (``call()``)
      * - Blocking
        - No
        - Yes, until response arrives
      * - Response
        - In ``_response_callback``
        - Inline after ``call()``
      * - Deadlock risk
        - None
        - Yes, without proper setup
      * - Executor
        - Any
        - ``MultiThreadedExecutor``

   **Asynchronous (call_async())**

   - Returns a ``Future`` immediately (the node keeps spinning).
   - Response is handled in ``_response_callback`` when it arrives.
   - No risk of deadlock (no thread is ever blocked).
   - No special executor or callback group required.
   - **Recommended** for most use cases.

   **Synchronous (call())**

   - Blocks the calling thread until the response arrives.
   - Response is handled inline (no callback needed).
   - Deadlock-prone if client and timer share the same callback group.
   - Requires a ``MutuallyExclusiveCallbackGroup`` for the client and a
     ``MultiThreadedExecutor``.
   - Use only when blocking behavior is explicitly required.


Actions
====================================================

Actions extend services with **feedback** and **cancellation** for
long-running tasks: navigation, arm motion, image processing pipelines,
etc.

.. note::

   All demos are **text-based** -- robot movement is simulated with log
   messages and ``time.sleep()``. No robot or simulator needed.

.. admonition:: Resources
   :class: resources

   - `Understanding Actions
     <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html>`_
   - `Writing an Action Server and Client (Python)
     <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html>`_


.. dropdown:: Action Communication Model

   An action is a three-part communication pattern:

   1. **Goal** -- the client sends a goal to the server (e.g., "navigate
      to (5, 3)").
   2. **Feedback** -- the server periodically publishes progress updates
      while executing (e.g., "distance remaining: 2.3 m").
   3. **Result** -- when the task completes (or is canceled), the server
      returns a final result (e.g., "total distance: 7.1 m").

   Actions are built on top of services and topics internally:

   - A service for sending goals and receiving acceptance/rejection
   - A service for querying the result
   - A service for canceling goals
   - A topic for publishing feedback


.. dropdown:: When to Use Actions vs. Services

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


Writing an Action Server
----------------------------------------------------

An action server handles incoming goals, publishes feedback during
execution, and returns a result.

In this demo we **simulate** navigation with a countdown loop -- no
actual robot is moving.


.. dropdown:: Server Constructor

   .. code-block:: python

      import time
      from rclpy.action import ActionServer
      from rclpy.node import Node
      from custom_interfaces.action import Navigate

      class NavigateServer(Node):
          def __init__(self):
              super().__init__("navigate_server")
              self._action_server = ActionServer(
                  self, Navigate, "navigate",
                  self._execute_callback,
              )
              self.get_logger().info("Navigate action server ready.")

   - ``ActionServer`` takes the node, action type, action name, and
     execute callback.
   - ``_execute_callback`` is called when a goal is accepted.


.. dropdown:: What is goal_handle (Server Side)?

   The framework passes a ``ServerGoalHandle`` to the execute callback.
   It is the server's interface to a specific goal.

   .. list-table::
      :widths: 50 50
      :header-rows: 1
      :class: compact-table

      * - Attribute / Method
        - Purpose
      * - ``goal_handle.request``
        - Access the goal data sent by the client
      * - ``goal_handle.publish_feedback(fb)``
        - Send a feedback update to the client
      * - ``goal_handle.succeed()``
        - Mark the goal as succeeded
      * - ``goal_handle.canceled()``
        - Mark the goal as canceled
      * - ``goal_handle.abort()``
        - Mark the goal as aborted (failure)
      * - ``goal_handle.is_cancel_requested``
        - ``True`` if a cancel request was accepted

   .. note::

      You must call exactly one of ``succeed()``, ``canceled()``, or
      ``abort()`` before returning from the execute callback. This sets
      the terminal state the client receives.


.. dropdown:: Publishing Feedback

   .. code-block:: python

      def _execute_callback(self, goal_handle):
          self.get_logger().info(
              f"Navigating to "
              f"({goal_handle.request.target_pose.position.x}, "
              f"{goal_handle.request.target_pose.position.y})"
          )
          feedback = Navigate.Feedback()
          total_distance = 10.0
          for i in range(10):
              feedback.distance_remaining = total_distance - (i + 1)
              feedback.percent_complete = float((i + 1) * 10)
              goal_handle.publish_feedback(feedback)
              self.get_logger().info(
                  f"Progress: {feedback.percent_complete:.0f}%")
              time.sleep(1.0)

   - ``goal_handle.request`` contains the goal data sent by the client.
   - A ``Feedback`` object is created and published at each iteration.
   - ``publish_feedback`` sends progress updates to the client in real
     time.


.. dropdown:: Handling Cancellation and Returning the Result

   .. code-block:: python

              # Inside the for loop
              if goal_handle.is_cancel_requested:
                  goal_handle.canceled()
                  self.get_logger().info("Navigation canceled.")
                  result = Navigate.Result()
                  result.success = False
                  return result

          # After the loop completes
          goal_handle.succeed()
          result = Navigate.Result()
          result.success = True
          result.total_distance = total_distance
          result.elapsed_time = 10.0
          return result

   - Each iteration checks ``is_cancel_requested`` and calls
     ``goal_handle.canceled()`` if true.
   - On completion, ``goal_handle.succeed()`` sets the terminal state.
   - A ``Result`` object is populated and returned in both cases.


.. dropdown:: Entry Point -- Why MultiThreadedExecutor?

   .. code-block:: python

      import rclpy
      from rclpy.executors import MultiThreadedExecutor

      def main(args=None):
          rclpy.init(args=args)
          node = NavigateServer("navigate_server")
          executor = MultiThreadedExecutor()
          executor.add_node(node)
          executor.spin()

   - The execute callback contains ``time.sleep()``, which **blocks its
     thread**.
   - With a ``SingleThreadedExecutor``, the cancel callback **cannot
     run** while the execute callback is sleeping -- the cancel request
     is never seen, causing the goal to run to completion.
   - ``MultiThreadedExecutor`` allows the cancel callback to run on a
     **separate thread**, so cancellation works during blocking
     operations.


.. dropdown:: Single-Threaded vs. Multi-Threaded Executor

   .. only:: html

      .. figure:: /_static/images/L10/action_multithread_light.png
         :alt: Single-threaded vs. multi-threaded executor for action servers
         :width: 100%
         :align: center
         :class: only-light

         Single-threaded vs. multi-threaded executor: with a single thread,
         the cancel callback cannot run while the execute callback is
         blocking. A multi-threaded executor allows both to run concurrently.

      .. figure:: /_static/images/L10/action_multithread_dark.png
         :alt: Single-threaded vs. multi-threaded executor for action servers
         :width: 100%
         :align: center
         :class: only-dark

         Single-threaded vs. multi-threaded executor: with a single thread,
         the cancel callback cannot run while the execute callback is
         blocking. A multi-threaded executor allows both to run concurrently.


.. dropdown:: Action Server Demonstration

   .. code-block:: console

      # Terminal 1
      ros2 run action_demo navigate_server

      # Terminal 2
      ros2 action list
      ros2 action type /navigate
      ros2 action info /navigate


Goal Handling and Cancellation
----------------------------------------------------

By default, every incoming goal is automatically accepted. Override
``goal_callback`` and ``cancel_callback`` for finer control over which
goals to accept and whether cancellation requests are honored.


.. dropdown:: Registering Goal and Cancel Callbacks

   .. code-block:: python

      from rclpy.action import CancelResponse, GoalResponse

      class NavigateServerAdvanced(Node):
          def __init__(self):
              super().__init__("navigate_server_adv")
              self._action_server = ActionServer(
                  self, Navigate, "navigate",
                  execute_callback=self._execute_callback,
                  goal_callback=self._goal_callback,
                  cancel_callback=self._cancel_callback,
              )

   - ``goal_callback`` is called **before** execution to accept or
     reject a goal.
   - ``cancel_callback`` is called when a client requests cancellation.
   - ``execute_callback`` runs the actual work (same as before).


.. dropdown:: Goal Validation

   .. code-block:: python

      def _goal_callback(self, goal_request):
          """Accept or reject a goal before execution."""
          if goal_request.max_speed <= 0.0:
              self.get_logger().warn(
                  "Rejected: speed must be positive.")
              return GoalResponse.REJECT
          self.get_logger().info("Goal accepted.")
          return GoalResponse.ACCEPT

   - Called **before** the execute callback -- the goal never starts if
     rejected.
   - ``GoalResponse.ACCEPT`` / ``GoalResponse.REJECT`` control whether
     the goal enters execution.
   - Use this to validate goal fields (speed, bounds, etc.).


.. dropdown:: Cancel Policy

   .. code-block:: python

      def _cancel_callback(self, goal_handle):
          """Accept or reject a cancellation request."""
          self.get_logger().info(
              "Cancel request received -- accepting.")
          return CancelResponse.ACCEPT

   - ``CancelResponse.ACCEPT`` tells the framework to mark the goal as
     cancel-requested.
   - ``CancelResponse.REJECT`` would refuse the cancel (e.g., during a
     critical operation).

   .. warning::

      Cancellation is **cooperative**. The cancel callback only *accepts*
      the request. The execute callback must check
      ``goal_handle.is_cancel_requested`` in its loop and call
      ``goal_handle.canceled()`` to actually stop.


Writing an Action Client
----------------------------------------------------

An action client sends a goal, receives feedback updates, and retrieves
the final result. The entire flow is asynchronous: each step returns a
``Future`` and the node continues spinning.

.. tip::

   You can call an action directly from the CLI without writing a
   client node.


.. dropdown:: Creating the Client

   .. code-block:: python

      from rclpy.action import ActionClient
      from custom_interfaces.action import Navigate

      class NavigateClient(Node):
          def __init__(self):
              super().__init__("navigate_client")
              self._client = ActionClient(
                  self,
                  Navigate,
                  "navigate"
              )

   - ``ActionClient`` takes the node, action type, and action name.
   - The action name must match the server's action name.


.. dropdown:: Sending a Goal

   .. code-block:: python

      def send_goal(self, x, y):
          self.get_logger().info("Waiting for action server...")
          self._client.wait_for_server()
          goal = Navigate.Goal()
          goal.target_pose.position.x = x
          goal.target_pose.position.y = y
          goal.max_speed = 1.0

          future = self._client.send_goal_async(
              goal,
              feedback_callback=self._feedback_callback)

          future.add_done_callback(self._goal_response_callback)

   - ``wait_for_server()`` blocks until the action server is available.
   - ``send_goal_async()`` sends the goal and returns a ``Future``.
   - ``feedback_callback`` is called each time the server publishes
     feedback.
   - ``add_done_callback`` registers ``_goal_response_callback`` to be
     invoked when the server accepts or rejects the goal.


.. dropdown:: Action Client Callbacks Overview

   - **_goal_response_callback**: Invoked when the server accepts or
     rejects the goal. If accepted, stores the goal handle and registers
     ``_result_callback`` via ``get_result_async()``.
   - **_feedback_callback**: Invoked each time the server publishes
     intermediate feedback. Logs progress and, if ``cancel_and_resend``
     is set and five feedback messages have been received, initiates a
     cancellation via ``cancel_goal_async()``.
   - **_cancel_done_callback**: Invoked when the server responds to a
     cancellation request. Logs whether the cancellation was accepted or
     rejected and resets ``self._canceling`` if rejected.
   - **_result_callback**: Invoked once when the goal reaches a terminal
     state. Logs the outcome for ``STATUS_SUCCEEDED``, triggers a new
     goal via ``send_goal()`` for ``STATUS_CANCELED``, and logs a
     warning otherwise.


.. dropdown:: Goal Response Callback Sequence

   .. only:: html

      .. figure:: /_static/images/L10/_goal_response_callback_sequence_light.png
         :alt: Sequence diagram for _goal_response_callback
         :width: 70%
         :align: center
         :class: only-light

         Sequence diagram for ``_goal_response_callback``: invoked once
         after ``send_goal_async()`` completes, branching on whether the
         server accepted or rejected the goal.

      .. figure:: /_static/images/L10/_goal_response_callback_sequence_dark.png
         :alt: Sequence diagram for _goal_response_callback
         :width: 70%
         :align: center
         :class: only-dark

         Sequence diagram for ``_goal_response_callback``: invoked once
         after ``send_goal_async()`` completes, branching on whether the
         server accepted or rejected the goal.


.. dropdown:: Handling the Goal Response

   .. code-block:: python

      def _goal_response_callback(self, future):
          goal_handle = future.result()
          if not goal_handle.accepted:
              self.get_logger().error("Goal rejected.")
              return
          # Log confirmation that the server accepted the goal
          self.get_logger().info("Goal accepted.")
          # Store the goal handle so other callbacks can cancel the goal
          self._goal_handle = goal_handle
          # Request the final result asynchronously and register a callback
          goal_handle.get_result_async().add_done_callback(
              self._result_callback)

   - ``future.result()`` returns a ``ClientGoalHandle``.
   - Check ``goal_handle.accepted`` to see if the server accepted the
     goal.
   - Store ``self._goal_handle`` -- needed later for cancellation.
   - ``get_result_async()`` returns another ``Future`` for the final
     result.


.. dropdown:: What is goal_handle (Client Side)?

   On the client, ``future.result()`` from ``send_goal_async`` returns a
   ``ClientGoalHandle``. This is a **different type** from the server's
   ``ServerGoalHandle`` (it is the client's reference to a specific
   goal).

   .. list-table::
      :widths: 50 50
      :header-rows: 1
      :class: compact-table

      * - Attribute / Method
        - Purpose
      * - ``goal_handle.accepted``
        - ``True`` if the server accepted the goal
      * - ``goal_handle.get_result_async()``
        - Request the final result (returns a ``Future``)
      * - ``goal_handle.cancel_goal_async()``
        - Send a cancellation request (returns a ``Future``)

   .. warning::

      Store ``self._goal_handle = goal_handle`` in your goal response
      callback. Without it, you cannot request the result or cancel the
      goal later.


.. dropdown:: Feedback Callback Sequence

   .. only:: html

      .. figure:: /_static/images/L10/_feedback_callback_sequence_light.png
         :alt: Sequence diagram for _feedback_callback
         :width: 70%
         :align: center
         :class: only-light

         Sequence diagram for ``_feedback_callback``: invoked repeatedly
         while the goal is executing, logging progress and optionally
         triggering a cancellation after five feedback messages.

      .. figure:: /_static/images/L10/_feedback_callback_sequence_dark.png
         :alt: Sequence diagram for _feedback_callback
         :width: 70%
         :align: center
         :class: only-dark

         Sequence diagram for ``_feedback_callback``: invoked repeatedly
         while the goal is executing, logging progress and optionally
         triggering a cancellation after five feedback messages.


.. dropdown:: Feedback Callback

   .. code-block:: python

      def _feedback_callback(self, feedback_msg):
          fb = feedback_msg.feedback
          self.get_logger().info(
              f"Feedback: {fb.percent_complete:.0f}% complete, "
              f"{fb.distance_remaining:.1f} m remaining")

          self._feedback_count += 1
          if (self._cancel_and_resend
                  and not self._canceling
                  and self._feedback_count == 5
                  and self._goal_handle is not None):
              self._canceling = True
              self.get_logger().info("Canceling goal after 5 feedback messages...")
              cancel_future = self._goal_handle.cancel_goal_async()
              cancel_future.add_done_callback(self._cancel_done_callback)

   - Invoked each time the server calls ``publish_feedback``.
   - Access the actual feedback data via ``feedback_msg.feedback``.
   - After five messages, cancellation is requested via
     ``cancel_goal_async()``.


.. dropdown:: Requesting Cancellation

   .. code-block:: python

      # self._goal_handle was stored in _goal_response_callback
      cancel_future = self._goal_handle.cancel_goal_async()
      cancel_future.add_done_callback(self._cancel_done_callback)

   - ``cancel_goal_async()`` sends a cancel request and returns a
     ``Future``.
   - The ``_goal_handle`` must have been saved from
     ``_goal_response_callback``.


.. dropdown:: Cancel Done Callback Sequence

   .. only:: html

      .. figure:: /_static/images/L10/_cancel_done_callback_light.png
         :alt: Sequence diagram for _cancel_done_callback
         :width: 70%
         :align: center
         :class: only-light

         Sequence diagram for ``_cancel_done_callback``: invoked once after
         ``cancel_goal_async()`` completes, branching on whether the server
         accepted or rejected the cancellation request.

      .. figure:: /_static/images/L10/_cancel_done_callback_dark.png
         :alt: Sequence diagram for _cancel_done_callback
         :width: 70%
         :align: center
         :class: only-dark

         Sequence diagram for ``_cancel_done_callback``: invoked once after
         ``cancel_goal_async()`` completes, branching on whether the server
         accepted or rejected the cancellation request.


.. dropdown:: Handling the Cancel Response

   .. code-block:: python

      def _cancel_done_callback(self, future):
          cancel_response = future.result()
          if len(cancel_response.goals_canceling) > 0:
              self.get_logger().info("Cancel accepted by server.")
          else:
              self.get_logger().warn("Cancel request was rejected.")
              self._canceling = False

   - ``goals_canceling`` lists goals the server agreed to cancel.
   - The actual result (with ``STATUS_CANCELED``) arrives later in
     ``_result_callback``.

   .. note::

      The cancel response only confirms the server accepted the request.
      The goal is not fully canceled until the execute callback checks
      ``is_cancel_requested``, calls ``goal_handle.canceled()``, and
      returns the result.


.. dropdown:: Result Callback Sequence

   .. only:: html

      .. figure:: /_static/images/L10/_result_callback_sequence_light.png
         :alt: Sequence diagram for _result_callback
         :width: 60%
         :align: center
         :class: only-light

         Sequence diagram for ``_result_callback``: invoked once when the
         goal reaches a terminal state, branching on ``STATUS_SUCCEEDED``,
         ``STATUS_CANCELED``, or any other status.

      .. figure:: /_static/images/L10/_result_callback_sequence_dark.png
         :alt: Sequence diagram for _result_callback
         :width: 60%
         :align: center
         :class: only-dark

         Sequence diagram for ``_result_callback``: invoked once when the
         goal reaches a terminal state, branching on ``STATUS_SUCCEEDED``,
         ``STATUS_CANCELED``, or any other status.


.. dropdown:: Result Callback

   .. code-block:: python

      def _result_callback(self, future):
          result = future.result().result
          status = future.result().status
          if status == GoalStatus.STATUS_SUCCEEDED:
              self.get_logger().info(
                  f"Done! Distance: {result.total_distance:.1f}"
                  f" m, Time: {result.elapsed_time:.1f} s")
          elif status == GoalStatus.STATUS_CANCELED:
              self.get_logger().info("Goal was canceled.")
              if self._canceling:
                  self._canceling = False
                  self._cancel_and_resend = False
                  self.get_logger().info("Sending new goal...")
                  self.send_goal(8.0, 6.0)
          else:
              self.get_logger().warn(
                  f"Navigation failed with status: {status}")

   - ``future.result().result`` -- the ``Result`` object from the server.
   - ``future.result().status`` -- the terminal status
     (``SUCCEEDED``, ``CANCELED``, ``ABORTED``).
   - Always check ``status`` rather than just the result fields.


.. dropdown:: Full Cancellation Flow

   1. Client calls ``cancel_goal_async()`` -- cancel request sent to
      server.
   2. Server's ``_cancel_callback`` returns ``CancelResponse.ACCEPT``.
   3. Client's ``_cancel_done_callback`` fires -- cancel was accepted.
   4. Server's execute loop checks ``is_cancel_requested``, calls
      ``goal_handle.canceled()``, returns result.
   5. Client's ``_result_callback`` fires with ``STATUS_CANCELED``.

   .. warning::

      The server's execute callback must be running on a **different
      thread** from the cancel callback. Use a
      ``MultiThreadedExecutor`` for the server -- otherwise the cancel
      callback cannot run while the execute callback is blocking, and
      the goal will run to completion.


.. dropdown:: Action Client Demonstration

   **Normal operation:**

   .. code-block:: console

      # Terminal 1
      ros2 run action_demo navigate_server

      # Terminal 2
      ros2 run action_demo navigate_client

   **Cancel and resend:**

   .. code-block:: console

      # Terminal 1
      ros2 run action_demo navigate_server

      # Terminal 2
      ros2 run action_demo navigate_client --ros-args -p cancel_and_resend:=true

   Expected behavior for cancel and resend:

   1. Client sends goal to (5.0, 3.0).
   2. After 50% progress, client cancels and sends a new goal to
      (8.0, 6.0).
   3. Second goal runs to completion.


Communication Pattern
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
