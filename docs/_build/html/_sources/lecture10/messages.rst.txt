====================================================
Messages
====================================================

Message Types
-------------

ROS 2 messages are strongly-typed structures defined in ``.msg`` files.

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: std_msgs
        :class-card: sd-border-secondary
        
        Basic primitives.
        
        *Strings, integers, booleans.*

    .. grid-item-card:: geometry_msgs
        :class-card: sd-border-secondary
        
        Spatial data.
        
        *Vectors, poses, twists.*

    .. grid-item-card:: sensor_msgs
        :class-card: sd-border-secondary
        
        Raw sensor data.
        
        *LaserScans, Images, PointClouds.*

    .. grid-item-card:: nav_msgs
        :class-card: sd-border-secondary
        
        Navigation data.
        
        *OccupancyGrids, Odometry.*

CLI Introspection tools
-----------------------

.. card::
    :class-card: sd-bg-light

    **Useful Commands**

    * List all topics:
        ``ros2 topic list``
    
    * Check topic type:
        ``ros2 topic info /cmd_vel``
        
    * See message structure:
        ``ros2 interface show geometry_msgs/msg/Twist``

Using Messages in C++
---------------------

To use a message, you must include the header and link the dependency.

.. code-block:: cpp

   #include "geometry_msgs/msg/twist.hpp"

   geometry_msgs::msg::Twist cmd;
   cmd.linear.x  = 0.5;
   cmd.angular.z = 0.0;
   
   publisher_->publish(cmd);

.. tip::
    Don't forget to add the package to ``ament_target_dependencies`` in ``CMakeLists.txt``.