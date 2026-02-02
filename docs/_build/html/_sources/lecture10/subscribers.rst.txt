====================================================
Subscribers
====================================================

Creating a Subscriber Node
--------------------------

.. grid:: 1 3 3 3
    :gutter: 2

    .. grid-item-card:: 1. Create Node
        :class-card: sd-border-success
        
        Inherit from ``rclcpp::Node``.

    .. grid-item-card:: 2. Create Subscription
        :class-card: sd-border-success
        
        Bind a callback function to a topic.

    .. grid-item-card:: 3. Spin
        :class-card: sd-border-success
        
        Process received messages via the callback.

Implementation
--------------

.. dropdown:: 📄 Complete C++ Example
    :open:
    :icon: code

    .. code-block:: cpp
       :linenos:

       #include "rclcpp/rclcpp.hpp"
       #include "std_msgs/msg/string.hpp"

       class MinimalSubscriber : public rclcpp::Node
       {
       public:
         MinimalSubscriber() : Node("minimal_subscriber")
         {
           // Subscribe to "chatter"
           subscription_ = this->create_subscription<std_msgs::msg::String>(
             "chatter",
             10,
             std::bind(&MinimalSubscriber::topic_callback, this, std::placeholders::_1));
         }

       private:
         void topic_callback(const std_msgs::msg::String::SharedPtr msg)
         {
           RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
         }

         rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
       };

Important: Matching Configs
---------------------------

.. card::
    :class-card: sd-border-warning sd-border-3

    **Debugging Connectivity**
    
    For communication to work, the Subscriber must match the Publisher on:
    
    1.  **Topic Name**
    2.  **Message Type**
    
    *If these do not match, no messages will be delivered.* Use ``ros2 topic info`` to debug.

Testing System
--------------

Run the nodes in separate terminals:

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item::
        
        **Terminal 1 (Pub)**
        
        .. code-block:: bash
        
           ros2 run pkg minimal_publisher

    .. grid-item::
        
        **Terminal 2 (Sub)**
        
        .. code-block:: bash
        
           ros2 run pkg minimal_subscriber