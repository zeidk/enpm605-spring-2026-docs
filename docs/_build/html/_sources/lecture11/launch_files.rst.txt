====================================================
Launch Files
====================================================

Overview
--------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Definition**
    
    Launch files provide a streamlined mechanism for initiating multiple nodes simultaneously while enabling dynamic configuration.

Purposes
--------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📦 Node Management
        :class-card: sd-border-info
        
        Launch, configure, and control individual ROS 2 nodes, including lifecycle and composable nodes, to define system behavior.

    .. grid-item-card:: 🧩 Modularity and Reuse
        :class-card: sd-border-info
        
        Structure complex systems by reusing launch files, grouping nodes, and managing namespace scopes for better organization and scalability.

    .. grid-item-card:: ⚙️ Configuration
        :class-card: sd-border-info
        
        Tailor launch behavior using arguments, environment variables, and substitutions that adapt to various runtime contexts.

    .. grid-item-card:: 🎮 Execution Control
        :class-card: sd-border-info
        
        Control timing and conditions under which nodes and actions are launched, including timers, conditionals, and event-driven execution.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🐍 Custom Logic
        :class-card: sd-border-secondary
        
        Use Python-based logic and functions to perform dynamic setup, computations, or system introspection before launching actions.

    .. grid-item-card:: 📊 Logging & Diagnostics
        :class-card: sd-border-secondary
        
        Monitor system behavior and assist debugging by printing messages, adjusting log levels, and tracking node status.

    .. grid-item-card:: 🔗 External Systems
        :class-card: sd-border-secondary
        
        Integrate external commands or scripts into your launch process to coordinate ROS 2 with other tools.

Anatomy
-------

A typical Python launch file contains:

- **Import statements**: Required launch and ROS dependencies.
- **Launch description**: A function that returns the launch description containing all node configurations.
- **Node configuration**: Information about nodes, parameters, remappings, and more.

.. note::
    Launch files are typically found in the ``launch`` directory within your package. Edit ``CMakeLists.txt`` to install launch files.

.. tip::
    **Naming Convention:** Launch files end with the ``.launch.py`` extension.

Basic Configurations
--------------------

There are two main configurations for launch files (choose one of them).

.. tab-set::

    .. tab-item:: Style 1: Add Actions

        **demo1.launch.py**

        .. code-block:: python
           :linenos:

           from launch import LaunchDescription
           from launch_ros.actions import Node

           # This function must be defined
           def generate_launch_description():
               ld = LaunchDescription()
               talker = Node(
                   package="demo_nodes_cpp", 
                   executable="talker")
               listener = Node(
                   package="demo_nodes_cpp", 
                   executable="listener")

               ld.add_action(talker)
               ld.add_action(listener)

               return ld

    .. tab-item:: Style 2: Return List

        **demo2.launch.py**

        .. code-block:: python
           :linenos:

           from launch import LaunchDescription
           from launch_ros.actions import Node

           # This function must be defined
           def generate_launch_description():
               return LaunchDescription(
                   [
                       Node(
                           package="demo_nodes_cpp",
                           executable="talker",
                       ),
                       Node(
                           package="demo_nodes_cpp",
                           executable="listener",
                       ),
                   ]
               )

.. card::
    :class-card: sd-border-secondary sd-shadow-sm

    **Run the launch files:**

    .. code-block:: bash

       ros2 launch launch_files_demo demo1.launch.py
       # or
       ros2 launch launch_files_demo demo2.launch.py

Advanced Features
-----------------

.. grid:: 1 2 3 3
    :gutter: 2

    .. grid-item-card:: 📥 Include Files
        :class-card: sd-border-primary
        
        Include launch files from other packages.

    .. grid-item-card:: 📝 Arguments
        :class-card: sd-border-primary
        
        Pass arguments to launch files.

    .. grid-item-card:: ❓ Conditionals
        :class-card: sd-border-primary
        
        Conditional execution of nodes.

    .. grid-item-card:: 📦 Grouping
        :class-card: sd-border-primary
        
        Group nodes together.

    .. grid-item-card:: 🔄 Remapping
        :class-card: sd-border-secondary
        
        Remap topic/service names (covered later).

    .. grid-item-card:: ⚙️ Parameters
        :class-card: sd-border-secondary
        
        Pass parameter files (covered later).

Include Other Launch Files
^^^^^^^^^^^^^^^^^^^^^^^^^^

Invoke another launch file from a different package.

.. card::
    :class-card: sd-border-secondary sd-shadow-sm

    .. code-block:: bash

       ros2 launch launch_files_demo demo3.launch.py

Conditional Launching
^^^^^^^^^^^^^^^^^^^^^

Start a node conditionally from a launch argument.

.. card::
    :class-card: sd-border-secondary sd-shadow-sm

    .. code-block:: bash

       ros2 launch launch_files_demo demo4.launch.py talker_arg:=true

.. tip::
    Check arguments that can be passed to a launch file with:
    
    ``ros2 launch <package> <launch file> --show-args``

Node Grouping
^^^^^^^^^^^^^

Start a group of nodes.

.. card::
    :class-card: sd-border-secondary sd-shadow-sm

    .. code-block:: bash

       ros2 launch launch_files_demo demo5.launch.py

Node Grouping with Conditional Launch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Start a group of nodes conditionally using a launch argument.

.. card::
    :class-card: sd-border-secondary sd-shadow-sm

    .. code-block:: bash

       ros2 launch sensor_demo_pkg demo6.launch.py enable_nav_sensors:=true

Resources
---------

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: 📘 Launch Tutorials
        :link: https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html
        :class-card: sd-border-secondary
        
        ROS 2 Documentation

    .. grid-item-card:: 📄 Creating Launch Files
        :link: https://docs.ros.org/en/humble/Tutorials/Launch/Creating-Launch-Files.html
        :class-card: sd-border-secondary
        
        ROS 2 Documentation

    .. grid-item-card:: 📋 File Formats
        :link: https://docs.ros.org/en/humble/How-To-Guides/Launch-file-different-formats.html
        :class-card: sd-border-secondary
        
        ROS 2 Documentation

    .. grid-item-card:: 🔧 Substitutions
        :link: https://docs.ros.org/en/humble/Tutorials/Launch/Using-Substitutions.html
        :class-card: sd-border-secondary
        
        ROS 2 Documentation