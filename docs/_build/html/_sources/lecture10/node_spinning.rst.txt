====================================================
Node Spinning
====================================================

Why Spinning Matters
--------------------

.. card::
    :class-card: sd-border-info
    
    Spinning is how a ROS 2 node processes incoming data. Without it, subscriptions, timers, and services will never be triggered.

Spinning Models
---------------



.. tab-set::

    .. tab-item:: Single-Threaded (Default)

        The simplest pattern. Processes callbacks one at a time.

        .. code-block:: cpp

           rclcpp::spin(node);

        * ✅ Easy to reason about and debug.
        * ✅ Suitable for many small nodes.

    .. tab-item:: Multi-Threaded

        For handling multiple callbacks (high-rate sensors/services) concurrently.

        .. code-block:: cpp

           rclcpp::executors::MultiThreadedExecutor executor;
           executor.add_node(node);
           executor.spin();

        * ✅ Callbacks run concurrently.
        * ⚠️ Requires thread safety for shared data.

Best Practices
--------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🛡️ Lifecycle
        :class-card: sd-border-secondary
        
        Always call ``rclcpp::shutdown()`` before exiting. Use RAII and smart pointers.

    .. grid-item-card:: 🧩 Composition
        :class-card: sd-border-secondary
        
        Prefer encapsulating functionality in classes rather than writing monolithic node code.

    .. grid-item-card:: ⚡ Performance
        :class-card: sd-border-secondary
        
        Keep callbacks small and focused. Offload heavy work to worker threads.