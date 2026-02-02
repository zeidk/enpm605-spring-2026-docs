====================================================
Publishers
====================================================

Creating a Publisher Node
-------------------------

.. grid:: 1 3 3 3
    :gutter: 2

    .. grid-item-card:: 1. Create Node
        :class-card: sd-border-primary
        
        Inherit from ``rclcpp::Node``.

    .. grid-item-card:: 2. Create Publisher
        :class-card: sd-border-primary
        
        Define the topic and queue size.

    .. grid-item-card:: 3. Publish
        :class-card: sd-border-primary
        
        Send messages periodically (e.g., using a timer).

Implementation
--------------

.. dropdown:: 📄 Complete C++ Example
    :open:
    :icon: code

    .. code-block:: cpp
       :linenos:

       #include "rclcpp/rclcpp.hpp"
       #include "std_msgs/msg/string.hpp"

       class MinimalPublisher : public rclcpp::Node
       {
       public:
         MinimalPublisher() : Node("minimal_publisher")
         {
           // Create publisher on topic "chatter" with queue size 10
           publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);
           
           // Create timer (500ms)
           timer_ = this->create_wall_timer(
             std::chrono::milliseconds(500),
             std::bind(&MinimalPublisher::timer_callback, this));
         }

       private:
         void timer_callback()
         {
           auto msg = std::make_unique<std_msgs::msg::String>();
           msg->data = "Hello ROS 2";
           RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg->data.c_str());
           publisher_->publish(std::move(msg));
         }

         rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
         rclcpp::TimerBase::SharedPtr timer_;
       };

Key Parameters
--------------

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Topic Name**
     - ``"chatter"`` (The channel nodes talk over)
   * - **Queue Size**
     - ``10`` (Affects buffering and QoS behavior)

Testing
-------

.. code-block:: bash

   ros2 run my_package minimal_publisher
   ros2 topic echo /chatter