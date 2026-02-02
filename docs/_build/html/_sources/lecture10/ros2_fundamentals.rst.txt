====================================================
ROS 2 - Introduction
====================================================

What is ROS 2?
--------------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Definition**
    
    ROS 2 (Robot Operating System 2) is a framework for building modular robot software. Instead of writing one large monolithic program, ROS 2 encourages you to build many small **nodes** that communicate with each other.

Motivation and Use Cases
------------------------



.. grid:: 1 2 3 3
    :gutter: 2

    .. grid-item-card:: 🚗 Autonomous Vehicles
        :class-card: sd-border-secondary
        
        Simulation platforms (CARLA, Autoware).
        
        *Lane keeping, perception, sensor fusion, and planners.*

    .. grid-item-card:: 🏭 Manufacturing
        :class-card: sd-border-secondary
        
        Industrial arms (KUKA, ABB) and collaborative robots.
        
        *Flexible production and logistics.*

    .. grid-item-card:: 🚁 Other Domains
        :class-card: sd-border-secondary
        
        Drones, aerial robotics, and maritime vessels.
        
        *Rail and transportation automation.*

Core Concepts
-------------



.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📦 Node
        :class-card: sd-border-info
        
        A process that uses the ROS 2 client library (e.g., ``rclcpp``).
        
        **Function:** Performs a focused task like reading sensors or computing controls.

    .. grid-item-card:: 📨 Topic
        :class-card: sd-border-info
        
        A named communication channel (e.g., ``/cmd_vel``).
        
        **Function:** Nodes publish or subscribe to messages here asynchronously.

    .. grid-item-card:: 📄 Message
        :class-card: sd-border-info
        
        Strongly-typed data structures defined in ``.msg`` files.
        
        **Examples:** ``sensor_msgs/msg/Image``, ``geometry_msgs/msg/Twist``.

    .. grid-item-card:: 📞 Service
        :class-card: sd-border-info
        
        Synchronous request/response communication.
        
        **Function:** Node A sends a request; Node B replies.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ⚙️ Parameters
        :class-card: sd-border-light
        
        Configuration values (e.g., ``max_speed``) changed at startup or runtime.

    .. grid-item-card:: 👻 ROS 2 Daemon
        :class-card: sd-border-light
        
        Background process maintaining the system-wide graph. Consulted by CLI tools.

Communication Layer (DDS)
-------------------------

.. card::
    :class-card: sd-border-warning sd-border-3

    **Under the Hood: DDS**
    
    ROS 2 uses **Data Distribution Service (DDS)** implementation to:
    
    * Handle discovery (finding nodes/topics).
    * Deliver messages with configurable **QoS (Quality of Service)** policies.
    * Enable communication across machines and networks.