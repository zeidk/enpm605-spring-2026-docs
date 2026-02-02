====================================================
Writing a Node
====================================================

Goal
----

Create a minimal C++ node that initializes the library, creates a node object, and spins until shutdown.

Implementation
--------------

.. tab-set::

    .. tab-item:: 📄 C++ Code (minimal_node.cpp)

        .. code-block:: cpp
           :linenos:

           #include "rclcpp/rclcpp.hpp"

           int main(int argc, char * argv[])
           {
             rclcpp::init(argc, argv);
             auto node = std::make_shared<rclcpp::Node>("minimal_node");

             RCLCPP_INFO(node->get_logger(), "Node has been started.");

             rclcpp::spin(node);
             rclcpp::shutdown();
             return 0;
           }

    .. tab-item:: 🛠️ CMakeLists.txt

        In the package configuration:

        .. code-block:: cmake

           find_package(rclcpp REQUIRED)

           add_executable(minimal_node src/minimal_node.cpp)
           ament_target_dependencies(minimal_node rclcpp)

           install(TARGETS
             minimal_node
             DESTINATION lib/${PROJECT_NAME})

Key API Components
------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Function/Class
     - Description
   * - ``rclcpp::init``
     - Initializes the ROS 2 system with command-line args.
   * - ``rclcpp::Node``
     - The class representing the node. Takes a name (e.g. "minimal_node").
   * - ``rclcpp::spin``
     - Enters a loop to process callbacks/timers. Keeps node alive.
   * - ``rclcpp::shutdown``
     - Cleans up resources before exiting.

Execution
---------

.. card::
    :class-card: sd-bg-light

    .. code-block:: bash

       colcon build
       source install/setup.bash
       ros2 run my_package minimal_node