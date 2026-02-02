====================================================
Quality of Service (QoS)
====================================================

Why QoS Matters
---------------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Definition**
    
    ROS 2 QoS policies control the reliability, performance, and resource usage of data exchange between nodes, enabling robust communication in diverse network conditions.

ROS 2 recognizes that different data types have different requirements. A 30 Hz camera feed can tolerate dropped frames, but an emergency stop command must arrive reliably. QoS policies let you express these requirements explicitly, ensuring your system behaves predictably under various network conditions and computational loads.

Core QoS Policies
-----------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔒 Reliability
        :class-card: sd-border-info
        
        Choose between **RELIABLE** (guaranteed delivery with retransmission) and **BEST_EFFORT** (fire-and-forget, lower latency).

    .. grid-item-card:: 💾 Durability
        :class-card: sd-border-info
        
        Determines whether late-joining subscribers receive previously published messages (**TRANSIENT_LOCAL**) or only new ones (**VOLATILE**).

    .. grid-item-card:: 📚 History
        :class-card: sd-border-info
        
        Controls message queueing—**KEEP_LAST(n)** maintains a rolling buffer, while **KEEP_ALL** preserves everything (memory permitting).

    .. grid-item-card:: 📏 Depth
        :class-card: sd-border-info
        
        Sets the queue size when using KEEP_LAST history.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ⏱️ Deadline
        :class-card: sd-border-secondary
        
        Specifies the maximum acceptable time between messages.

    .. grid-item-card:: 💓 Liveliness
        :class-card: sd-border-secondary
        
        Monitors whether entities are still active in the system.

    .. grid-item-card:: ⏳ Lifespan
        :class-card: sd-border-secondary
        
        Defines how long a message remains valid before automatic disposal.

QoS Compatibility
-----------------

.. card::
    :class-card: sd-border-warning sd-border-3

    **Request-Offered Model**
    
    Publishers and subscribers must have `compatible QoS settings <https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html>`_ to communicate.
    
    ROS 2 follows a *Request-Offered* model where **subscribers request** certain guarantees and publishers offer them. For example, a subscriber requesting RELIABLE delivery can only connect to publishers offering RELIABLE (not BEST_EFFORT). This compatibility checking happens automatically during the discovery phase, preventing silent communication failures.

Sensor Monitor Implementation
-----------------------------

Header File
^^^^^^^^^^^

.. dropdown:: 📄 include/qos_demo/sensor_monitor.hpp
    :open:
    :icon: code

    .. code-block:: cpp
       :linenos:

       #pragma once

       #include "rclcpp/rclcpp.hpp"
       #include "sensor_msgs/msg/temperature.hpp"
       #include "rclcpp/qos.hpp"

       class SensorMonitor : public rclcpp::Node {
       public:
         SensorMonitor();

       private:
         void timer_callback();
         void reliable_callback(const sensor_msgs::msg::Temperature::SharedPtr msg);
         void best_effort_callback(const sensor_msgs::msg::Temperature::SharedPtr msg);
       };

Publisher with Sensor QoS
^^^^^^^^^^^^^^^^^^^^^^^^^

.. dropdown:: 📄 Sensor Data Publisher
    :open:
    :icon: code

    .. code-block:: cpp
       :linenos:

       SensorMonitor::SensorMonitor() : Node("sensor_monitor")
       {
         // Publisher with sensor data QoS profile
         sensor_publisher_ = create_publisher<sensor_msgs::msg::Temperature>(
           "temperature", 
           rclcpp::SensorDataQoS()  // Best-effort, volatile, keep last 5
         );
         
         // Timer for publishing
         timer_ = create_wall_timer(
           std::chrono::milliseconds(100),
           std::bind(&SensorMonitor::timer_callback, this)
         );
         
         RCLCPP_INFO(get_logger(), "Sensor monitor started with SensorDataQoS");
       }

Subscribers with Different QoS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tab-set::

    .. tab-item:: Reliable Subscriber

        .. code-block:: cpp

           // Reliable subscriber - will miss some messages from best-effort publisher
           auto reliable_qos = rclcpp::QoS(10)
               .reliability(rclcpp::ReliabilityPolicy::Reliable)
               .durability(rclcpp::DurabilityPolicy::Volatile);

           reliable_subscriber_ = create_subscription<sensor_msgs::msg::Temperature>(
             "temperature", reliable_qos,
             std::bind(&SensorMonitor::reliable_callback, this, std::placeholders::_1)
           );

    .. tab-item:: Best-Effort Subscriber

        .. code-block:: cpp

           // Best-effort subscriber - compatible with sensor data QoS
           best_effort_subscriber_ = create_subscription<sensor_msgs::msg::Temperature>(
               "temperature", 
               rclcpp::SensorDataQoS(),
               std::bind(&SensorMonitor::best_effort_callback, this, std::placeholders::_1)
           );

    .. tab-item:: Custom QoS Profile

        .. code-block:: cpp

           // Custom QoS with specific requirements
           auto custom_qos = rclcpp::QoS(rclcpp::KeepLast(50))
             .reliability(rclcpp::ReliabilityPolicy::Reliable)
             .durability(rclcpp::DurabilityPolicy::TransientLocal)
             .deadline(std::chrono::milliseconds(200))
             .lifespan(std::chrono::seconds(10));

           custom_subscriber_ = create_subscription<sensor_msgs::msg::Temperature>(
             "temperature", custom_qos,
             [this](const sensor_msgs::msg::Temperature::SharedPtr msg) {
               RCLCPP_INFO(get_logger(), "Custom QoS received: %.2f°C", msg->temperature);
             }
           );

Publisher Implementation
^^^^^^^^^^^^^^^^^^^^^^^^

.. dropdown:: 📄 Temperature Publishing
    :icon: code

    .. code-block:: cpp
       :linenos:

       void SensorMonitor::timer_callback() {
         auto msg = sensor_msgs::msg::Temperature();
         msg.header.stamp = now();
         msg.header.frame_id = "sensor_frame";
         
         // Simulate temperature readings with noise
         static double base_temp = 25.0;
         base_temp += (std::rand() % 100 - 50) * 0.01;  // ±0.5°C noise
         msg.temperature = base_temp;
         msg.variance = 0.1;
         
         sensor_publisher_->publish(msg);
         
         // Log every 10th message to avoid spam
         static int count = 0;
         if (++count % 10 == 0) {
           RCLCPP_INFO(get_logger(), "Published temperature: %.2f°C", 
                       msg.temperature);
         }
       }

Testing QoS
-----------

.. card::
    :class-card: sd-border-secondary

    **Build and Run**

    .. code-block:: bash

       colcon build --packages-select qos_demo
       source install/setup.bash
       ros2 run qos_demo sensor_monitor

QoS Inspection Commands
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 50 50
   :class: compact-table

   * - ``ros2 topic info /temperature --verbose``
     - View QoS settings for publishers and subscribers
   * - ``ros2 node info /sensor_monitor``
     - Inspect node's topics and QoS
   * - ``ros2 topic echo /temperature --qos-reliability best_effort``
     - Echo with specific QoS
   * - ``ros2 topic hz /temperature``
     - Monitor publish rate
   * - ``ros2 doctor --report``
     - System-wide diagnostics