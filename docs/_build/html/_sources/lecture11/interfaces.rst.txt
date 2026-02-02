====================================================
Interfaces
====================================================

Overview
--------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Definition**
    
    An interface defines the data structure used for communication between nodes. Interfaces specify what kind of data is exchanged but not how it is transmitted.

CLI Commands
^^^^^^^^^^^^

.. code-block:: bash

   ros2 interface -h
   ros2 interface list

Interface Types
---------------

ROS 2 provides three types of interfaces:

.. grid:: 1 3 3 3
    :gutter: 2

    .. grid-item-card:: 📄 Message (.msg)
        :class-card: sd-border-info
        
        Used for topics (one-way communication).
        
        *Asynchronous, publish-subscribe pattern.*

    .. grid-item-card:: 🔄 Service (.srv)
        :class-card: sd-border-info
        
        Used for request/response communication (synchronous).
        
        *Client sends request, server sends reply.*

    .. grid-item-card:: 🎯 Action (.action)
        :class-card: sd-border-info
        
        Used for goal-oriented tasks with feedback (asynchronous).
        
        *Long-running tasks with progress updates.*

Key Benefits
^^^^^^^^^^^^

.. grid:: 1 3 3 3
    :gutter: 2

    .. grid-item-card:: 🔒 Type Safety
        :class-card: sd-border-success
        
        Compile-time checking prevents data type mismatches.

    .. grid-item-card:: 🌐 Language Agnostic
        :class-card: sd-border-success
        
        Same interface definition works across C++, Python, etc.

    .. grid-item-card:: 📏 Standardization
        :class-card: sd-border-success
        
        Consistent communication contracts across nodes.

Scenario: Robot Status Publishing
---------------------------------

A mobile robot publishes its operational status to monitor its health and performance. The robot continuously sends sensor readings and operational mode.

Topic Communication
^^^^^^^^^^^^^^^^^^^

The system uses simple topic-based communication:

- **Publisher**: ``robot_monitor`` node publishes status data.
- **Topic**: ``/robot_status`` carries the status messages.
- **Subscriber**: ``fleet_monitor`` node receives and processes status.

Interface Package
-----------------

Custom interfaces are created in a dedicated package with no implementation code. This package should have the suffix **_msgs** or **_interfaces**.

.. tip::
    The provided package ``robot_custom_interfaces`` was created with:
    
    ``ros2 pkg create robot_custom_interfaces --dependencies std_msgs``

Package Structure
^^^^^^^^^^^^^^^^^

.. code-block:: text

   robot_custom_interfaces/
   ├── msg/
   │   └── RobotStatus.msg
   ├── CMakeLists.txt
   └── package.xml

.. note::
    For this topic message example, we only need the ``msg`` folder. The ``src`` and ``include`` folders are not needed.

Message Structure
-----------------

Complex Message: RobotStatus.msg
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This message demonstrates key ROS 2 message features including constants, header, string, and arrays.

.. dropdown:: 📄 msg/RobotStatus.msg
    :open:
    :icon: code

    .. code-block:: text
       :linenos:

       # Robot operational mode constants
       uint8 MODE_IDLE=0
       uint8 MODE_MOVING=1
       uint8 MODE_WORKING=2
       uint8 MODE_CHARGING=3
       uint8 MODE_ERROR=4

       # Standard ROS header with timestamp and frame
       std_msgs/Header header

       # Robot identification and current mode
       string robot_name
       uint8 mode # Use mode constants above

       # Sensor readings (temperature, humidity, etc.)
       float32[] sensor_readings

Message Structure Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - **Constants**
     - Predefined values (``MODE_*``) improve code readability and prevent magic numbers.
   * - **header**
     - Standard ROS header providing timestamp and coordinate frame reference.
   * - **string**
     - Variable-length text field for robot identification.
   * - **float32[]**
     - Dynamic array of sensor readings (temperatures, voltages, distances).

Usage Examples
^^^^^^^^^^^^^^

- ``sensor_readings[0]``: Battery voltage (V)
- ``sensor_readings[1]``: Internal temperature (°C)
- ``sensor_readings[2]``: Distance to nearest obstacle (m)

Building Custom Interfaces
--------------------------

package.xml
^^^^^^^^^^^

.. code-block:: xml

   <buildtool_depend>rosidl_default_generators</buildtool_depend>
   <exec_depend>rosidl_default_runtime</exec_depend>
   <member_of_group>rosidl_interface_packages</member_of_group>

CMakeLists.txt
^^^^^^^^^^^^^^

.. code-block:: cmake
   :linenos:
   :emphasize-lines: 5

   find_package(rosidl_default_generators REQUIRED)

   # Generate custom interfaces
   rosidl_generate_interfaces(${PROJECT_NAME}
     "msg/RobotStatus.msg"
     DEPENDENCIES std_msgs
   )

   ament_export_dependencies(rosidl_default_runtime)

Generate Message in Target Language
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
    :class-card: sd-border-3

    **Build Steps:**

    1. Build the package:
    
       .. code-block:: bash
       
          colcon build --packages-select robot_custom_interfaces

    2. Source the workspace.

    3. Check the message interface:
    
       .. code-block:: bash
       
          ros2 interface show robot_custom_interfaces/msg/RobotStatus

    4. Check the ``install`` folder to see that ``RobotStatus.msg`` was converted to C++ and Python code.

Using Custom Interfaces
-----------------------

.. card::
    :class-card: sd-border-warning sd-border-3

    **Dependency Requirement**
    
    Any package that uses ``robot_custom_interfaces/msg/RobotStatus`` must include ``robot_custom_interfaces`` as a dependency.

The package ``robot_interfaces_demo`` was created with:

.. code-block:: bash

   ros2 pkg create robot_interfaces_demo --dependencies std_msgs robot_custom_interfaces rclcpp

Implementation
--------------

.. card::
    :class-card: sd-border-3

    **Build and Run:**

    1. Build the package:
    
       .. code-block:: bash
       
          colcon build --packages-up-to robot_interfaces_demo

    2. Source the workspace.

    3. Start the robot monitor (publisher and subscriber):
    
       .. code-block:: bash
       
          ros2 run robot_interfaces_demo robot_status_demo

Resources
---------

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: 📘 ROS 2 Interfaces
        :link: https://docs.ros.org/en/rolling/Concepts/Basic/About-Interfaces.html
        :class-card: sd-border-secondary
        
        Official ROS 2 Documentation